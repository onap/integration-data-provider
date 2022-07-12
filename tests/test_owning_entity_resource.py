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
from unittest import mock

from onap_data_provider.resources.owning_entity_resource import (
    OwningEntityResource,
    ResourceNotFound,
)


OWNING_ENTITY = {"name": "test-name"}


@mock.patch(
    "onap_data_provider.resources.owning_entity_resource.OwningEntity.get_by_owning_entity_name"
)
def test_owning_entity_resource_owning_entity_property(mock_get_by_name):

    owning_entity = OwningEntityResource(OWNING_ENTITY)
    mock_get_by_name.side_effect = ResourceNotFound
    assert owning_entity.owning_entity is None

    mock_get_by_name.side_effect = None
    assert owning_entity.owning_entity is not None


@mock.patch(
    "onap_data_provider.resources.owning_entity_resource.OwningEntityResource.owning_entity",
    new_callable=mock.PropertyMock,
)
def test_owning_entity_resource_exists(mock_owning_entity):

    owning_entity = OwningEntityResource(OWNING_ENTITY)
    assert owning_entity.exists is True
    mock_owning_entity.return_value = None
    assert owning_entity.exists is False


@mock.patch(
    "onap_data_provider.resources.owning_entity_resource.OwningEntityResource.exists",
    new_callable=mock.PropertyMock,
)
@mock.patch(
    "onap_data_provider.resources.owning_entity_resource.OwningEntity.send_message"
)
def test_owning_entity_create(mock_send_message, mock_exists):
    mock_exists.return_value = True
    owning_entity = OwningEntityResource(OWNING_ENTITY)
    owning_entity.create()
    mock_send_message.assert_not_called()
    mock_exists.return_value = False
    owning_entity.create()
    mock_send_message.assert_called()
