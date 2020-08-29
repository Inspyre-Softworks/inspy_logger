#!/usr/bin/env python3
import logging, colorlog
from colorlog import ColoredFormatter
from logging import DEBUG, INFO, WARNING, getLogger, Logger

LEVELS = ["debug", "info", "warning"]


class InspyLogger(Logger):
    def adjust_level(self, name, lvl):

        _log = getLogger(name)

        if lvl == "debug":
            _ = DEBUG
        elif lvl == "info":
            _ = INFO
        elif lvl == "warn" or lvl == "warning":
            _ = WARNING

        _log.setLevel(_)

    def __start__(self):
        if self.started:
            self.device.warning(
                "There already is a base logger for this program. I am using it to deliever this message."
            )
            return None

        formatter = ColoredFormatter(
            "%(bold_cyan)s%(asctime)-s%(reset)s%(log_color)s::.%(name)s%(module)s-14s::%(levelname)-10s%(reset)s%("
            "blue)s%(message)-s",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "bold_cyan",
                "INFO": "bold_green",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_red",
            },
        )

        self.device = logging.getLogger(self.root_name)
        self.main_handler = logging.StreamHandler()
        self.main_handler.setFormatter(formatter)
        self.device.addHandler(self.main_handler)
        self.adjust_level(self.root_name, self.l_lvl)
        self.device.info(f"Logger started for %s" % self.root_name)
        self.started = True

    def __init__(self, device_name, log_level):
        """
        Starts a colored and formatted logging device for you.

        Starts a colored and formatted logging device for you. No need to worry about handlers, etc

        Args:

            device_name (str): A string containing the name you'd like to choose for the root logger

            log_level (str): A string containing the name of the level you'd like InspyLogger to be limited to.
            You can choose between:
              - debug
              - info
              - warning
    """

        if log_level is None:
            log_level = "info"
        self.l_lvl = log_level.lower()
        self.root_name = device_name
        self.started = False
        self.device = None
        self.__start__()
