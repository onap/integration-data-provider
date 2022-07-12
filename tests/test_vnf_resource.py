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
from unittest.mock import MagicMock, patch, PropertyMock

from onap_data_provider.resources.vnf_resource import VnfResource

VNF_RESOURCE_DATA = {"name": "test_vnf"}


@patch(
    "onap_data_provider.resources.vnf_resource.VnfResource.vnf",
    new_callable=PropertyMock,
)
def test_vnf_resource_exists(mock_vnf):
    mock_vnf.return_value = None
    vnf_resource = VnfResource(VNF_RESOURCE_DATA)
    assert vnf_resource.exists is False
    mock_vnf.return_value = 1  # Anything but not None
    assert vnf_resource.exists is True


@patch(
    "onap_data_provider.resources.vnf_resource.Vf.created",
)
def test_vnf_resource_vnf(mock_vnf_created):
    mock_vnf_created.return_value = False
    vnf_resource = VnfResource(VNF_RESOURCE_DATA)
    assert vnf_resource.vnf is None
    mock_vnf_created.return_value = True
    assert vnf_resource.vnf is not None


@patch(
    "onap_data_provider.resources.vnf_resource.Vf.create",
)
@patch(
    "onap_data_provider.resources.vnf_resource.Vf.add_resource",
)
@patch(
    "onap_data_provider.resources.vnf_resource.Vf.onboard",
)
@patch(
    "onap_data_provider.resources.vnf_resource.VnfResource.vnf",
    new_callable=PropertyMock,
)
@patch(
    "onap_data_provider.resources.xnf_resource.Vfc",
)
def test_vnf_resource_onboards_with_vfc(
    mock_vfc, mock_vnf, mock_onboard, mock_add_resource, mock_vnf_create
):
    mock_vfc = MagicMock()
    mock_vnf.return_value = None
    data_no_composition = {"name": "test_vnf"}
    vnf_resource = VnfResource(data_no_composition)
    vnf_resource.create()
    mock_add_resource.assert_not_called()
    data_with_composition = {
        "name": "test_vnf",
        "resources": [{"name": "test", "xnf_type": "VFC"}],
    }
    vnf_resource = VnfResource(data_with_composition)
    vnf_resource.create()
    mock_add_resource.assert_called_once()
