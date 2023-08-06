# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Context manager that wraps an AutoML run context."""
import time
from automl.client.core.common.automl_run_context import AutoMLAbstractRunContext
from azureml.core import Run


class AzureAutoMLRunContext(AutoMLAbstractRunContext):

    def _get_run_internal(self):
        """Retrieve a run context if needed and return it."""
        # In case we use get_run in nested with statements, only get the run context once
        if self._refresh_needed():
            self._last_refresh = time.time()
            self._run = Run.get_context(_batch_upload_metrics=False)
        return self._run

    def _refresh_needed(self) -> bool:
        if self._run is None:
            return True
        if self._is_adb_run:
            current_time = time.time()
            if current_time - self._last_refresh > self._timeout_interval:
                return True
        return False

    def __init__(self, run, is_adb_run: bool = False) -> None:
        """
        Create an AzureAutoMLRunContext object that wraps a run context.

        :param run: the run context to use
        :param is_adb_run: whether we are running in Azure DataBricks or not
        """
        self._run = run
        self._is_adb_run = is_adb_run

        # Refresh the run context after 15 minutes if running under adb
        self._timeout_interval = 900
        self._last_refresh = 0
