# TODO: fix the response of the examples
import json


class SourcesMixin(object):

    def get_sources(self, project_id, include_config=None,
                    include_run_stats=None):
        """Get all sources for the provided project.

        :param project_id: Project identifier.
        :param include_config: Bool, whether or not to include the config for
            all the Sources.
        :param include_run_stats: Bool, whether or not to include the run stats
            for all the Sources.

        :returns: A list of sources.

        Example::

            >>> client.get_sources('2sic33jZTi-ifflvQAVcfw')
            [
                {
                    u'config': {
                        u'market': u'de-CH',
                        u'query': u'squirro',
                        u'vertical': u'News',
                    },
                    u'id': u'hw8j7LUBRM28-jAellgQdA',
                    u'modified_at': u'2012-10-09T07:54:12',
                    u'source_id': u'2VkLodDHTmiMO3rlWi2MVQ',
                    u'title': u'News Alerts for "squirro" in Switzerland',
                    u'workflow': {
                        u'name': u'Default Workflow',
                        u'project_default': True,
                        u'id': u'kAvdogQOQvGHijqcIPi_WA',
                        u'project_id': u'FzbcEMMNTBeQcG2wnwnxLQ'
                    }
                }
            ]
        """

        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s'
               '/sources')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id}

        params = {}
        if include_config:
            params['include_config'] = include_config
        if include_run_stats:
            params['include_run_stats'] = include_run_stats

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_source(self, project_id, source_id, include_config=None,
                   include_run_stats=None):
        """Get source details.

        :param project_id: Project identifier.
        :param source_id: Source identifier.
        :param include_config: Bool, whether or not to include the config for
            the Source.
        :param include_run_stats: Bool, whether or not to include the run stats
            for the Source.
        :returns: A dictionary which contains the source.

        Example::

            >>> client.get_source(
            ...     '2sic33jZTi-ifflvQAVcfw', 'hw8j7LUBRM28-jAellgQdA')
            {
                u'config': {
                    u'market': u'de-CH',
                    u'query': u'squirro',
                    u'vertical': u'News',
                },
                u'deleted': False,
                u'id': u'hw8j7LUBRM28-jAellgQdA',
                u'modified_at': u'2012-10-09T07:54:12',
                u'source_id': u'2VkLodDHTmiMO3rlWi2MVQ',
                u'title': u'News Alerts for "squirro" in Switzerland',
                u'processed': True,
                u'paused': False,
                u'workflow': {
                    u'name': u'Default Workflow',
                    u'project_default': True,
                    u'id': u'kAvdogQOQvGHijqcIPi_WA',
                    u'project_id': u'FzbcEMMNTBeQcG2wnwnxLQ'
                }
            }
        """

        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s'
               '/sources/%(source_id)s')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}

        params = {}
        if include_config:
            params['include_config'] = include_config
        if include_run_stats:
            params['include_run_stats'] = include_run_stats

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def new_source(self, project_id, name, config, scheduling_options,
                   pipeline_workflow_id=None, source_id=None):
        """Create a new source.

        :param project_id: Project identifier.
        :param name: Name for the Source.
        :param config: dict, config including dataloader_options and
            dataloader_plugin_options for the Source.
        :param scheduling_options: dict, scheduling options for the run of a
            Source.
        :param pipeline_workflow_id: Optional id of the pipeline workflow to
            apply to the data of this Source. If not specified, then the
            default workflow of the project with `project_id` will be applied.
        :param source_id: Optional string parameter to create the
            source with the provided id. The length of the parameter must
            be 22 characters. Useful when exporting and importing projects
            across multiple Squirro servers.
        :returns: A dictionary which contains the new source.

        Example::

            >>> client.new_source(
            ...     '2sic33jZTi-ifflvQAVcfw',
            ...     {'url': 'http://blog.squirro.com/rss'})
            {u'config': {u'url': u'http://blog.squirro.com/rss'},
             u'deleted': False,
             u'id': u'oTvI6rlaRmKvmYCfCvLwpw',
             u'link': u'http://blog.squirro.com/rss',
             u'modified_at': u'2012-10-12T09:32:09',
             u'provider': u'feed',
             u'seeder': u'team',
             u'source_id': u'D3Q8AiPoTg69bIkqFhe3Bw',
             u'title': u'Squirro',
             u'processed': False,
             u'paused': False,
             u'workflow': {
                u'name': u'Default Workflow',
                u'project_default': True,
                u'id': u'kAvdogQOQvGHijqcIPi_WA',
                u'project_id': u'FzbcEMMNTBeQcG2wnwnxLQ'}
            }
        """

        headers = {'Content-Type': 'application/json'}
        url = ('%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/sources')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id}

        # build data
        data = {
            'config': config,
            'name': name,
            'squirro_token': self.refresh_token
        }
        if source_id is not None:
            data['source_id'] = source_id
        if pipeline_workflow_id is not None:
            data['pipeline_workflow_id'] = pipeline_workflow_id
        if scheduling_options is not None:
            data['scheduling_options'] = scheduling_options

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [200, 201])

    def modify_source(self, project_id, source_id, name=None, config=None,
                      scheduling_options=None, pipeline_workflow_id=None):
        """Modify an existing source.

        :param project_id: Project identifier.
        :param source_id: Source identifier.
        :param pipeline_workflow_id: Optional pipeline workflow id to change
            the source to.
        :param config: Changed config of the source.

        :returns: A dictionary which contains the source.

        Example::

            >>> client.modify_source(
            ...     '2sic33jZTi-ifflvQAVcfw',
            ...     'oTvI6rlaRmKvmYCfCvLwpw',
            ...     config={'url': 'http://blog.squirro.com/atom'})
        """

        headers = {'Content-Type': 'application/json'}
        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s/sources/%(source_id)s')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}

        # build data
        data = {}
        if name is not None:
            data['name'] = name
        if config is not None:
            data['config'] = config
        if scheduling_options is not None:
            data['scheduling_options'] = scheduling_options
        if pipeline_workflow_id is not None:
            data['pipeline_workflow_id'] = pipeline_workflow_id

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [200])

    def delete_source(self, project_id, source_id):
        """Delete an existing Source.

        :param project_id: Project identifier.
        :param source_id: Source identifier.

        Example::

            >>> client.delete_source('2sic33jZTi-ifflvQAVcfw',
            ...                      'oTvI6rlaRmKvmYCfCvLwpw')

        """

        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s'
               '/sources/%(source_id)s')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    def pause_source(self, project_id, source_id):
        """Pause a source.

        :param project_id: Project identifier.
        :param source_id: Source identifier.

        Example::

            >>> client.pause_source('2sic33jZTi-ifflvQAVcfw',
            ...                     'hw8j7LUBRM28-jAellgQdA')
        """

        url = ('%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s'
               '/sources/%(source_id)s/pause')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}

        res = self._perform_request('put', url)
        self._process_response(res, [200, 204])

    def resume_source(self, project_id, source_id):
        """Resume a paused source.

        :param project_id: Project identifier.
        :param source_id: Source identifier.

        Example::

            >>> client.resume_source(
            ...     '2sic33jZTi-ifflvQAVcfw',
            ...     'hw8j7LUBRM28-jAellgQdA')
        """

        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s'
               '/sources/%(source_id)s/resume')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}

        res = self._perform_request('put', url)
        self._process_response(res, [200, 204])

    def run_source(self, project_id, source_id):
        """Runs a source now.

        :param project_id: Project identifier.
        :param source_id: Source identifier.

        Example::

            >>> client.run_source(
            ...     '2sic33jZTi-ifflvQAVcfw',
            ...     'hw8j7LUBRM28-jAellgQdA')
        """

        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s'
               '/sources/%(source_id)s/run')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}
        res = self._perform_request('put', url)
        self._process_response(res, [200, 204])

    def reset_source(self, project_id, source_id, delete_source_data=None):
        """Resets and run the source.

        :param project_id: Project identifier.
        :param source_id: Source identifier.
        :param delete_source_data: Bool, to determine whether to delete the
            data associated with a source or not

        Example::

            >>> client.reset_source(
            ...     '2sic33jZTi-ifflvQAVcfw',
            ...     'hw8j7LUBRM28-jAellgQdA')
        """

        url = ('%(ep)s/%(version)s/%(tenant)s'
               '/projects/%(project_id)s'
               '/sources/%(source_id)s/reset')
        url = url % {
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id}
        params = {}

        if delete_source_data:
            params['delete_source_data'] = delete_source_data

        res = self._perform_request('put', url, params=params)
        self._process_response(res, [200, 204])

    def get_preview(self, project_id, config):
        """Preview the source configuration.

        :param project_id: Project identifier.
        :param config: Provider configuration.
        :returns: A dictionary which contains the source preview items.

        Example::

            >>> client.get_preview(
            ...     project_id='2sic33jZTi-ifflvQAVcfw',
            ...     config={
            ...         "dataloader_plugin_options": {
            ...         "source_file": "path:/tmp/test.csv"
            ...         },
            ...         "dataloader_options": {
            ...              "plugin_name": "csv_plugin",
            ...             "project_id": project_id,
            ...              "map_title": "title"
            ...         }
            ...     })
            {
                u'count': 2,
                u'items': [
                    {
                        u'title': u'title01',
                        u'id': u'F_UjaJvWTpeReE6qAy_Rsg',
                        u'name': u'name01'
                    },
                    {u'title':
                    u'title02',
                    u'id': u'2zPyhE3jS8CrGTFq4CH9Dg',
                    u'name': u'name02'
                    }
                ],
                u'data_schema': [u'name', u'title'],
                u'title': u'CSV load'}
        """

        url = ('%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/'
               'preview') % {
                   'ep': self.topic_api_url, 'project_id': project_id,
                   'version': self.version, 'tenant': self.tenant}

        # build params
        params = {'config': json.dumps(config)}

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)
