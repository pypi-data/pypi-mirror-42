# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Activity-based loggers."""
from abc import ABC, abstractmethod
from automl.client.core.common import constants as constants
from automl.client.core.common import logging_utilities as logging_util
from datetime import datetime

import contextlib
import uuid


class ActivityLogger(ABC):
    """Abstract base class for activity loggers."""

    @abstractmethod
    def _log_activity(self, logger, activity_name, activity_type=None, custom_dimensions=None):
        """
        Log activity - should be overridden by subclasses with a proper implementation.

        :param logger:
        :param activity_name:
        :param activity_type:
        :param custom_dimensions:
        :return:
        """
        raise NotImplementedError

    @contextlib.contextmanager
    def log_activity(self, logger, activity_name, activity_type=None, custom_dimensions=None):
        """
        Log an activity using the given logger.

        :param logger:
        :param activity_name:
        :param activity_type:
        :param custom_dimensions:
        :return:
        """
        return self._log_activity(logger, activity_name, activity_type, custom_dimensions)


class DummyActivityLogger(ActivityLogger):
    """Dummy activity logger."""

    def _log_activity(self, logger, activity_name, activity_type=None, custom_dimensions=None):
        """
        Do nothing.

        :param logger:
        :param activity_name:
        :param activity_type:
        :param custom_dimensions:
        """
        yield None


class TelemetryActivityLogger(ActivityLogger):
    """Telemetry activity logger."""

    def __init__(self, namespace=None,
                 filename=None,
                 verbosity=None,
                 custom_dimensions=None,
                 component_name=None):
        """
        Construct activity logger object.

        :param namespace: namespace
        :param filename: log file name
        :param verbosity: logger verbosity
        :param custom_dimensions: custom dimensions
        :param component_name: component name for telemetry state.
        """
        self.namespace = namespace
        self.filename = filename
        self.verbosity = verbosity
        self.component_name = component_name

        self.custom_dimensions = custom_dimensions if custom_dimensions is not None else {}
        self.module_logger = self._get_logger()

    def __getstate__(self):
        """
        Get state picklable objects.

        :return: state
        """
        return {
            'namespace': self.namespace,
            'filename': self.filename,
            'verbosity': self.verbosity,
            'component_name': self.component_name,
            'custom_dimensions': self.custom_dimensions,
            'module_logger': None,
        }

    def __setstate__(self, state):
        """
        Set state for object reconstruction.

        :param state: pickle state
        """
        self.namespace = state['namespace']
        self.filename = state['filename']
        self.verbosity = state['verbosity']
        self.component_name = state['component_name']
        self.custom_dimensions = state['custom_dimensions']
        self.module_logger = self._get_logger()

    def _get_logger(self):
        return logging_util.get_logger(namespace=self.namespace,
                                       filename=self.filename,
                                       verbosity=self.verbosity,
                                       component_name=self.component_name)

    def _log_activity(self, logger, activity_name, activity_type=None, custom_dimensions=None):
        """
        Log activity with duration and status.

        :param logger: logger
        :param activity_name: activity name
        :param activity_type: activity type
        :param custom_dimensions: custom dimensions
        """
        activity_info = {'activity_id': str(uuid.uuid4()),
                         'activity_name': activity_name,
                         'activity_type': activity_type}

        activity_info.update(self.custom_dimensions)
        properties = dict()
        custom_dimensions = custom_dimensions or {}
        activity_info.update(custom_dimensions)
        properties['properties'] = activity_info

        completion_status = constants.TelemetryConstants.SUCCESS

        start_time = datetime.utcnow()
        self.module_logger.info("ActivityStarted: {}".format(activity_name), extra=properties)

        try:
            yield
        except Exception:
            completion_status = constants.TelemetryConstants.FAILURE
            raise
        finally:
            end_time = datetime.utcnow()
            duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)
            activity_info["durationMs"] = duration_ms
            activity_info["completionStatus"] = completion_status

            self.module_logger.info("ActivityCompleted: Activity={}, HowEnded={}, Duration={}[ms]".
                                    format(activity_name, completion_status, duration_ms), extra=properties)
