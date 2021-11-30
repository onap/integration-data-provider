from unittest.mock import MagicMock, patch, PropertyMock

from onap_data_provider.resources.customer_resource import CustomerResource

from onapsdk.exceptions import ResourceNotFound

CUSTOMER_DATA = {
    "global-customer-id": "test_id",
    "subscriber-name": "test_name",
    "subscriber-type": "Customer",
    "service-subscriptions": [{"service-type": "test_voip"}],
}

SERVICE_SUBSCRIPTION_WITH_TENANTS_DATA = {
    "service-type": "test-service-subscription",
    "tenants": [
        {
            "tenant-id": "1234",
            "cloud-owner": "test-cloud-owner",
            "cloud-region-id": "test-cloud-region",
        }
    ],
}


@patch(
    "onap_data_provider.resources.customer_resource.Customer.get_by_global_customer_id"
)
def test_customer_resource_customer(mock_customer_get_by_global_customer_id):
    mock_customer_get_by_global_customer_id.side_effect = ResourceNotFound
    customer_resource = CustomerResource(CUSTOMER_DATA)
    assert customer_resource.customer is None
    mock_customer_get_by_global_customer_id.side_effect = None
    mock_customer_get_by_global_customer_id.return_value = 1
    assert customer_resource.customer == 1


@patch(
    "onap_data_provider.resources.customer_resource.CustomerResource.customer",
    new_callable=PropertyMock,
)
def test_customer_exists(mock_customer):
    mock_customer.return_value = None
    customer_resource = CustomerResource(CUSTOMER_DATA)
    assert customer_resource.exists is False
    mock_customer.return_value = 1  # Anything but not None
    assert customer_resource.exists is True


@patch(
    "onap_data_provider.resources.customer_resource.CustomerResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.customer_resource.Customer.create")
def test_customer_create(mock_customer_create, mock_exists):
    customer_resource = CustomerResource(CUSTOMER_DATA)
    assert customer_resource.data == CUSTOMER_DATA
    mock_exists.return_value = False
    customer_resource.create()
    assert mock_customer_create.called_once_with(
        global_customer_id="test_id",
        subscriber_name="test_name",
        subscriber_type="Customer",
    )


@patch(
    "onap_data_provider.resources.customer_resource.CustomerResource.ServiceSubscriptionResource.service_subscription",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.customer_resource.CloudRegion")
def test_service_subscription_with_tenants(
    mock_cloud_region, _
):
    cloud_region_mock = MagicMock()
    mock_cloud_region.get_by_id.return_value = cloud_region_mock
    service_subscription_resource = CustomerResource.ServiceSubscriptionResource(
        SERVICE_SUBSCRIPTION_WITH_TENANTS_DATA, MagicMock()
    )
    service_subscription_resource.create()
    mock_cloud_region.get_by_id.assert_called_once_with(
        "test-cloud-owner", "test-cloud-region"
    )
    cloud_region_mock.get_tenant.assert_called_once_with("1234")
