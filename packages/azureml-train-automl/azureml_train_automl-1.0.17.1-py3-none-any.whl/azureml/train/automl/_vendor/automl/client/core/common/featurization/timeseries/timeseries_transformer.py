# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for timeseries preprocessing."""

import warnings
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from automl.client.core.common.constants import TimeSeries
from automl.client.core.common.featurization.logger import TransformerLogger
from automl.client.core.common.featurization.timeseries.missingdummies_transformer import MissingDummiesTransformer
from automl.client.core.common.featurization.timeseries.numericalize_transformer import NumericalizeTransformer
from automl.client.core.common.featurization.timeseries.abstract_timeseries_transformer \
    import AbstractTimeSeriesTransformer


# Prevent warnings when using Jupyter
warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None


class TimeSeriesTransformer(AbstractTimeSeriesTransformer):
    """Class for timeseries preprocess."""

    def __init__(self, logger=None, **kwargs):
        """
        Construct for the class.

        :param logger: The logger to be used in the pipeline.
        :type logger: logging.Logger
        :param kwargs: dictionary contains metadata for TimeSeries.
                       time_column_name: The column containing dates.
                       grain_column_names: The set of columns defining the
                       multiple time series.
                       origin_column_name: latest date from which actual values
                       of all features are assumed to be known with certainty.
                       drop_column_names: The columns which will needs
                       to be removed from the data set.
                       group: the group column name.
        :type kwargs: dict

        """
        super(TimeSeriesTransformer, self).__init__(logger, **kwargs)

    def _construct_pre_processing_pipeline(self, tsdf, drop_column_names):
        """Return the featurization pipeline."""
        from .forecasting_pipeline import AzureMLForecastPipeline
        from .grain_index_featurizer import GrainIndexFeaturizer
        from .time_series_imputer import TimeSeriesImputer
        from .time_index_featurizer import TimeIndexFeaturizer

        numerical_columns = [x for x in tsdf.select_dtypes(include=[np.number]).columns
                             if x not in drop_column_names]
        if self.target_column_name in numerical_columns:
            numerical_columns.remove(self.target_column_name)
        if self.original_order_column in numerical_columns:
            numerical_columns.remove(self.original_order_column)

        imputation_dict = {col: tsdf[col].median() for col in numerical_columns}
        impute_missing_numerical_values = TimeSeriesImputer(
            input_column=numerical_columns, value=imputation_dict, freq=self.freq)

        time_index_featurizer = TimeIndexFeaturizer(overwrite_columns=True)

        categorical_columns = [x for x in tsdf.select_dtypes(['object', 'category', 'bool']).columns
                               if x not in drop_column_names]
        if self.group_column in categorical_columns:
            categorical_columns.remove(self.group_column)

        # pipeline:
        default_pipeline = AzureMLForecastPipeline([
            ('make_numeric_na_dummies', MissingDummiesTransformer(numerical_columns)),
            ('impute_na_numeric_columns', impute_missing_numerical_values),
            ('make_time_index_featuers', time_index_featurizer)
        ])

        # Don't apply grain featurizer when there is single timeseries
        if self.dummy_grain_column not in self.grain_column_names:
            grain_index_featurizer = GrainIndexFeaturizer(overwrite_columns=True)
            default_pipeline.add_pipeline_step('make_grain_features', grain_index_featurizer)

        default_pipeline.add_pipeline_step('make_categoricals_numeric', NumericalizeTransformer())
        return default_pipeline
