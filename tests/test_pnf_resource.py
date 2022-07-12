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

from onap_data_provider.resources.pnf_resource import PnfResource

PNF_RESOURCE_DATA = {"name": "test_pnf"}


@patch(
    "onap_data_provider.resources.pnf_resource.PnfResource.pnf",
    new_callable=PropertyMock,
)
def test_pnf_resource_exists(mock_pnf):
    mock_pnf.return_value = None
    pnf_resource = PnfResource(PNF_RESOURCE_DATA)
    assert pnf_resource.exists is False
    mock_pnf.return_value = 1  # Anything but not None
    assert pnf_resource.exists is True


@patch(
    "onap_data_provider.resources.pnf_resource.Pnf.created",
)
def test_pnf_resource_pnf(mock_pnf_created):
    mock_pnf_created.return_value = False
    pnf_resource = PnfResource(PNF_RESOURCE_DATA)
    assert pnf_resource.pnf is None
    mock_pnf_created.return_value = True
    assert pnf_resource.pnf is not None


@patch(
    "onap_data_provider.resources.pnf_resource.Pnf.create",
)
@patch(
    "onap_data_provider.resources.pnf_resource.Pnf.add_resource",
)
@patch(
    "onap_data_provider.resources.pnf_resource.Pnf.onboard",
)
@patch(
    "onap_data_provider.resources.pnf_resource.PnfResource.pnf",
    new_callable=PropertyMock,
)
@patch(
    "onap_data_provider.resources.xnf_resource.Vfc",
)
def test_pnf_resource_onboards_with_vfc(
    mock_vfc, mock_pnf, mock_onboard, mock_add_resource, mock_pnf_create
):
    mock_vfc = MagicMock()
    mock_pnf.return_value = None
    data_no_composition = {"name": "test_pnf"}
    pnf_resource = PnfResource(data_no_composition)
    pnf_resource.create()
    mock_add_resource.assert_not_called()
    data_with_composition = {
        "name": "test_pnf",
        "resources": [{"name": "test", "xnf_type": "VFC"}],
    }
    pnf_resource = PnfResource(data_with_composition)
    pnf_resource.create()
    mock_add_resource.assert_called_once()
