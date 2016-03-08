# -*- coding: utf-8 -*-
# Copyright (C) 2015 Red Hat, Inc.
#
# bugyou_plugins is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# bugyou_plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# bugyou_plugins.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
#

from bugyou_plugins.constants import SERVICES_CONFIG_FILEPATH
from bugyou_plugins.utility import load_config


class BaseService(object):
    def __init__(self, *args, **kwargs):
        self.config = load_config(SERVICES_CONFIG_FILEPATH)

    def _get_issues_titles(self):
        """ Returns a set of all the issues titles """
        return {issue['title'] for issue in self.issues}
