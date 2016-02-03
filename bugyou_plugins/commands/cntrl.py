# Copyright (C) 2012 Red Hat, Inc.
#
# fedmsg is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# fedmsg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with fedmsg; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
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


if __name__ == '__main__':
    u = PluginController()
    u.notifier()
