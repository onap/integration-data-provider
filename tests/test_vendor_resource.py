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
