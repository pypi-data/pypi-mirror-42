import fileinput
import os

from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copytree, move
from typing import List

from limis.core import get_version
from limis.management import exit_codes, messages


class Command(ABC):
    """
    Command

    Abstract class that defines a command.

    :attribute help: Command help text.
    :attribute help_arguments: Command arguments help text.
    :attribute name: Command name argument.
    """
    help = None
    help_arguments = None
    name = None

    @classmethod
    def invalid_arguments(cls) -> int:
        """
        Displays the invalid arguments message and arguments help text. Called when a command has been called with an
        invalid set of arguments.

        :return: Command line exit code, default INVALID_ARGUMENTS.
        """
        print(messages.COMMAND_LINE_INTERFACE_RUN_INVALID_ARGUMENTS)
        print(cls.help_arguments)

        return exit_codes.INVALID_ARGUMENTS

    @classmethod
    @abstractmethod
    def run(cls, args: List[str]) -> int:
        """
        Abstract method to execute the command logic.

        :param args: List of arguments passed to the command.
        :return: Exit code.
        """


class CreateProject(Command):
    """
    CreateProject

    Creates a new limis project.
    """
    help = 'Creates a limis project'
    help_arguments = '<project_name> [project_directory]'
    name = 'create_project'

    @classmethod
    def __replace_template_strings(cls, project_directory: Path, template_strings: List[str], value_strings: List[str]):
        """
        Replaces template strings with values in a new project.

        :param project_directory: New project directory.
        :param template_strings: List of template strings to replace, should be name only without template '{{}}'
        characters.
        :param value_strings: List of strings to replace template strings with.
        """
        cwd = Path.cwd()

        os.chdir(str(project_directory))

        for filename in os.listdir():
            if not os.path.isdir(filename):
                with fileinput.FileInput(filename, inplace=True) as file:
                    for line in file:
                        for i in enumerate(template_strings):
                            template_string = i[1]
                            value_string = value_strings[i[0]]
                            print(line.replace('{{%s}}' % template_string, value_string), end='')

        os.chdir(str(cwd))

    @classmethod
    def run(cls, args: List[str]) -> int:
        """
        Executes the create_project command. This command creates a new limis project based on the project template that
        is stored in limis.core.project_template. If the directory is not passed with the arguments the current
        working directory is used as the parent and new directory with the project name will be created.

        :param args: Arguments should be a list with the project name and optionally the project directory.
        :return: Command line exit code.
        """
        if len(args) < 1 or len(args) > 2:
            return cls.invalid_arguments()

        name = args[0]
        directory = None

        if len(args) == 2:
            directory = args[1]

        print(messages.COMMAND_CREATE_PROJECT_RUN_STARTED.format(name))

        if not directory:
            directory = Path.cwd() / name

        project_template_directory = Path(__file__).parent.parent / Path('resources/project_template')

        try:
            copytree(str(project_template_directory), str(directory))
            move(str(directory / 'project'), str(directory / name))
        except OSError:
            print(messages.COMMAND_CREATE_PROJECT_RUN_DIRECTORY_ERROR.format(directory))
            return False

        cls.__replace_template_strings(directory, ['name'], [name])

        print(messages.COMMAND_CREATE_PROJECT_RUN_COMPLETED.format(name))

        return exit_codes.SUCCESS


class Version(Command):
    """
    Version

    Command to retreive the installed version of limis.
    """
    help = 'Returns the current limis version'
    help_arguments = ''
    name = 'version'

    @classmethod
    def run(cls, args: List[str]) -> int:
        """
        Executes the version command.

        :param args: Arguments are not used for this command.
        :return: Command line exit code, defaults to SUCCESS.
        """
        print(messages.COMMAND_VERSION.format(get_version()))
        return exit_codes.SUCCESS
