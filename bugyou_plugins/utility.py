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

