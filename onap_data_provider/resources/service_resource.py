"""Service resource module."""
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
from typing import Any, Dict, List, Mapping, Optional, Type

from onapsdk.sdc.pnf import Pnf  # type: ignore
from onapsdk.sdc.sdc_resource import SdcResource  # type: ignore
from onapsdk.sdc.service import Service, ServiceInstantiationType  # type: ignore
from onapsdk.sdc.vf import Vf  # type: ignore
from onapsdk.sdc.vl import Vl  # type: ignore

from .resource import Resource
from .sdc_properties_mixins import SdcPropertiesMixins


class ServiceResource(Resource, SdcPropertiesMixins):
    """Service resource class."""

    RESOURCES: Mapping[str, Type[SdcResource]] = {"PNF": Pnf, "VF": Vf, "VL": Vl}

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize Service resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._service: Optional[Service] = None

    def create(self) -> None:
        """Create Service resource."""
        if not self.exists:
            service = Service(
                name=self.data["name"],
                instantiation_type=ServiceInstantiationType.MACRO,
            )
            service.create()
            for resource_data in self.data.get("resources", []):
                resource = self.RESOURCES[resource_data["type"].upper()](
                    name=resource_data["name"]
                )
                service.add_resource(resource)
                component = service.get_component(resource)
                properties_data = resource_data.get("properties", [])
                if properties_data and isinstance(properties_data, List):
                    self.set_properties(component, properties_data)
                else:
                    # backward compatibility
                    for prop_key, prop_value in resource_data.get(
                        "properties", {}
                    ).items():
                        prop = component.get_property(prop_key)
                        prop.value = prop_value
                self.set_inputs(component, resource_data.get("inputs", []))
            self.set_properties(service, self.data.get("properties", []))
            self.set_inputs(service, self.data.get("inputs", []))
            service.checkin()
            service.onboard()
            self._service = service

    @property
    def exists(self) -> bool:
        """Check if Service exists in SDC.

        Returns:
            bool: True if Service exists, False otherwise

        """
        return self.service is not None and self.service.distributed

    @property
    def service(self) -> Optional[Service]:
        """Service property.

        Returns:
            Service: Service object which is describer by provided data. None if does not exist yet.

        """
        if not self._service:
            service: Service = Service(name=self.data["name"])
            if not service.created():
                return None
            self._service = service
        return self._service
