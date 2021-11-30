"""Vendor resource module."""
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

from onapsdk.sdc.vendor import Vendor  # type: ignore
from .resource import Resource


class VendorResource(Resource):
    """Vendor resource class.

    Creates vendor.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize vendor resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._vendor: Vendor = None

    def create(self) -> None:
        """Create vendor resource.

        Create vendor resource.

        """
        if not self.exists:
            logging.debug("Create Vendor %s", self.data["name"])
            self._vendor = Vendor(name=self.data["name"])
            self._vendor.onboard()

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.vendor is not None

    @property
    def vendor(self) -> Vendor:
        """Vendor property.

        Vendor which is represented by the data provided by user.

        Returns:
            Vendor: Vendor object

        """
        if (vendor := Vendor(name=self.data["name"])).created():
            self._vendor = vendor
            return self._vendor
        return None
