from retask import Task
from retask import Queue

from bugyou_plugins.constants import CONFIG_FILEPATH
from bugyou_plugins.utility import load_config

class PluginController(object):
    def __init__(self):

        # Get all the plugins from the config file
        self.config = load_config(CONFIG_FILEPATH)
        self.plugins = config.sections()

        self.active_plugins = {}
        for entry_point in pkg_resources.iter_entry_points('bugyou.plugins'):
            plugin_name = entry_point.name
            self.active_plugins[plugin_name] = plugin_name

    def notify_bugyou(self):

        # Connect to the instruction queue and notify bugyou to create a queue
        # for the plugin and start pushing the fedmsg messags.

        queue = Queue('instruction')
        for plugin in self.plugins:
            topic = self.config.get(plugin, 'topic')
            payload = {
                'type': 'create',
                'queue_name': plugin,
                'topic': topic,
            }
            task = Task(payload)
            queue.enqueue(task)

            if plugin in self.active_plugins:
                Plugin = self.active_plugins[plugin].load()
                plugin_obj = Plugin()
                plugin_obj.intialize()
