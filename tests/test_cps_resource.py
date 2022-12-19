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
from unittest.mock import MagicMock, NonCallableMagicMock, patch, PropertyMock
from onapsdk.exceptions import APIError, ResourceNotFound
from pytest import raises
from onap_data_provider.resources.cps_resource import AnchorNodeResource, AnchorResource, DataspaceResource, SchemaSetResource


DATASPACE_RESOURCE_DATA = {
    "dataspace-name": "test-dataspace-resource",
}

DATASPACE_WITH_SCHEMASETS_DATA = {
    "dataspace-name": "test-dataspace-resource",
    "schema-sets": [
        {
            "schema-set-name": "test-schema-set",
            "schema-set-file": "test-schema-set-file"
        }
    ]
}

DATASPACE_WITH_ANCHORS_DATA = {
    "dataspace-name": "test-dataspace-resource",
    "anchors": [
        {
            "anchor-name": "test-anchor",
            "schema-set-name": "test-schema-set",
            "anchor-node-name": "test-anchor-node"
        }
    ]
}

SCHEMA_SET_DATA = {
    "schema-set-name": "test-schema-set",
    "dataspace-name": "test-dataspace",
    "schema-set-file": "test-schema-set-file"
}

ANCHOR_DATA = {
    "anchor-name": "test-anchor",
    "dataspace-name": "test-dataspace",
    "schema-set-name": "test-schema-set",
    "anchor-node-name": "test-anchor-node"
}


@patch("onap_data_provider.resources.cps_resource.Dataspace")
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

@patch("onap_data_provider.resources.cps_resource.Dataspace")
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

@patch("onap_data_provider.resources.cps_resource.Dataspace")
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

@patch("onap_data_provider.resources.cps_resource.SchemaSetResource.dataspace", new_callable=PropertyMock)
def test_schema_set_schema_set_property(mock_dataspace_property):
    ssr = SchemaSetResource(SCHEMA_SET_DATA)

    mock_dataspace_property.return_value.get_schema_set.side_effect = APIError("Dataspace not found")
    with raises(ValueError):
        ssr.schema_set

    mock_dataspace_property.return_value.get_schema_set.side_effect = APIError("Schema Set not found")
    assert ssr.schema_set is None

    mock_dataspace_property.return_value.get_schema_set.side_effect = None
    assert ssr.schema_set is not None

@patch("onap_data_provider.resources.cps_resource.SchemaSetResource.schema_set", new_callable=PropertyMock)
@patch("onap_data_provider.resources.cps_resource.SchemaSetResource.dataspace", new_callable=PropertyMock)
def test_schema_set_resource(mock_dataspace_property, mock_schema_set_property):
    ssr = SchemaSetResource(SCHEMA_SET_DATA)

    mock_schema_set_property.side_effect = ValueError
    with raises(ValueError):
        ssr.create()

    mock_schema_set_property.side_effect = None

    with patch("builtins.open"):
        ssr.create()
        mock_dataspace_property.return_value.create_schema_set.assert_not_called()

    mock_schema_set_property.return_value = None
    with patch("builtins.open"):
        ssr.create()
        mock_dataspace_property.return_value.create_schema_set.assert_called_once()

@patch("onap_data_provider.resources.cps_resource.AnchorResource.schema_set", new_callable=PropertyMock)
@patch("onap_data_provider.resources.cps_resource.AnchorResource.dataspace", new_callable=PropertyMock)
def test_anchor_resource(mock_dataspace_property, mock_schema_set_property):
    ar = AnchorResource(ANCHOR_DATA)

    mock_schema_set_property.side_effect = ValueError
    with raises(ValueError):
        ar.create()

    mock_schema_set_property.side_effect = None
    mock_schema_set_property.return_value = None
    with raises(ValueError):
        ar.create()

    mock_schema_set_property.side_effect = None
    mock_schema_set_property.return_value = MagicMock()
    ar.create()
    mock_dataspace_property.return_value.get_anchor.assert_called_once_with("test-anchor")
    mock_dataspace_property.return_value.create_anchor.assert_not_called()

@patch('builtins.input', return_value='/path/to/something')
@patch("onap_data_provider.resources.cps_resource.AnchorNodeResource.dataspace", new_callable=PropertyMock)
def test_anchor_node_resource(mock_dataspace_property, mock_schema_set_property):
    ar = AnchorNodeResource(ANCHOR_DATA)

    mock_schema_set_property.side_effect = ValueError
    with raises(ValueError):
        ar.create()

    mock_schema_set_property.side_effect = OSError
    with raises(OSError):
        ar.create()

    mock_schema_set_property.side_effect = None
    mock_schema_set_property.return_value = MagicMock()
    ar.create()
    mock_dataspace_property.return_value.create_node.assert_not_called()