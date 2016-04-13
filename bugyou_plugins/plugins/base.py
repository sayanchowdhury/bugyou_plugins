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

import abc
import copy
import multiprocessing

from retask.queue import Queue

from bugyou_plugins.constants import PLUGINS_CONFIG_FILEPATH
from bugyou_plugins.utility import get_active_services, load_config

import logging
log = logging.getLogger("bugyou")

class BasePlugin(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.config = load_config(PLUGINS_CONFIG_FILEPATH)
        self.active_services = get_active_services()
        self.services = []

    def initialize(self):
        self.init_retask_connection()
        self.load_services()
        self.init_worker()

    def init_retask_connection(self):
        """ Connect to the retask queue for the plugin """
        self.queue = Queue(self.plugin_name)
        conn = self.queue.connect()
        log.info("Initializing redis conection: %s" % self.plugin_name)
        if not conn:
            log.error("Could not connect to %s queue" % self.plugin_name)
            return False

    def consume(self):
        while True:
            task = self.queue.wait()
            if task:
                log.debug("Processing Message: %s" % task.data['msg']['body']['msg_id'])
                self.process(task.data['msg'])

    def init_worker(self):
        """ Create a process and start consuming the messages """
        process = multiprocessing.Process(target=self.consume)
        process.start()

    def load_services(self):
        """ Load the services for the plugin """
        services = self.config.get(self.plugin_name, 'services').split(',')
        log.info("Start loading services")
        for service in services:
            self.services.append(self.active_services[service].load())
        log.info("Complete loading services %s" % self.services)

    @abc.abstractmethod
    def process(self):
        """ Consumes the messages from retask """
        return

    @abc.abstractmethod
    def do_pagure(self):
        """ Override to do activity related to pagure """
        return
