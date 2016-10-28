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

from bugyou_plugins.services.base import BaseService

import libpagure

class PagureService(BaseService):
    """ Service for Pagure """

    SERVICE = 'pagure'

    def __init__(self, plugin_name):
        """ Initiate the Pagure Service """
        super(PagureService, self).__init__()

        self.name = self.SERVICE
        self.repo_name = self.config.get("{}_{}".format(plugin_name,
                                                           self.SERVICE),
                                            'repo_name')
        self.access_token = self.config.get("{}_{}".format(plugin_name,
                                                           self.SERVICE),
                                            'access_token')

        self.project = libpagure.Pagure(pagure_token=self.access_token,
                                        pagure_repository=self.repo_name)

    def get_issues(self):
        """ Return list of all the issues in the repo """
        return self.project.list_issues()

    def create_issue(self, title, content, private=False):
        """ Creates an issue in the service repo
        :args title: Title for the issue
        :args content: Content for the issue
        :args private: Mark issue as private/public
        """

        params = {
            'title': title,
            'content': content,
            'private': private,
        }

        try:
            self.project.create_issue(**params)
        except Exception as e:
            pass

    def close_issue(self, issue_id):
        """ Closes the issue in the service repo
        :args issue_id: id of the issue
        """
        params = {
            'issue_id': issue_id,
            'new_status': 'Fixed',
        }

        try:
            self.project.change_issue_status(**params)
        except Exception as e:
            pass

    def update_issue(self, issue_id, content):
        """ Updates the issue with a comment
        :args issue_id: id of the issue
        :args content: content of the comment in the issue
        """
        params = {
            'issue_id': issue_id,
            'body': content,
        }
        try:
            self.project.comment_issue(**params)
        except Exception as e:
            pass

