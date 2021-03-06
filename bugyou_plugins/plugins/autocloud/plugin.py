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

import re

from bugyou_plugins.plugins.base import BasePlugin
from bugyou_plugins.services.pagure import PagureService

import logging
log = logging.getLogger("bugyou")

class AutocloudPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        self.plugin_name = 'autocloud'
        super(AutocloudPlugin, self).__init__(*args, **kwargs)

    def process(self, msg):
        for service in self.services:
            log.info("Executing Service %s" % service.SERVICE)
            getattr(self, 'do_%s'%service.SERVICE)(msg)

    def _get_issues_title(self, issues):
        """ Returns a set of all the issue title
        """
        return {issue['title'] for issue in issues}

    def do_pagure(self, msg):
        log.info("Received message %s" % msg['body']['msg_id'])
        pagure_obj = PagureService(plugin_name=self.plugin_name)

        issue_content_templ = """
        The image {image_name}({compose_id}) for the release - {release} failed.
        The output can be seen here - {output_url}
        """

        output_url_tmpl = "https://apps.fedoraproject.org/autocloud/jobs/{job_id}/output"
        lookup_key_tmpl = "{image_name}-{release}"

        issues = pagure_obj.get_issues()
        issue_titles = self._get_issues_title(issues)

        msg_info = msg['body']['msg']
        topic = msg['body']['topic']
        image_name = msg_info['image_name']
        release = msg_info['release']
        job_id = msg_info['job_id']
        compose_id = msg_info['compose_id']

        # Generalize image_name here. The image_name contains the compose date
        # and the respin. The regex is to remove those.
        pattern = '[-]\d{8}(.n)?.\d'
        formatted_image_name = re.sub(pattern, '', image_name)
        lookup_key = lookup_key_tmpl.format(image_name=formatted_image_name,
                                            release=release)

        lookup_key_exists = lookup_key in issue_titles

        if 'failed' in topic:
            output_url = output_url_tmpl.format(job_id=job_id)
            content = issue_content_templ.format(image_name=image_name,
                                                 compose_id=compose_id,
                                                 release=release,
                                                 output_url=output_url)

            if lookup_key_exists:
                matched_issue = (issue for issue in issues
                                 if issue['title'] == lookup_key).next()
                issue_id = matched_issue['id']
                log.info("Updating issue %s:%s" % (self.plugin_name, issue_id))
                pagure_obj.update_issue(issue_id=issue_id,
                                        content=content)

            elif 'failed' in topic:
                log.info("Creating issue %s" % self.plugin_name)
                pagure_obj.create_issue(title=lookup_key, content=content)

        if 'success' in topic:
            if lookup_key_exists:
                matched_issue = (issue for issue in issues
                                 if issue['title'] == lookup_key).next()
                issue_id = matched_issue['id']

                log.info("Closing issue %s:%s" % (self.plugin_name, issue_id))
                pagure_obj.close_issue(issue_id=issue_id)
