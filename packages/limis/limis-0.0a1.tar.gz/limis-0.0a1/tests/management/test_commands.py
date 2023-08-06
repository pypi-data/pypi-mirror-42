import io
import shutil

from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase

from limis.management import exit_codes
from limis.management.commands import Command, CreateProject, Version


class TestCommand(TestCase):
    def test_invalid_arguments(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(Command.invalid_arguments(), exit_codes.INVALID_ARGUMENTS)


class TestCreateProject(TestCase):
    def __remove_test_project_directories(self):
        if self.test_project_default_directory.exists():
            shutil.rmtree(str(self.test_project_default_directory), ignore_errors=False)

        if self.test_project_directory.exists():
            shutil.rmtree(str(self.test_project_directory), ignore_errors=False)

    def setUp(self):
        self.test_project_name = 'test_project'
        self.test_project_default_directory = Path.cwd() / 'test_project'
        self.test_project_directory = Path.cwd() / 'test_project_directory'

        self.__remove_test_project_directories()

    def tearDown(self):
        self.__remove_test_project_directories()

    def test_run(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(CreateProject.run([]), exit_codes.INVALID_ARGUMENTS)

            self.assertEqual(CreateProject.run([self.test_project_name]), exit_codes.SUCCESS)
            self.assertTrue(self.test_project_default_directory.exists())
            self.assertTrue((self.test_project_default_directory / self.test_project_name).exists())

            with open(str(self.test_project_default_directory / 'management.py')) as file:
                self.assertTrue(file.read(), 'name = \'{}\''.format(self.test_project_name))
                file.close()

            self.assertEqual(CreateProject.run([self.test_project_name, self.test_project_directory]),
                             exit_codes.SUCCESS)
            self.assertTrue(self.test_project_directory.exists())
            self.assertTrue((self.test_project_directory / self.test_project_name).exists())

            with open(str(self.test_project_directory / 'management.py')) as file:
                self.assertTrue(file.read(), 'name = \'{}\''.format(self.test_project_name))
                file.close()

            self.assertFalse(CreateProject.run([self.test_project_name]))


class TestVersion(TestCase):
    def test_run(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(Version.run(args=[]), exit_codes.SUCCESS)
