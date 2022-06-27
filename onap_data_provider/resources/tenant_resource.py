"""Tenant resource module."""
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
from typing import Any, Dict, Optional

from onapsdk.aai.aai_element import Relationship  # type: ignore
from onapsdk.aai.cloud_infrastructure import CloudRegion, Tenant  # type: ignore
from onapsdk.aai.business import LineOfBusiness, OwningEntity  # type: ignore

from .resource import Resource
from onapsdk.exceptions import ResourceNotFound  # type: ignore


class TenantResource(Resource):
    """Tenant resource class.

    Creates tenant.
    """

    def __init__(self, data: Dict[str, Any], cloud_region: CloudRegion) -> None:
        """Tenant resource initialization.

        Args:
            data (Dict[str, Any]): Data needed to create tenant
            cloud_region (CloudRegion): Cloud region for which tenant is going to be created

        """
        super().__init__(data)
        self.cloud_region: CloudRegion = cloud_region
        self._tenant: Optional[Tenant] = None

    def create(self) -> None:
        """Create tenant resource.

        Add tenant to provided cloud region

        """
        if not self.exists:
            self.cloud_region.add_tenant(
                tenant_id=self.data["tenant-id"],
                tenant_name=self.data["tenant-name"],
                tenant_context=self.data.get("tenant-context"),
            )

        for lines_of_business_data in self.data.get("lines-of-business", []):
            try:
                line_of_business: LineOfBusiness = LineOfBusiness.get_by_name(lines_of_business_data["line-of-business"]["name"])
            except ResourceNotFound:
                line_of_business = LineOfBusiness.create(lines_of_business_data["line-of-business"]["name"])
            line_of_business.add_relationship(
                Relationship(
                    related_to="tenant",
                    related_link=self.tenant.url,
                    relationship_data=[]
                )
            )

        for owning_entities_data in self.data.get("owning-entities", []):
            try:
                owning_entity: OwningEntity = OwningEntity.get_by_owning_entity_name(owning_entities_data["owning-entity"]["name"])
            except ResourceNotFound:
                owning_entity = OwningEntity.create(owning_entities_data["owning-entity"]["name"],
                                                    owning_entities_data["owning-entity"]["id"])
            owning_entity.add_relationship(
                Relationship(
                    related_to="tenant",
                    related_link=self.tenant.url,
                    relationship_data=[]
                )
            )

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.tenant is not None

    @property
    def tenant(self) -> Tenant:
        """Tenant property.

        Returns:
            Tenant: Tenant object

        """
        if not self._tenant:
            try:
                self._tenant = self.cloud_region.get_tenant(self.data["tenant-id"])
            except ResourceNotFound:
                logging.error(
                    "Tenant %s does not exist in %s cloud region",
                    self.data["tenant-id"],
                    self.cloud_region.cloud_region_id,
                )
                return None
        return self._tenant
