import abc
import copy
import multiprocessing

from retask import Queue

from bugyou_plugins.utility import get_active_services, load_config


class BasePlugin(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        filepath = '/etc/bugyou/bugyou_plugins.cfg'
        self.config = load_config(filepath)
        self.active_services = get_active_services()

    def initialize(self):
        self.init_retask_connection()
        self.init_worker()

    def init_retask_connection(self):
        """ Connect to the retask queue for the plugin """
        self.queue = Queue(self.plugin_name)
        conn = self.queue.connect()
        if not conn:
            log.debug('Could not connect to %s queue' % self.plugin_name)
            return False

    def consume(self):
        while True:
            task = self.queue.wait()
            self.process(task)

    def init_worker(self):
        """ Create a process and start consuming the messages """
        process = multiprocessing.Process(target=self.consume)
        process.start()

    def load_services(self):
        """ Load the services for the plugin """
        services = self.config.get(self.plugin_name, 'services')
        for service in services:
            self.services.append(self.active_services[serivce].load())

    @abc.abstractmethod
    def process(self):
        """ Consumes the messages from retask """

    @abc.abstractmethod
    def do_pagure(self):
        """ Override to do activity related to pagure """
