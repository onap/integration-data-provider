"""SDC properties mixins module."""
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
from abc import ABC
from typing import Any, Dict, List, Union

from onapsdk.exceptions import SDKException, ValidationError, ParameterError  # type: ignore
from onapsdk.sdc.component import Component  # type: ignore
from onapsdk.sdc.properties import NestedInput, Property, ComponentProperty  # type: ignore
from onapsdk.sdc.sdc_resource import SdcResource  # type: ignore


class SdcPropertiesMixins(ABC):
    """Mixins class for properties handling.

    Mixin class for propoerties preparation for SdcResources and Components.
    """

    def set_properties(
        self, propresource: Union[SdcResource, Component], data: List[Any]
    ) -> None:
        """Set properties an  SdcResource.

        Args:
            sdcresource (SdcResource): the SdcResource the properties should belong to
            data (Dict[List, Any]): Data needed to create resource.

        Raises ValidationError
        """
        for property_data in data:

            if any(
                (prop.name == property_data["name"] for prop in propresource.properties)
            ):
                prop = propresource.get_property(property_data["name"])
                prop.value = property_data.get("value")
            else:
                proptype = property_data.get("type")
                if proptype is None:
                    raise ValidationError(
                        f"New Property '{str(property_data['name'])}' is missing a type!"
                    )

                property = Property(
                    name=property_data["name"],
                    property_type=proptype,
                    value=property_data.get("value"),
                )
                try:
                    propresource.add_property(property)
                except SDKException:
                    raise ParameterError(
                        f"Creation of new property '{str(property_data['name'])}' "
                        f"for resourceclass '{str(propresource.__class__.__name__)}' is not provided yet!"
                    )

    def declare_input(self, propresource: Union[SdcResource, Component], property_data: Dict[str, Any]) -> None:
        """Declare input.

        Method to get a property from a component and create an input for it.

        Args:
            propresource (Union[SdcResource, Component]): Resource to create an input
            property_data (Dict[str, Any]): Data used to create an input

        Raises:
            ValidationError: Provided data is invalid - missing property type
            ParameterError: Declaring input returns an SDC error

        """
        proptype = property_data.get("type")
        if proptype is None:
            raise ValidationError(
                "New input '{0}' is missing a type!".format(
                    str(property_data["name"])
                )
            )

        property = Property(
            name=property_data["name"],
            property_type=proptype,
            value=property_data.get("value"),
        )
        try:
            propresource.add_property(property)
            propresource.declare_input(property)
        except SDKException:
            raise ParameterError(
                f"Creation of new input '{str(property_data['name'])}' is not provided yet!"
            )

    def declare_nested_input(self, propresource: Union[SdcResource, Component], data: Dict[str, Any]) -> None:
        """Declare nested input.

        Args:
            propresource (SdcResource): Resource for which nested input is going to be declared
            data (Dict[str, Any]): Data used for input creation.
        """
        if not isinstance(propresource, SdcResource):
            logging.error("Can't declare nested inputs for components!")
            return
        comp: Component = propresource.get_component_by_name(data["resource"])
        propresource.declare_input(NestedInput(comp.sdc_resource, comp.sdc_resource.get_input(data["name"])))

    def declare_resource_property_input(
        self, sdc_resource: Union[SdcResource, Component], input_data: Dict[str, Any]
    ) -> None:
        """Declare input from resource's property.

        Args:
            sdc_resource (SdcResource): Resource for which input is going to be declared
            input_data (Dict[str, Any]): Data used for input creation.
        """
        resource_component: Component = sdc_resource.get_component_by_name(
            input_data["resource"]
        )
        component_property: ComponentProperty = resource_component.get_property(
            input_data["name"]
        )
        sdc_resource.declare_input(Property(
            name=component_property.name,
            property_type=component_property.property_type,
            value=component_property.value,
        ))

    def set_inputs(
        self, sdc_resource: Union[SdcResource, Component], inputs_data: List[Dict[str, Any]],
    ) -> None:
        """Set inputs of an SdcResource.

        Args:
            sdc_resource (SdcResource): the SdcResource the inputs should belong to
            inputs_data (Dict[str, Any]): Input data to be set into resource.
        """
        for input_data in inputs_data:  # type: Dict[str, Any]
            if input_data.get("nested-input"):
                self.declare_nested_input(sdc_resource, input_data)
            elif input_data.get("resource-property"):
                self.declare_resource_property_input(sdc_resource, input_data)
            # In case resource already has input with given name then set its value only
            elif any(
                (
                    resource_input.name == input_data["name"]
                    for resource_input in sdc_resource.inputs
                )
            ):
                sdc_resource.set_input_default_value(
                    sdc_resource.get_input(input_data["name"]),
                    input_data.get("value"),
                )
            else:
                self.declare_input(sdc_resource, input_data)
