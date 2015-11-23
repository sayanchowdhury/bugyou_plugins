from bugyou_plugins.plugins.base import BasePlugin

class AutocloudPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        self.plugin_name = 'autocloud'
        super(AutocloudPlugin, self).__init__(*args, **kwargs)

    def process(self, task):
        print task

    def do_pagure(self):
        print 'Hello'
