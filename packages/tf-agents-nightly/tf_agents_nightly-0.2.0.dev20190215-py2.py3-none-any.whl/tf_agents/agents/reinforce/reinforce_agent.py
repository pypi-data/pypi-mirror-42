# coding=utf-8
# Copyright 2018 The TF-Agents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A REINFORCE Agent.

Implements the REINFORCE algorithm from (Williams, 1992):
http://www-anw.cs.umass.edu/~barto/courses/cs687/williams92simple.pdf
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tf_agents.agents import tf_agent
from tf_agents.environments import time_step as ts
from tf_agents.policies import actor_policy
from tf_agents.policies import greedy_policy
from tf_agents.utils import common
from tf_agents.utils import eager_utils
import gin.tf


@gin.configurable
class ReinforceAgent(tf_agent.TFAgent):
  """A REINFORCE Agent."""

  def __init__(self,
               time_step_spec,
               action_spec,
               actor_network,
               optimizer,
               normalize_returns=True,
               gradient_clipping=None,
               debug_summaries=False,
               summarize_grads_and_vars=False,
               name=None):
    """Creates a REINFORCE Agent.

    Args:
      time_step_spec: A `TimeStep` spec of the expected time_steps.
      action_spec: A nest of BoundedTensorSpec representing the actions.
      actor_network: A tf_agents.network.Network to be used by the agent. The
        network will be called with call(observation, step_type).
      optimizer: Optimizer for the actor network.
      normalize_returns: Whether to normalize returns across episodes when
        computing the loss.
      gradient_clipping: Norm length to clip gradients.
      debug_summaries: A bool to gather debug summaries.
      summarize_grads_and_vars: If True, gradient and network variable summaries
        will be written during training.
      name: The name of this agent. All variables in this module will fall
        under that name. Defaults to the class name.
    """
    tf.experimental.Module.__init__(self, name=name)

    self._actor_network = actor_network
    collect_policy = actor_policy.ActorPolicy(
        time_step_spec=time_step_spec,
        action_spec=action_spec,
        actor_network=self._actor_network,
        clip=True)
    policy = greedy_policy.GreedyPolicy(collect_policy)

    self._optimizer = optimizer
    self._normalize_returns = normalize_returns
    self._gradient_clipping = gradient_clipping

    super(ReinforceAgent, self).__init__(
        time_step_spec,
        action_spec,
        policy,
        collect_policy,
        train_sequence_length=None,
        debug_summaries=debug_summaries,
        summarize_grads_and_vars=summarize_grads_and_vars)

  def _initialize(self):
    return tf.no_op()

  def _train(self, experience, weights=None, train_step_counter=None):
    # TODO(sfishman): Support batch dimensions >1.
    if experience.step_type.shape[0] != 1:
      raise NotImplementedError('ReinforceAgent does not yet support batch '
                                'dimensions greater than 1.')
    experience = tf.nest.map_structure(lambda t: tf.squeeze(t, 0), experience)
    returns = common.compute_returns(experience.reward,
                                     experience.discount)
    if self._debug_summaries:
      tf.contrib.summary.histogram('rewards', experience.reward)
      tf.contrib.summary.histogram('discounts', experience.discount)
      tf.contrib.summary.histogram('returns', returns)

    # TODO(kbnaoop): replace with tensor normalizer.
    if self._normalize_returns:
      ret_mean, ret_var = tf.nn.moments(x=returns, axes=[0])
      returns = (returns - ret_mean) / (tf.sqrt(ret_var) + 1e-6)
      if self._debug_summaries:
        tf.contrib.summary.histogram('normalized_returns', returns)

    # TODO(kbanoop): remove after changing network interface to accept
    # observations and step_types, instead of time_steps.
    time_step = ts.TimeStep(experience.step_type,
                            tf.zeros_like(experience.reward),
                            tf.zeros_like(experience.discount),
                            experience.observation)
    # TODO(kbanoop): Filter boundary steps.

    loss_info = self._loss(time_step,
                           experience.action,
                           tf.stop_gradient(returns),
                           weights=weights)

    clip_gradients = None
    if self._gradient_clipping:
      clip_gradients = eager_utils.clip_gradient_norms_fn(
          self._gradient_clipping)

    loss_info = eager_utils.create_train_step(
        loss_info,
        self._optimizer,
        total_loss_fn=lambda loss_info: loss_info.loss,
        global_step=train_step_counter,
        transform_grads_fn=clip_gradients,
        summarize_gradients=self._summarize_grads_and_vars,
        variables_to_train=lambda: self._actor_network.trainable_weights,
    )

    if self._summarize_grads_and_vars:
      with tf.name_scope('Variables/'):
        for var in self._actor_network.trainable_weights:
          tf.contrib.summary.histogram(var.name.replace(':', '_'), var)

    return loss_info

  @eager_utils.future_in_eager_mode
  def _loss(self, time_steps, actions, returns, weights):
    return self.policy_gradient_loss(time_steps, actions, returns, weights)

  def policy_gradient_loss(self, time_steps, actions, returns, weights=None):
    """Computes the policy gradient loss.

    Args:
      time_steps: TimeStep object with a batch of observations.
      actions: Tensor with a batch of actions.
      returns: Tensor with a return from each timestep, aligned on index. Works
        better when returns are normalized.
      weights: Optional scalar or element-wise (per-batch-entry) importance
        weights.  May include a mask for invalid timesteps.

    Returns:
      policy_gradient_loss: A tensor that will contain policy gradient loss for
        the on-policy experience.
    """
    tf.nest.assert_same_structure(time_steps, self.time_step_spec())
    actions_distribution = self.collect_policy().distribution(time_steps).action

    # TODO(kbanoop): Add class IndependentNested(tfd.Distribution) to handle
    # nests of independent distributions like this.
    action_log_prob = common.log_probability(actions_distribution, actions,
                                             self.action_spec())
    action_log_prob_times_return = action_log_prob * returns

    if weights is not None:
      action_log_prob_times_return *= weights

    if self._debug_summaries:
      tf.contrib.summary.histogram('action_log_prob', action_log_prob)
      tf.contrib.summary.histogram('action_log_prob_times_return',
                                   action_log_prob_times_return)

    # Policy gradient loss is defined as the sum, over timesteps, of action
    #   log-probability times the cumulative return from that timestep onward.
    #   For more information, see (Williams, 1992)
    policy_gradient_loss = -tf.reduce_sum(
        input_tensor=action_log_prob_times_return)

    with tf.name_scope('Losses/'):
      tf.contrib.summary.scalar('policy_gradient_loss',
                                policy_gradient_loss)

    return tf_agent.LossInfo(policy_gradient_loss, ())
