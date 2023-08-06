# coding=utf-8
import os
import time
from logging.handlers import BaseRotatingHandler


class TimefileHandler(BaseRotatingHandler):
    """
    Handler for logging to a file
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False):
        self.rawFilename = filename
        # Replace datetime placeholder with real datetime
        filename = self._mkFilename(filename)
        # Cache current filename
        self.usingFilename = filename

        BaseRotatingHandler.__init__(self, filename, mode, encoding, delay)

    def shouldRollover(self, record):
        curFilename = self._mkFilename(self.rawFilename)
        if curFilename == self.usingFilename:
            return False
        return True

    def doRollover(self):
        """
        close old file handler and create a new file
        :return:
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        self.baseFilename = self._normalizeFilename(self._mkFilename(self.rawFilename))
        if not self.delay:
            self.stream = self._open()

    def getFilename(self):
        return self.baseFilename

    @staticmethod
    def _mkFilename(filename):
        return time.strftime(filename)

    @staticmethod
    def _normalizeFilename(filename):
        filename = os.fspath(filename)
        return os.path.abspath(filename)
