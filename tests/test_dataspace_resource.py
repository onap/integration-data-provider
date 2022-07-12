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

from onapsdk.exceptions import APIError
from pytest import raises

from onap_data_provider.resources.dataspace_resource import DataspaceResource


DATASPACE_RESOURCE_DATA = {
    "name": "test-dataspace-resource",
}

DATASPACE_WITH_SCHEMASETS_DATA = {
    "name": "test-dataspace-resource",
    "schema-sets": [
        {
            "name": "test-schema-set",
            "schema-set-file": "test-schema-set-file"
        }
    ]
}

DATASPACE_WITH_ANCHORS_DATA = {
    "name": "test-dataspace-resource",
    "anchors": [
        {
            "name": "test-anchor",
            "schema-set-name": "test-schema-set"
        }
    ]
}


@patch("onap_data_provider.resources.dataspace_resource.Dataspace")
def test_dataspace_resource_create(mock_dataspace):
    dr = DataspaceResource(DATASPACE_RESOURCE_DATA)
    dr.create()
    mock_dataspace.create.assert_called_once_with("test-dataspace-resource")
    mock_dataspace.assert_not_called()

    mock_dataspace.reset_mock()
    mock_dataspace.create.side_effect = APIError("409 error")
    dr.create()
    mock_dataspace.create.assert_called_once_with("test-dataspace-resource")
    mock_dataspace.assert_called_once_with("test-dataspace-resource")

    mock_dataspace.reset_mock()
    mock_dataspace.create.side_effect = APIError("404")
    with raises(APIError):
        dr.create()

@patch("onap_data_provider.resources.dataspace_resource.Dataspace")
def test_dataspace_resource_with_schemasets(mock_dataspace):
    dr = DataspaceResource(DATASPACE_WITH_SCHEMASETS_DATA)
    dr.create()
    mock_dataspace.create.assert_called_once_with("test-dataspace-resource")
    mock_dataspace.create.return_value.get_schema_set.assert_called_once_with("test-schema-set")
    mock_dataspace.create.return_value.create_schema_set.assert_not_called()

    mock_dataspace.reset_mock()
    mock_dataspace.create.return_value.get_schema_set.side_effect = APIError("409 error")
    with patch("builtins.open") as mock_open:
        dr.create()
        mock_dataspace.create.assert_called_once_with("test-dataspace-resource")
        mock_dataspace.create.return_value.get_schema_set.assert_called_once_with("test-schema-set")
        mock_dataspace.create.return_value.create_schema_set.assert_called_once()
        mock_open.assert_called_once_with("test-schema-set-file", "rb")

@patch("onap_data_provider.resources.dataspace_resource.Dataspace")
def test_dataspace_resource_with_anchors(mock_dataspace):
    dr = DataspaceResource(DATASPACE_WITH_ANCHORS_DATA)
    dr.create()
    mock_dataspace.create.assert_called_once_with("test-dataspace-resource")
    mock_dataspace.create.return_value.get_anchor.assert_called_once_with("test-anchor")
    mock_dataspace.create.return_value.create_anchor.assert_not_called()

    mock_dataspace.reset_mock()
    mock_dataspace.create.return_value.get_anchor.side_effect = APIError("409 error")
    dr.create()
    mock_dataspace.create.assert_called_once_with("test-dataspace-resource")
    mock_dataspace.create.return_value.get_anchor.assert_called_once_with("test-anchor")
    mock_dataspace.create.return_value.get_schema_set.assert_called_once_with("test-schema-set")
    mock_dataspace.create.return_value.create_anchor.assert_called_once()
