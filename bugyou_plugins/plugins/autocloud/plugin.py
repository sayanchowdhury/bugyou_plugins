from bugyou_plugins.plugins.base import BasePlugin
from bugyou_plugins.services.pagure import PagureService

class AutocloudPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        self.plugin_name = 'autocloud'
        super(AutocloudPlugin, self).__init__(*args, **kwargs)

    def process(self, msg):
        for service in self.services:
            print msg
            """
            getattr(self, 'do_%s'%service.SERVICE)(msg)
            """

    def do_pagure(self, msg):
        pagure_obj = PagureService(repo_name=self.plugin_name)

        issue_content_templ = """
        The image {image_name} for the release - {release} failed.
        The output can be seen here - {output_url}
        """

        output_url_tmpl = "https://apps.fedoraproject.org/autocloud/jobs/{job_id}/output"

        issues = pagure_obj.get_issues()
        issue_titles = self._get_issues_titles(issues)

        msg_info = msg['body']['msg']
        topic = msg['body']['topic']
        image_name = msg_info['image_name']
        release = msg_info['release']
        job_id = msg_info['job_id']

        lookup_key = pagure_obj.lookup_key_tmpl.format(image_name=image_name,
                                                 release=release)

        lookup_key_exists = lookup_key in issue_titles

        if 'failed' in topic:
            output_url = output_url_tmpl.format(job_id=job)
            content = issue_content_template.format(image_name=image_name,
                                                    release=release,
                                                    output_url=output_url)

            if lookup_key_exists:
                matched_issue = (issue for issue in issues
                                 if issue['title'] == loopkup_key).next()
                issue_id = matched_issue['id']

                pagure_obj.update_issue_comment(issue_id=issue_id,
                                                content=content)

            elif 'failed' in topic:
                pagure_obj.create_issue(title=lookup_key, content=content)

        if 'success' in topic:
            if lookup_key_exists:
                matched_issue = (issue for issue in issues
                                 if issue['title'] == lookup_key).next()
                issue_id = matched_issue['id']

                pagure_obj.close_issue(issue_id=issue_id)
