"""Customer resource module."""
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

from onapsdk.aai.business import Customer, ServiceSubscription  # type: ignore
from onapsdk.aai.cloud_infrastructure import CloudRegion, Tenant  # type: ignore

from onapsdk.sdc.service import Service  # type: ignore

from .resource import Resource
from onapsdk.exceptions import ResourceNotFound  # type: ignore


class CustomerResource(Resource):
    """Customer resource class.

    Creates customer.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize customer resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._customer: Customer = None

    def create(self) -> None:
        """Create customer resource.

        Create customer resource and all related resources.

        """
        logging.debug("Create Customer %s", self.data["global-customer-id"])
        if not self.exists:
            self._customer = Customer.create(
                global_customer_id=self.data["global-customer-id"],
                subscriber_name=self.data["subscriber-name"],
                subscriber_type=self.data["subscriber-type"],
            )

        for service_subscription in self.data.get("service-subscriptions", []):
            resource = CustomerResource.ServiceSubscriptionResource(
                service_subscription, self._customer
            )
            resource.create()

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.customer is not None

    @property
    def customer(self) -> Customer:
        """Access to customer property.

        Customer property containing Customer object.

        Returns:
            Customer: Customer object

        """
        if not self._customer:
            try:
                self._customer = Customer.get_by_global_customer_id(
                    self.data["global-customer-id"]
                )
            except ResourceNotFound:
                logging.error(
                    "Customer %s does not exist",
                    self.data["global-customer-id"],
                )
                return None
        return self._customer

    class ServiceSubscriptionResource(Resource):
        """Service subscription class.

        Creates service subscription.
        """

        def __init__(self, data: Dict[str, str], customer: Customer) -> None:
            """Initialize service subscription resource.

            Args:
                data (Dict[str, str]): Data needed to create resource.
                customer (Customer): Related Customer object.

            """
            super().__init__(data)
            self._service_subscription: ServiceSubscription = None
            self._customer: Customer = customer

        def create(self) -> None:
            """Create Service subscription resource.

            Create service subscription resource belonging to a customer.

            """
            logging.debug("Create ServiceSubscription %s", self.data["service-type"])
            if not self.exists:
                self._service_subscription = self._customer.subscribe_service(
                    self.data["service-type"]
                )

            for tenant_cloud_region_data in self.data.get("tenants", []):
                try:
                    cloud_region: CloudRegion = CloudRegion.get_by_id(
                        tenant_cloud_region_data["cloud-owner"],
                        tenant_cloud_region_data["cloud-region-id"],
                    )
                except ResourceNotFound:
                    logging.error(
                        f"Cloud region {tenant_cloud_region_data['cloud-owner']} {tenant_cloud_region_data['cloud-region-id']} does not exists"
                    )
                    continue
                try:
                    tenant: Tenant = cloud_region.get_tenant(
                        tenant_cloud_region_data["tenant-id"]
                    )
                except ResourceNotFound:
                    logging.error(
                        f"Tenant {tenant_cloud_region_data['tenant-id']} does not exist"
                    )
                    continue

                self.service_subscription.link_to_cloud_region_and_tenant(
                    cloud_region, tenant
                )
                logging.debug(
                    f"Service subscription linked to {tenant.name} tenant and {cloud_region.cloud_region_id} cloud region"
                )

        @property
        def exists(self) -> bool:
            """Determine if resource already exists or not.

            Returns:
                bool: True if object exists, False otherwise

            """
            return self.service_subscription is not None

        @property
        def service_subscription(self) -> ServiceSubscription:
            """Get ServiceSubscription instance.

            Get ServiceSubscription instance.

            Returns:
                ServiceSubscription: Created `ServiceSubscription` subclass instance.
            """
            if not self._service_subscription:
                try:
                    self._service_subscription = (
                        self._customer.get_service_subscription_by_service_type(
                            self.data["service-type"]
                        )
                    )
                except ResourceNotFound:
                    logging.error(
                        "Service type %s does not exist",
                        self.data["service-type"],
                    )
                    return None
            return self._service_subscription
