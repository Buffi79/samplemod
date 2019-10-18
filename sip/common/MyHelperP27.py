#!/usr/bin/python

from configparser import ConfigParser
import sys
import logging
import pyinotify


datafolder = "./config/"
settings = "settings.ini"

class Logger():
    _logger = None

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super().__new__(self)
        return self.instance

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
            self._logger.warning(settings+': '+errors)

    def getLogger(self):
        return self._logger


class Config():
    _config = None

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super().__new__(self)
        return self.instance

    def __init__(self):
        self._config = ConfigParser()
        self._loadConfig()
        Notifier()

    def _loadConfig(self):
        self._config.read(datafolder+settings)

    def getConfig(self):
        return self._config

    def getConfigVal(self, section, key, type='string'):
        try:
            if 'int' == type:
                return self._config.getint(section, key)
            elif 'boolean' == type:
                return self._config.getboolean(section, key)
            elif 'float' == type:
                return self._config.getfloat(section, key)
            return self._config.get(section, key)
        except Exception as e:
            getLogger().error('ConfigError: '+e.message)
            return None

class Notifier():
    _notifier = None

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super().__new__(self)
        return self.instance

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
            if event.name == settings:
                Config()._loadConfig()
                Logger()._setupLogger()
                getLogger().info("configuration reloaded")


def getLogger():
    return Logger().getLogger()

def getConfig():
    return Config().getConfig()

def getConfigVal(section, key, type='string'):
    return Config().getConfigVal(section, key, type)


if __name__ == "__main__":
    logger = getLogger()
    logger.info("Hello, Logger")
    logger.debug("bug occured")
    conf = getConfig()
    print conf.get("LOG","level")