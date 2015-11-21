from bugyou_plugins.base import BasePlugin

class AutocloudPlugin(BasePlugin):
    def __init__(self):
        self.queue_name = 'autocloud'

    def process(self, task):
        print task



