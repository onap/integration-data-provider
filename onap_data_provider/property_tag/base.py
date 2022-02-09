"""Base module for property tag classes."""
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

from abc import ABC
from typing import Any, Type

from onapsdk.onap_service import OnapService  # type: ignore


class BasePropertyTagResource(ABC):
    """Base property tag resource class.

    Abstract class which all resource classes should inherit from.
    Subclasses has to implement `resource` property to get the valid object
        using Python ONAP SDK classes.

    Subclass could also implement `__init__` method to get more attributes from
        the user which uses the tag.

    """

    def __init__(self, property_name: str) -> None:
        """Init property tag resource object.

        Args:
            property_name (str): Name of the property to get

        """
        self.property_name: str = property_name

    @property
    def resource(self) -> OnapService:
        """Resource property abstract method.

        Returns an object from which the property is going to be get.

        Raises:
            NotImplementedError: That method is an abstract one

        Returns:
            OnapService: Any OnapService subclass

        """
        raise NotImplementedError

    @property
    def resource_property(self) -> Any:
        """Resource property.

        Using `getattr` function get the property from resource.

        Returns:
            Any: Property value

        Raises:
            AttributeError: Resource has no property with given name.

        """
        return getattr(self.resource, self.property_name)
