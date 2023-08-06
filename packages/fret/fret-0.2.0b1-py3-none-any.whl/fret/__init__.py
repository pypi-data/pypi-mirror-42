from .util import colored, nonbreak, stateful
from .app import *

import logging

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)


class _ColoredFormatter(logging.Formatter):
    _LOG_COLORS = {
        'WARNING': 'y',
        'INFO': 'g',
        'DEBUG': 'b',
        'CRITICAL': 'y',
        'ERROR': 'r'
    }

    def format(self, record):  # pragma: no cover
        levelname = record.levelname
        if levelname in self._LOG_COLORS:
            record.levelname = colored(
                record.levelname[0],
                self._LOG_COLORS[record.levelname],
                style='b'
            )
        return logging.Formatter.format(self, record)


log_formatter = _ColoredFormatter(
    '%(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
_logger.addHandler(console_handler)


__all__ = ['app', 'workspace', 'configurable', 'command', 'arg',
           'nonbreak', 'stateful']
