#!/usr/bin/python

from configparser import ConfigParser
import sys
import logging
import pyinotify
import envhelper
import MyLogger

datafolder = "./config/"

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object, metaclass=SingletonType):
    _config = None
    _notifier = None

    def __init__(self):
        self._config = ConfigParser()
        self._loadConfig()

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

    def _loadConfig(self):
        self._config.read(datafolder+"settings.ini")

    def getConfig(self):
        return self._config

    def getConfigVal(self, section, key, type='string'):
        try:
            value = self._config.get(section, key)
            return value
        except Exception as e:
            logger = MyLogger.getLogger()
            logger.error('ConfigError: '+e.message)
            return None

class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            if event.name == 'settings.ini':
                Config.__call__()._readConfig()

def getConfig():
    return Config().getConfig()

def getConfigVal(section, key, type='string'):
    return Config().getConfigVal(section, key, type)
