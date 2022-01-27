from unittest.mock import patch, PropertyMock

from onapsdk.cds import DataDictionarySet
from onap_data_provider.resources.data_dictionary_resource import (
    DataDictionarySetResource,
)


@patch(
    "onap_data_provider.resources.data_dictionary_resource.DataDictionarySet.load_from_file"
)
def test_data_dictionary_resource_data_dictionary_set(
    mock_data_dictionary_set_load_from_file,
):
    dds = DataDictionarySetResource({"json-file-path": "test/file.json"})
    mock_data_dictionary_set_load_from_file.return_value = 1
    assert dds.data_dictionaries is not None


@patch(
    "onap_data_provider.resources.data_dictionary_resource.DataDictionarySetResource.data_dictionaries",
    new_callable=PropertyMock,
)
def test_data_dictionary_resource_data_dictionary_set_exists(mock_data_dictionaries):
    dd = DataDictionarySetResource({"file-path": "test/file.json"})
    mock_data_dictionaries.return_value = 1
    assert dd.exists is True
    mock_data_dictionaries.return_value = None
    assert dd.exists is False


@patch("onap_data_provider.resources.data_dictionary_resource.DataDictionarySet.upload")
@patch(
    "onap_data_provider.resources.data_dictionary_resource.DataDictionarySet.load_from_file"
)
def test_data_dictionary_resource_data_dictionary_set_create(
    mock_load_from_file, mock_data_dictionary_set_upload
):
    dd = DataDictionarySetResource({"file-path": "test/file.json"})
    mock_load_from_file.return_value = None
    dd.create()
    mock_data_dictionary_set_upload.assert_not_called()
    mock_load_from_file.return_value = DataDictionarySet()
    dd.create()
    mock_data_dictionary_set_upload.assert_called()
