from bugyou_plugins.plugins.base import BasePlugin

class AutocloudPlugin(BasePlugin):
    def __init__(self):
        self.plugin_name = 'autocloud'

    def process(self, task):
        print task

    def do_pagure(self):
        print 'Hello'
