from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from onap_data_provider.resources.service_instance_resource import (
    ServiceInstanceResource,
    ServiceInstantiation,
    ServiceInstanceResource_1_1
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


def test_so_service():
    si_resource = ServiceInstanceResource(INSTANTIATION_PARAMETERS_DATA)
    so_service = si_resource.so_service
    assert so_service.subscription_service_type == "service1"
    assert len(so_service.vnfs) == 1
    vnf = so_service.vnfs[0]
    assert vnf["model_name"] == "test"
    assert vnf["vnf_name"] == "test"
    assert len(vnf["parameters"]) == 2
    assert len(vnf["vf_modules"]) == 1
    vf_module = vnf["vf_modules"][0]
    assert vf_module["model_name"] == "base_ubuntu20"
    assert vf_module["vf_module_name"] == "base_ubuntu20"
    assert len(vf_module["parameters"]) == 10


@patch("onap_data_provider.resources.service_instance_resource.AaiService.get_all")
def test_service_instance_resource_version_1_0_and_1_1(mock_aai_service_get_all):
    si_resource_1_0 = ServiceInstanceResource(RESOURCE_DATA_1_0)
    assert si_resource_1_0.aai_service is None
    mock_aai_service_get_all.assert_not_called()

    mock_aai_service_get_all.return_value = iter([MagicMock()])
    si_resource_1_0 = ServiceInstanceResource(RESOURCE_DATA_1_1)
    assert si_resource_1_0.aai_service is not None
    mock_aai_service_get_all.assert_called_once()
