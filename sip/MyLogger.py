#!/usr/bin/python

from configparser import ConfigParser
import sys
import logging
import pyinotify
import envhelper

datafolder = "./config/"

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyLogger(object, metaclass=SingletonType):
    _logger = None
    _notifier = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._setupLogger()

        # add Filewatch
        wm = pyinotify.WatchManager()  # Watch Manager
        wm.add_watch(datafolder, pyinotify.IN_CLOSE_WRITE)

        self._notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
        self._notifier.daemon = True
        self._notifier.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self._notifier.stop()

    def __del__(self):
        self._notifier.stop()

    def _setupLogger(self):
        config = envhelper.getConfig()
        verbosity = None
        errors = ''
        try:
            verbosity = config.get("LOG", "level")
        except Exception as e:
            errors = e.message
            pass

        logformat = '%(asctime)s %(levelname)-8s- %(message)s'

        try:
            logformat = config.get("LOG", "format")
        except Exception as e:
            errors = e.message +", " + errors
            pass

        log_level = logging.INFO #Deault logging level
        if "ERROR" == verbosity:
            log_level = logging.ERROR
        elif "WARN" == verbosity:
            log_level = logging.WARN
        elif "INFO" == verbosity:
            log_level = logging.INFO
        elif "DEBUG" == verbosity:
            log_level = logging.DEBUG

        logging.basicConfig(stream=sys.stdout, format=logformat, datefmt="%d.%m.%Y %H:%M:%S", level=log_level)

        self._logger.setLevel(log_level)
        for handler in self._logger.handlers:
            handler.setLevel(log_level)

        if len(errors) > 0:
            self._logger.warning('settings.ini: '+errors)

    def getLogger(self):
        return self._logger

class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            if event.name == 'settings.ini':
                MyLogger.__call__()._setupLogger()

def getLogger():
    return MyLogger().getLogger()


if __name__ == "__main__":
    logger = getLogger()
    logger.info("Hello, Logger")
    logger.debug("bug occured")