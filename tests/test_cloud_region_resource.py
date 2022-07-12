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
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

from onapsdk.aai.cloud_infrastructure.complex import Complex

from onap_data_provider.resources.cloud_region_resource import (
    CloudRegion,
    CloudRegionResource,
)
from onapsdk.exceptions import ResourceNotFound

CLOUD_REGION_DATA = {
    "cloud-owner": "test",
    "cloud-region-id": "test",
    "orchestration-disabled": True,
    "in-maint": False,
}

CLOUD_REGION_K8S_TYPE = {
    "cloud-region-id": "k8s-test",
    "cloud-owner": "k8s-test",
    "orchestration-disabled": True,
    "in-maint": False,
    "cloud-type": "k8s",
    "kube-config": Path(Path(__file__).parent, "test-kube-config"),
}


@patch("onap_data_provider.resources.cloud_region_resource.CloudRegion.get_by_id")
def test_cloud_region_resource_cloud_region(mock_cloud_region_get_by_id):
    mock_cloud_region_get_by_id.side_effect = ResourceNotFound
    cloud_region_resource = CloudRegionResource(CLOUD_REGION_DATA)
    assert cloud_region_resource.cloud_region is None

    mock_cloud_region_get_by_id.side_effect = None
    mock_cloud_region_get_by_id.return_value = 1
    assert cloud_region_resource.cloud_region == 1


@patch(
    "onap_data_provider.resources.cloud_region_resource.CloudRegionResource.cloud_region",
    new_callable=PropertyMock,
)
def test_cloud_region_resource_exists(mock_cloud_region):
    mock_cloud_region.return_value = None
    cloud_region_resource = CloudRegionResource(CLOUD_REGION_DATA)
    assert cloud_region_resource.exists is False
    mock_cloud_region.return_value = 1  # Anything but not None
    assert cloud_region_resource.exists is True


@patch(
    "onap_data_provider.resources.cloud_region_resource.CloudRegionResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.cloud_region_resource.CloudRegion.create")
def test_cloud_region_create(mock_cloud_region_create, mock_exists):

    cloud_region_resource = CloudRegionResource(CLOUD_REGION_DATA)
    assert cloud_region_resource.data == CLOUD_REGION_DATA

    mock_exists.return_value = False
    cloud_region_resource.create()
    assert mock_cloud_region_create.called_once_with(
        cloud_owner="test",
        cloud_region_id="test",
        orchestration_disabled=True,
        in_maint=False,
    )

    mock_exists.reset_mock()
    mock_cloud_region_create.reset_mock()

    mock_exists.return_value = True
    cloud_region_resource.create()
    mock_cloud_region_create.assert_not_called()


@patch(
    "onap_data_provider.resources.cloud_region_resource.CloudRegionResource.cloud_region",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.cloud_region_resource.Complex.get_by_physical_location_id")
def test_cloud_region_resource_link_to_complex(
    mock_complex_get_by_physical_location_id, mock_cloud_region_property
):
    mock_cloud_region_property.return_value.complex = MagicMock()
    cloud_region_resource = CloudRegionResource(CLOUD_REGION_DATA)
    cloud_region_resource._link_to_complex("test")
    mock_complex_get_by_physical_location_id.assert_not_called()

    mock_cloud_region_property.return_value.complex = None
    mock_complex_get_by_physical_location_id.side_effect = ResourceNotFound
    cloud_region_resource._link_to_complex("test")
    mock_cloud_region_property.return_value.link_to_complex.assert_not_called()

    mock_complex_get_by_physical_location_id.side_effect = None
    mock_complex_get_by_physical_location_id.return_value = Complex("test")
    cloud_region_resource._link_to_complex("test")
    mock_cloud_region_property.return_value.link_to_complex.assert_called_once()


@patch(
    "onap_data_provider.resources.cloud_region_resource.CloudRegionResource.cloud_region",
    new_callable=PropertyMock,
)
def test_cloud_region_resource_create_availability_zones(mock_cloud_region_property):
    cloud_region_resource = CloudRegionResource(CLOUD_REGION_DATA)
    cloud_region_resource.data["availability-zones"] = [
        {"availability-zone-name": "testzone1", "hypervisor-type": "OpenStackTest"}
    ]
    cloud_region_resource.create()
    mock_cloud_region_property.return_value.add_availability_zone.assert_called_once()


@patch(
    "onap_data_provider.resources.cloud_region_resource.CloudRegionResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.cloud_region_resource.ConnectivityInfo")
@patch("onap_data_provider.resources.cloud_region_resource.CloudRegion.create")
@patch("onap_data_provider.resources.cloud_region_resource.CloudRegion.complex")
@patch("onap_data_provider.resources.cloud_region_resource.SoDbAdapter.add_cloud_site")
def test_cloud_region_k8s_type(
    mock_add_cloud_site,
    _,
    mock_cloud_region_create,
    mock_connectivity_info,
    mock_exists,
):
    mock_exists.return_value = False
    mock_cloud_region_create.return_value = CloudRegion(
        cloud_owner=CLOUD_REGION_K8S_TYPE["cloud-owner"],
        cloud_region_id=CLOUD_REGION_K8S_TYPE["cloud-region-id"],
        orchestration_disabled=CLOUD_REGION_K8S_TYPE["orchestration-disabled"],
        in_maint=CLOUD_REGION_K8S_TYPE["in-maint"],
        cloud_type=CLOUD_REGION_K8S_TYPE["cloud-type"],
    )
    cloud_region_resource = CloudRegionResource(CLOUD_REGION_K8S_TYPE)
    cloud_region_resource.create()
    mock_connectivity_info.get_connectivity_info_by_region_id.assert_called_once_with(
        CLOUD_REGION_K8S_TYPE["cloud-region-id"]
    )
    mock_add_cloud_site.assert_called_once()

    mock_connectivity_info.get_connectivity_info_by_region_id.side_effect = (
        ResourceNotFound
    )
    cloud_region_resource.create()
    mock_connectivity_info.create.assert_called_once()
