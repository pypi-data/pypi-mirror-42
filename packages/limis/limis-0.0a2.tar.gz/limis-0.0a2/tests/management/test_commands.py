import io
import os
import shutil
import signal
import time

from contextlib import redirect_stdout
from pathlib import Path
from threading import Thread
from typing import List
from unittest import TestCase

from limis.core import settings
from limis.management import exit_codes
from limis.management.commands import Command, CreateProject, Server, Version

from tests import listening


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
            command = CreateProject()
            self.assertEqual(command.run([]), exit_codes.INVALID_ARGUMENTS)

            self.assertEqual(command.run([self.test_project_name]), exit_codes.SUCCESS)
            self.assertTrue(self.test_project_default_directory.exists())
            self.assertTrue((self.test_project_default_directory / self.test_project_name).exists())

            with open(str(self.test_project_default_directory / 'management.py')) as file:
                self.assertTrue(file.read(), 'name = \'{}\''.format(self.test_project_name))
                file.close()

            self.assertEqual(command.run([self.test_project_name, self.test_project_directory]),
                             exit_codes.SUCCESS)
            self.assertTrue(self.test_project_directory.exists())
            self.assertTrue((self.test_project_directory / self.test_project_name).exists())

            with open(str(self.test_project_directory / 'management.py')) as file:
                self.assertTrue(file.read(), 'name = \'{}\''.format(self.test_project_name))
                file.close()

            self.assertFalse(command.run([self.test_project_name]))


class TestServer(TestCase):
    project_name = 'test_project'
    project_directory = Path.cwd() / project_name

    @staticmethod
    def __run_command(args: List[str]):
        global server_command

        server_command = Server()

        with redirect_stdout(io.StringIO()):
            server_command.run(args=args)

    @classmethod
    def setUpClass(cls):
        command = CreateProject()

        with redirect_stdout(io.StringIO()):
            command.run([cls.project_name])

        settings_file = cls.project_directory / cls.project_name / 'settings.ini'

        os.environ['LIMIS_PROJECT_NAME'] = cls.project_name
        os.environ['LIMIS_PROJECT_SETTINGS'] = str(settings_file)

        if settings_file.exists():
            settings_file.unlink()

        with open(str(settings_file), 'w') as file:
            print('[test_project]', file=file)
            print('root_services={}.{}.services'.format(cls.project_name, cls.project_name), file=file)

    @classmethod
    def tearDownClass(cls):
        if cls.project_directory.exists():
                shutil.rmtree(str(cls.project_directory), ignore_errors=False)

        os.environ.pop('LIMIS_PROJECT_NAME')
        os.environ.pop('LIMIS_PROJECT_SETTINGS')

    def setUp(self):
        try:
            del server_command
        except NameError:
            pass

    def tearDown(self):
        try:
            if server_command._http_server_running() or server_command._websocket_server_running():
                server_command._signal_handler(signal.SIGINT, None)

                while server_command._http_server_running() or server_command._websocket_server_running():
                    time.sleep(3)
        except NameError:
            pass

    def test__http_server_running(self):
        self.assertFalse(Server._http_server_running())

    def test__websocket_server_running(self):
        self.assertFalse(Server._websocket_server_running())

    def test__signal_handler(self):
        Server._signal_handler(signal.SIGINT, None)

    def test_parse_arguments_none(self):
        command = Server()
        command.parse_arguments(args=[])
        self.assertTrue(command.http)

    def test_parse_arguments_debug(self):
        command = Server()
        command.parse_arguments(args=['-d'])
        self.assertTrue(command.debug)

        command = Server()
        command.parse_arguments(args=['--debug'])
        self.assertTrue(command.debug)

    def test_parse_arguments_http(self):
        command = Server()
        command.parse_arguments(args=['-p'])
        self.assertTrue(command.http)

        command = Server()
        command.parse_arguments(args=['--http'])
        self.assertTrue(command.http)

    def test_parse_arguments_http_port(self):
        command = Server()
        command.parse_arguments(['--http_port', '8000'])
        self.assertEqual(command.http_port, 8000)

        command = Server()
        with self.assertRaises(ValueError):
            with redirect_stdout(io.StringIO()):
                command.parse_arguments(['--http_port', 'invalid'])

        command = Server()
        with self.assertRaises(ValueError):
            with redirect_stdout(io.StringIO()):
                command.parse_arguments(['--http_port'])

    def test_parse_arguments_websocket_port(self):
        command = Server()
        command.parse_arguments(['--websocket_port', '8000'])
        self.assertEqual(command.websocket_port, 8000)

        command = Server()
        with self.assertRaises(ValueError):
            with redirect_stdout(io.StringIO()):
                command.parse_arguments(['--websocket_port', 'invalid'])

        command = Server()
        with self.assertRaises(ValueError):
            with redirect_stdout(io.StringIO()):
                command.parse_arguments(['--websocket_port'])

    def test_parse_arguments_websocket(self):
        command = Server()
        command.parse_arguments(args=['-w'])
        self.assertTrue(command.websocket)

        command = Server()
        command.parse_arguments(args=['--websocket'])
        self.assertTrue(command.websocket)

    def test_run(self):
        thread = Thread(target=self.__run_command, kwargs={'args': []})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(int(settings.server['default_http_port'])))

    def test_run_invalid_arguments(self):
        command = Server()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(command.run(args=['--http_port', 'invalid']), exit_codes.INVALID_ARGUMENTS)

    def test_run_http(self):
        thread = Thread(target=self.__run_command, kwargs={'args': ['-p']})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(int(settings.server['default_http_port'])))

    def test_run_http_with_port(self):
        thread = Thread(target=self.__run_command, kwargs={'args': ['-p', '--http_port=8001']})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(8001))

    def test_run_websocket(self):
        thread = Thread(target=self.__run_command, kwargs={'args': ['-w']})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(int(settings.server['default_websocket_port'])))

    def test_run_websocket_with_port(self):
        thread = Thread(target=self.__run_command, kwargs={'args': ['-w', '--websocket_port=8001']})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(8001))

    def test_run_http_and_websocket(self):
        thread = Thread(target=self.__run_command, kwargs={'args': ['-p', '-w']})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(int(settings.server['default_http_port'])))
        self.assertTrue(listening(int(settings.server['default_websocket_port'])))

    def test_run_http_and_websocket_with_ports(self):
        thread = Thread(target=self.__run_command,
                        kwargs={'args': ['-p', '--http_port=8001', '-w', '--websocket_port=8002']})
        thread.daemon = True
        thread.start()
        time.sleep(3)

        self.assertTrue(listening(8001))
        self.assertTrue(listening(8002))


class TestVersion(TestCase):
    def test_run(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(Version.run(args=[]), exit_codes.SUCCESS)
