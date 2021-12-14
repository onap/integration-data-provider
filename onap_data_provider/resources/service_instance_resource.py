"""Service instance resource module."""
"""
   Copyright 2021 Deutsche Telekom AG

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
import logging
from typing import Any, Dict

from onapsdk.aai.cloud_infrastructure import CloudRegion, Tenant  # type: ignore
from onapsdk.aai.business import Customer, OwningEntity  # type: ignore
from onapsdk.aai.service_design_and_creation import Service as AaiService  # type: ignore
from onapsdk.sdc.service import Service  # type: ignore
from onapsdk.vid import LineOfBusiness, Platform, Project  # type: ignore
from onapsdk.aai.business import ServiceSubscription
from onapsdk.aai.business import ServiceInstance
from onapsdk.so.instantiation import (  # type: ignore
    ServiceInstantiation,
    SoService,
)

from .resource import Resource
from onapsdk.exceptions import APIError, ResourceNotFound  # type: ignore


class ServiceInstanceResource(Resource):
    """Service instance resource class.

    Creates service instance.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Service instance resource initialization.

        Args:
            data (Dict[str, Any]): Data needed to create service instance

        """
        super().__init__(data)
        self._customer: Customer = None
        self._service_subscription: ServiceSubscription = None
        self._service_instance: ServiceInstance = None
        self._aai_service: AaiService = None

    def create(self) -> None:
        """Create ServiceInstance resource."""
        if not self.exists:

            service: Service = Service(name=self.data["service_name"])
            if not service.distributed:
                raise AttributeError(
                    "Service not distrbuted - instance can't be created"
                )
            if (cloud_region_id := self.data["cloud_region_id"]) is not None:
                cloud_region: CloudRegion = CloudRegion.get_by_id(
                    cloud_owner=self.data["cloud_owner"],
                    cloud_region_id=cloud_region_id,
                )
                tenant: Tenant = cloud_region.get_tenant(self.data["tenant_id"])
                self.service_subscription.link_to_cloud_region_and_tenant(
                    cloud_region, tenant
                )
            else:
                cloud_region, tenant = None, None
            try:
                owning_entity = OwningEntity.get_by_owning_entity_name(
                    self.data["owning_entity"]
                )
            except APIError:
                owning_entity = OwningEntity.create(self.data["owning_entity"])

            try:
                aai_service = next(
                    AaiService.get_all(service_id=self.data["aai_service"])
                )
            except StopIteration:
                raise ValueError(
                    f"A&AI Service {self.data['aai_service']} does not exist"
                )

            service_instantiation: ServiceInstantiation = (
                ServiceInstantiation.instantiate_macro(
                    sdc_service=service,
                    customer=self.customer,
                    owning_entity=owning_entity,
                    project=Project(self.data["project"]),
                    line_of_business=LineOfBusiness(self.data["line_of_business"]),
                    platform=Platform(self.data["platform"]),
                    cloud_region=cloud_region,
                    tenant=tenant,
                    service_instance_name=self.data["service_instance_name"],
                    so_service=self.so_service,
                    aai_service=aai_service,
                )
            )
            service_instantiation.wait_for_finish(
                timeout=self.data.get("timeout")
            )  # 20 minutes timeout

            if service_instantiation.failed == True:
                logging.error(
                    "Service instantiation failed for %s",
                    self.data["service_instance_name"],
                )
                return
            self._service_instance = (
                self.service_subscription.get_service_instance_by_name(
                    self.data["service_instance_name"]
                )
            )

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.service_instance is not None

    @property
    def service_instance(self) -> ServiceInstance:
        """Serviceinstance property.

        Returns:
            ServiceInstance: ServiceInstance object

        """
        if not self._service_instance:
            try:
                service_instance: ServiceInstance = (
                    self.service_subscription.get_service_instance_by_name(
                        self.data["service_instance_name"]
                    )
                )
                if service_instance:
                    self._service_instance = service_instance
            except ResourceNotFound:
                logging.error(
                    "Customer %s does not exist",
                    self.data["customer_id"],
                )
        return self._service_instance

    @property
    def customer(self) -> Customer:
        """Access to Customer object property.

        Returns:
            Customer: Customer object

        """
        if not self._customer:
            self._customer = Customer.get_by_global_customer_id(
                self.data["customer_id"]
            )
        return self._customer

    @property
    def service_subscription(self) -> ServiceSubscription:
        """Service subscription property.

        Returns:
            ServiceSubscription: ServiceSubscription object

        """
        if not self._service_subscription and self.customer:
            self._service_subscription = (
                self.customer.get_service_subscription_by_service_type(
                    service_type=self.data.get(
                        "service_subscription_type", self.data["service_name"]
                    )
                )
            )
        return self._service_subscription

    @property
    def so_service(self) -> SoService:
        """Create an object with parameters for the service instantiation.

        Based on the instance definition data create an object
        which is used for instantiation.

        Returns:
            SoService: SoService object

        """
        return SoService(
            subscription_service_type=self.data.get(
                "service_subscription_type", self.data["service_name"]
            ),
            vnfs=[
                {
                    "model_name": vnf["vnf_name"],
                    "vnf_name": vnf.get("instance_name", vnf["vnf_name"]),
                    "parameters": vnf.get("parameters", {}),
                    "vf_modules": [
                        {
                            "model_name": vf_module["name"],
                            "vf_module_name": vf_module.get(
                                "instance_name", vf_module["name"]
                            ),
                            "parameters": vf_module.get("parameters", {}),
                        }
                        for vf_module in vnf.get("vf_modules", [])
                    ],
                }
                for vnf in self.data.get("instantiation_parameters", [])
            ],
        )

    @property
    def aai_service(self) -> AaiService:
        """A&AI service which is used during the instantiation.

        Raises:
            ValueError: AaiService with given service id doesn't exist

        Returns:
            AaiService: AaiService object

        """
        if (
            not self._aai_service
            and (aai_service_id := self.data.get("aai_service")) is not None
        ):
            try:
                self._aai_service = next(AaiService.get_all(service_id=aai_service_id))
            except StopIteration:
                raise ValueError(f"A&AI Service {aai_service_id} does not exist")
        return self._aai_service


class ServiceInstanceResource_1_1(ServiceInstanceResource):
    """Service instance resource class.

    That's the Service instance resource class for 1.1 schema version.
    """

    @property
    def aai_service(self) -> AaiService:
        """A&AI service which is used during the instantiation.

        Raises:
            ValueError: AaiService with given service id doesn't exist

        Returns:
            AaiService: AaiService object

        """
        if not self._aai_service:
            try:
                self._aai_service = next(
                    AaiService.get_all(service_id=self.data["aai_service"])
                )
            except StopIteration:
                raise ValueError(
                    f"A&AI Service {self.data['aai_service']} does not exist"
                )
        return self._aai_service