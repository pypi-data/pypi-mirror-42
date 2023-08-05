import logging
import sys
from enum import Enum

from nio.util.nio_time import get_nio_time


class NIOAdapter(logging.LoggerAdapter):

    """ The base logger adapter class for NIO.  """

    detail_errors = True

    def __init__(self, logger, extra={}):
        super().__init__(logger, extra)

    def setLevel(self, level):
        """ Set the specified level on the underlying logger.  """
        log_level = level.value if isinstance(level, Enum) else level
        super().setLevel(log_level)

    def exception(self, msg, *args, **kwargs):
        """ Log an exception inside of a handler.

        Delegate an exception call to the underlying logger and log exception
        or error depending of running flag "detail_errors"
        """
        if self.__class__.detail_errors:
            super().exception(msg, *args, **kwargs)
        else:
            _, exc_value, _ = sys.exc_info()
            msg = "{0}, (Exception details: {1})".format(
                msg, self.exc_info(exc_value))
            super().error(msg, *args, **kwargs)

    @classmethod
    def exc_info(cls, ex):
        """ Returns string information for an exception.  """
        try:
            if isinstance(ex, Exception) and hasattr(ex, 'message'):
                ex_str = "{0}{1}{2}".format(type(ex).__name__,
                                            " - " if ex.message else "",
                                            ex.message)
            else:
                ex_str = str(ex)
                ex_str = "{0}{1}{2}".format(
                    type(ex).__name__, " - " if ex_str else "", ex_str)
        except:
            ex_str = repr(ex)
        return ex_str

    def process(self, msg, kwargs):
        """ Add some additional context to our log record

        Args:
            msg (str): The message to be logged.

        Kwargs:
            see LoggerAdapter.process

        Returns:
            The (possibly modified) versions of the arguments passed in.
        """

        self.extra["niotime"] = get_nio_time()
        self.extra["context"] = self.logger.name
        return super().process(msg, kwargs)

    @classmethod
    def name_to_level(cls, name):
        """ Converts from level name to level identifier

        Args:
            name (str): Log name

        Returns:
            log level identifier
        """
        return getattr(logging, name.upper(), None)
