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
