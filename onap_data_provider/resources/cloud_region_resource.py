"""Cloud region resource module."""
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

from onap_data_provider.resources.esr_system_info_resource import (
    EsrSystemInfoResource,
)
import logging
from typing import Any, Dict

from onapsdk.aai.aai_element import Relationship  # type: ignore
from onapsdk.aai.business import Project  # type: ignore
from onapsdk.aai.cloud_infrastructure import CloudRegion, Complex  # type: ignore
from onapsdk.msb.k8s.connectivity_info import ConnectivityInfo  # type: ignore
from onapsdk.so.so_db_adapter import SoDbAdapter, IdentityService  # type: ignore

from .resource import Resource
from .tenant_resource import TenantResource
from onapsdk.exceptions import APIError, ResourceNotFound  # type: ignore


class CloudRegionResource(Resource):
    """Cloud region resource class.

    Creates cloud region.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize cloud region resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._cloud_region: CloudRegion = None

    def create(self) -> None:
        """Create cloud region resource.

        Create cloud region resource and all related resources.

        """
        logging.debug("Create CloudRegion %s", self.data["cloud-region-id"])
        if not self.exists:
            self._cloud_region = CloudRegion.create(
                cloud_owner=self.data["cloud-owner"],
                cloud_region_id=self.data["cloud-region-id"],
                orchestration_disabled=self.data["orchestration-disabled"],
                in_maint=self.data["in-maint"],
                cloud_type=self.data.get("cloud-region-type", "openstack"),
                cloud_region_version="pike",
            )

        # Create tenants
        for tenant_data in self.data.get("tenants", []):
            tenant_resource = TenantResource(
                tenant_data, cloud_region=self._cloud_region
            )
            tenant_resource.create()

        # Link with complex
        if (
            complex_physical_id := self.data.get("complex", {}).get(
                "physical-location-id"
            )
        ) is not None:
            self._link_to_complex(complex_physical_id)

        # Add availability zones
        try:
            for az_data in self.data.get("availability-zones", []):
                self.cloud_region.add_availability_zone(
                    availability_zone_name=az_data["availability-zone-name"],
                    availability_zone_hypervisor_type=az_data["hypervisor-type"],
                )
        except APIError:
            logging.error("Availability zone update not supported.")

        # Create external system infos
        for esr_system_info_data in self.data.get("esr-system-infos", []):
            esr_system_info_resource: EsrSystemInfoResource = EsrSystemInfoResource(
                esr_system_info_data, cloud_region=self._cloud_region
            )
            esr_system_info_resource.create()

        if self.data.get("register-to-multicloud", False):
            self.cloud_region.register_to_multicloud()

        # Create connectivity info for Cloud region if it's type is k8s
        if self.cloud_region.cloud_type == "k8s":
            try:
                ConnectivityInfo.get_connectivity_info_by_region_id(
                    self.cloud_region.cloud_region_id
                )
            except APIError:
                with open(self.data["kube-config"], "rb") as kube_config:
                    ConnectivityInfo.create(
                        cloud_owner=self.cloud_region.cloud_owner,
                        cloud_region_id=self.cloud_region.cloud_region_id,
                        kubeconfig=kube_config.read(),
                    )
            if not self.cloud_region.complex:
                logging.error(
                    "k8s cloud region should have complex linked to create SO cloud site DB entry"
                )
            else:
                SoDbAdapter.add_cloud_site(
                    self.cloud_region.cloud_region_id,
                    self.cloud_region.complex.physical_location_id,
                    IdentityService("DEFAULT_KEYSTONE"),
                )

        # Link with project
        for project_data in self.data.get("projects", []):
            try:
                project: Project = Project.get_by_name(project_data["project"]["name"])
            except ResourceNotFound:
                project = Project.create(project_data["project"]["name"])
            project.add_relationship(
                Relationship(
                    related_to="cloud-region",
                    related_link=self.cloud_region.url,
                    relationship_data=[]
                )
            )

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.cloud_region is not None

    @property
    def cloud_region(self) -> CloudRegion:
        """Cloud region property.

        Cloud region which is represented by the data provided by user.

        Returns:
            CloudRegion: Cloud region object

        """
        if not self._cloud_region:
            try:
                self._cloud_region = CloudRegion.get_by_id(
                    self.data["cloud-owner"], self.data["cloud-region-id"]
                )
            except ResourceNotFound:
                logging.error(
                    "Cloud region %s does not exist",
                    self.data["cloud-region-id"],
                )
                return None
        return self._cloud_region

    def _link_to_complex(self, complex_physical_id: str) -> None:
        if self.cloud_region.complex:
            logging.info(
                "Cloud region has relationship with complex: %s. New relationship can't be created",
                self.cloud_region.complex.physical_location_id,
            )
            return
        try:
            cmplx: Complex = Complex.get_by_physical_location_id(complex_physical_id)
            self.cloud_region.link_to_complex(cmplx)
        except ResourceNotFound:
            logging.error(
                "Complex %s does not exist, please create it before cloud region creation",
                complex_physical_id,
            )
