# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Wrapper over pandas.cut for binning the train data into intervals and then applying them to test data."""
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class BinTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """
    Wrapper over pandas.cut for binning the train data into intervals and then applying them to test data.

    :param num_bins: Number of bins for binning the values into discrete
    intervals.
    :type num_bins: int
    """

    def __init__(self, num_bins: int = 5, logger: TransformerLogger = None):
        """
        Construct the BinTransformer.

        :param num_bins: Number of bins for binning the values into discrete intervals.
        :param logger: Logger to be injected to usage in this class.
        """
        self._num_bins = num_bins
        self._bins = None
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Identify the distribution of values with repect to the number of specified bins.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        _, self._bins = pd.cut(x, self._num_bins, retbins=True)
        return self

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Return the bins identified for the input values.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :return: The transformed data.
        """
        if self._bins is None:
            raise ValueError("BinTransformer not fit")
        return pd.cut(x, bins=self._bins, labels=False)
