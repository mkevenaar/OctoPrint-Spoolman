import unittest

from octoprint_Spoolman import __plugin_load__


class TestPlugin(unittest.TestCase):
    def test_load(self):
        __plugin_load__()
