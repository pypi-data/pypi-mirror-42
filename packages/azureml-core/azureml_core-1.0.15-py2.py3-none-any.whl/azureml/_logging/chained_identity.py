# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import six

if six.PY2:
    from contextlib2 import ContextDecorator
else:
    from contextlib import ContextDecorator

START_MSG = "[START]"
STOP_MSG = "[STOP]"


class ChainedIdentity(object):
    """A mixin that provides structured, chained logging for objects and contexts"""

    DELIM = "#"

    def __init__(self, _ident=None, _parent_logger=None, **kwargs):
        """
        Internal class used to improve logging information

        :param _ident: Identity of the object
        :type _ident: str
        :param _parent_logger: Parent logger, used to maintain creation hierarchy
        :type _parent_logger: logging.Logger
        """

        # TODO: Ideally move constructor params to None defaulted
        # and pick up the stack trace as a reasonable approximation
        self._identity = self.__class__.__name__ if _ident is None else _ident
        parent = logging.getLogger("azureml") if _parent_logger is None else _parent_logger
        self._logger = parent.getChild(self._identity)
        if kwargs:
            self._logger.debug("Found extra key word arguments: {}".format(kwargs))
        super(ChainedIdentity, self).__init__(**kwargs)

    @property
    def identity(self):
        return self._identity

    def _log_context(self, context_name):
        return LogScope(_ident=context_name, _parent_logger=self._logger)


class LogScope(ChainedIdentity, ContextDecorator):
    '''Convenience for logging a context'''

    def __enter__(self):
        self._logger.debug(START_MSG)
        return self._logger

    def __exit__(self, etype, value, traceback):
        if value is not None:
            self._logger.debug("Error {0}: {1}\n{2}".format(etype, value, traceback))
        self._logger.debug(STOP_MSG)
