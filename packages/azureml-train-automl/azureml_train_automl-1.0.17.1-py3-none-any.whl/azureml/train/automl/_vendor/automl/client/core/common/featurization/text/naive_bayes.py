# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Wrapper for sklearn Multinomial Naive Bayes."""
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.naive_bayes import MultinomialNB

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class NaiveBayes(BaseEstimator, TransformerMixin, TransformerLogger):
    """Wrapper for sklearn Multinomial Naive Bayes."""

    def __init__(self, logger: TransformerLogger = None):
        """Construct the Naive Bayes transformer.

        :param logger: Logger to be injected to usage in this class.
        """
        self.model = MultinomialNB()
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Naive Bayes transform to learn conditional probablities for textual data.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        self.model.fit(x, y)
        return self

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Transform data x.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :return: Prediction probability values from Naive Bayes model.
        """
        return self.model.predict_proba(x)
