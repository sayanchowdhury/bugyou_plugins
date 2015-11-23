from bugyou_plugins.services import load_config

class BaseService(object):
    def __init__(self, *args, **kwargs):
        self.config = load_config()

    def get_issues_titles(self):
        """ Returns a set of all the issues titles """
        return {issue['title'] for issue in self.issues}
