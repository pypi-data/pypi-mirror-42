import os

from distutils.version import StrictVersion
from unittest import TestCase

import limis
from limis.core import get_version, initialize_logging, Settings
from tests import remove_logfile


class TestMethods(TestCase):
    def tearDown(self):
        remove_logfile()

    def test_initialize_logging(self):
        initialize_logging()

        os.environ['LIMIS_PROJECT_SETTINGS_MODULE'] = 'tests.core.data.settings_logging'

        with self.assertRaises(ValueError):
            initialize_logging()

        os.environ.pop('LIMIS_PROJECT_SETTINGS_MODULE')

    def test_get_version(self):
        version = get_version()
        self.assertEqual(version, StrictVersion('.'.join(map(str, limis.VERSION))))


class TestSettings(TestCase):
    def tearDown(self):
        remove_logfile()

    def test_init(self):
        initialize_logging()

        settings_instance = Settings()

        with self.assertRaises(ImportError):
            invalid_module = 'invalid_module'
            settings_instance = Settings([invalid_module])

        settings_instance = Settings(['tests.core.data.settings'])

        self.assertEqual(settings_instance.VALID_SETTING, 'valid')
        self.assertFalse(hasattr(settings_instance, 'invalid_setting'))
        self.assertFalse(hasattr(settings_instance, 'nonexistent_setting'))

        os.environ['LIMIS_PROJECT_SETTINGS_MODULE'] = 'tests.core.data.settings'

        settings_instance = Settings()
        self.assertEqual(settings_instance.VALID_SETTING, 'valid')

