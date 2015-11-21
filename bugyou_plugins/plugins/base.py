import abc
import copy
import multiprocessing

from retask import Queue


class BasePlugin(object):
    __metaclass__ = abc.ABCMeta

    def initialize(self):
        self.init_retask_connection()
        self.init_worker()

    def init_retask_connection(self):
        """ Connect to the retask queue for the plugin """
        self.queue = Queue(self.queue_name)
        conn = self.queue.connect()
        if not conn:
            log.debug('Could not connect to %s queue' % self.queue_name)
            return False

    def consume(self):
        while True:
            task = self.queue.wait()
            self.process(task)

    def init_worker(self):
        """ Create a process and start consuming the messages """
        process = multiprocessing.Process(target=self.consume)
        process.start()

    @abc.abstractmethod
    def process(self):
        """ Consumes the messages from retask """
