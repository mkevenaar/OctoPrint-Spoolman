# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util.version import is_octoprint_compatible
from flask_babel import gettext

class SpoolmanPlugin(
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
):

    # ~~ StartupPlugin
    def on_after_startup(self):
        self._logger.info("Spoolman URL: (%s)" %
                          self._settings.get(["spoolman_url"]))

    # ~~ SettingsPlugin
    def get_settings_defaults(self):
        return {
            "spoolman_url": None,
        }

    def get_settings_restricted_paths(self):
        return {
            "admin": [
                ["spoolman_url"],
            ]
        }

    def get_settings_version(self):
        return 1


    # ~~ TemplatePlugin
    def get_template_configs(self):
        configs = [
            {
                "type": "settings",
                "name": gettext("Spoolman Companion"),
                "template": "spoolman_settings.jinja2",
                "custom_bindings": False,
            },
            {
                "type": "sidebar",
                "name": gettext("Spoolman Companion"),
                "template": "spoolman_sidebar.jinja2",
                "custom_bindings": False,
            }
        ]

        return configs

    # ~~ AssetPlugin
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/Spoolman.js"],
            "css": ["css/Spoolman.css"],
            "less": ["less/Spoolman.less"]
        }

    # ~~ Softwareupdate
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
                        "name": "Development",
                        "branch": "devel",
                        "comittish": ["devel", "main"],
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
__plugin_version__ = "0.1.0"
__plugin_description__ = "Spoolman integration for OctoPrint"
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
    __plugin_implementation__ = SpoolmanPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    }
