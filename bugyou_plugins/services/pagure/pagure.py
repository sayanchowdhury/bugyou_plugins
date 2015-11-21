class PagureService(BaseService):
    """ Service for Pagure """
    def __init__(self, *args, **kwargs):

        self.config = kwargs.get('config')
        self.section = kwargs.get('section')

        self.access_token = self.config.get(section, 'access_token')
        self.repo_name = self.config.get(section, 'repo_name')

        self.project = libpagure.Pagure(pagure_token=self.access_token,
                                        pagure_repository=self.repo_name)

    def get_issues(self):
        """ Return list of all the issues in the repo """
        return self.project.list_issues()

    def create_issue(self, *args, **kwargs):
        """ Creates an issue in the service repo """
        title = kwargs.get('title')
        content = kwargs.get('content')

        params = {
            'title': title,
            'content': content,
            'private': False,
        }

        try:
            self.project.create_issue(**params)
        except Exception as e:
            pass

    def close_issue(self, *args, **kwargs):
        """ Closes the issue in the service repo """
        issue_id = kwargs.get('issue_id')

        params = {
            'issue_id': issue_id,
            'new_status': 'Fixed',
        }

        try:
            self.project.comment_issue(**params)
        except Exception as e:
            pass

    def update_issue(self, *args, **kwargs):
        """ Updates the issue with a comment """

        issue_id = kwargs.get('issue_id')
        content = kwargs.get('content')

        params = {
            'issue_id': issue_id,
            'content': content,
        }
        try:
            self.project.update_issue(**params)
        except:
            pass

