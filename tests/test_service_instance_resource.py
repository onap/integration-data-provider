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

from onap_data_provider.resources.service_instance_resource import (
    ServiceInstanceResource
)
from onapsdk.exceptions import APIError

RESOURCE_DATA_1_0 = {
    "service_instance_name": "vFW-Macro-1",
    "service_name": "service1",
    "cloud_region": "test",
    "customer_id": "*cust1",
    "owning_entity": "test",
    "project": "test",
    "platform": "test",
    "line_of_business": "test",
    "cloud_region_id": "*cloudregionid1",
    "cloud_owner": "*cloudowner1",
    "tenant_id": "test",
    "instantiation_parameters": [],
}


RESOURCE_DATA_1_1 = {
    "service_instance_name": "vFW-Macro-1",
    "service_name": "service1",
    "cloud_region": "test",
    "customer_id": "*cust1",
    "owning_entity": "test",
    "project": "test",
    "platform": "test",
    "line_of_business": "test",
    "cloud_region_id": "*cloudregionid1",
    "cloud_owner": "*cloudowner1",
    "tenant_id": "test",
    "instantiation_parameters": [],
    "aai_service": "test"
}


INSTANTIATION_PARAMETERS_DATA = {
    "service_name": "service1",
    "instantiation_parameters": [
        {
            "vnf_name": "test",
            "parameters": {"a": "b", "c": "d"},
            "vf_modules": [
                {
                    "name": "base_ubuntu20",
                    "parameters": {
                        "ubuntu20_image_name": "Ubuntu_2004",
                        "ubuntu20_key_name": "cleouverte",
                        "ubuntu20_pub_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDY15cdBmIs2XOpe4EiFCsaY6bmUmK/GysMoLl4UG51JCfJwvwoWCoA+6mDIbymZxhxq9IGxilp/yTA6WQ9s/5pBag1cUMJmFuda9PjOkXl04jgqh5tR6I+GZ97AvCg93KAECis5ubSqw1xOCj4utfEUtPoF1OuzqM/lE5mY4N6VKXn+fT7pCD6cifBEs6JHhVNvs5OLLp/tO8Pa3kKYQOdyS0xc3rh+t2lrzvKUSWGZbX+dLiFiEpjsUL3tDqzkEMNUn4pdv69OJuzWHCxRWPfdrY9Wg0j3mJesP29EBht+w+EC9/kBKq+1VKdmsXUXAcjEvjovVL8l1BrX3BY0R8D imported-openssh-key",
                        "ubuntu20_flavor_name": "m1.smaller",
                        "VM_name": "ubuntu20agent-VM-01",
                        "vnf_id": "ubuntu20agent-VNF-instance",
                        "vf_module_id": "ubuntu20agent-vfmodule-instance",
                        "vnf_name": "ubuntu20agent-VNF",
                        "admin_plane_net_name": "admin",
                        "ubuntu20_name_0": "ubuntu20agent-VNF",
                    },
                }
            ],
        }
    ]
}

PNF_VNF_INSTANTIATION_PARAMETERS_DATA = {
    "service_name": "service1",
    "service_subscripion_type": "ss_1",
    "instantiation_parameters": [
        {
            "vnf_name": "test_vnf",
            "parameters": {"a": "b", "c": "d"}
        },
        {
            "pnf_name": "test_pnf",
            "instance_name": "test_pnf_instance"
        }
    ]
}


@patch(
    "onap_data_provider.resources.service_instance_resource.ServiceInstanceResource.service_instance",
    new_callable=PropertyMock,
)
def test_si_resource_exists(mock_si):
    mock_si.return_value = None
    si_resource = ServiceInstanceResource(RESOURCE_DATA_1_1)
    assert si_resource.exists is False
    mock_si.return_value = 1  # Anything but not None
    assert si_resource.exists is True


@patch(
    "onap_data_provider.resources.service_instance_resource.ServiceInstanceResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.service_instance_resource.Customer")
@patch("onap_data_provider.resources.service_instance_resource.Project")
@patch("onap_data_provider.resources.service_instance_resource.OwningEntity")
@patch("onap_data_provider.resources.service_instance_resource.CloudRegion")
@patch("onap_data_provider.resources.service_instance_resource.ServiceInstantiation")
@patch("onap_data_provider.resources.service_instance_resource.Service")
@patch("onap_data_provider.resources.service_instance_resource.AaiService")
def test_si_resource_create(
    mock_aai_service,
    mock_service,
    mock_service_instantionation,
    mock_cr,
    mock_oe,
    mock_project,
    mock_customer,
    mock_si_resource_exists,
):
    si_resource = ServiceInstanceResource(RESOURCE_DATA_1_1)
    mock_oe.get_by_owning_entity_name.side_effect = APIError
    mock_si_resource_exists.return_value = True
    si_resource.create()
    mock_service.assert_not_called()

    mock_si_resource_exists.return_value = False
    si_resource.create()
    mock_oe.create.assert_called_once()
    mock_oe.get_by_owning_entity_name.assert_called_once()
    mock_aai_service.get_all.called_once_with(service_id="test")
    mock_service_instantionation.instantiate_macro.assert_called_once()


@patch("onap_data_provider.resources.service_instance_resource.ServiceInstanceResource.service_subscription", new_callable=PropertyMock)
def test_so_service(mock_service_subscription):
    si_resource = ServiceInstanceResource(INSTANTIATION_PARAMETERS_DATA)
    so_service = si_resource.so_service
    assert len(so_service.vnfs) == 1
    vnf = so_service.vnfs[0]
    assert vnf.model_name == "test"
    assert vnf.instance_name == "test"
    assert len(vnf.parameters) == 2
    assert len(vnf.vf_modules) == 1
    vf_module = vnf.vf_modules[0]
    assert vf_module.model_name == "base_ubuntu20"
    assert vf_module.instance_name == "base_ubuntu20"
    assert len(vf_module.parameters) == 10


@patch("onap_data_provider.resources.service_instance_resource.AaiService.get_all")
def test_service_instance_resource_version_1_0_and_1_1(mock_aai_service_get_all):
    si_resource_1_0 = ServiceInstanceResource(RESOURCE_DATA_1_0)
    assert si_resource_1_0.aai_service is None
    mock_aai_service_get_all.assert_not_called()

    mock_aai_service_get_all.return_value = iter([MagicMock()])
    si_resource_1_0 = ServiceInstanceResource(RESOURCE_DATA_1_1)
    assert si_resource_1_0.aai_service is not None
    mock_aai_service_get_all.assert_called_once()


@patch("onap_data_provider.resources.service_instance_resource.ServiceInstanceResource.service_subscription", new_callable=PropertyMock)
def test_test_service_instance_resource_vnf_and_pnf_instantiation(mock_service_subscription):
    si_resource = ServiceInstanceResource(PNF_VNF_INSTANTIATION_PARAMETERS_DATA)

    so_service = si_resource.so_service
    assert len(so_service.vnfs) == 1
    assert len(so_service.pnfs) == 1

    vnf = so_service.vnfs[0]
    assert vnf.instance_name == "test_vnf"
    assert vnf.model_name == "test_vnf"
    assert vnf.parameters == {"a": "b", "c": "d"}

    pnf = so_service.pnfs[0]
    assert pnf.instance_name == "test_pnf_instance"
    assert pnf.model_name == "test_pnf"


@patch(
    "onap_data_provider.resources.service_instance_resource.ServiceInstanceResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.service_instance_resource.Customer")
@patch("onap_data_provider.resources.service_instance_resource.Project")
@patch("onap_data_provider.resources.service_instance_resource.OwningEntity")
@patch("onap_data_provider.resources.service_instance_resource.CloudRegion")
@patch("onap_data_provider.resources.service_instance_resource.ServiceInstantiation")
@patch("onap_data_provider.resources.service_instance_resource.Service")
@patch("onap_data_provider.resources.service_instance_resource.AaiService")
def test_si_resource_create_with_tenant_name(
    mock_aai_service,
    mock_service,
    mock_service_instantionation,
    mock_cr,
    mock_oe,
    mock_project,
    mock_customer,
    mock_si_resource_exists,
):
    data = RESOURCE_DATA_1_1
    data.pop("tenant_id")
    data.update({"tenant_name": "test_1"})
    si_resource = ServiceInstanceResource(data)
    mock_oe.get_by_owning_entity_name.side_effect = APIError
    mock_si_resource_exists.return_value = True
    si_resource.create()
    mock_service.assert_not_called()
    mock_si_resource_exists.return_value = False
    try:
        si_resource.create()
    except ValueError:
        assert True
