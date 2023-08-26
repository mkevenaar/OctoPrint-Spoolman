# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util.version import is_octoprint_compatible

from .api import SpoolmanApi
from .data import Spoolman

class SpoolmanPlugin(SpoolmanApi,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):

    def __init__(self):
        self.spoolman = None

    def initialize(self):
        spoolman_url = self._settings.get(["spoolman_url"])
        print(spoolman_url)
        try:
            # initialize Spoolman
            self.spoolman = Spoolman(spoolman_url)
            # self.spoolman.initialize()
        except Exception as e:
            self._logger.error("Failed to initialize spoolman: {message}".format(message=str(e)))
            self._logger.exception("Failed to initialize spoolman: {message}".format(message=str(e)))

    ##~~ SettingsPlugin
	
    def get_settings_version(self):
        return 1

    def get_settings_defaults(self):
        return dict(
            spoolman_url="",
        )
    
    def get_settings_restricted_paths(self):
        # only used in OctoPrint versions > 1.2.16
        return dict(admin=[["spoolman_url"], ])
    
    def on_settings_save(self, data):
        # before saving
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        self.initialize(self)

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/Spoolman.js"],
            "css": ["css/Spoolman.css"],
            "less": ["less/Spoolman.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "Spoolman": {
                "displayName": "Spoolman Companion",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "mkevenaar",
                "repo": "OctoPrint-Spoolman",
                "current": self._plugin_version,

                # stable releases
                "stable_branch": {
                    "name": "Stable",
                    "branch": "main",
                    "comittish": ["main"],
                },
                # release candidates
                "prerelease_branches": [
                    {
                        "name" : "Development",
                        "branch" : "devel",
                        "comittish" : ["devel", "main"],
                    },
                    {
                        "name": "Release Candidate",
                        "branch": "rc",
                        "comittish": ["rc", "main"],
                    }
                ],
                # update method: pip
                "pip": "https://github.com/mkevenaar/OctoPrint-Spoolman/archive/{target_version}.zip",
            }
        }

__plugin_name__ = "Spoolman Companion Plugin"
__plugin_pythoncompat__ = ">=3,<4"
__required_octoprint_version__ = ">=1.8.0"

def __plugin_load__():
    if not is_octoprint_compatible(__required_octoprint_version__):
        import logging
        logger = logging.getLogger(__name__)
        logger.error("OctoPrint version is not compatible ({version} required)"
                     .format(version=__required_octoprint_version__))
        return
    global __plugin_implementation__
    global __plugin_hooks__

    __plugin_implementation__ = SpoolmanPlugin()

    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    }
