from unittest.mock import patch, PropertyMock

from onap_data_provider.resources.vendor_resource import VendorResource

VENDOR_RESOURCE_DATA = {"name": "testVendor"}


@patch(
    "onap_data_provider.resources.vendor_resource.VendorResource.vendor",
    new_callable=PropertyMock,
)
def test_vendor_resource_exists(mock_vendor):
    mock_vendor.return_value = None
    vendor_resource = VendorResource(VENDOR_RESOURCE_DATA)
    assert vendor_resource.exists is False
    mock_vendor.return_value = 1  # Anything but not None
    assert vendor_resource.exists is True


@patch(
    "onap_data_provider.resources.vendor_resource.Vendor.created",
)
def test_vendor_resource_vendor(mock_vendor_created):
    mock_vendor_created.return_value = False
    vendor_resource = VendorResource(VENDOR_RESOURCE_DATA)
    assert vendor_resource.vendor is None
    mock_vendor_created.return_value = True
    assert vendor_resource.vendor is not None
