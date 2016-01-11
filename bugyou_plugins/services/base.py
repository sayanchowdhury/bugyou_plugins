from bugyou_plugins.utility import load_config


class BaseService(object):
    def __init__(self, *args, **kwargs):
        filepath = '/etc/bugyou/bugyou_services.cfg'
        self.config = load_config(filepath)

    def _get_issues_titles(self):
        """ Returns a set of all the issues titles """
        return {issue['title'] for issue in self.issues}
