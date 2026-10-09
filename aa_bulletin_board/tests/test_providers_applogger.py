"""
Test for the providers module.
"""

# Standard Library
import importlib
import logging
import sys
import typing

# AA Bulletin Board
from aa_bulletin_board import __title__
from aa_bulletin_board.providers.applogger import AppLogger
from aa_bulletin_board.tests import BaseTestCase


class TestAppLogger(BaseTestCase):
    """
    Test the AppLogger provider.
    """

    def test_adds_prefix_to_log_message(self):
        """
        Tests that the AppLogger correctly adds a prefix to log messages.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger)

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("This is a test message")

        self.assertIn(f"[{__title__}] This is a test message", log.output[0])

    def test_handles_empty_message(self):
        """
        Tests that the AppLogger handles an empty log message correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger)

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("")

        self.assertIn(f"[{__title__}] ", log.output[0])

    def test_type_checking_block_imports_typing_names_when_enabled(self):
        """
        Ensure that when typing.TYPE_CHECKING is True at import time, the
        module-level names `Any` and `MutableMapping` are present in the
        module namespace.

        :return:
        """

        module_name = "aa_bulletin_board.providers.applogger"
        orig_module = sys.modules.get(module_name)
        orig_flag = typing.TYPE_CHECKING

        try:
            if module_name in sys.modules:
                del sys.modules[module_name]

            typing.TYPE_CHECKING = True
            mod = importlib.import_module(module_name)

            self.assertTrue(hasattr(mod, "Any"))
            self.assertTrue(hasattr(mod, "MutableMapping"))
        finally:
            typing.TYPE_CHECKING = orig_flag
            if orig_module is not None:
                sys.modules[module_name] = orig_module
            else:
                sys.modules.pop(module_name, None)

    def test_type_checking_block_does_not_import_typing_names_when_disabled(self):
        """
        Ensure that when typing.TYPE_CHECKING is False at import time, the
        module-level names `Any` and `MutableMapping` are not present in the
        module namespace.

        :return:
        """

        module_name = "aa_bulletin_board.providers.applogger"
        orig_module = sys.modules.get(module_name)
        orig_flag = typing.TYPE_CHECKING

        try:
            if module_name in sys.modules:
                del sys.modules[module_name]

            typing.TYPE_CHECKING = False
            mod = importlib.import_module(module_name)

            self.assertFalse(hasattr(mod, "Any"))
            self.assertFalse(hasattr(mod, "MutableMapping"))
        finally:
            typing.TYPE_CHECKING = orig_flag
            if orig_module is not None:
                sys.modules[module_name] = orig_module
            else:
                sys.modules.pop(module_name, None)
