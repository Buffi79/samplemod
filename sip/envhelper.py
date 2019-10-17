#!/usr/bin/python

from configparser import ConfigParser
import sys
import logging

datafolder = "./config/"

def setupLogger():
    config = getConfig()
    verbosity = config.get("LOG", "level")
    logformat = '%(asctime)s %(levelname)-8s- %(message)s'
    errors = None
    try:
        logformat = config.get("LOG", "format")
    except Exception as e:
        errors = 'ConfigError: '+e.message
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

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, format=logformat, datefmt="%d.%m.%Y %H:%M:%S", level=log_level)

    if errors is not None:
        logging.error(errors)

    return logger


def getConfig():
    config = ConfigParser()
    config.read(datafolder+"settings.ini")
    return config

def getConfigVal(section, key, type='string'):
    config = getConfig()

    try:
        value = config.get(section, key)
        return value
    except Exception as e:
        logging.error('ConfigError: '+e.message)
        return None
