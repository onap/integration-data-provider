from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.pnf_resource import PnfResource

PNF_RESOURCE_DATA = {"name": "test_pnf"}


@patch(
    "onap_data_provider.resources.pnf_resource.PnfResource.pnf",
    new_callable=PropertyMock,
)
def test_pnf_resource_exists(mock_pnf):
    mock_pnf.return_value = None
    pnf_resource = PnfResource(PNF_RESOURCE_DATA)
    assert pnf_resource.exists is False
    mock_pnf.return_value = 1  # Anything but not None
    assert pnf_resource.exists is True


@patch(
    "onap_data_provider.resources.pnf_resource.Pnf.created",
)
def test_pnf_resource_pnf(mock_pnf_created):
    mock_pnf_created.return_value = False
    pnf_resource = PnfResource(PNF_RESOURCE_DATA)
    assert pnf_resource.pnf is None
    mock_pnf_created.return_value = True
    assert pnf_resource.pnf is not None
