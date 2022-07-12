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
from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.aai_service_resource import AaiService, AaiServiceResource, ResourceNotFound


AAI_SERVICE_DATA = {
    "service-id": "123",
    "service-description": "123"
}


@patch("onap_data_provider.resources.aai_service_resource.AaiService.get_all")
def test_aai_service_resource_aai_resource(mock_aai_service_get_all):
    mock_aai_service_get_all.side_effect = ResourceNotFound
    mock_aai_service_get_all.return_value = iter([])
    aai_service_resource = AaiServiceResource(AAI_SERVICE_DATA)
    assert aai_service_resource.aai_service is None
    mock_aai_service_get_all.side_effect = None
    mock_aai_service_get_all.return_value = iter([AaiService(service_id="123", service_description="123", resource_version="123")])
    assert aai_service_resource.aai_service is not None


@patch(
    "onap_data_provider.resources.aai_service_resource.AaiServiceResource.aai_service",
    new_callable=PropertyMock,
)
def test_aai_service_resource_exists(mock_aai_service):
    mock_aai_service.return_value = None
    aai_service_resource = AaiServiceResource(AAI_SERVICE_DATA)
    assert aai_service_resource.exists is False
    mock_aai_service.return_value = 1  # Anything but not None
    assert aai_service_resource.exists is True


@patch(
    "onap_data_provider.resources.aai_service_resource.AaiServiceResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.aai_service_resource.AaiService.create")
def test_aai_service_resource_create(mock_aai_service_create, mock_exists):
    mock_exists.return_value = True
    aai_service_resource = AaiServiceResource(AAI_SERVICE_DATA)
    aai_service_resource.create()
    mock_aai_service_create.assert_not_called()

    mock_exists.return_value = False
    aai_service_resource.create()
    mock_aai_service_create.assert_called_once_with(
        service_id="123",
        service_description="123"
    )
