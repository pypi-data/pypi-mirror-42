import fileinput
import glob
import os
import re

from pathlib import Path
from typing import List


def replace_template_strings(project_directory: Path, template_strings: List[str], value_strings: List[str]):
    """
    Replaces template strings with values in a new project.

    :param project_directory: New project directory.
    :param template_strings: List of template strings to replace, should be name only without template {{}}
    characters.
    :param value_strings: List of strings to replace template strings with.
    """
    cwd = Path.cwd()
    os.chdir(str(project_directory))

    for entry in glob.iglob(str(project_directory) + '/**', recursive=True):
        if not os.path.isdir(entry) and not entry.startswith('__pycache__') and entry.endswith('tpl'):
            with fileinput.FileInput(entry, inplace=True) as file:
                for line in file:
                    new_line = line

                    for i in enumerate(template_strings):
                        template_string = i[1]
                        value_string = value_strings[i[0]]

                        regex = '{{%s}}' % template_string
                        new_line = re.sub(regex, value_string, new_line)

                    print(new_line, end='')

            Path(entry).rename(entry.split('.tpl')[0])

    os.chdir(str(cwd))
