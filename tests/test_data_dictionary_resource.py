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
from unittest.mock import patch

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
