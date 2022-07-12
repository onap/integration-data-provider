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
from unittest.mock import MagicMock, patch, PropertyMock

from onap_data_provider.resources.tenant_resource import TenantResource
from onapsdk.exceptions import ResourceNotFound


TENANT_RESOURCE_DATA = {"tenant-id": "Test ID", "tenant-name": "Test name"}


def test_tenant_resource_tenant():
    cloud_region_mock = MagicMock()
    tenant_resource = TenantResource(TENANT_RESOURCE_DATA, cloud_region_mock)
    cloud_region_mock.get_tenant.side_effect = ResourceNotFound
    assert tenant_resource.tenant is None

    cloud_region_mock.get_tenant.side_effect = None
    cloud_region_mock.get_tenant.return_value = 1
    assert tenant_resource.tenant == 1

    cloud_region_mock.reset_mock()
    assert tenant_resource.tenant == 1
    cloud_region_mock.assert_not_called()


@patch(
    "onap_data_provider.resources.tenant_resource.TenantResource.tenant",
    new_callable=PropertyMock,
)
def test_tenant_resource_exists(mock_tenant):
    mock_tenant.return_value = None
    cloud_region_mock = MagicMock()
    tenant_resource = TenantResource(TENANT_RESOURCE_DATA, cloud_region_mock)
    assert tenant_resource.exists is False

    mock_tenant.return_value = 1
    assert tenant_resource.exists is True


@patch(
    "onap_data_provider.resources.tenant_resource.TenantResource.exists",
    new_callable=PropertyMock,
)
def test_tenant_resource_create(mock_exists):

    cloud_region_mock = MagicMock()
    tenant_resource = TenantResource(TENANT_RESOURCE_DATA, cloud_region_mock)

    mock_exists.return_value = True
    tenant_resource.create()
    cloud_region_mock.add_tenant.assert_not_called()

    mock_exists.return_value = False
    tenant_resource.create()
    cloud_region_mock.add_tenant.assert_called_once_with(
        tenant_id="Test ID", tenant_name="Test name", tenant_context=None
    )
