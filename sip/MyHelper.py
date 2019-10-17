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

class Logger(object, metaclass=SingletonType):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._setupLogger()
        Notifier()

    def _setupLogger(self):
        config = Config().getConfig()
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


class Config(object, metaclass=SingletonType):
    _config = None

    def __init__(self):
        self._config = ConfigParser()
        self._loadConfig()
        Notifier()

    def _loadConfig(self):
        self._config.read(datafolder+"settings.ini")

    def getConfig(self):
        return self._config

    def getConfigVal(self, section, key, type='string'):
        try:
            value = self._config.get(section, key)
            return value
        except Exception as e:
            logger = Logger.getLogger()
            logger.error('ConfigError: '+e.message)
            return None

class Notifier(object, metaclass=SingletonType):
    _notifier = None

    def __init__(self):
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

class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            if event.name == 'settings.ini':
                Logger()._setupLogger()
                Config()._loadConfig()
                getLogger().info("Configuration reloaded")


def getLogger():
    return Logger().getLogger()

def getConfig():
    return Config().getConfig()


if __name__ == "__main__":
    logger = getLogger()
    logger.info("Hello, Logger")
    logger.debug("bug occured")
    conf = getConfig()
    print (conf.get("LOG","level"))
