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

import os
import ConfigParser
import pkg_resources

def load_config(filepath):
    """ Load the configuration file """
    if not os.path.exists(filepath):
        raise Exception('Please add a proper cofig file under /etc/bugyou')

    config = ConfigParser.RawConfigParser()
    config.read(filepath)

    return config

def get_active_services():
    """ Returns a dictionary with all the currently active services """

    active_services = {}
    for entry_point in pkg_resources.iter_entry_points('bugyou.services'):
        service_name = entry_point.name
        active_services[service_name] = entry_point

    return active_services

