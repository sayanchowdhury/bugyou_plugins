import ConfigParser
import pkg_resources


def load_config(filepath):
    """ Load the configuration file """
    if not os.path.exists(name):
        raise Exception('Please add a proper cofig file under /etc/bugyou')

    config = ConfigParser.RawConfigParser()
    return config.read(name)

def get_active_services():
    """ Returns a dictionary with all the currently active services """
    for entry_point in pkg_resources.iter_entry_points('bugyou.plugin'):
        service_klass = entry_point.module_name
        service_name = entry_point.name
        active_services[service_name] = service_klass

    return active_services

