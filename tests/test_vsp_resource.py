from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.vsp_resource import VspResource


VSP_RESOURCE_DATA = {"name": "test", "vendor": "test", "package": "test"}


@patch("onap_data_provider.resources.vsp_resource.Vsp.created")
def test_vsp_resource_vsp_property(mock_vsp_created):
    vsp_resource = VspResource(VSP_RESOURCE_DATA)
    mock_vsp_created.return_value = False
    assert vsp_resource.vsp is None

    mock_vsp_created.return_value = True
    assert vsp_resource.vsp is not None


@patch(
    "onap_data_provider.resources.vsp_resource.VspResource.vsp",
    new_callable=PropertyMock,
)
def test_vsp_resource_exists(mock_vsp):
    mock_vsp.return_value = None
    vsp_resource = VspResource(VSP_RESOURCE_DATA)
    assert not vsp_resource.exists
    mock_vsp.return_value = 1
    assert vsp_resource.exists
