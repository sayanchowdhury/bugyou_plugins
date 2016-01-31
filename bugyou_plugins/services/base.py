from bugyou_plugins.constants import CONFIG_FILEPATH
from bugyou_plugins.utility import load_config


class BaseService(object):
    def __init__(self, *args, **kwargs):
        self.config = load_config(CONFIG_FILEPATH)

    def _get_issues_titles(self):
        """ Returns a set of all the issues titles """
        return {issue['title'] for issue in self.issues}
