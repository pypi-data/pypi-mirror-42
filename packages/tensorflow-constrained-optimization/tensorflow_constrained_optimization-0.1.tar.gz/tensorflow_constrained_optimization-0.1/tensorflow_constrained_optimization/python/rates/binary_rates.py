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
"""Contains functions for constructing binary classification rate expressions.

A rate constraints problem is constructed as an objective function and set of
constraints, all of which are represented as `Expression`s, each of which
represents a linear combination of `Term`s (which represent rates) and
`Tensor`s.

Rates are things like the error rate, the false positive rate, and so on. The
functions in this file are responsible for constructing the objects that
represent such rates, which then are minimized or constrained to form an
optimization problem.

Example
=======

Suppose that "examples_tensor" and "labels_tensor" are placeholder `Tensor`s
containing training examples and their associated labels, and the "model"
function evaluates the model you're trying to train, returning a `Tensor` of
model evaluations. Further suppose that we wish to impose a fairness-style
constraint on a protected class (the "blue" examples). The following code will
create three contexts (see subsettable_context.py) representing all of the
examples, and only the "blue" examples, respectively.

>>> ctx = rate_context(model(examples_tensor), labels_tensor)
>>> blue_ctx = ctx.subset(examples_tensor[:, is_blue_idx])

Now that we have the contexts, we can create the rates. We'll try to minimize
the overall error rate, while constraining the true positive rate on the "blue"
class to be between 90% and 110% of the overall true positive rate:

>>> objective = error_rate(ctx)
>>> constraints = [
>>>     true_positive_rate(blue_ctx) >= 0.9 * true_positive_rate(ctx),
>>>     true_positive_rate(blue_ctx) <= 1.1 * true_positive_rate(ctx)
>>> ]

The error_rate() and true_positive_rate() functions are two of the
rate-constructing functions that are defined in this file. This objective and
list of constraints can then be passed on to the MinimizationProblem constructor
in rate_minimization_problem.py.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numbers
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

from tensorflow_constrained_optimization.python.rates import basic_expression
from tensorflow_constrained_optimization.python.rates import expression
from tensorflow_constrained_optimization.python.rates import loss
from tensorflow_constrained_optimization.python.rates import subsettable_context
from tensorflow_constrained_optimization.python.rates import term

_DEFAULT_PENALTY_LOSS = loss.HingeLoss()
_DEFAULT_CONSTRAINT_LOSS = loss.ZeroOneLoss()


def _binary_classification_rate(positive_coefficient=0.0,
                                negative_coefficient=0.0,
                                numerator_context=None,
                                denominator_context=None,
                                penalty_loss=_DEFAULT_PENALTY_LOSS,
                                constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing positive and negative rates.

  The result of this function represents:
    total_rate := (positive_coefficient * positive_rate +
        negative_coefficient * negative_rate)
  where:
    positive_rate := sum_i{w_i * c_i * d_i * 1{z_i >  0}} / sum_i{w_i * d_i}
    negative_rate := sum_i{w_i * c_i * d_i * 1{z_i <= 0}} / sum_i{w_i * d_i}
  where z_i and w_i are the given predictions and weights, and c_i and d_i are
  indicators for which examples to include the numerator and denominator (all
  four of z, w, c and d are in the contexts).

  The resulting `Expression` contains *two* different approximations to
  "total_rate". The "penalty" `BasicExpression` is an approximation to using
  penalty_loss, while the "constraint" `BasicExpression` is based on
  constraint_loss (if constraint_loss is the zero-one loss, which is the
  default, then the "constraint" expression will be exactly total_rate as
  defined above, with no approximation).

  The reason an `Expression` contains two `BasicExpression`s is that the
  "penalty" `BasicExpression` will be differentiable, while the "constraint"
  `BasicExpression` need not be. During optimization, the former will be used
  whenever we need to take gradients, and the latter otherwise.

  Args:
    positive_coefficient: float, scalar coefficient on the positive prediction
      rate.
    negative_coefficient: float, scalar coefficient on the negative prediction
      rate.
    numerator_context: `SubsettableContext`, the block of data to use when
      calculating the numerators of the rates.
    denominator_context: `SubsettableContext`, the block of data to use when
      calculating the denominators of the rates.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rates.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rates.

  Returns:
    An `Expression` representing total_rate (as defined above).

  Raises:
    TypeError: if either context is not a SubsettableContext, or either loss is
      not a BinaryClassificationLoss.
    ValueError: if either context is not provided, or the two contexts are
      incompatible (have different predictions, labels or weights).
  """
  if numerator_context is None or denominator_context is None:
    raise ValueError("both numerator_context and denominator_context must be "
                     "provided")
  if not (
      isinstance(numerator_context, subsettable_context.SubsettableContext) and
      isinstance(denominator_context, subsettable_context.SubsettableContext)):
    raise TypeError("numerator and denominator contexts must be "
                    "SubsettableContexts")
  raw_context = numerator_context.raw_context
  if denominator_context.raw_context != raw_context:
    raise ValueError("numerator and denominator contexts must be compatible")

  if not (isinstance(penalty_loss, loss.BinaryClassificationLoss) and
          isinstance(constraint_loss, loss.BinaryClassificationLoss)):
    raise TypeError("penalty and constraint losses must be "
                    "BinaryClassificationLosses")

  penalty_term = term.BinaryClassificationTerm.ratio(
      positive_coefficient, negative_coefficient,
      raw_context.penalty_predictions, raw_context.penalty_weights,
      numerator_context.penalty_predicate,
      denominator_context.penalty_predicate, penalty_loss)
  constraint_term = term.BinaryClassificationTerm.ratio(
      positive_coefficient, negative_coefficient,
      raw_context.constraint_predictions, raw_context.constraint_weights,
      numerator_context.constraint_predicate,
      denominator_context.constraint_predicate, constraint_loss)

  return expression.Expression(
      basic_expression.BasicExpression([penalty_term]),
      basic_expression.BasicExpression([constraint_term]))


def positive_prediction_rate(context,
                             penalty_loss=_DEFAULT_PENALTY_LOSS,
                             constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing a positive prediction rate.

  The result of this function represents:
    positive_rate := sum_i{w_i * c_i * 1{z_i > 0}} / sum_i{w_i * c_i}
  where z_i and w_i are the given predictions and weights, and c_i is an
  indicator for which examples to include in the rate (all three of z, w and c
  are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing positive_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
  """
  return _binary_classification_rate(
      positive_coefficient=1.0,
      numerator_context=context,
      denominator_context=context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


def negative_prediction_rate(context,
                             penalty_loss=_DEFAULT_PENALTY_LOSS,
                             constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing a negative prediction rate.

  The result of this function represents:
    negative_rate := sum_i{w_i * c_i * 1{z_i <= 0}} / sum_i{w_i * c_i}
  where z_i and w_i are the given predictions and weights, and c_i is an
  indicator for which examples to include in the rate (all three of z, w and c
  are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing negative_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
  """
  return _binary_classification_rate(
      negative_coefficient=1.0,
      numerator_context=context,
      denominator_context=context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


def error_rate(context,
               penalty_loss=_DEFAULT_PENALTY_LOSS,
               constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing an error rate.

  The result of this function represents:
    error_rate := (
        sum_i{w_i * c_i * 1{y_i <= 0} * 1{z_i > 0}} +
        sum_i{w_i * c_i * 1{y_i > 0} * 1{z_i <= 0}}
    ) / sum_i{w_i * c_i}
  where z_i, y_i and w_i are the given predictions, labels and weights, and c_i
  is an indicator for which examples to include in the rate (all four of z, y, w
  and c are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing error_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels.
  """
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("error_rate requires a context with labels")

  positive_context = context.subset(raw_context.penalty_labels > 0,
                                    raw_context.constraint_labels > 0)
  negative_context = context.subset(raw_context.penalty_labels <= 0,
                                    raw_context.constraint_labels <= 0)

  positive_expression = _binary_classification_rate(
      negative_coefficient=1.0,
      numerator_context=positive_context,
      denominator_context=context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)
  negative_expression = _binary_classification_rate(
      positive_coefficient=1.0,
      numerator_context=negative_context,
      denominator_context=context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)

  return positive_expression + negative_expression


def accuracy_rate(context,
                  penalty_loss=_DEFAULT_PENALTY_LOSS,
                  constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing an accuracy rate.

  The result of this function represents:
    accuracy_rate := (
        sum_i{w_i * c_i * 1{y_i > 0} * 1{z_i > 0}} +
        sum_i{w_i * c_i * 1{y_i <= 0} * 1{z_i <= 0}}
    ) / sum_i{w_i * c_i}
  where z_i, y_i and w_i are the given predictions, labels and weights, and c_i
  is an indicator for which examples to include in the rate (all four of z, y, w
  and c are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing accuracy_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels.
  """
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("accuracy_rate requires a context with labels")

  positive_context = context.subset(raw_context.penalty_labels > 0,
                                    raw_context.constraint_labels > 0)
  negative_context = context.subset(raw_context.penalty_labels <= 0,
                                    raw_context.constraint_labels <= 0)

  positive_expression = _binary_classification_rate(
      positive_coefficient=1.0,
      numerator_context=positive_context,
      denominator_context=context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)
  negative_expression = _binary_classification_rate(
      negative_coefficient=1.0,
      numerator_context=negative_context,
      denominator_context=context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)

  return positive_expression + negative_expression


def true_positive_rate(context,
                       penalty_loss=_DEFAULT_PENALTY_LOSS,
                       constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing a true positive rate.

  The result of this function represents:
    true_positive_rate :=
        sum_i{w_i * c_i * 1{y_i > 0} * 1{z_i > 0}}
            / sum_i{w_i * c_i * 1{y_i > 0}}
  where z_i, y_i and w_i are the given predictions, labels and weights, and c_i
  is an indicator for which examples to include in the rate (all four of z, y, w
  and c are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing true_positive_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels.
  """
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("true_positive_rate requires a context with labels")

  positive_context = context.subset(raw_context.penalty_labels > 0,
                                    raw_context.constraint_labels > 0)

  return _binary_classification_rate(
      positive_coefficient=1.0,
      numerator_context=positive_context,
      denominator_context=positive_context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


# The "true positive rate" is the same thing as the "recall", so we allow it to
# be accessed by either name.
recall = true_positive_rate


def false_negative_rate(context,
                        penalty_loss=_DEFAULT_PENALTY_LOSS,
                        constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing a false negative rate.

  The result of this function represents:
    false_negative_rate :=
        sum_i{w_i * c_i * 1{y_i > 0} * 1{z_i <= 0}}
            / sum_i{w_i * c_i * 1{y_i > 0}}
  where z_i, y_i and w_i are the given predictions, labels and weights, and c_i
  is an indicator for which examples to include in the rate (all four of z, y, w
  and c are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing false_negative_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels.
  """
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("false_negative_rate requires a context with labels")

  positive_context = context.subset(raw_context.penalty_labels > 0,
                                    raw_context.constraint_labels > 0)

  return _binary_classification_rate(
      negative_coefficient=1.0,
      numerator_context=positive_context,
      denominator_context=positive_context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


def false_positive_rate(context,
                        penalty_loss=_DEFAULT_PENALTY_LOSS,
                        constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing a false positive rate.

  The result of this function represents:
    false_positive_rate :=
        sum_i{w_i * c_i * 1{y_i <= 0} * 1{z_i > 0}}
            / sum_i{w_i * c_i * 1{y_i <= 0}}
  where z_i, y_i and w_i are the given predictions, labels and weights, and c_i
  is an indicator for which examples to include in the rate (all four of z, y, w
  and c are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing false_positive_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels.
  """
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("false_positive_rate requires a context with labels")

  negative_context = context.subset(raw_context.penalty_labels <= 0,
                                    raw_context.constraint_labels <= 0)

  return _binary_classification_rate(
      positive_coefficient=1.0,
      numerator_context=negative_context,
      denominator_context=negative_context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


def true_negative_rate(context,
                       penalty_loss=_DEFAULT_PENALTY_LOSS,
                       constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing a true negative rate.

  The result of this function represents:
    true_negative_rate :=
        sum_i{w_i * c_i * 1{y_i <= 0} * 1{z_i <= 0}}
            / sum_i{w_i * c_i * 1{y_i <= 0}}
  where z_i, y_i and w_i are the given predictions, labels and weights, and c_i
  is an indicator for which examples to include in the rate (all four of z, y, w
  and c are in the context).

  Please see the documentation of _binary_classification_rate() for further
  details.

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate.

  Returns:
    An `Expression` representing true_negative_rate (as defined above).

  Raises:
    TypeError: if the context is not a SubsettableContext, or either loss is not
      a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels.
  """
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("true_negative_rate requires a context with labels")

  negative_context = context.subset(raw_context.penalty_labels <= 0,
                                    raw_context.constraint_labels <= 0)

  return _binary_classification_rate(
      negative_coefficient=1.0,
      numerator_context=negative_context,
      denominator_context=negative_context,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


def _roc_auc(context,
             bins,
             lower_bound=False,
             upper_bound=False,
             penalty_loss=_DEFAULT_PENALTY_LOSS,
             constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing an approximate ROC AUC.

  The result of this function represents a Riemann approximation to the area
  under the ROC curve (false positive rate on the horizontal axis, true positive
  rate on the vertical axis), using the constraint-based method proposed by:

  > Eban, Schain, Mackey, Gordon, Rifkin and Elidan. "Scalable Learning of
  > Non-Decomposable Objectives". AISTATS 2017.

  If you're going to be lower-bounding or maximizing the result of this
  function, then need to set the lower_bound parameter to `True`. Likewise, if
  you're going to be upper-bounding or minimizing the result of this function
  (which normally wouldn't make much sense for ROC AUC), then the upper_bound
  parameter must be `True`. At least one of these parameters *must* be `True`,
  and it's permitted for both of them to be `True` (but we recommend against
  this, since it would result in equality constraints, which might cause
  problems during optimization and/or post-processing).

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    bins: positive integer, the number of "rectangles" to use for the Riemann
      approximation to ROC AUC.
    lower_bound: bool, `True` if you want the result of this function to
      lower-bound the approximate ROC AUC.
    upper_bound: bool, `True` if you want the result of this function to
      upper-bound the approximate ROC AUC.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate. This loss must be "normalized" (see
      `BinaryClassificationLoss.is_normalized`).

  Returns:
    An `Expression` representing a Riemann approximation to ROC AUC.

  Raises:
    TypeError: if the context is not a SubsettableContext, the number of bins is
      not an integer, or either loss is not a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels, the number of bins is
      nonpositive, both lower_bound and upper_bound are `False`, or the
      constraint_loss is not normalized.
  """
  if not isinstance(context, subsettable_context.SubsettableContext):
    raise TypeError("context must be a SubsettableContext")
  raw_context = context.raw_context
  if (raw_context.penalty_labels is None or
      raw_context.constraint_labels is None):
    raise ValueError("roc_auc_lower_bound requires a context with labels")

  if not isinstance(bins, numbers.Integral):
    raise TypeError("number of roc_auc_lower_bound bins must be an integer")
  if bins <= 0:
    raise ValueError("number of roc_auc_lower_bound bins must be strictly "
                     "positive")

  # One could set both lower_bound and upper_bound to True, in which case the
  # result of this function could be treated as the Riemann approximation to ROC
  # AUC itself (instead of a {lower,upper} bound of it). However, this would
  # come with some drawbacks: it would of course make optimization more
  # difficult, but more importantly, it would potentially cause post-processing
  # for feasibility (e.g. using "shrinking") to fail to find a feasible
  # solution.
  if not (lower_bound or upper_bound):
    raise ValueError("at least one of lower_bound or upper_bound must be True")

  if not (isinstance(penalty_loss, loss.BinaryClassificationLoss) and
          isinstance(constraint_loss, loss.BinaryClassificationLoss)):
    raise TypeError("penalty and constraint losses must be "
                    "BinaryClassificationLosses")

  # For the constraints on the false positive rates to make sense, it would be
  # best to be using a normalized loss. The reason for this is that, if both
  # lower_bound and upper_bound are True (or if one imposes constraints
  # including separate lower and upper bounds), our constraints on the false
  # positive rates will be equality constraints, which could be infeasible for
  # an unnormalized loss. This could be changed to a warning, however.
  if not constraint_loss.is_normalized:
    raise ValueError("roc_auc_lower_bound can only be used with a normalized "
                     "constraint_loss (e.g. zero/one, sigmoid or ramp)")

  dtype = raw_context.penalty_predictions.dtype.real_dtype
  if dtype != raw_context.constraint_predictions.dtype.real_dtype:
    raise ValueError("penalty and constraint predictions must have the same "
                     "dtype")
  # We use a lambda to initialize the thresholds so that, if this function call
  # is inside the scope of a tf.control_dependencies() block, the dependencies
  # will not be applied to the initializer.
  thresholds = tf.Variable(
      lambda: tf.zeros((bins,)), dtype=dtype, name="roc_auc_thresholds")

  positive_context = context.subset(raw_context.penalty_labels > 0,
                                    raw_context.constraint_labels > 0)
  negative_context = context.subset(raw_context.penalty_labels <= 0,
                                    raw_context.constraint_labels <= 0)

  penalty_average_tpr_terms = []
  constraint_average_tpr_terms = []
  extra_constraints = set()
  for bin_index in xrange(bins):
    threshold = thresholds[bin_index]

    # It's tempting to wrap tf.stop_gradient() around the threshold, so that
    # only the model parameters (and not the thresholds) will be adjusted to
    # increase the average true positive rate. However, this would prevent the
    # one-sided constraint, as described below, from working, since we need
    # something to be "pushing against" the constraint.
    penalty_tpr_term = term.BinaryClassificationTerm.ratio(
        1.0, 0.0, raw_context.penalty_predictions - threshold,
        raw_context.penalty_weights, positive_context.penalty_predicate,
        positive_context.penalty_predicate, penalty_loss)
    constraint_tpr_term = term.BinaryClassificationTerm.ratio(
        1.0, 0.0, raw_context.constraint_predictions - threshold,
        raw_context.constraint_weights, positive_context.constraint_predicate,
        positive_context.constraint_predicate, constraint_loss)

    penalty_average_tpr_terms.append(penalty_tpr_term / bins)
    constraint_average_tpr_terms.append(constraint_tpr_term / bins)

    # We wrap tf.stop_gradient() around the predictions because we want to
    # adjust the thresholds, and only the thresholds, to satisfy the false
    # positive rate constraints.
    penalty_fpr_term = term.BinaryClassificationTerm.ratio(
        1.0, 0.0,
        tf.stop_gradient(raw_context.penalty_predictions) - threshold,
        raw_context.penalty_weights, negative_context.penalty_predicate,
        negative_context.penalty_predicate, penalty_loss)
    constraint_fpr_term = term.BinaryClassificationTerm.ratio(
        1.0, 0.0,
        tf.stop_gradient(raw_context.constraint_predictions) - threshold,
        raw_context.constraint_weights, negative_context.constraint_predicate,
        negative_context.constraint_predicate, constraint_loss)

    fpr_expression = expression.Expression(
        basic_expression.BasicExpression([penalty_fpr_term]),
        basic_expression.BasicExpression([constraint_fpr_term]))
    target_fpr = (bin_index + 0.5) / bins
    # Ideally fpr_expression would equal target_fpr, but we prefer to only
    # impose a one-sided constraint (when exactly one of lower_bound or
    # upper_bound is True) since using an equality constraint would come with
    # drawbacks: it would of course make optimization more difficult, but more
    # importantly, it would potentially cause post-processing for feasibility
    # (e.g. using "shrinking") to fail to find a feasible solution.
    #
    # The reason why a <= constraint results in a lower bound, and a >=
    # constraint results in an upper bound, is that, in the lower-bound case
    # (the upper-bound case is similar), adjusting the threshold to increase the
    # FPR will increase the corresponding TPR, and therefore the ROC AUC
    # estimate. In other words, the objective (increasing ROC AUC, and therefore
    # the FPR of each bin) will be "pushing against" the constraint.
    if lower_bound:
      extra_constraints.add(fpr_expression <= target_fpr)
    if upper_bound:
      extra_constraints.add(fpr_expression >= target_fpr)

  return expression.Expression(
      basic_expression.BasicExpression(penalty_average_tpr_terms),
      basic_expression.BasicExpression(constraint_average_tpr_terms),
      extra_constraints)


def roc_auc_lower_bound(context,
                        bins,
                        penalty_loss=_DEFAULT_PENALTY_LOSS,
                        constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing an approximate lower bound on ROC AUC.

  The result of this function represents a lower bound on a Riemann
  approximation to the area under the ROC curve (false positive rate on the
  horizontal axis, true positive rate on the vertical axis), using the
  constraint-based method proposed by:

  > Eban, Schain, Mackey, Gordon, Rifkin and Elidan. "Scalable Learning of
  > Non-Decomposable Objectives". AISTATS 2017.

  If you're going to be lower-bounding or maximizing the result of this
  function, then you can think of it as being the approximate ROC AUC itself.
  It's different if you're going to be upper-bounding or minimizing the result,
  however, since the consequence would be to decrease the value of the lower
  bound, without affecting the model.

  Notice that the result of this function is *not* a lower bound on the ROC AUC.
  Rather, it's a lower bound on a Riemann approximation. As the number of bins
  increases, this approximation will improve (and the cost, in the form of the
  difficulty of optimizing a constrained optimization problem including an
  approximate ROC AUC, will increase).

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    bins: positive integer, the number of "rectangles" to use for the Riemann
      approximation to ROC AUC.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate. This loss must be "normalized" (see
      `BinaryClassificationLoss.is_normalized`).

  Returns:
    An `Expression` representing a lower bound on a Riemann approximation to ROC
    AUC.

  Raises:
    TypeError: if the context is not a SubsettableContext, the number of bins is
      not an integer, or either loss is not a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels, the number of bins is
      nonpositive, or the constraint_loss is not normalized.
  """
  return _roc_auc(
      context,
      bins,
      lower_bound=True,
      upper_bound=False,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)


def roc_auc_upper_bound(context,
                        bins,
                        penalty_loss=_DEFAULT_PENALTY_LOSS,
                        constraint_loss=_DEFAULT_CONSTRAINT_LOSS):
  """Creates an `Expression` representing an approximate upper bound on ROC AUC.

  The result of this function represents an upper bound on a Riemann
  approximation to the area under the ROC curve (false positive rate on the
  horizontal axis, true positive rate on the vertical axis), using the
  constraint-based method proposed by:

  > Eban, Schain, Mackey, Gordon, Rifkin and Elidan. "Scalable Learning of
  > Non-Decomposable Objectives". AISTATS 2017.

  If you're going to be upper-bounding or minimizing the result of this
  function, then you can think of it as being the approximate ROC AUC itself.
  It's different if you're going to be lower-bounding or maximizing the result,
  however, since the consequence would be to increase the value of the upper
  bound, without affecting the model.

  Notice that the result of this function is *not* an upper bound on the ROC
  AUC. Rather, it's an upper bound on a Riemann approximation. As the number of
  bins increases, this approximation will improve (and the cost, in the form of
  the difficulty of optimizing a constrained optimization problem including an
  approximate ROC AUC, will increase).

  Args:
    context: `SubsettableContext`, the block of data to use when calculating the
      rate. This context *must* contain labels.
    bins: positive integer, the number of "rectangles" to use for the Riemann
      approximation to ROC AUC.
    penalty_loss: `BinaryClassificationLoss`, the (differentiable) loss function
      to use when calculating the "penalty" approximation to the rate.
    constraint_loss: `BinaryClassificationLoss`, the (not necessarily
      differentiable) loss function to use when calculating the "constraint"
      approximation to the rate. This loss must be "normalized" (see
      `BinaryClassificationLoss.is_normalized`).

  Returns:
    An `Expression` representing an upper bound on a Riemann approximation to
    ROC AUC.

  Raises:
    TypeError: if the context is not a SubsettableContext, the number of bins is
      not an integer, or either loss is not a BinaryClassificationLoss.
    ValueError: if the context doesn't contain labels, the number of bins is
      nonpositive, or the constraint_loss is not normalized.
  """
  return _roc_auc(
      context,
      bins,
      lower_bound=False,
      upper_bound=True,
      penalty_loss=penalty_loss,
      constraint_loss=constraint_loss)
