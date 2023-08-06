import io
import sys
from contextlib import redirect_stdout
from unittest import TestCase

from limis.management import CommandLineInterface, execute_limis_management, execute_limis_project_management, \
    exit_codes


class TestCommandLineInterface(TestCase):
    def test_run(self):
        with redirect_stdout(io.StringIO()):
            original_sys_argv = sys.argv

            sys.argv = [original_sys_argv[0]]
            self.assertEqual(CommandLineInterface.run(), exit_codes.SUCCESS)

            sys.argv = [original_sys_argv[0]] + ['help']
            self.assertEqual(CommandLineInterface.run(), exit_codes.SUCCESS)

            sys.argv = [original_sys_argv[0]] + ['unknown_command']
            self.assertEqual(CommandLineInterface.run(), exit_codes.UNKNOWN_COMMAND)

            sys.argv = [original_sys_argv[0]] + ['version']
            self.assertEqual(CommandLineInterface.run(), exit_codes.SUCCESS)

            sys.argv = original_sys_argv


class TestMethods(TestCase):
    def test_execute_limis_management(self):
        with redirect_stdout(io.StringIO()):
            original_sys_argv = sys.argv

            sys.argv = [original_sys_argv[0]]
            self.assertEqual(execute_limis_management(), exit_codes.SUCCESS)

            sys.argv = original_sys_argv

    def test_execute_limis_project_management(self):
        with redirect_stdout(io.StringIO()):
            original_sys_argv = sys.argv

            sys.argv = [original_sys_argv[0]]
            self.assertEqual(execute_limis_project_management(), exit_codes.SUCCESS)

            sys.argv = original_sys_argv
