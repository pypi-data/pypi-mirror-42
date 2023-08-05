# Copyright 2018 The TensorFlow Constrained Optimization Authors. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
# ==============================================================================
"""Tests for proxy_lagrangian_optimizer.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

from tensorflow_constrained_optimization.python.train import proxy_lagrangian_optimizer
from tensorflow_constrained_optimization.python.train import test_util


class ProxyLagrangianOptimizerWrapper(
    proxy_lagrangian_optimizer.ProxyLagrangianOptimizer):
  """Testing wrapper class around ProxyLagrangianOptimizer.

  This class is identical to ProxyLagrangianOptimizer, except that it caches the
  internal optimization state when _create_state() is called, so that we can
  test that the stochastic matrices take on their expected values.
  """

  def __init__(self,
               optimizer,
               constraint_optimizer=None,
               regret_type="swap",
               update_type="multiplicative",
               minimum_multiplier_radius=None,
               initial_multiplier_radius=None):
    """Same as ProxyLagrangianOptimizer.__init__()."""
    super(ProxyLagrangianOptimizerWrapper, self).__init__(
        optimizer=optimizer,
        constraint_optimizer=constraint_optimizer,
        regret_type=regret_type,
        update_type=update_type,
        minimum_multiplier_radius=minimum_multiplier_radius,
        initial_multiplier_radius=initial_multiplier_radius)
    self._cached_state = None

  @property
  def state(self):
    """Returns the cached state."""
    return self._cached_state

  def _create_state(self, num_constraints):
    """Caches the internal state for testing."""
    self._cached_state = super(ProxyLagrangianOptimizerWrapper,
                               self)._create_state(num_constraints)
    return self._cached_state


class ProxyLagrangianOptimizerTest(tf.test.TestCase):
  """Tests the `ProxyLagrangianOptimizer` and associated helper functions."""

  def _optimizer_test_helper(self,
                             minimization_problem,
                             expected_states,
                             regret_type,
                             update_type,
                             minimum_multiplier_radius=None,
                             initial_multiplier_radius=None):
    """Tests that the states at each iteration match the expected states."""
    optimizer = ProxyLagrangianOptimizerWrapper(
        tf.train.GradientDescentOptimizer(1.0),
        regret_type=regret_type,
        update_type=update_type,
        minimum_multiplier_radius=minimum_multiplier_radius,
        initial_multiplier_radius=initial_multiplier_radius)
    train_op = optimizer.minimize_constrained(minimization_problem)

    states = []
    with self.session() as session:
      session.run(tf.global_variables_initializer())
      while len(states) < len(expected_states):
        states.append(session.run(optimizer.state))
        session.run(train_op)

    for expected, actual in zip(expected_states, states):
      self.assertAllClose(expected, actual, rtol=0, atol=1e-6)

  def test_maximum_eigenvector_power_method(self):
    """Tests power method routine on some known left-stochastic matrices."""
    matrix1 = np.matrix([[0.6, 0.1, 0.1], [0.0, 0.6, 0.9], [0.4, 0.3, 0.0]])
    matrix2 = np.matrix([[0.4, 0.4, 0.2], [0.2, 0.1, 0.5], [0.4, 0.5, 0.3]])

    with self.session() as session:
      eigenvector1 = session.run(
          proxy_lagrangian_optimizer._maximal_eigenvector_power_method(
              tf.constant(matrix1)))
      eigenvector2 = session.run(
          proxy_lagrangian_optimizer._maximal_eigenvector_power_method(
              tf.constant(matrix2)))

    # Check that eigenvector1 and eigenvector2 are eigenvectors of matrix1 and
    # matrix2 (respectively) with associated eigenvalue 1.
    matrix_eigenvector1 = np.tensordot(matrix1, eigenvector1, axes=1)
    matrix_eigenvector2 = np.tensordot(matrix2, eigenvector2, axes=1)
    self.assertAllClose(eigenvector1, matrix_eigenvector1, rtol=0, atol=1e-6)
    self.assertAllClose(eigenvector2, matrix_eigenvector2, rtol=0, atol=1e-6)

  def test_project_distribution_wrt_euclidean_norm(self):
    """Tests Euclidean projection routine on some known values."""
    distributions = [
        tf.constant([-0.1, -0.8, -0.3]),
        tf.constant([-0.1, 0.4, 0.1]),
        tf.constant([0.4, 1.2, 0.2])
    ]
    expected_projected_distributions = [
        np.array([0.6, 0.0, 0.4]),
        np.array([0.1, 0.6, 0.3]),
        np.array([0.1, 0.9, 0.0])
    ]

    projected_distributions = []
    with self.session() as session:
      for distribution in distributions:
        projected_distributions.append(
            session.run(
                proxy_lagrangian_optimizer
                ._project_distribution_wrt_euclidean_norm(distribution)))

    self.assertAllClose(
        expected_projected_distributions,
        projected_distributions,
        rtol=0,
        atol=1e-6)

  def test_project_distribution_wrt_euclidean_norm_on_matrix(self):
    """Tests Euclidean projection routine on some known values."""
    matrix = tf.constant([[-0.1, -0.1, 0.4], [-0.8, 0.4, 1.2], [-0.3, 0.1,
                                                                0.2]])
    expected_projected_matrix = np.array([[0.6, 0.1, 0.1], [0.0, 0.6, 0.9],
                                          [0.4, 0.3, 0.0]])

    with self.session() as session:
      projected_matrix = session.run(
          proxy_lagrangian_optimizer._project_distribution_wrt_euclidean_norm(
              matrix))

    self.assertAllClose(
        expected_projected_matrix, projected_matrix, rtol=0, atol=1e-6)

  def test_project_log_distribution_wrt_kl_divergence(self):
    """Tests KL-divergence projection routine on some known values."""
    distributions = [
        tf.constant([0.2, 0.1, 0.2]),
        tf.constant([0.8, 0.2, 1.0]),
        tf.constant([0.6, 1.5, 0.9])
    ]
    expected_projected_distributions = [
        np.array([0.4, 0.2, 0.4]),
        np.array([0.4, 0.1, 0.5]),
        np.array([0.2, 0.5, 0.3])
    ]

    projected_distributions = []
    with self.session() as session:
      for distribution in distributions:
        projected_distributions.append(
            session.run(
                tf.exp(
                    proxy_lagrangian_optimizer
                    ._project_log_distribution_wrt_kl_divergence(
                        tf.log(distribution)))))

    self.assertAllClose(
        expected_projected_distributions,
        projected_distributions,
        rtol=0,
        atol=1e-6)

  def test_project_log_distribution_wrt_kl_divergence_on_matrix(self):
    """Tests KL-divergence projection routine on some known values."""
    matrix = tf.constant([[0.2, 0.8, 0.6], [0.1, 0.2, 1.5], [0.2, 1.0, 0.9]])
    expected_projected_matrix = np.array([[0.4, 0.4, 0.2], [0.2, 0.1, 0.5],
                                          [0.4, 0.5, 0.3]])

    with self.session() as session:
      projected_matrix = session.run(
          tf.exp(
              proxy_lagrangian_optimizer
              ._project_log_distribution_wrt_kl_divergence(tf.log(matrix))))

    self.assertAllClose(
        expected_projected_matrix, projected_matrix, rtol=0, atol=1e-6)

  def test_additive_external_proxy_lagrangian_optimizer(self):
    """Tests that the distributions update as expected."""
    minimization_problem = test_util.ConstantMinimizationProblem(
        np.array([0.6, -0.1, 0.4]))
    # Calculated using a numpy+python implementation of the algorithm.
    expected_states = [
        np.array([1.0, 0.0, 0.0, 0.0]),
        np.array([0.66666667, 0.26666667, 0.0, 0.06666667]),
        np.array([0.33333333, 0.53333333, 0.0, 0.13333333]),
    ]

    self._optimizer_test_helper(
        minimization_problem,
        expected_states,
        regret_type="external",
        update_type="additive")

  def test_multiplicative_external_proxy_lagrangian_optimizer(self):
    """Tests that the distributions update as expected."""
    minimization_problem = test_util.ConstantMinimizationProblem(
        np.array([0.6, -0.1, 0.4]))
    # Calculated using a numpy+python implementation of the algorithm.
    expected_states = [
        np.log(np.array([0.4, 0.2, 0.2, 0.2])),
        np.log(np.array([0.32160644, 0.29300257, 0.14550077, 0.23989022])),
        np.log(np.array([0.23910893, 0.3969348, 0.09788292, 0.26607335])),
    ]

    self._optimizer_test_helper(
        minimization_problem,
        expected_states,
        regret_type="external",
        update_type="multiplicative",
        initial_multiplier_radius=0.8)

  def test_additive_swap_proxy_lagrangian_optimizer(self):
    """Tests that the stochastic matrices update as expected."""
    minimization_problem = test_util.ConstantMinimizationProblem(
        np.array([0.6, -0.1, 0.4]))
    # Calculated using a numpy+python implementation of the algorithm.
    expected_states = [
        np.array([[1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]),
        np.array([[0.66666667, 1.0, 1.0, 1.0], [0.26666667, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0], [0.06666667, 0.0, 0.0, 0.0]]),
        np.array([[0.41666667, 0.93333333, 1.0, 0.98333333],
                  [0.46666667, 0.05333333, 0.0,
                   0.01333333], [0.0, 0.0, 0.0, 0.0],
                  [0.11666667, 0.01333333, 0.0, 0.00333333]]),
    ]

    self._optimizer_test_helper(
        minimization_problem,
        expected_states,
        regret_type="swap",
        update_type="additive")

  def test_multiplicative_swap_proxy_lagrangian_optimizer(self):
    """Tests that the stochastic matrices update as expected."""
    minimization_problem = test_util.ConstantMinimizationProblem(
        np.array([0.6, -0.1, 0.4]))
    # Calculated using a numpy+python implementation of the algorithm.
    expected_states = [
        np.log(
            np.array([[0.4, 0.4, 0.4, 0.4], [0.2, 0.2, 0.2, 0.2],
                      [0.2, 0.2, 0.2, 0.2], [0.2, 0.2, 0.2, 0.2]])),
        np.log(
            np.array([[0.36999014, 0.38528351, 0.38528351, 0.38528351],
                      [0.23517483, 0.21720297, 0.21720297, 0.21720297],
                      [0.17774131, 0.18882719, 0.18882719, 0.18882719],
                      [0.21709373, 0.20868632, 0.20868632, 0.20868632]])),
        np.log(
            np.array([[0.33972109, 0.36811863, 0.37118462, 0.36906575],
                      [0.27114826, 0.23738228, 0.23376693, 0.23626491],
                      [0.15712313, 0.17641793, 0.17858959, 0.17708679],
                      [0.23200752, 0.21808115, 0.21645886, 0.21758255]])),
    ]

    self._optimizer_test_helper(
        minimization_problem,
        expected_states,
        regret_type="swap",
        update_type="multiplicative",
        initial_multiplier_radius=0.8)


if __name__ == "__main__":
  tf.test.main()
