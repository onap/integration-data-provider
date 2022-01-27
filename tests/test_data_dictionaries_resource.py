from unittest.mock import patch, PropertyMock

from onapsdk.cds import DataDictionarySet
from onapsdk.exceptions import FileError
from onap_data_provider.resources.data_dictionary_resource import (
    DataDictionarySetResource,
)


@patch(
    "onap_data_provider.resources.data_dictionary_resource.DataDictionarySet.load_from_file"
)
def test_data_dictionary_resource_data_dictionary_set(
    mock_data_dictionary_set_load_from_file,
):
    dds = DataDictionarySetResource({"json-file-path": "test"})
    mock_data_dictionary_set_load_from_file.return_value = 1
    assert dds.data_dictionaries is not None


@patch("onap_data_provider.resources.data_dictionary_resource.DataDictionarySet.upload")
@patch(
    "onap_data_provider.resources.data_dictionary_resource.DataDictionarySet.load_from_file"
)
def test_data_dictionary_resource_data_dictionary_set_create(
    mock_load_from_file, mock_data_dictionary_set_upload
):
    ddsr = DataDictionarySetResource({"file-path": "test"})
    mock_load_from_file.side_effect = FileError
    mock_data_dictionary_set_upload.assert_not_called()
    mock_load_from_file.side_effect = None
    mock_load_from_file.return_value = DataDictionarySet()
    ddsr.create()
    mock_data_dictionary_set_upload.assert_called()
