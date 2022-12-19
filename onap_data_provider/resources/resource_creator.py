"""Resource creator module."""
from __future__ import annotations

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

from onap_data_provider.resources.platform_resource import PlatformResource
import typing
from abc import ABC

from .aai_service_resource import AaiServiceResource
from .blueprint_resource import BlueprintResource
from .cds_resource_template import BlueprintResourceTemplateResource
from .cloud_region_resource import CloudRegionResource
from .complex_resource import ComplexResource
from .customer_resource import CustomerResource
from .data_dictionary_resource import DataDictionarySetResource
from .cps_resource import AnchorNodeResource, AnchorResource, DataspaceResource, SchemaSetResource
from .line_of_business_resource import LineOfBusinessResource
from .msb_k8s_definition import MsbK8SDefinitionResource
from .owning_entity_resource import OwningEntityResource
from .pnf_resource import PnfResource
from .project_resource import ProjectResource
from .service_resource import ServiceResource
from .service_instance_resource import (
    ServiceInstanceResource,
    ServiceInstanceResource_1_1,
)
from .vendor_resource import VendorResource
from .vnf_resource import VnfResource
from .vsp_resource import VspResource
from ..versions import VersionsEnum

if typing.TYPE_CHECKING:
    from .resource import Resource


class ResourceCreator(ABC):
    """Resource creator.

    Provides a method to create `Resource` instances.
    """

    RESOURCES_TYPES_DICT: typing.Mapping[
        str, typing.Mapping[VersionsEnum, typing.Type[Resource]]
    ] = {
        "aai-service": {
            VersionsEnum.NONE: AaiServiceResource,
            VersionsEnum.V1_0: AaiServiceResource,
            VersionsEnum.V1_1: AaiServiceResource,
            VersionsEnum.V2_0: AaiServiceResource,
        },
        "cloud-region": {
            VersionsEnum.NONE: CloudRegionResource,
            VersionsEnum.V1_0: CloudRegionResource,
            VersionsEnum.V1_1: CloudRegionResource,
            VersionsEnum.V2_0: CloudRegionResource,
        },
        "complex": {
            VersionsEnum.NONE: ComplexResource,
            VersionsEnum.V1_0: ComplexResource,
            VersionsEnum.V1_1: ComplexResource,
            VersionsEnum.V2_0: ComplexResource,
        },
        "customer": {
            VersionsEnum.NONE: CustomerResource,
            VersionsEnum.V1_0: CustomerResource,
            VersionsEnum.V1_1: CustomerResource,
            VersionsEnum.V2_0: CustomerResource,
        },
        "vsp": {
            VersionsEnum.NONE: VspResource,
            VersionsEnum.V1_0: VspResource,
            VersionsEnum.V1_1: VspResource,
            VersionsEnum.V2_0: VspResource,
        },
        "service": {
            VersionsEnum.NONE: ServiceResource,
            VersionsEnum.V1_0: ServiceResource,
            VersionsEnum.V1_1: ServiceResource,
            VersionsEnum.V2_0: ServiceResource,
        },
        "vendor": {
            VersionsEnum.NONE: VendorResource,
            VersionsEnum.V1_0: VendorResource,
            VersionsEnum.V1_1: VendorResource,
            VersionsEnum.V2_0: VendorResource,
        },
        "pnf": {
            VersionsEnum.NONE: PnfResource,
            VersionsEnum.V1_0: PnfResource,
            VersionsEnum.V1_1: PnfResource,
            VersionsEnum.V2_0: PnfResource,
        },
        "vnf": {
            VersionsEnum.NONE: VnfResource,
            VersionsEnum.V1_0: VnfResource,
            VersionsEnum.V1_1: VnfResource,
            VersionsEnum.V2_0: VnfResource,
        },
        "service-instance": {
            VersionsEnum.NONE: ServiceInstanceResource,
            VersionsEnum.V1_0: ServiceInstanceResource,
            VersionsEnum.V1_1: ServiceInstanceResource_1_1,
            VersionsEnum.V2_0: ServiceInstanceResource_1_1,
        },
        "line-of-business": {
            VersionsEnum.NONE: LineOfBusinessResource,
            VersionsEnum.V1_0: LineOfBusinessResource,
            VersionsEnum.V1_1: LineOfBusinessResource,
            VersionsEnum.V2_0: LineOfBusinessResource,
        },
        "project": {
            VersionsEnum.NONE: ProjectResource,
            VersionsEnum.V1_0: ProjectResource,
            VersionsEnum.V1_1: ProjectResource,
            VersionsEnum.V2_0: ProjectResource,
        },
        "platform": {
            VersionsEnum.NONE: PlatformResource,
            VersionsEnum.V1_0: PlatformResource,
            VersionsEnum.V1_1: PlatformResource,
            VersionsEnum.V2_0: PlatformResource,
        },
        "owning-entity": {
            VersionsEnum.NONE: OwningEntityResource,
            VersionsEnum.V1_0: OwningEntityResource,
            VersionsEnum.V1_1: OwningEntityResource,
            VersionsEnum.V2_0: OwningEntityResource,
        },
        "msb-k8s-definition": {
            VersionsEnum.NONE: MsbK8SDefinitionResource,
            VersionsEnum.V1_0: MsbK8SDefinitionResource,
            VersionsEnum.V1_1: MsbK8SDefinitionResource,
            VersionsEnum.V2_0: MsbK8SDefinitionResource,
        },
        "data-dictionaries": {
            VersionsEnum.NONE: DataDictionarySetResource,
            VersionsEnum.V1_0: DataDictionarySetResource,
            VersionsEnum.V1_1: DataDictionarySetResource,
            VersionsEnum.V2_0: DataDictionarySetResource,
        },
        "blueprint": {
            VersionsEnum.V1_1: BlueprintResource,
            VersionsEnum.V2_0: BlueprintResource,
        },
        "blueprint-resource-template": {
            VersionsEnum.V1_1: BlueprintResourceTemplateResource,
            VersionsEnum.V2_0: BlueprintResourceTemplateResource,
        },
        "cps-dataspace": {
            VersionsEnum.V1_1: DataspaceResource,
            VersionsEnum.V2_0: DataspaceResource,
        },
        "cps-schema-set": {
            VersionsEnum.V1_1: SchemaSetResource,
            VersionsEnum.V2_0: SchemaSetResource,
        },
        "cps-anchor": {
            VersionsEnum.V1_1: AnchorResource,
            VersionsEnum.V2_0: AnchorResource,
        },
        "cps-anchor-node": {
            VersionsEnum.V1_1: AnchorNodeResource,
            VersionsEnum.V2_0: AnchorNodeResource
        }
    }

    @classmethod
    def create(
        cls,
        resource_type: str,
        data: typing.Dict[str, typing.Any],
        version: VersionsEnum,
    ) -> Resource:
        """Resources factory method.

        Based on provided `resource_type` creates `Resource` subclass.

        Supported `resource_type` values:
         - aai-service: AaiServiceResource
         - cloud-region: CloudRegionResource
         - complex: ComplexResource
         - customer: CustomerResource
         - vsp: VspResource
         - service: ServiceResource
         - vendor: VendorResource
         - pnf: PnfResource
         - vnf: VnfResource
         - service-instance: ServiceInstanceResource
         - line-of-business: LineOfBusinessResource
         - project: ProjectResource
         - platform: PlatformResource
         - owning-entity: OwningEntityResource
         - msb-k8s-definition: MsbK8SDefinitionResource
         - data-dictionaries: DataDictionarySetResource
         - blueprints: BlueprintResource
         - blueprint-resource-template: BlueprintResourceTemplateResource
         - cps-dataspace: DataspaceResource
         - cps-schema-set: SchemaSetResource
         - cps-anchor: AnchorResource

        Args:
            resource_type (str): Resource type to create
            data (typing.Dict[str, typing.Any]): Resource data

        Raises:
            ValueError: Not support `resource_type` value provided.

        Returns:
            Resource: Created `Resource` subclass instance.

        """
        try:
            return cls.RESOURCES_TYPES_DICT[resource_type][version](data)
        except KeyError as key_error:
            raise ValueError(
                "Invalid resource type provided: %d", resource_type
            ) from key_error
