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
from collections import namedtuple
from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.service_resource import ServiceResource


SERVICE_RESOURCE_DATA = {
    "name": "test",
    "inputs": [
        {"name": "itest", "type": "string", "value": "itest"},
        {"name": "itest1", "type": "boolean"},
    ],
    "properties": [
        {"name": "test", "type": "string", "value": "test"},
        {"name": "test1", "type": "boolean"},
    ],
}


@patch("onap_data_provider.resources.service_resource.Service.created")
def test_service_resource_service_property(mock_service_created):
    service_resource = ServiceResource(SERVICE_RESOURCE_DATA)
    mock_service_created.return_value = False
    assert service_resource.service is None

    mock_service_created.return_value = True
    assert service_resource.service is not None


@patch(
    "onap_data_provider.resources.service_resource.ServiceResource.service",
    new_callable=PropertyMock,
)
def test_service_resource_exists(mock_service_resource_service):
    service_resource = ServiceResource(SERVICE_RESOURCE_DATA)
    mock_service_resource_service.return_value = None
    assert service_resource.exists is False
    ServiceNamedtuple = namedtuple(
        "ServiceNamedtuple", ["distributed"], defaults=[True]
    )
    mock_service_resource_service.return_value = ServiceNamedtuple()
    assert service_resource.exists is True


@patch(
    "onap_data_provider.resources.service_resource.ServiceResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.service_resource.Service")
def test_service_resource_create(mock_service, mock_service_resource_exists):
    service_resource = ServiceResource(SERVICE_RESOURCE_DATA)
    mock_service_resource_exists.return_value = True
    service_resource.create()
    mock_service.assert_not_called()

    mock_service_resource_exists.return_value = False
    service_resource.create()
    mock_service.assert_called_once()
