# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Cast input to string."""
from sklearn.base import BaseEstimator, TransformerMixin

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class StringCastTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """
    Cast input to string.

    The input and output type is same for this transformer.
    """

    def __init__(self, logger: TransformerLogger = None):
        """Initialize the Logger object.

        :param logger: Logger to be injected to usage in this class.
        """
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Fit function for string cast transform.

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
        Transform data x into array of strings.

        :param x: The data to transform.
        :type x: numpy.ndarray
        :return: The transformed data which is an array of strings.
        """
        return x.astype(str)
