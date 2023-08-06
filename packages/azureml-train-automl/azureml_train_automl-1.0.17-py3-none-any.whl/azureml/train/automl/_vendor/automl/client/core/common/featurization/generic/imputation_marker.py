# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Add boolean imputation marker for values that are imputed."""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class ImputationMarker(BaseEstimator, TransformerMixin, TransformerLogger):
    """Add boolean imputation marker for values that are imputed."""

    def __init__(self, logger: TransformerLogger = None):
        """
        Initialize the Logger object.

        :param logger: Logger to be injected to usage in this class.
        """
        self.logger = logger

    def fit(self, x, y=None):
        """
        Fit function for imputation marker transform.

        :param x: Input array of integers or strings.
        :type x: numpy.ndarray or pandas.series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        return self

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Transform function for imputation marker.

        :param x: Input array of integers or strings.
        :type x: numpy.ndarray or pandas.series
        :return: Boolean array having True where the value is not present.
        """
        return pd.isnull(x).values
