"""Properties getter module."""
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

import logging
from typing import Any, Mapping, Type, TYPE_CHECKING

from .base import BasePropertyTagResource
from .sdc_service import SdcServicePropertyTagResource

if TYPE_CHECKING:
    from typing import Any, Mapping


class PropertiesGetter:
    """Properties getter class.

    Uses to get values of properties from already existing ONAP resources.

    Contains a mapper to select right class to get the values from.
    """

    RESOURCES: Mapping[str, Type[BasePropertyTagResource]] = {
        "service": SdcServicePropertyTagResource
    }

    @classmethod
    def get_property(cls, resource_type: str, *args: str) -> Any:
        """Get property class method.

        Maps the input `resource_type` into `BasePropertyTagResource` class
            and get it's `resource_property` property

        Args:
            resource_type (str): Type of the resource - uses by a mapper
            *args (str): Args to be passed to the service class init

        Raises:
            ValueError: Given resource type is not supported

        Returns:
            Any: Resource property value

        """
        try:
            return cls.RESOURCES[resource_type](*args).resource_property
        except KeyError:
            msg = f"Resource type \"{resource_type}\" is not supported"
            logging.error(msg)
            raise ValueError(msg)

