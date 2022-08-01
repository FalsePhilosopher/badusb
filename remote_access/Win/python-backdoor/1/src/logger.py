"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""

import logging.config

LOGGER_ID = "pb_logger"


# https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format_detail = "%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s"
    format = "[%(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: format_detail,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format
    }

    def format(self, record):
        formatter = logging.Formatter(self.FORMATS.get(record.levelno), datefmt='%H:%M:%S')

        return formatter.format(record)


def init(_args):
    level = logging.DEBUG if _args.debug else logging.INFO

    logger = logging.getLogger(LOGGER_ID)

    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
