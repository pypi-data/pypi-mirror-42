# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Helper methods to execute an AutoML pipeline fit."""
from typing import Any, Dict, List, Optional, Tuple, Union
import copy
import json
import os

import sklearn.pipeline
from sklearn.pipeline import Pipeline as SKPipeline
from automl.client.core.common import pipeline_spec as pipeline_spec_module
from automl.client.core.common.datasets import ClientDatasets, SubsampleCacheStrategy
from automl.client.core.common.exceptions import ConfigException
from automl.client.core.common.limit_function_call_for_win import enforce_time_limit
from automl.client.core.common.logging_utilities import LogConfig
from automl.client.core.common.metrics import get_default_metrics
from automl.client.core.common.model_wrappers import PipelineWithYTransformations
from automl.client.core.common.resource_limits import default_resource_limits, safe_enforce_limits
from automl.client.core.common.runner import ClientRunner

from . import constants, utilities
from .automl_base_settings import AutoMLBaseSettings
from .automl_pipeline import AutoMLPipeline
from .automl_run_context import AutoMLAbstractRunContext
from .data_context import TransformedDataContext

SOURCE_WRAPPER_MODULE = 'automl.client.core.common.model_wrappers'
DEFAULT_DATASET_NAME = 'NoName'


class PipelineRunOutput:
    """Data class used to encapsulate return values from calling run_pipeline."""

    def __init__(self, automl_settings: AutoMLBaseSettings, pipeline_obj: SKPipeline, training_type: str):
        """
        Initialize a PipelineRunOutput object.

        :param automl_settings: the settings object used for pipeline execution
        :param pipeline_obj: the pipeline being executed
        :param training_type: the training type
        """
        self._training_type = training_type
        self._run_template = 'automl_child'
        self._run_preprocessor, self._run_algorithm = self._get_preprocessor_and_algorithm(automl_settings,
                                                                                           pipeline_obj)
        self._fit_time = 0
        self._scores = constants.Defaults.INVALID_PIPELINE_VALIDATION_SCORES
        self._fitted_pipeline = constants.Defaults.INVALID_PIPELINE_FITTED  # type: Union[SKPipeline, str]
        self._fitted_pipelines_train = constants.Defaults.INVALID_PIPELINE_FITTED  # type: Union[List[SKPipeline], str]

    def record_pipeline_output(self,
                               scores: Dict[str, Any],
                               fit_time: float,
                               fitted_pipeline: SKPipeline,
                               fitted_pipelines_train: Union[List[SKPipeline], str]):
        """
        Save output from a successful pipeline execution.

        :param scores: a dictionary containing metric scores
        :param fit_time: the time taken to execute the pipeline, in seconds
        :param fitted_pipeline: the fitted model
        :param fitted_pipelines_train: the partially trained pipelines when using cross validation
        :return:
        """
        self._scores = scores
        self._fit_time = fit_time
        self._fitted_pipeline = fitted_pipeline
        self._fitted_pipelines_train = fitted_pipelines_train

    @property
    def fit_time(self) -> float:
        """
        Get the fit time.

        TODO: when Jasmine PR #181653 goes in, this will only describe the fit time, not fit + predict time.
        """
        return self._fit_time

    @property
    def scores(self) -> Dict[str, Any]:
        """Get the scores."""
        return self._scores

    @property
    def fitted_pipeline(self) -> Union[SKPipeline, str]:
        """Get the fitted model."""
        return self._fitted_pipeline

    @property
    def fitted_pipelines_train(self) -> Union[List[SKPipeline], str]:
        """Get the partially trained fitted models."""
        return self._fitted_pipelines_train

    @property
    def run_properties(self) -> Optional[str]:
        """Get the pipeline run properties."""
        if self.fitted_pipeline is None:
            return None
        try:
            pipeline_step_str = str(self.fitted_pipeline.steps[1][1])
            return pipeline_step_str[pipeline_step_str.find("(") + 1:
                                     pipeline_step_str.find(")")]
        except IndexError:
            return None

    @property
    def training_type(self) -> str:
        """Get the training type."""
        return self._training_type

    @property
    def pretrain_props(self) -> Dict[str, Optional[str]]:
        """Get the pretrain properties."""
        return {
            'run_template': self._run_template,
            'run_preprocessor': self._run_preprocessor,
            'run_algorithm': self._run_algorithm
        }

    @property
    def pretrain_props_sanitized(self) -> Dict[str, str]:
        """Get the pretrain properties with None converted to empty string."""
        return utilities.convert_dict_values_to_str(self.pretrain_props)

    @classmethod
    def _get_preprocessor_and_algorithm(cls,
                                        automl_settings: AutoMLBaseSettings,
                                        pipeline_obj: SKPipeline) -> Tuple[Optional[str], Optional[str]]:
        """
        Given a sklearn pipeline, retrieve the preprocessor and algorithm names.

        :param pipeline_obj: sklearn.pipeline.Pipeline
        :return: a tuple of preprocessor and algorithm names
        """
        try:
            # for the Ensemble pipelines we will not have any preprocessors
            if len(pipeline_obj.steps) == 1:
                preprocessor = None
                algorithm = pipeline_obj.steps[0][0]
            else:
                preprocessor = pipeline_obj.steps[0][0]
                algorithm = pipeline_obj.steps[1][0]
            return preprocessor, cls._map_algorithm_name(automl_settings, algorithm)
        except Exception:
            return None, None

    @staticmethod
    def _map_algorithm_name(automl_settings: AutoMLBaseSettings, run_algorithm: str) -> str:
        if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
            return constants.ModelNameMappings.ClassNameToCustomerFacingModelMapClassification.get(run_algorithm,
                                                                                                   run_algorithm)
        elif automl_settings.task_type == constants.Tasks.REGRESSION:
            return constants.ModelNameMappings.ClassNameToCustomerFacingModelMapRegression.get(run_algorithm,
                                                                                               run_algorithm)


def run_pipeline(automl_settings: AutoMLBaseSettings,
                 automl_pipeline: AutoMLPipeline,
                 automl_run_context: AutoMLAbstractRunContext,
                 iteration_timeout_min: Optional[int],
                 transformed_data_context: TransformedDataContext,
                 logger,
                 remote: bool) -> PipelineRunOutput:
    """
    Run a pipeline using the given settings and context.

    :param automl_settings: settings object to use for this job.
    :param automl_pipeline: the pipeline definition to use for this job.
    :param automl_run_context: the run context to use for this job.
    :param iteration_timeout_min: upper bound for how long this job can take. Passing None disables timeout.
    :param transformed_data_context: the data to use for this job.
    :param logger: the logger to use for this job.
    :param remote: whether we are running remotely or not.
    :return: a PipelineRunOutput object containing the results
    """
    enforce_time_on_win_required = False
    if iteration_timeout_min is not None and \
            not safe_enforce_limits.ok and \
            automl_settings.enforce_time_on_windows and \
            os.name == 'nt':
        enforce_time_on_win_required = True

    metrics = get_default_metrics(automl_settings.task_type)

    # for CV, we'll save the partially trained models on each split,
    # along with the model trained on full set

    dataset, pipeline_spec, training_type, problem_info = \
        _get_training_args(transformed_data_context.X,
                           transformed_data_context.y,
                           transformed_data_context.sample_weight,
                           transformed_data_context.X_valid,
                           transformed_data_context.y_valid,
                           transformed_data_context.sample_weight_valid,
                           transformed_data_context.cv_splits,
                           automl_settings.num_classes,
                           automl_settings.task_type,
                           automl_settings.y_min,
                           automl_settings.y_max,
                           automl_pipeline.pipeline_script,
                           automl_settings.max_cores_per_iteration,
                           logger=logger,
                           remote=remote,
                           y_transformer=transformed_data_context.transformers.get('y_transformer'))

    pipeline_obj = pipeline_spec.instantiate_pipeline_spec(problem_info)
    pipeline_run_output = PipelineRunOutput(automl_settings, pipeline_obj, training_type)

    with automl_run_context.get_run() as run:
        run.add_properties(pipeline_run_output.pretrain_props_sanitized)

    # min to sec conversion
    timeout = None
    if iteration_timeout_min:
        timeout = iteration_timeout_min * 60

    log_config = LogConfig(automl_settings.debug_log, automl_settings.verbosity, 'automl-client-core-common')

    # TODO: We still need to clean up this code
    if enforce_time_on_win_required:
        results, status = _train_pipeline_enforce_time_limit_on_windows(
            metrics=metrics,
            X=transformed_data_context.X,
            y=transformed_data_context.y,
            sample_weight=transformed_data_context.sample_weight,
            X_valid=transformed_data_context.X_valid,
            y_valid=transformed_data_context.y_valid,
            sample_weight_valid=transformed_data_context.sample_weight_valid,
            cv_splits=transformed_data_context.cv_splits,
            num_classes=automl_settings.num_classes,
            task_type=automl_settings.task_type,
            y_min=automl_settings.y_min,
            y_max=automl_settings.y_max,
            pipeline_spec=pipeline_spec,
            problem_info=problem_info,
            max_time_sec=timeout,
            is_ensemble_iteration=automl_pipeline.is_ensemble_pipeline,
            train_frac=automl_pipeline.training_size,
            subsample_seed=automl_settings.subsample_seed,
            remote=remote,
            y_transformer=transformed_data_context.transformers.get('y_transformer'),
            log_config=log_config)

        runner = ClientRunner(dataset, metrics=metrics,
                              task=automl_settings.task_type,
                              log_config=log_config)
    else:
        # todo can move to helper, but not necessary
        runtime_constraints = default_resource_limits.copy()
        runtime_constraints['mem_in_mb'] = automl_settings.mem_in_mb
        runtime_constraints['wall_time_in_s'] = timeout
        problem_info.runtime_constraints = runtime_constraints

        runner = ClientRunner(dataset, metrics=metrics,
                              task=automl_settings.task_type)

        results, status = runner.run(dataset,
                                     pipeline_spec,
                                     problem_info,
                                     sets_to_run=[training_type],
                                     is_ensemble_iteration=automl_pipeline.is_ensemble_pipeline,
                                     subsample_percent=automl_pipeline.training_percent,
                                     subsample_seed=automl_settings.subsample_seed,
                                     enforce_limits=True,
                                     include_models=True)

    if isinstance(status, BaseException):
        raise status
    if results is None:
        raise Exception("Failed to train pipeline. Status: {}".format(status))

    # for cross validation train the model on full data set.
    if not automl_pipeline.is_ensemble_pipeline:
        results = _map_results(results, training_type)
        if results is not None and len(results) > 2:
            if training_type in \
                    [constants.TrainingType.CrossValidation, constants.TrainingType.MeanCrossValidation]:
                result_full, status = runner.run(
                    dataset, pipeline_spec, problem_info, sets_to_run=[
                        constants.TrainingType.TrainFull],
                    include_models=True)
                result_full = _map_results(
                    result_full, constants.TrainingType.TrainFull)
                if isinstance(status, BaseException):
                    raise status

                if result_full is None or len(result_full) <= 2:
                    raise RuntimeError("Failed while training full result.")

                score_valid = results[0]
                fit_time = results[1]
                fitted_pipeline = result_full[2]
                fitted_pipelines_train = results[2]

                augmented_pipeline, augmented_pipelines_train = _augment_transformers(transformed_data_context,
                                                                                      fitted_pipeline,
                                                                                      fitted_pipelines_train)
                pipeline_run_output.record_pipeline_output(score_valid,
                                                           fit_time,
                                                           augmented_pipeline,
                                                           augmented_pipelines_train)
                return pipeline_run_output

    score_valid, fit_time, fitted_pipeline = results
    fitted_pipelines_train = constants.Defaults.INVALID_PIPELINE_FITTED
    if isinstance(fitted_pipeline, list) and len(fitted_pipeline):
        fitted_pipeline = fitted_pipeline[0]

    augmented_pipeline, augmented_pipelines_train = _augment_transformers(transformed_data_context,
                                                                          fitted_pipeline,
                                                                          fitted_pipelines_train)
    pipeline_run_output.record_pipeline_output(score_valid,
                                               fit_time,
                                               augmented_pipeline,
                                               augmented_pipelines_train)
    return pipeline_run_output


def _train_pipeline_enforce_time_limit_on_windows(metrics,
                                                  X,
                                                  y,
                                                  sample_weight,
                                                  X_valid,
                                                  y_valid,
                                                  sample_weight_valid,
                                                  cv_splits,
                                                  num_classes,
                                                  task_type,
                                                  y_min,
                                                  y_max,
                                                  pipeline_spec,
                                                  problem_info,
                                                  max_time_sec,
                                                  is_ensemble_iteration,
                                                  train_frac=None,
                                                  subsample_seed=0,
                                                  remote=True,
                                                  y_transformer=None,
                                                  log_config=None):
    """
    Train the pipeline enforcing timeout.

    :param metrics:
    :param X:
    :param y:
    :param sample_weight:
    :param X_valid:
    :param y_valid:
    :param sample_weight_valid:
    :param cv_splits:
    :param num_classes:
    :param task_type:
    :param y_min:
    :param y_max:
    :param pipeline_spec:
    :param problem_info:
    :param max_time_sec:
    :param is_ensemble_iteration:
    :param train_frac:
    :param subsample_seed:
    :param remote:
    :param y_transformer:
    :param log_config:
    :return:
    """
    args = {
        "metrics": metrics,
        "X": X,
        "y": y,
        "sample_weight": sample_weight,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": sample_weight_valid,
        "cv_splits": cv_splits,
        "num_classes": num_classes,
        "task_type": task_type,
        "y_min": y_min,
        "y_max": y_max,
        "pipeline_spec": pipeline_spec,
        "problem_info": problem_info,
        "is_ensemble_iteration": is_ensemble_iteration,
        "train_frac": train_frac,
        "subsample_seed": subsample_seed,
        "remote": remote,
        "y_transformer": y_transformer,
        "log_config": log_config
    }
    return enforce_time_limit(max_time_sec, _train_pipeline_on_win_spawn_process, args)


def _get_dataset(X,
                 y,
                 sample_weight=None,
                 X_valid=None,
                 y_valid=None,
                 sample_weight_valid=None,
                 cv_splits=None,
                 num_classes=None,
                 task_type=constants.Tasks.CLASSIFICATION,
                 y_min=None,
                 y_max=None,
                 init_all_stats=False,
                 remote=True,
                 y_transformer=None):
    """
    Get the ClientDataset.

    :param X:
    :param y:
    :param sample_weight:
    :param X_valid:
    :param y_valid:
    :param sample_weight_valid:
    :param cv_splits:
    :param num_classes:
    :return:
    """
    assert_failures = []

    if cv_splits:
        frac_valid = cv_splits.get_fraction_validation_size()
        cv_splits_indices = cv_splits.get_custom_split_indices()
        num_cv_folds = cv_splits.get_num_k_folds()
    else:
        frac_valid = None
        cv_splits_indices = None
        num_cv_folds = None

    subsample_cache_strategy = SubsampleCacheStrategy.Classic if remote \
        else SubsampleCacheStrategy.Preshuffle

    dataset = ClientDatasets(subsample_cache_strategy=subsample_cache_strategy)

    if X_valid is not None:
        training_type = _get_training_type(
            constants.TrainingType.TrainAndValidation)

        if not (num_cv_folds == 0 or num_cv_folds is None):
            assert_failures.append(
                'n_cross_validations cannot be specified when X_valid is provided.')

        if not (frac_valid == 0.0 or frac_valid is None):
            assert_failures.append(
                'validation_size cannot be specified when X_valid is provided.')

        if y_valid is None:
            assert_failures.append(
                'y_valid must also be provided when X_valid is provided.')

        if len(assert_failures) > 0:
            raise ConfigException("Bad fit parameters. Please review documentation for fit. " +
                                  ' '.join(assert_failures))
        dataset.parse_simple_train_validate(name=DEFAULT_DATASET_NAME,
                                            X=X,
                                            y=y,
                                            sample_weight=sample_weight,
                                            X_valid=X_valid,
                                            y_valid=y_valid,
                                            sample_weight_valid=sample_weight_valid,
                                            task=task_type,
                                            y_min=y_min,
                                            y_max=y_max,
                                            init_all_stats=init_all_stats,
                                            y_transformer=y_transformer)

    else:
        if(num_cv_folds == 0 or num_cv_folds is None) and cv_splits_indices is None:
            training_type = _get_training_type(
                constants.TrainingType.TrainAndValidation)
        else:
            if cv_splits_indices is not None:
                num_cv_folds = len(cv_splits_indices)
            training_type = _get_training_type(
                constants.TrainingType.MeanCrossValidation, num_cv_folds)

        if len(assert_failures) > 0:
            raise ConfigException("Bad fit parameters. Please review documentation for fit. " +
                                  ' '.join(assert_failures))

        dataset.parse_data(name=DEFAULT_DATASET_NAME,
                           X=X,
                           y=y,
                           sample_weight=sample_weight,
                           cv_splits=cv_splits,
                           num_classes=num_classes,
                           task=task_type,
                           y_min=y_min,
                           y_max=y_max,
                           init_all_stats=init_all_stats,
                           y_transformer=y_transformer)
    return dataset, training_type


def _get_pipeline(pipeline_script, problem_info, logger=None):
    """
    Get the Pipeline object.

    :param pipeline_script: returned from service that is a dictionary of pipeline
    : spec
    : or for backward compatibility a dictionary of normal and sparse pipeline
    : definition that can be eval'd
    :param problem_info: The metadata on the dataset.
    :return: a tuple of ProblemInfo object and a PipelineSpec object.
    """
    pipeline_dict = json.loads(pipeline_script)

    # Wrap the standard scaler.
    scaler = [o for o in pipeline_dict["objects"]
              if o['spec_class'] == pipeline_spec_module.PREPROC_NAME and o['class_name'] == 'StandardScaler']
    if len(scaler) == 1:
        scaler[0]['class_name'] = 'StandardScalerWrapper'
        scaler[0]['module'] = SOURCE_WRAPPER_MODULE

    # If there are any single threaded pipelines, force the number of threads to 1.
    pinfo = problem_info
    if problem_info.num_threads != 1:
        stmodel = [o for o in pipeline_dict["objects"]
                   if o['spec_class'] == pipeline_spec_module.SKLEARN_NAME and
                   any([(algo_name in o['class_name']) for algo_name in constants.SINGLE_THREADED_ALGORITHMS])]
        if len(stmodel) == 1:
            pinfo = copy.deepcopy(problem_info)
            pinfo.num_threads = 1
            if logger:
                logger.warning("resetting the number of threads to 1\
                               for pipeline with {0}".
                               format(stmodel[0]['class_name']))
    spec = pipeline_spec_module.PipelineSpec.from_dict(pipeline_dict)
    return pinfo, spec


def _train_pipeline_on_win_spawn_process(metrics,
                                         X,
                                         y,
                                         sample_weight,
                                         X_valid,
                                         y_valid,
                                         sample_weight_valid,
                                         cv_splits,
                                         num_classes,
                                         task_type,
                                         y_min,
                                         y_max,
                                         pipeline_spec,
                                         problem_info,
                                         is_ensemble_iteration=False,
                                         train_frac=1,
                                         subsample_seed=0,
                                         remote=True,
                                         y_transformer=None,
                                         log_config=None):
    """
    Train the pipeline on a spawned process.

    :param metrics:
    :param X:
    :param y:
    :param sample_weight:
    :param X_valid:
    :param y_valid:
    :param sample_weight_valid:
    :param cv_splits:
    :param num_classes:
    :param task_type:
    :param y_min:
    :param y_max:
    :param pipeline_spec:
    :param is_ensemble_iteration:
    :param train_frac:
    :param subsample_seed:
    :param remote:
    :param y_transformer:
    :param log_config:
    :return:
    """
    from . import constants  # noqa: F401,F811
    from automl.client.core.common.datasets import ClientDatasets  # noqa: F401,F811
    from automl.client.core.common.model_wrappers import (
        LightGBMClassifier, SparseNormalizer, TruncatedSVDWrapper,
        CalibratedModel, LightGBMRegressor, LinearSVMWrapper,
        NBWrapper, NuSVCWrapper, SGDClassifierWrapper, SVCWrapper)  # noqa: F401,F811
    from automl.client.core.common.exceptions import DataException, ServiceException  # noqa: F401,F811
    from automl.client.core.common.metrics import minimize_or_maximize  # noqa: F401,F811
    from automl.client.core.common.preprocess import DataTransformer, LaggingTransformer  # noqa: F401,F811
    from automl.client.core.common.runner import ClientRunner   # noqa: F401,F811
    import logging  # noqa: F401,F811
    import numpy as np  # noqa: F401,F811
    import pandas as pd  # noqa: F401,F811
    import pickle  # noqa: F401,F811
    import os  # noqa: F401,F811
    import os.path  # noqa: F401,F811
    import scipy  # noqa: F401,F811
    import sys  # noqa: F401,F811
    import tempfile  # noqa: F401,F811
    import traceback  # noqa: F401,F811
    import sklearn  # noqa: F401,F811
    from sklearn import pipeline, preprocessing, linear_model, decomposition, ensemble  # noqa: F401,F811
    from sklearn.metrics import recall_score, precision_score  # noqa: F401,F811
    from sklearn.model_selection import cross_val_score  # noqa: F401,F811
    from sklearn.pipeline import make_pipeline  # noqa: F401,F811
    from azureml.core.run import Run  # noqa: F401,F811

    try:
        dataset, _, training_type, _ = \
            _get_training_args(X,
                               y,
                               sample_weight,
                               X_valid,
                               y_valid,
                               sample_weight_valid,
                               cv_splits,
                               num_classes,
                               task_type,
                               y_min,
                               y_max,
                               remote=remote,
                               y_transformer=y_transformer)
        runner = ClientRunner(dataset, metrics=metrics,
                              task=task_type)

        return runner.run(dataset,
                          pipeline_spec,
                          problem_info,
                          sets_to_run=[training_type],
                          is_ensemble_iteration=is_ensemble_iteration,
                          subsample_percent=train_frac * 100,
                          subsample_seed=subsample_seed,
                          include_models=True)
    except Exception as e:
        return None, e


def _get_training_args(X,
                       y,
                       sample_weight,
                       X_valid,
                       y_valid,
                       sample_weight_valid,
                       cv_splits,
                       num_classes,
                       task_type,
                       y_min,
                       y_max,
                       pipeline_script=None,
                       max_cores_per_iteration=None,
                       logger=None,
                       remote=True,
                       y_transformer=None):

    dataset, training_type = _get_dataset(X=X,
                                          y=y,
                                          sample_weight=sample_weight,
                                          X_valid=X_valid,
                                          y_valid=y_valid,
                                          sample_weight_valid=sample_weight_valid,
                                          cv_splits=cv_splits,
                                          num_classes=num_classes,
                                          task_type=task_type,
                                          y_min=y_min,
                                          y_max=y_max,
                                          init_all_stats=False,
                                          remote=remote,
                                          y_transformer=y_transformer)
    problem_info = dataset.get_problem_info()
    problem_info.num_threads = max_cores_per_iteration
    pipeline_spec = None
    if pipeline_script:
        problem_info, pipeline_spec = _get_pipeline(pipeline_script, problem_info, logger)
    return dataset, pipeline_spec, training_type, problem_info


def _map_results(results, training_type):
    training_types = constants.TrainingType
    result_types = constants.TrainingResultsType

    if training_type in [training_types.TrainAndValidation, training_types.TrainValidateTest]:
        status = results[result_types.TRAIN_VALIDATE_STATUS]
        if status:
            raise Exception(status)
        scores = results[result_types.VALIDATION_METRICS]
        train_time = results[result_types.VALIDATION_METRICS][result_types.TRAIN_TIME]
        model = results[result_types.MODELS][training_type]
    elif training_type == training_types.TrainFull:
        status = results[result_types.TRAIN_FULL_STATUS]
        if status:
            raise Exception(status)
        scores = results[result_types.TRAIN_FROM_FULL_METRICS]
        train_time = results[result_types.TRAIN_FROM_FULL_METRICS][result_types.TRAIN_TIME]
        model = results[result_types.MODELS][training_type]
    elif training_type == training_types.CrossValidation:
        status = results[result_types.CV_STATUS]
        if status:
            raise Exception(status)
        scores = results[result_types.CV_METRICS]
        train_time = [x[result_types.TRAIN_TIME]
                      for x in results[result_types.CV_METRICS]]
        model = results[result_types.MODELS][training_type]
    elif training_type == training_types.MeanCrossValidation:
        status = results[result_types.CV_STATUS]
        if status:
            raise Exception(status)
        scores = results[result_types.CV_MEAN_METRICS]
        train_time = results[result_types.CV_MEAN_METRICS][result_types.TRAIN_TIME]
        model = results[result_types.MODELS][training_types.CrossValidation]
    else:
        raise ValueError('Invalid training type {} specified.'.format(training_type))

    return scores, train_time, model


def _get_training_type(training_type, folds=0):
    """
    Determine what type of training and validation to do based on user inputs.

    :param training_type: str representing what type fo training and validation to do
    :param folds: int number of
    :return: None
    """
    valid_training_types = (constants.TrainingType.TrainAndValidation,
                            constants.TrainingType.MeanCrossValidation)
    if training_type not in valid_training_types:
        raise ConfigException(
            "%s and %s are the only supported training types." % valid_training_types)
    is_cv = training_type == constants.TrainingType.MeanCrossValidation
    if not ((is_cv and folds) or (not is_cv and not folds)):
        raise ConfigException("Cannot specify number of folds "
                              "if training type is not %s" % constants.TrainingType.MeanCrossValidation)
    if folds < 0 or folds == 1:
        raise ConfigException(
            "Cross validation folds must be greater than 1, got %d" % folds)
    return training_type


def _augment_transformers(transformed_data_context, fitted_pipeline, fitted_pipelines_train):
    transformer = transformed_data_context.transformers.get(constants.Transformers.X_TRANSFORMER)
    lag_transformer = transformed_data_context.transformers.get(constants.Transformers.LAG_TRANSFORMER)
    ts_transformer = transformed_data_context.transformers.get(constants.Transformers.TIMESERIES_TRANSFORMER)
    y_transformer = transformed_data_context.transformers.get(constants.Transformers.Y_TRANSFORMER)

    # Augment the pipeline with our own transformers
    if (transformer is not None or lag_transformer is not None or ts_transformer is not None) and \
            fitted_pipeline is not constants.Defaults.INVALID_PIPELINE_FITTED:
        fitted_pipeline = _add_transformer_x(
            transformer, lag_transformer, ts_transformer, fitted_pipeline)
        if fitted_pipelines_train is not constants.Defaults.INVALID_PIPELINE_FITTED:
            transformed_train_pipelines = []
            for pipe in fitted_pipelines_train:
                transformed_train_pipelines.append(
                    _add_transformer_x(transformer, lag_transformer, ts_transformer, pipe))
            fitted_pipelines_train = transformed_train_pipelines

    if y_transformer is not None:
        # if y_transformer is not None, add a wrapper of the fitted model with transformer.
        if isinstance(fitted_pipeline, sklearn.pipeline.Pipeline) and \
                fitted_pipeline is not constants.Defaults.INVALID_PIPELINE_FITTED:
            fitted_pipeline = PipelineWithYTransformations(
                fitted_pipeline, "LabelEncoder", y_transformer)
        if isinstance(fitted_pipelines_train, sklearn.pipeline.Pipeline) and \
                fitted_pipelines_train is not constants.Defaults.INVALID_PIPELINE_FITTED:
            fitted_pipeline = PipelineWithYTransformations(
                fitted_pipelines_train, "LabelEncoder", y_transformer)

    return fitted_pipeline, fitted_pipelines_train


def _add_transformer_x(transformer, lag_transformer, ts_transformer, pipeline_spec):
    """
    Add transformer as first step of the pipeline.

    :param pipeline_spec: pipeline to which the transformer should be added
    :param transformer: a pipeline compatible transformation that implements fit, transform and predict
    :return: pipeline with transformer prepended
    """
    transformers = filter(lambda x: x is not None, [
                          transformer, lag_transformer, ts_transformer])

    return sklearn.pipeline.make_pipeline(*transformers, *[s[1] for s in pipeline_spec.steps])
