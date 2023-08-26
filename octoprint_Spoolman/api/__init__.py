# coding=utf-8
from __future__ import absolute_import

import os
import tempfile
import shutil
from datetime import datetime

from flask import jsonify, request, make_response
# from werkzeug.exceptions import BadRequest

import octoprint.plugin
from octoprint.settings import valid_boolean_trues
# from octoprint.server import admin_permission
# from octoprint.access.permissions import Permissions
# from octoprint.server.util.flask import restricted_access, check_lastmodified, check_etag
# from octoprint.util import dict_merge

from .util import *


class SpoolmanApi(octoprint.plugin.BlueprintPlugin):

    @octoprint.plugin.BlueprintPlugin.route("/spools", methods=["GET"])
    def get_spools_list(self):
        archived = request.values.get("archived", "false") in valid_boolean_trues

        try:
            all_spools = self.spoolman.get_all_spools(archived)
            response = jsonify(dict(spools=all_spools))
            return response
        except Exception as e:
            self._logger.error("Failed to fetch spools: {message}".format(message=str(e)))
            self._logger.exception("Failed to fetch spools: {message}".format(message=str(e)))
            return make_response("Failed to fetch spools, see the log for more details", 500)