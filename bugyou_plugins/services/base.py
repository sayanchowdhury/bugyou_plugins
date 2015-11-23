from bugyou_plugins import load_config


class BaseService(object):
    def __init__(self, *args, **kwargs):
        filepath = '/etc/bugyou/bugyou_services.cfg'
        self.config = load_config(filepath)

    def get_issues_titles(self):
        """ Returns a set of all the issues titles """
        return {issue['title'] for issue in self.issues}
