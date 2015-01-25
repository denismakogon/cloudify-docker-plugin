########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

# Built-in Imports
import testtools
import os

# Third Party Imports
from docker import Client
from docker import errors

# Cloudify Imports is imported and used in operations
from docker_plugin import tasks
from cloudify.mocks import MockCloudifyContext
from cloudify.exceptions import NonRecoverableError


class TestImportImage(testtools.TestCase):

    def get_client(self, daemon_client):
        try:
            return Client(**daemon_client)
        except errors.DockerException as e:
            raise NonRecoverableError('Error while getting client: '
                                      '{0}.'.format(str(e)))

    def mock_ctx(self, test_name):
        """ Creates a mock context for the instance
            tests
        """
        source_file = os.path.join(os.path.dirname(__file__),
                                   'resources', 'example.tar')

        test_node_id = test_name
        test_properties = {
            'resource_id': 'example-repo',
            'use_external_resource': False,
            'src': source_file,
            'params': {
                'repository': '{}{}'.format('test/', test_name)
            }
        }

        ctx = MockCloudifyContext(
            node_id=test_node_id,
            properties=test_properties
        )

        return ctx

    def test_import_image_clean(self):
        """ This test builds a docker image from
            the docker hub and deletes it.
        """

        ctx = self.mock_ctx('test_import_image_clean')
        daemon_client = {}
        client = self.get_client(daemon_client)

        tasks.import_image(ctx=ctx)
        image_id = ctx.instance.runtime_properties['image_id']
        if client.images(name=image_id) is not None:
            test_passed = True
            client.remove_image(image_id)
        self.assertEqual(test_passed, True)
