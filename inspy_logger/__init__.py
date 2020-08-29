#!/usr/bin/env python3
import logging, colorlog
from logging import DEBUG, INFO, WARNING, getLogger, Logger


started = False
base_logger = None

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

    def start(self):
        global started, base_logger
        """

        Start a formatted root-logger

        :type name: str
        :param debug: Boolean - If True logger will start in at debug level. This is most useful if you're trying to see
                                the internal goings-on immediately on starting the logger.

        :param name: str - The name you want to give to the root logger

        """

        if started:
            base_logger.warning(
                "There already is a base logger for this program. I am using it to deliever this message."
            )
            return None

        from colorlog import ColoredFormatter

        formatter = ColoredFormatter(
            "%(bold_cyan)s%(asctime)-s%(reset)s%(log_color)s::%(module)s.%(name)-14s::%(levelname)-10s%(reset)s%("
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
        started = True
        base_logger = self.device
        return self.device

    def __init__(self, device_name, log_level):
        if log_level is None:
            log_level = "info"
        self.l_lvl = log_level.lower()
        self.root_name = device_name
        self.start()
        print(dir(self))
