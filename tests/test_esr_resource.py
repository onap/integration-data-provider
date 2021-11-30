from collections import namedtuple
from unittest.mock import MagicMock, patch, PropertyMock

from onap_data_provider.resources.esr_system_info_resource import (
    CloudRegion,
    EsrSystemInfoResource,
)


ESR_RESOURCE_DATA = {
    "esr-system-info-id": "Test ID",
    "user-name": "Test name",
    "password": "testpass",
    "system-type": "test type",
    "service-url": "test url",
    "cloud-domain": "test cloud domain",
}


EsrSystemInfoNamedtuple = namedtuple("EsrSystemInfo", ["esr_system_info_id"])


@patch(
    "onap_data_provider.resources.esr_system_info_resource.CloudRegion.esr_system_infos",
    new_callable=PropertyMock,
)
def test_esr_system_info_resource_esr_system_info(mock_cloud_region_esr_system_infos):
    cloud_region = CloudRegion(
        cloud_owner="test",
        cloud_region_id="test",
        orchestration_disabled=True,
        in_maint=True,
    )
    esr_resource = EsrSystemInfoResource(ESR_RESOURCE_DATA, cloud_region)
    mock_cloud_region_esr_system_infos.return_value = iter([])
    assert esr_resource.esr_system_info is None

    mock_cloud_region_esr_system_infos.return_value = iter(
        [EsrSystemInfoNamedtuple("Test ID")]
    )
    assert esr_resource.esr_system_info is not None


@patch(
    "onap_data_provider.resources.esr_system_info_resource.EsrSystemInfoResource.esr_system_info",
    new_callable=PropertyMock,
)
def test_esr_system_info_resource_exists(mock_esr_system_info):
    mock_esr_system_info.return_value = None
    cloud_region_mock = MagicMock()
    esr_resource = EsrSystemInfoResource(ESR_RESOURCE_DATA, cloud_region_mock)
    assert esr_resource.exists is False

    mock_esr_system_info.return_value = 1
    assert esr_resource.exists is True


@patch(
    "onap_data_provider.resources.esr_system_info_resource.EsrSystemInfoResource.exists",
    new_callable=PropertyMock,
)
def test_esr_system_info_resource_create(mock_exists):

    cloud_region_mock = MagicMock()
    esr_resource = EsrSystemInfoResource(ESR_RESOURCE_DATA, cloud_region_mock)

    mock_exists.return_value = True
    esr_resource.create()
    cloud_region_mock.add_esr_system_info.assert_not_called()

    mock_exists.return_value = False
    esr_resource.create()
    cloud_region_mock.add_esr_system_info.assert_called_once_with(
        esr_system_info_id="Test ID",
        user_name="Test name",
        password="testpass",
        system_type="test type",
        system_status="active",
        service_url="test url",
        cloud_domain="test cloud domain",
        default_tenant=None,
    )
