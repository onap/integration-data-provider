from unittest.mock import patch, PropertyMock

import pytest

from onap_data_provider.tag_handlers import join, generate_random_uuid, resource_property


def test_generate_random_uuid():
    uuid1 = generate_random_uuid(None, None)
    uuid2 = generate_random_uuid(None, None)
    assert isinstance(uuid1, str)
    assert uuid1 != uuid2


@patch("yaml.SafeLoader", new_callable=PropertyMock)
def test_join(mock_safe_loader):
    mock_safe_loader.construct_sequence.return_value = ["-", ["cloud", "owner", "DC1"]]
    assert join(mock_safe_loader, None) == "cloud-owner-DC1"


@patch("yaml.SafeLoader", new_callable=PropertyMock)
@patch("onap_data_provider.property_tag.sdc_service.Service")
def test_resource_property(mock_service, mock_safe_loader):
    mock_safe_loader.construct_scalar.return_value = "unknown"
    with pytest.raises(ValueError, match="Resource type \"unknown\" is not supported"):
        resource_property(mock_safe_loader, None)
    mock_service.return_value.identifier = "123"
    mock_safe_loader.construct_scalar.return_value = "service identifier test_name"
    assert resource_property(mock_safe_loader, None) == "123"
