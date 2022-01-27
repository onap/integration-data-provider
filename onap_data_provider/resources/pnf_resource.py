"""Pnf resource module."""
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

from onapsdk.sdc.pnf import Pnf  # type: ignore
from onapsdk.sdc.vendor import Vendor  # type: ignore
from .resource import Resource
from .xnf_resource import XnfResource


class PnfResource(Resource, XnfResource):
    """Pnf resource class.

    Creates pnf.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize pnf resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)

    def create(self) -> None:
        """Create pnf resource.

        Create pnf resource and link to provided resources.

        """
        if not self.exists:
            logging.debug("Create Pnf %s", self.data["name"])
            self._xnf = Pnf(self.data["name"], category=self.data.get("category"), subcategory=self.data.get("subcategory"))
            if (vendor_name := self.data.get("vendor")) is not None:
                self._xnf.vendor = Vendor(vendor_name)
            self.onboard_resource_with_properties(self.data)

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.pnf is not None

    @property
    def pnf(self) -> Pnf:
        """Pnf property.

        Pnf which is represented by the data provided by user.

        Returns:
            Pnf: Pnf object

        """
        if (pnf := Pnf(name=self.data["name"])).created():
            self._xnf = pnf
            return self._xnf
        return None
