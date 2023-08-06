# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Preprocessing class that can be added in pipeline for input."""

import json
import math

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import Imputer
from sklearn_pandas import DataFrameMapper

from automl.client.core.common import constants, utilities
from automl.client.core.common._engineered_feature_names import _GenerateEngineeredFeatureNames, \
    FeatureTypeRecognizer, _Transformer, _TransformationFunctionNames, _FeatureTransformers, _OperatorNames
from automl.client.core.common.logging_utilities import function_debug_log_wrapped

from automl.client.core.common.featurization.categorical import HashOneHotVectorizerTransformer, \
    LabelEncoderTransformer, CatImputer

from automl.client.core.common.featurization.datetime import DateTimeFeaturesTransformer
from automl.client.core.common.featurization.generic import ImputationMarker
from automl.client.core.common.stats_computation import PreprocessingStatistics as _PreprocessingStatistics
from automl.client.core.common.featurization.text import StringCastTransformer, NaiveBayes, \
    get_ngram_len, max_ngram_len

from automl.client.core.common.featurization.logger import TransformerLogger
from automl.client.core.common.column_purpose_detection.columnpurpose_detector import ColumnPurposeDetector


class DataTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """
    Preprocessing class that can be added in pipeline for input.

    This class does the following:
    1. Numerical inputs treated as it is.
    2. For dates: year, month, day and hour are features
    3. For text, tfidf features
    4. Small number of unique values for a column that is not float become
        categoricals

    :param task: 'classification' or 'regression' depending on what kind of
    ML problem to solve.
    :type task: str or automl.client.core.common.constants.Tasks
    """

    def __init__(self, task=constants.Tasks.CLASSIFICATION, logger=None):
        """
        Initialize for data transformer for pre-processing raw user data.

        :param task: 'classification' or 'regression' depending on what kind
        of ML problem to solve.
        :type task: str or azureml.train.automl.constants.Tasks
        :param logger: External logger handler.
        :type logger: logging.Logger
        """
        if task not in \
                [constants.Tasks.CLASSIFICATION, constants.Tasks.REGRESSION]:
            raise ValueError("Unknown task")

        self._task_type = task
        self.mapper = None

        # External logger if None, then no logs
        self._init_logger(logger)
        # Maintain a list of raw feature names
        self._raw_feature_names = []
        # Maintain engineered feature name class
        self._engineered_feature_names_class = None
        # Maintain statistics about the pre-processing stage
        self._pre_processing_stats = _PreprocessingStatistics()
        # Hashing seed value for murmurhash
        self._hashing_seed_value = 314489979

    def _learn_transformations(self, df, y=None):
        """
        Learn data transformation to be done on the raw data.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        """
        utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if self._engineered_feature_names_class is None:
            # Create class for engineered feature names
            self._engineered_feature_names_class = \
                _GenerateEngineeredFeatureNames()

        self.mapper = DataFrameMapper(
            self._get_transforms(df), input_df=True, sparse=True)

    def fit_transform_with_logger(self, X, y=None, logger=None, **fit_params):
        """
        Wrap the fit_transform function for the Data transformer class.

        :param X: Dataframe representing text, numerical or categorical input.
        :type X:numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        :param fit_params: Additional parameters for fit_transform().
        :param logger: External logger handler.
        :type logger: logging.Logger
        :return: Transformed data.
        """
        # Init the logger
        self.logger = logger
        # Call the fit and transform function
        return self.fit_transform(X, y, **fit_params)

    def fit(self, df, y=None):
        """
        Perform the raw data validation and identify the transformations to apply.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        :return: DataTransform object.
        :raises: Value Error for non-dataframe and empty dataframes.
        """
        utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if not self.mapper:
            self._logger_wrapper(
                'info', 'Featurizer mapper not found so learn all ' +
                'the transforms')
            self._learn_transformations(df, y)

        self.mapper.fit(df, y)

        return self

    @function_debug_log_wrapped
    def transform(self, df):
        """
        Transform the input raw data with the transformations idetified in fit stage.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :return: Numpy array.
        """
        if not self.mapper:
            raise Exception("fit not called")

        utilities.check_input(df)

        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        transformed_data = self.mapper.transform(df)

        if self._engineered_feature_names_class is not None:
            if not self._engineered_feature_names_class.are_engineered_feature_names_available():
                # Generate engineered feature names if they are not already generated
                self._engineered_feature_names_class.parse_raw_feature_names(self.mapper.transformed_names_)

        return transformed_data

    def get_engineered_feature_names(self):
        """
        Get the engineered feature names.

        Return the list of engineered feature names as string after data transformations on the
        raw data have been finished.

        :return: The list of engineered fearure names as strings
        """
        return self._engineered_feature_names_class._engineered_feature_names

    def _get_json_str_for_engineered_feature_name(self,
                                                  engineered_feature_name):
        """
        Return JSON string for engineered feature name.

        :param engineered_feature_name: Engineered feature name for
                                        whom JSON string is required
        :return: JSON string for engineered feature name
        """
        engineered_feature_name_json_obj = \
            self._engineered_feature_names_class.\
            get_json_object_for_engineered_feature_name(
                engineered_feature_name)

        # If the JSON object is not valid, then return None
        if engineered_feature_name_json_obj is None:
            self._logger_wrapper(
                'info', "Not a valid feature name " + engineered_feature_name)
            return None

        # Convert JSON into string and return
        return json.dumps(engineered_feature_name_json_obj)

    def get_json_strs_for_engineered_feature_names(self,
                                                   engi_feature_name_list):
        """
        Return JSON string list for engineered feature names.

        :param engi_feature_name_list: Engineered feature names for
                                       whom JSON strings are required
        :return: JSON string list for engineered feature names
        """
        engineered_feature_names_json_str_list = []

        # Walk engineering feature name list and get the corresponding
        # JSON string
        for engineered_feature_name in engi_feature_name_list:

            json_str = \
                self._get_json_str_for_engineered_feature_name(
                    engineered_feature_name)

            if json_str is not None:
                engineered_feature_names_json_str_list.append(json_str)

        # Return the list of JSON strings for engineered feature names
        return engineered_feature_names_json_str_list

    def _get_transforms(self, df):
        """
        Identify the transformations for all the columns in the dataframe.

        :param df: Input dataframe.
        :type df: numpy.ndarray or pandas.DataFrame
        :return: Transformations that go into datamapper.
        """
        transforms = []

        # drop columns that have only missing data
        df = df.dropna(axis=1, how="all")

        # In case column names are not specified by the user,
        # append the some column name with a counter to generate a
        # raw feature name
        column_name = 'C'
        index_raw_columns = 0

        self._logger_wrapper('info', "Start getting transformers.")
        for dtype, column in zip(df.dtypes, df.columns):

            # If column name is not an integer, then record it
            # in the raw feature name
            if not isinstance(column, (int, np.integer)):
                self._raw_feature_names.append(column)
                new_column_name = column
            else:
                # If the column name is missing, create a new column name
                # for the transformations
                index_raw_columns += 1
                new_column_name = column_name + str(index_raw_columns)

            # Get stats_computation for the current column
            raw_stats, feature_type_detected = ColumnPurposeDetector._detect_feature_type(column, df)

            utilities._log_raw_data_stat(
                raw_stats, self.logger,
                prefix_message="[XColNum:{}]".format(
                    df.columns.get_loc(column)
                )
            )

            self._logger_wrapper(
                'info',
                "Preprocess transformer for col {}, datatype: {}, detected "
                "datatype {}".format(
                    df.columns.get_loc(column),
                    str(dtype),
                    str(feature_type_detected)
                )
            )

            # Update pre-processing stats_computation
            self._pre_processing_stats.update_raw_feature_stats(
                feature_type_detected)

            if feature_type_detected == FeatureTypeRecognizer.Numeric:
                transforms.extend(self._get_numeric_transforms(
                    column, new_column_name))
                # if there are lot of imputed values, add an imputation marker
                if raw_stats.num_na > 0.01 * raw_stats.total_number_vals:
                    transforms.extend(
                        self._get_imputation_marker_transforms(
                            column, new_column_name))
            elif feature_type_detected == FeatureTypeRecognizer.DateTime:
                transforms.extend(self._get_datetime_transforms(
                    column, new_column_name))
            elif feature_type_detected == \
                    FeatureTypeRecognizer.CategoricalHash:
                transforms.extend(self._get_categorical_hash_transforms(
                    column, new_column_name, raw_stats.num_unique_vals))
            elif feature_type_detected == \
                    FeatureTypeRecognizer.Categorical:
                transforms.extend(self._get_categorical_transforms(
                    column, new_column_name, raw_stats.num_unique_vals))
            elif feature_type_detected == FeatureTypeRecognizer.Text:
                transforms.extend(
                    self._get_text_transforms(column, new_column_name, get_ngram_len(raw_stats.lengths)))
            else:
                # skip if hashes or ignore case
                self._logger_wrapper(
                    'info',
                    "Hashes or single value column detected. No transforms "
                    "needed")
                continue

        if not transforms:
            # can happen when we get all hashes
            self._logger_wrapper(
                'warning', "No features could be identified or generated")
            raise ValueError("No features could be identified or generated")

        # Log the transformations done for raw data into the logs
        self._logger_wrapper('info',
                             self._get_transformations_str(df, transforms))

        # Log stats_computation about raw data
        self._logger_wrapper('info',
                             self._pre_processing_stats.get_raw_data_stats())

        self._logger_wrapper('info', "End getting transformers.")

        return transforms

    def _get_categorical_hash_transforms(self,
                                         column,
                                         column_name,
                                         num_unique_categories):
        """
        Create a list of transforms for categorical hash data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param num_unique_categories: Number of unique categories
        :return: Categorical hash transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the hashing one hot encode transform.
        categorical_hash_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None,
            feature_type=FeatureTypeRecognizer.CategoricalHash,
            should_output=False)
        # This transformation depends on the previous# transformation
        categorical_hash_onehot_encode_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.HashOneHotEncode,
            operator=None, feature_type=None,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = \
            _FeatureTransformers(
                [categorical_hash_string_cast_transformer,
                 categorical_hash_onehot_encode_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.
        number_of_bits = pow(2, int(math.log(num_unique_categories, 2)) + 1)
        tr = [(column, [StringCastTransformer(logger=self.logger),
                        HashOneHotVectorizerTransformer(
                            hashing_seed_val=self._hashing_seed_value,
                            num_cols=int(number_of_bits),
                            logger=self.logger)],
               {'alias': str(alias_column_name)})]

        return tr

    def _get_datetime_transforms(self, column, column_name):
        """
        Create a list of transforms for date time data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Date time transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the date time transform.
        datatime_imputer_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.Imputer,
            operator=_OperatorNames.Mode,
            feature_type=FeatureTypeRecognizer.DateTime,
            should_output=True)
        # This transformation depends on the previous transformation
        datatime_string_cast_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None, feature_type=None,
            should_output=False)
        # This transformation depends on the previous transformation
        datatime_datetime_transformer = _Transformer(
            parent_feature_list=[2],
            transformation_fnc=_TransformationFunctionNames.DateTime,
            operator=None, feature_type=None,
            should_output=False)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers(
            [datatime_imputer_transformer,
             datatime_string_cast_transformer,
             datatime_datetime_transformer])
        # Create the JSON object
        json_obj = \
            feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.
        tr = [(column,
               [CatImputer(logger=self.logger),
                StringCastTransformer(logger=self.logger),
                DateTimeFeaturesTransformer(logger=self.logger)],
               {'alias': str(alias_column_name)})]

        return tr

    def _get_categorical_transforms(self, column,
                                    column_name,
                                    num_unique_categories):
        """
        Create a list of transforms for categorical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param num_unique_categories: Number of unique categories
        :return: Categorical transformations to use in a list.
        """
        if num_unique_categories <= 2:

            # Add the transformations to be done and get the alias name
            # for the hashing label encode transform.
            cat_two_category_imputer_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=_TransformationFunctionNames.Imputer,
                operator=_OperatorNames.Mode,
                feature_type=FeatureTypeRecognizer.Categorical,
                should_output=True)
            # This transformation depends on the previous transformation
            cat_two_category_string_cast_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=_TransformationFunctionNames.StringCast,
                operator=None, feature_type=None,
                should_output=False)
            # This transformation depends on the previous transformation
            cat_two_category_label_encode_transformer = _Transformer(
                parent_feature_list=[2],
                transformation_fnc=_TransformationFunctionNames.LabelEncoder,
                operator=None, feature_type=None,
                should_output=True)
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers(
                [cat_two_category_imputer_transformer,
                 cat_two_category_string_cast_transformer,
                 cat_two_category_label_encode_transformer])
            # Create the JSON object
            json_obj = \
                feature_transformers.encode_transformations_from_list()
            # Persist the JSON object for later use and obtain an alias name
            alias_column_name = \
                self._engineered_feature_names_class.\
                get_raw_feature_alias_name(json_obj)

            # Add the transformations to be done and get the alias name
            # for the raw column.
            tr = [(column,
                   [CatImputer(logger=self.logger),
                    StringCastTransformer(logger=self.logger),
                    LabelEncoderTransformer(
                        hashing_seed_val=self._hashing_seed_value,
                        logger=self.logger)],
                   {'alias': str(alias_column_name)})]

            return tr
        else:
            # Add the transformations to be done and get the alias name
            # for the hashing one hot encode transform.
            cat_multiple_category_string_cast_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=_TransformationFunctionNames.StringCast,
                operator=None, feature_type=FeatureTypeRecognizer.Categorical,
                should_output=False)
            # This transformation depends on the previous transformation
            cat_multiple_category_countvec_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=_TransformationFunctionNames.CountVec,
                operator=_OperatorNames.CharGram, feature_type=None,
                should_output=True)
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers([
                cat_multiple_category_string_cast_transformer,
                cat_multiple_category_countvec_transformer])
            # Create the JSON object
            json_obj = \
                feature_transformers.encode_transformations_from_list()
            # Persist the JSON object for later use and obtain an alias name
            alias_column_name = \
                self._engineered_feature_names_class.\
                get_raw_feature_alias_name(json_obj)

            # use CountVectorizer for both Hash and CategoricalHash for now
            tr = [(column, [StringCastTransformer(logger=self.logger),
                            CountVectorizer(
                                tokenizer=self._wrap_in_lst,
                                binary=True)
                            ],
                   {'alias': str(alias_column_name)})]

            return tr

    def _get_numeric_transforms(self, column, column_name):
        """
        Create a list of transforms for numerical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Numerical transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the numerical transform
        numeric_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.Imputer,
            operator=_OperatorNames.Mean,
            feature_type=FeatureTypeRecognizer.Numeric,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([numeric_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        # floats or ints go as they are, we only fix NaN
        tr = [([column], [Imputer()], {'alias': str(alias_column_name)})]

        return tr

    def _get_imputation_marker_transforms(self, column, column_name):
        """
        Create a list of transforms for numerical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Numerical transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        imputation_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.ImputationMarker,
            operator=None, feature_type=FeatureTypeRecognizer.Numeric,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([imputation_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        tr = [([column],
               [ImputationMarker(logger=self.logger)],
               {'alias': str(alias_column_name)})]

        return tr

    def _get_text_transforms(self, column, column_name, ngram_len):
        """
        Create a list of transforms for text data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param ngram_len: Continous length of characters or number of words.
        :return: Text transformations to use in a list.
        """
        ngram_len = min(max_ngram_len, ngram_len)

        # Add the transformations to be done and get the alias name
        # for the trichar transform.
        text_trichar_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None, feature_type=FeatureTypeRecognizer.Text,
            should_output=False)
        # This transformation depends on the previous transformation
        text_trichar_tfidf_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.Tf,
            operator=_OperatorNames.CharGram, feature_type=None,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([
            text_trichar_string_cast_transformer,
            text_trichar_tfidf_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        tfidf_trichar_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the bigram word transform.
        text_biword_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None, feature_type=FeatureTypeRecognizer.Text,
            should_output=False)
        # This transformation depends on the previous transformation
        text_biword_tfidf_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.Tf,
            operator=_OperatorNames.WordGram, feature_type=None,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([
            text_biword_string_cast_transformer,
            text_biword_tfidf_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        tfidf_biword_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)
        tr = [(column,
               [
                   StringCastTransformer(logger=self.logger),
                   TfidfVectorizer(use_idf=False, norm='l2', max_df=0.95,
                                   analyzer='char',
                                   ngram_range=(1, ngram_len))
               ],
               {
                   'alias': str(tfidf_trichar_column_name)
               }
               ),
              (column,
               [
                   StringCastTransformer(logger=self.logger),
                   TfidfVectorizer(use_idf=False, norm='l2',
                                   analyzer='word',
                                   ngram_range=(1, 2))
               ],
               {
                   'alias': str(tfidf_biword_column_name)
               }
               )]

        if self._task_type == constants.Tasks.CLASSIFICATION:
            # Add the transformations to be done and get the alias name
            # for the count vec transform.
            text_imputer_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=_TransformationFunctionNames.Imputer,
                operator=_OperatorNames.Mode,
                feature_type=FeatureTypeRecognizer.Text,
                should_output=True)
            # This transformation depends on the previous transformation
            text_string_cast_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=_TransformationFunctionNames.StringCast,
                operator=None, feature_type=None,
                should_output=False)
            # This transformation depends on the previous transformation
            text_countvec_transformer = _Transformer(
                parent_feature_list=[2],
                transformation_fnc=_TransformationFunctionNames.CountVec,
                operator=_OperatorNames.WordGram, feature_type=None,
                should_output=True)
            # This transformation depends on the previous transformation
            text_naivebayes_transformer = _Transformer(
                parent_feature_list=[3],
                transformation_fnc=_TransformationFunctionNames.NaiveBayes,
                operator=None, feature_type=None,
                should_output=True)
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers([
                text_imputer_transformer,
                text_string_cast_transformer,
                text_countvec_transformer,
                text_naivebayes_transformer])
            # Create the JSON object
            json_obj = feature_transformers.encode_transformations_from_list()
            # Persist the JSON object for later use and obtain an alias name
            count_vec_column_name = \
                self._engineered_feature_names_class.\
                get_raw_feature_alias_name(json_obj)

            # Add the transformations to be done and get the alias name
            # for the raw column.
            tr.append((column,
                       [
                           CatImputer(logger=self.logger),
                           StringCastTransformer(logger=self.logger),
                           CountVectorizer(analyzer='word',
                                           ngram_range=(1, 1)),
                           NaiveBayes(logger=self.logger)
                       ],
                       {
                           'alias': str(count_vec_column_name)
                       }))

        return tr

    def _wrap_in_lst(self, x):
        """
        Wrap an element in list.

        :param x: Element like string or integer.
        """
        return [x]

    def _get_transformations_str(self, df, transforms):
        """
        Get the data transformations recorded for raw columns as strings.

        :param df: Input dataframe.
        :type df:numpy.ndarray or pandas.DataFrame or sparse matrix
        :param transforms: List of applied transformations for various raw
        columns as a string.
        :type transforms: List
        """
        transformation_str = 'Transforms:\n'
        list_of_transforms_as_list = []

        # Walk all columns in the input dataframe
        for column in df.columns:

            # Get all the indexes of transformations for the current column
            column_matches_transforms = \
                [i for i in range(0, len(transforms))
                 if transforms[i][0] == column]

            # If no matches for column name is found, then look for list having
            # this column name
            if len(column_matches_transforms) == 0:
                column_matches_transforms = \
                    [i for i in range(0, len(transforms))
                     if transforms[i][0] == [column]]

            # Walk all the transformations found for the current column and add
            # to a string
            for transform_index in column_matches_transforms:
                some_str = 'col {}, transformers: {}'.format(
                    df.columns.get_loc(column),
                    '\t'.join([tf.__class__.__name__ for tf
                               in transforms[transform_index][1]]))
                list_of_transforms_as_list.append(some_str)

        transformation_str += '\n'.join(list_of_transforms_as_list)

        # Return the string representation of all the transformations
        return transformation_str
