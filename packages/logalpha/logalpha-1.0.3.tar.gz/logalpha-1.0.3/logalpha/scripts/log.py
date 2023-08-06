# This file is part of the LogAlpha package.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Logging from the command line."""


# standard libs
import os
import re
import sys
import shlex
from subprocess import check_output, STDOUT
from typing import List, Dict

# internal libs
from logalpha.handlers import BaseHandler, ConsoleHandler, FileHandler
from logalpha.loggers import BaseLogger


LOGLEVEL         = os.getenv('LOGALPHA_LOGLEVEL', default='INFO')
USE_CONSOLE      = os.getenv('LOGALPHA_NOCONSOLE') is None
CONSOLE_LOGLEVEL = os.getenv('LOGALPHA_CONSOLE_LOGLEVEL', default=LOGLEVEL)
FILE_LOGLEVEL    = os.getenv('LOGALPHA_FILE_LOGLEVEL', default=LOGLEVEL)
FILE_PATHS       = os.getenv('LOGALPHA_FILE_PATHS', default=None)
TEMPLATE         = os.getenv('LOGALPHA_TEMPLATE', default='{level} {message}')
CONSOLE_TEMPLATE = os.getenv('LOGALPHA_CONSOLE_TEMPLATE', default=TEMPLATE)
FILE_TEMPLATE    = os.getenv('LOGALPHA_FILE_TEMPLATE', default=TEMPLATE)


VAR_REGEX = re.compile(r'{(\w*)(:\S*}|})')
def get_variables(template: str) -> List[str]:
    """Pull out variables from a template."""
    return [match[0] for match in VAR_REGEX.findall(template)]


def shell(command: str, timeout: int=1, **kwargs) -> str:
    """Evaluate 'command' and return output."""
    cmdlets = shlex.split(command)
    return check_output(cmdlets, timeout=timeout, stderr=STDOUT,
                        **kwargs).decode('utf-8').strip()


def process_template(template: str) -> Dict[str, str]:
    """Builds callback dictionary from shell commands."""
    spec = dict()
    for name in get_variables(template):
        if name not in BaseHandler.default_labels:
            command = os.getenv(name)
            if command is None:
                raise ValueError(f'{name} is not defined!')
            else:
                spec[name] = lambda: shell(command)
    return spec


handlers = list()
if USE_CONSOLE is True:
    ch = ConsoleHandler(level=CONSOLE_LOGLEVEL, template=CONSOLE_TEMPLATE,
                        **process_template(CONSOLE_TEMPLATE))
    handlers.append(ch)

if FILE_PATHS is not None:
    for filepath in FILE_PATHS.split(':'):
        fh = FileHandler(level=FILE_LOGLEVEL, template=FILE_TEMPLATE,
                         file=filepath, **process_template(CONSOLE_TEMPLATE))
        handlers.append(fh)

log = BaseLogger(handlers)
msg = ' '.join(sys.argv[1:])


def debug() -> int:
    log.debug(msg)
    return 0


def info() -> int:
    log.info(msg)
    return 0


def warning() -> int:
    log.warning(msg)
    return 0


def error() -> int:
    log.error(msg)
    return 0


def critical() -> int:
    log.critical(msg)
    return 0
