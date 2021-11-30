"""Vnf resource module."""
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

from onapsdk.sdc.vf import Vf  # type: ignore
from .resource import Resource
from .xnf_resource import XnfResource


class VnfResource(Resource, XnfResource):
    """Vnf resource class.

    Creates vnf.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize vnf resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)

    def create(self) -> None:
        """Create vnf resource.

        Create vnf resource and link to specified resources.

        """
        if not self.exists:
            logging.debug("Create Vnf %s", self.data["name"])
            self._xnf = Vf(name=self.data["name"])
            self.onboard_resource_with_properties(self.data)

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.vnf is not None

    @property
    def vnf(self) -> Vf:
        """Vnf property.

        Vnf which is represented by the data provided by user.

        Returns:
            Vf: Vf object

        """
        if (vnf := Vf(name=self.data["name"])).created():
            self._xnf = vnf
            return self._xnf
        return None
