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

from onap_data_provider.resources.line_of_business_resource import (
    LineOfBusinessResource,
    ResourceNotFound,
)


LINE_OF_BUSINESS = {"name": "test-name"}


@mock.patch(
    "onap_data_provider.resources.line_of_business_resource.LineOfBusiness.get_by_name"
)
def test_line_of_business_resource_line_of_business_property(mock_get_by_name):

    lob = LineOfBusinessResource(LINE_OF_BUSINESS)
    mock_get_by_name.side_effect = ResourceNotFound
    assert lob.line_of_business is None

    mock_get_by_name.side_effect = None
    assert lob.line_of_business is not None


@mock.patch(
    "onap_data_provider.resources.line_of_business_resource.LineOfBusinessResource.line_of_business",
    new_callable=mock.PropertyMock,
)
def test_line_of_business_resource_exists(mock_line_of_business):

    lob = LineOfBusinessResource(LINE_OF_BUSINESS)
    assert lob.exists is True
    mock_line_of_business.return_value = None
    assert lob.exists is False


@mock.patch(
    "onap_data_provider.resources.line_of_business_resource.LineOfBusinessResource.exists",
    new_callable=mock.PropertyMock,
)
@mock.patch(
    "onap_data_provider.resources.line_of_business_resource.LineOfBusiness.send_message"
)
def test_line_of_business_create(mock_send_message, mock_exists):
    mock_exists.return_value = True
    lob = LineOfBusinessResource(LINE_OF_BUSINESS)
    lob.create()
    mock_send_message.assert_not_called()
    mock_exists.return_value = False
    lob.create()
    mock_send_message.assert_called()
