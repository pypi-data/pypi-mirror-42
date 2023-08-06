"""
limis core module

Provides solution wide functionality for managing logging, settings, applications, etc.
"""
import logging
import logging.config
import os

from configparser import ConfigParser
from distutils.version import StrictVersion
from importlib import import_module
from pathlib import Path
from setuptools import find_packages
from typing import List

from limis import VERSION
from limis.core import messages


# TODO - Move environment variable names to separate file
LIMIS_PROJECT_NAME_ENVIRONMENT_VARIABLE = 'LIMIS_PROJECT_NAME'
LIMIS_PROJECT_SETTINGS_ENVIRONMENT_VARIABLE = 'LIMIS_PROJECT_SETTINGS'


def get_version() -> str:
    """
    Retrieves the version of this module.

    :return: String with the strict current version
    """
    return str(StrictVersion('.'.join(map(str, VERSION))))


def initialize_logging():
    """
    Initializes logging for the application.

    The logging configuration file is determined by the logging['config_file'] setting.

    :raises ValueError: Error indicating specified logging configuration file does not exist
    """
    logging_config_file = Settings().logging['config_file']

    path = Path(logging_config_file)
    if not path.exists():
        path = Path(__file__).parent / logging_config_file

        if not path.exists():
            raise ValueError(messages.LOGGING_CONFIG_FILE_NOT_FOUND.format(logging_config_file))

    logging.config.fileConfig(str(path))

    logging.getLogger(__name__).debug(messages.LOGGING_INITIALIZED)


def get_root_services():
    """
    Returns the root services module as defined in settings. Settings attribute is set by the
    "<project_name>['root_services']" value. LIMIS_PROJECT_NAME environment variable is used to set the project_name'.
    """
    project_name = os.environ.get(LIMIS_PROJECT_NAME_ENVIRONMENT_VARIABLE)

    try:
        root_services_name = getattr(Settings(), project_name)['root_services']
    except AttributeError:
        raise AttributeError(messages.GET_ROOT_SERVICES_INVALID_PROJECT_ERROR.format(project_name))
    except TypeError:
        raise TypeError(messages.GET_ROOT_SERVICES_INVALID_PROJECT_NAME_TYPE)

    try:
        module = import_module(root_services_name)
    except ImportError:
        raise ImportError(messages.GET_ROOT_SERVICES_IMPORT_ERROR.format(root_services_name))

    return module


class Settings:
    """
    Settings for global application

    Most packages defined within limis have a settings.ini file and the default settings are loaded for each of those
    modules. Settings may be overwritten by passing additional settings files to the class initialization method.
    Additional settings files specified are loaded after limis modules. Limis packages without settings.ini are
    ignored, modules passed with additional_settings_files or the environment variable that do not exist will raise
    an error.

    Project specific settings are loaded from the environment variable "LIMIS_PROJECT_SETTINGS".

    Settings are loaded as attributes of instantiated Settings class. Each attribute name represents a section and is
    a dictionary of settings values.
    """
    def __init__(self, additional_settings_files: List[str] = None):
        """
        Initializes the Settings class.

        :param additional_settings_files: List of additional settings modules to load in addition to built-ins
        """
        self._limis_path = Path(__file__).parent.parent
        self._settings_files = [
            self._limis_path / package / 'settings.ini' for package in find_packages(str(self._limis_path))
        ]

        if additional_settings_files:
            additional_settings_files_as_paths = [Path(settings_file) for settings_file in additional_settings_files]
            self._settings_files = self._settings_files + additional_settings_files_as_paths

        project_settings_file = os.environ.get(LIMIS_PROJECT_SETTINGS_ENVIRONMENT_VARIABLE)

        if project_settings_file:
            self._settings_files = self._settings_files + [Path(project_settings_file)]

        self.load_settings()

    def load_settings(self):
        """
        Loads settings from settings files.

        :raises ValueError: Error indicating one of the settings file was not found.
        """
        for settings_file in self._settings_files:
            if settings_file.exists():
                config = ConfigParser()
                config.read(str(settings_file))

                for section in config:
                    config_settings = {}

                    for setting in config[section]:
                        config_settings[setting] = config[section][setting]

                    setattr(self, section, config_settings)
            elif not str(settings_file).startswith(str(self._limis_path)):
                raise ValueError(messages.SETTINGS_LOAD_SETTINGS_FILE_NOT_FOUND.format(settings_file))


settings = Settings()
