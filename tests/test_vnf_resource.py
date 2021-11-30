from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.vnf_resource import VnfResource

VNF_RESOURCE_DATA = {"name": "test_vnf"}


@patch(
    "onap_data_provider.resources.vnf_resource.VnfResource.vnf",
    new_callable=PropertyMock,
)
def test_vnf_resource_exists(mock_vnf):
    mock_vnf.return_value = None
    vnf_resource = VnfResource(VNF_RESOURCE_DATA)
    assert vnf_resource.exists is False
    mock_vnf.return_value = 1  # Anything but not None
    assert vnf_resource.exists is True


@patch(
    "onap_data_provider.resources.vnf_resource.Vf.created",
)
def test_vnf_resource_vnf(mock_vnf_created):
    mock_vnf_created.return_value = False
    vnf_resource = VnfResource(VNF_RESOURCE_DATA)
    assert vnf_resource.vnf is None
    mock_vnf_created.return_value = True
    assert vnf_resource.vnf is not None
