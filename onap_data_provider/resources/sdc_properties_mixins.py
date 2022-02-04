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
from onapsdk.sdc.properties import NestedInput, Property  # type: ignore
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

    def set_inputs(
        self, propresource: Union[SdcResource, Component], data: List[Dict[str, Any]]
    ) -> None:
        """Set inputs of an  SdcResource.

        Args:
            sdcresource (SdcResource): the SdcResource the inputs should belong to
            data (Dict[str, Any]): Data needed to create resource.
        """
        for property_data in data:  # type: Dict[str, Any]
            if property_data.get("nested-input"):
                self.declare_nested_input(propresource, property_data)
            elif any(
                (prop.name == property_data["name"] for prop in propresource.inputs)
            ):
                propresource.set_input_default_value(
                    propresource.get_input(property_data["name"]),
                    property_data.get("value"),
                )
            else:
                self.declare_input(propresource, property_data)
