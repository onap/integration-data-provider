from unittest.mock import patch, PropertyMock
from onap_data_provider.tag_handlers import join, generate_random_uuid


def test_generate_random_uuid():
    uuid1 = generate_random_uuid(None, None)
    uuid2 = generate_random_uuid(None, None)
    assert isinstance(uuid1, str)
    assert uuid1 != uuid2


@patch("yaml.SafeLoader", new_callable=PropertyMock)
def test_join(mock_safe_loader):
    mock_safe_loader.construct_sequence.return_value = ["-", ["cloud", "owner", "DC1"]]
    assert join(mock_safe_loader, None) == "cloud-owner-DC1"
