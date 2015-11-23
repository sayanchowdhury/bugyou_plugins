import ConfigParser

def load_config(filepath):
    if not os.path.exists(name):
        raise Exception('Please add a proper cofig file under /etc/bugyou')

    config = ConfigParser.RawConfigParser()
    return config.read(name)
