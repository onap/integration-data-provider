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

from onap_data_provider.resources.platform_resource import (
    PlatformResource,
    ResourceNotFound,
)


PLATFORM = {"name": "test-name"}


@mock.patch("onap_data_provider.resources.platform_resource.Platform.get_by_name")
def test_platform_resource_platform_property(mock_get_by_name):

    platform = PlatformResource(PLATFORM)
    mock_get_by_name.side_effect = ResourceNotFound
    assert platform.platform is None

    mock_get_by_name.side_effect = None
    assert platform.platform is not None


@mock.patch(
    "onap_data_provider.resources.platform_resource.PlatformResource.platform",
    new_callable=mock.PropertyMock,
)
def test_platform_resource_exists(mock_platform):

    platform = PlatformResource(PLATFORM)
    assert platform.exists is True
    mock_platform.return_value = None
    assert platform.exists is False


@mock.patch(
    "onap_data_provider.resources.platform_resource.PlatformResource.exists",
    new_callable=mock.PropertyMock,
)
@mock.patch("onap_data_provider.resources.platform_resource.Platform.send_message")
def test_platform_create(mock_send_message, mock_exists):
    mock_exists.return_value = True
    platform = PlatformResource(PLATFORM)
    platform.create()
    mock_send_message.assert_not_called()
    mock_exists.return_value = False
    platform.create()
    mock_send_message.assert_called()
