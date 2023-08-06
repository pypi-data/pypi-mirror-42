# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Lamda function based transformer."""
from typing import Callable
from sklearn.base import BaseEstimator, TransformerMixin

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class LambdaTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """
    Transforms column through a lambda function.

    :param func: The lambda function to use in the transformation.
    :type func: function
    """

    def __init__(self, func: Callable, logger=None):
        """
        Construct the LambdaTransformer.

        :param func: The lambda function to use in the transformation.
        :param logger: Logger to be injected to usage in this class.
        :return:
        """
        self.func = func
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Fit function for lambda transform.

        :param x: Input array.
        :type x: numpy.ndarray
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        return self

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Lambda transform which calls the lambda function over the input.

        :param x: Input array.
        :type x: numpy.ndarray
        :return: Result of lambda transform.
        """
        return self.func(x)
