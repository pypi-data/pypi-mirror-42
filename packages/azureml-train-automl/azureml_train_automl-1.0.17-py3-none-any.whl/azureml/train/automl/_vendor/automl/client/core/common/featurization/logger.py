# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base logger class for all the transformers."""


class TransformerLogger(object):
    """Base logger class for all the transformers."""

    def __init__(self):
        """Init the logger class."""
        self.logger = None

    def __getstate__(self):
        """
        Overriden to remove logger object when pickling.

        :return: this object's state as a dictionary
        """
        state = self.__dict__.copy()
        state['logger'] = None
        return state

    def _init_logger(self, logger):
        """
        Init the logger.

        :param logger: the logger handle.
        :type logger: logging.Logger.
        """
        self.logger = logger

    def _logger_wrapper(self, level, message):
        """
        Log a message with a given debug level in a log file.

        :param logger: the logger handle
        :type logger: logging.Logger
        :param level: log level (info or debug)
        :param message: log message
        :type message: str
        """
        # Check if the logger object is valid. If so, log the message
        # otherwise pass
        if self.logger is not None:
            if level == 'info':
                self.logger.info(message)
            elif level == 'warning':
                self.logger.warning(message)
            elif level == 'debug':
                self.logger.debug(message)
