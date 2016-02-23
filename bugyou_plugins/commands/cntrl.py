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

import pkg_resources
import ConfigParser

from retask import Task
from retask import Queue

from bugyou_plugins.constants import CONFIG_FILEPATH
from bugyou_plugins.utility import load_config


class PluginController(object):
    def __init__(self):

        # Get all the plugins from the config file
        self.config = load_config(CONFIG_FILEPATH)
        self.plugins = self.config.sections()

        self.active_plugins = {}
        for entry_point in pkg_resources.iter_entry_points('bugyou.plugins'):
            plugin_object = entry_point.load()
            plugin_name = entry_point.name
            self.active_plugins[plugin_name] = plugin_object

    def notifier(self):
        # Connect to the instruction queue and notify bugyou to create a queue
        # for the plugin and start pushing the fedmsg messags.

        queue = Queue('instruction')
        queue.connect()
        for plugin in self.plugins:
            try:
                topic = self.config.get(plugin, 'topic')
            except ConfigParser.NoOptionError:
                print 'topic does not exists'
            if topic is None:
                print 'Topic does not exists'
                continue

            payload = {
                'type': 'create',
                'queue_name': plugin,
                'topic': topic,
            }
            task = Task(payload)
            queue.enqueue(task)

            if plugin in self.active_plugins:
                Plugin = self.active_plugins[plugin]
                plugin_obj = Plugin()
                plugin_obj.initialize()


def cntrl():
    u = PluginController()
    u.notifier()
