# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Transforms column using a label encoder to encode categories into numbers."""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import murmurhash3_32

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class LabelEncoderTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """Transforms column using a label encoder to encode categories into numbers."""

    def __init__(self, hashing_seed_val: int, logger: TransformerLogger = None):
        """
        Initialize for label encoding transform.

        :param hashing_seed_val: Seed value used for hashing if needed.
        :param logger: Logger to be injected to usage in this class.
        :return:
        """
        self._label_encoder = LabelEncoder()
        self._hashing_seed_val = hashing_seed_val
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Fit function for label encoding transform which learns the labels.

        :param x: Input array of integers or strings.
        :type x: numpy.ndarray
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        # Keep track of the labels
        self._label_encoder.fit(x)
        return self

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Label encoding transform categorical data into integers.

        :param x: Input array of integers or strings.
        :type x: numpy.ndarray
        :return: Label encoded array of ints.
        """
        # Find the new classes in 'x'
        new_classes = np.unique(x)

        # Check if new classes are being label encoded
        if len(
                np.intersect1d(
                    new_classes,
                    self._label_encoder.classes_)) < len(new_classes):

            # Create a set of new classes that are detected
            new_classes = np.setdiff1d(new_classes,
                                       self._label_encoder.classes_)

            # Walk each entry in x and map the new classes to existing classes
            x_new_with_known_classes = []
            for entry in x:
                if entry in new_classes:
                    # Compute the hash for the entry and then map it to some
                    # existing class
                    entry = self._label_encoder.classes_[
                        (murmurhash3_32(entry,
                                        seed=self._hashing_seed_val)) % len(
                            self._label_encoder.classes_)]

                x_new_with_known_classes.append(entry)

            # It is safe to run label encoder on all the existing classes
            return self._label_encoder.transform(x_new_with_known_classes)

        # Label encode x column
        return self._label_encoder.transform(x)
