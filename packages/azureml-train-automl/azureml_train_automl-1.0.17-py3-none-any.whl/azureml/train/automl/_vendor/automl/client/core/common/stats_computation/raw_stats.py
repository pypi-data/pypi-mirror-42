# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for computing feature stats_computation from raw features."""
from collections import defaultdict
import numpy as np

from automl.client.core.common import utilities
from automl.client.core.common._engineered_feature_names import FeatureTypeRecognizer
from automl.client.core.common.featurization.datetime import is_date


class RawFeatureStats:
    """
    Class for computing feature stats_computation from raw features.

    :param raw_column: Column having raw data.
    :type raw_column: numpy.ndarray
    """

    # max size in characters for ngram
    _max_ngram = 3
    # Hashing seed value for murmurhash
    _hashing_seed_value = 314489979

    def __init__(self, raw_column):
        """
        Calculate stats_computation for the input column.

        These stats_computation are needed for deciding the data type of the column.

        :param raw_column: Column having raw data.
        :type raw_column: numpy.ndarray
        """
        # Number of unique values in the column
        self.num_unique_vals = raw_column.unique().shape[0]
        # Total number of values in the column
        self.total_number_vals = raw_column.shape[0]
        # Create a series having lengths of the entries in the column
        self.lengths = raw_column.apply(lambda x: len(str(x)))
        # Calculate the number of lengths of the entries in the column
        self.num_unique_lens = self.lengths.unique().shape[0]
        # Get the column type
        self.column_type = utilities._get_column_data_type_as_str(raw_column.values)
        # Average lengths of an entry in the column
        self.average_entry_length = 0
        # Average number of spaces in an entry in the column
        self.average_number_spaces = 0
        # Number of missing values in the column
        self.num_na = raw_column.isnull().sum()

        # Detect if the column has date time format
        non_na = raw_column.dropna()
        num_dates = np.sum(non_na.apply(str).apply(is_date))
        self.is_datetime = False
        if num_dates == non_na.shape[0] and non_na.shape[0] > 0:
            self.is_datetime = True

        for column_entry in raw_column:
            # if not np.isnan(column_entry):
            self.average_entry_length += len(str(column_entry))
            self.average_number_spaces += str(column_entry).count(' ')

        self.average_entry_length /= 1.0 * self.total_number_vals
        self.average_number_spaces /= 1.0 * self.total_number_vals

        self.cardinality_ratio = (1.0 * self.num_unique_vals) / self.total_number_vals


class PreprocessingStatistics:
    """
    Keeps statistics about the pre-processing stage in AutoML.

    Records the number of various feature types detected from
    the raw data
    """

    def __init__(self):
        """Initialize all statistics about the raw data."""
        # Dictionary to capture all raw feature stats_computation
        self.num_raw_feature_type_detected = defaultdict(int)

    def update_raw_feature_stats(self, feature_type):
        """Increment the counters for different types of features."""
        if feature_type in FeatureTypeRecognizer.FULL_SET:
            self.num_raw_feature_type_detected[feature_type] += 1

    def get_raw_data_stats(self):
        """Return the string for overall raw feature stats_computation."""
        str_overall_raw_stats = 'The stats_computation for raw data are following:-'
        for feature_type in FeatureTypeRecognizer.FULL_SET:
            str_overall_raw_stats += \
                '\n\tNumber of ' + feature_type + ' features: ' + \
                str(self.num_raw_feature_type_detected[feature_type])

        return str_overall_raw_stats
