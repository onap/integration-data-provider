"""
   Copyright 2022 Deutsche Telekom AG

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from unittest import mock

from onap_data_provider.resources.project_resource import (
    ProjectResource,
    ResourceNotFound,
)


PROJECT = {"name": "test-name"}


@mock.patch("onap_data_provider.resources.project_resource.Project.get_by_name")
def test_project_resource_project_property(mock_get_by_name):

    project = ProjectResource(PROJECT)
    mock_get_by_name.side_effect = ResourceNotFound
    assert project.project is None

    mock_get_by_name.side_effect = None
    assert project.project is not None


@mock.patch(
    "onap_data_provider.resources.project_resource.ProjectResource.project",
    new_callable=mock.PropertyMock,
)
def test_project_resource_exists(mock_project):

    project = ProjectResource(PROJECT)
    assert project.exists is True
    mock_project.return_value = None
    assert project.exists is False


@mock.patch(
    "onap_data_provider.resources.project_resource.ProjectResource.exists",
    new_callable=mock.PropertyMock,
)
@mock.patch("onap_data_provider.resources.project_resource.Project.send_message")
def test_project_create(mock_send_message, mock_exists):
    mock_exists.return_value = True
    project = ProjectResource(PROJECT)
    project.create()
    mock_send_message.assert_not_called()
    mock_exists.return_value = False
    project.create()
    mock_send_message.assert_called()
