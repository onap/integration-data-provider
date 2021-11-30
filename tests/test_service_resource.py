from collections import namedtuple
from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.service_resource import ServiceResource


SERVICE_RESOURCE_DATA = {
    "name": "test",
}


@patch("onap_data_provider.resources.service_resource.Service.created")
def test_service_resource_service_property(mock_service_created):
    service_resource = ServiceResource(SERVICE_RESOURCE_DATA)
    mock_service_created.return_value = False
    assert service_resource.service is None

    mock_service_created.return_value = True
    assert service_resource.service is not None


@patch(
    "onap_data_provider.resources.service_resource.ServiceResource.service",
    new_callable=PropertyMock,
)
def test_service_resource_exists(mock_service_resource_service):
    service_resource = ServiceResource(SERVICE_RESOURCE_DATA)
    mock_service_resource_service.return_value = None
    assert service_resource.exists is False
    ServiceNamedtuple = namedtuple(
        "ServiceNamedtuple", ["distributed"], defaults=[True]
    )
    mock_service_resource_service.return_value = ServiceNamedtuple()
    assert service_resource.exists is True


@patch(
    "onap_data_provider.resources.service_resource.ServiceResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.service_resource.Service")
def test_service_resource_create(mock_service, mock_service_resource_exists):
    service_resource = ServiceResource(SERVICE_RESOURCE_DATA)
    mock_service_resource_exists.return_value = True
    service_resource.create()
    mock_service.assert_not_called()

    mock_service_resource_exists.return_value = False
    service_resource.create()
    mock_service.assert_called_once()
