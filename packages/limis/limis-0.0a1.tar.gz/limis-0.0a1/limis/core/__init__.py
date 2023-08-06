"""
limis core module

Provides solution wide functionality for managing logging, settings, applications, etc.
"""
import logging
import logging.config
import os

from distutils.version import StrictVersion
from importlib import import_module
from pathlib import Path
from setuptools import find_packages
from typing import List

from limis import VERSION
from limis.core import messages


LIMIS_PROJECT_SETTINGS_ENVIRONMENT_VARIABLE = 'LIMIS_PROJECT_SETTINGS_MODULE'


def get_version() -> str:
    """
    Retrieves the version of this module.

    :return: String with the strict current version
    """
    return str(StrictVersion('.'.join(map(str, VERSION))))


def initialize_logging():
    """
    Initializes logging for the application.

    The logging configuration file is determined by the LOGGING_CONFIG_FILE setting.

    :raises ValueError: Error indicating specified logging configuration file does not exist
    """
    logging_config_file = Settings().LOGGING_CONFIG_FILE

    path = Path(logging_config_file)
    if not path.exists():
        raise ValueError(messages.LOGGING_CONFIG_FILE_NOT_FOUND.format(logging_config_file))

    logging.config.fileConfig(str(logging_config_file))

    logging.getLogger(__name__).debug(messages.LOGGING_INITIALIZED)


class Settings:
    """
    Settings for global application

    Most packages defined within limis have a settings.py file and the default settings are loaded for each of those
    modules. Settings may be overwritten by passing additional settings modules to the class initialization method.
    Additional settings modules specified are loaded after limis modules. Limis packages without settings.py are
    ignored, modules passed with additional_settings_modules or the environment variable that do not exist will raise
    an error.

    Project specific settings are loaded from the environment variable "LIMIS_PROJECT_SETTINGS_MODULE".

    .. note::
        Only settings with names in uppercase are loaded to the Settings class. Lowercase or mixed-case variables
        are ignored.
    """
    def __init__(self, additional_settings_modules: List[str] = None):
        """
        Initializes the Settings class.

        :param additional_settings_modules: List of additional settings modules to load in addition to built-ins
        :raises ImportError: Error indicating one of the modules was not found.
        """
        path = Path(__file__).parent.parent
        settings_modules = ['limis.' + package + '.settings' for package in find_packages(str(path))]

        if additional_settings_modules:
            settings_modules = settings_modules + additional_settings_modules

        project_settings_module = os.environ.get(LIMIS_PROJECT_SETTINGS_ENVIRONMENT_VARIABLE)

        if project_settings_module:
            settings_modules = settings_modules + [project_settings_module]

        for settings_module in settings_modules:
            try:
                settings_data = import_module(settings_module)
                for setting in dir(settings_data):
                    if setting.isupper():
                        value = getattr(settings_data, setting)
                        setattr(self, setting, value)
            except ImportError:
                if not settings_module.startswith('limis'):
                    raise ImportError(messages.SETTINGS_INIT_MODULE_NOT_FOUND.format(settings_module))


settings = Settings()
