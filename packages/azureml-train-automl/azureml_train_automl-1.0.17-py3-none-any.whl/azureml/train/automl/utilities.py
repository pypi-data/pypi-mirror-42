# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""automated machine learning SDK utilities."""
import json

from automl.client.core.common import utilities as common_utilities
from automl.client.core.common.exceptions import AutoMLException

from . import _constants_azureml


def friendly_http_exception(exception, api_name):
    """
    Friendly exceptions for a http exceptions.

    :param exception: Exception.
    :param api_name: string.
    :raise: ServiceException
    """
    try:
        # Raise bug with msrest team that response.status_code is always 500
        status_code = exception.error.response.status_code
        if status_code == 500:
            message = exception.message
            substr = 'Received '
            status_code = message[message.find(
                substr) + len(substr): message.find(substr) + len(substr) + 3]
    except Exception:
        raise exception

    if status_code in _constants_azureml.HTTP_ERROR_MAP:
        http_error = _constants_azureml.HTTP_ERROR_MAP[status_code]
    else:
        http_error = _constants_azureml.HTTP_ERROR_MAP['default']
    if api_name in http_error:
        error_message = http_error[api_name]
    else:
        error_message = http_error['default']
    raise AutoMLException("{0} error raised. {1}".format(http_error['Name'], error_message), http_error['type']) \
        from exception


def get_primary_metrics(task):
    """
    Get the primary metrics supported for a given task as a list.

    :param task: string "classification" or "regression".
    :return: A list of the primary metrics supported for the task.
    """
    return common_utilities.get_primary_metrics(task)


def _log_user_sdk_dependencies(run, logger):
    """
    Log the AzureML packages currently installed on the local machine to the given run.

    :param run: The run to log user depenencies.
    :param logger: The logger to write user dependencies.
    :return:
    :type: None
    """
    dependencies = {'dependencies_versions': json.dumps(common_utilities.get_sdk_dependencies())}
    logger.info("[RunId:{}]SDK dependencies versions:{}."
                .format(run.id, dependencies['dependencies_versions']))
    run.add_properties(dependencies)
