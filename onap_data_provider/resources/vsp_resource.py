"""VSP resource module."""
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
from typing import Any, Dict, Optional
from onapsdk.sdc.vendor import Vendor  # type: ignore
from onapsdk.sdc.vsp import Vsp  # type: ignore

from .resource import Resource


class VspResource(Resource):
    """VSP resource class."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize VSP resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._vsp: Optional[Vsp] = None

    def create(self) -> None:
        """Create VSP resource."""
        if not self.exists:
            with open(self.data["package"], "rb") as package:
                self._vsp = Vsp(
                    name=self.data["name"],
                    vendor=Vendor(self.data["vendor"]),
                    package=package,
                )
                self._vsp.onboard()

    @property
    def exists(self) -> bool:
        """Check if VSP exists.

        Returns:
            bool: True if VSP exists, False otherwise

        """
        return self.vsp is not None

    @property
    def vsp(self) -> Vsp:
        """VSP property.

        Returns:
            Vsp: VSP object which is describer by provided data. None if does not exist yet.

        """
        if not self._vsp:
            vsp: Vsp = Vsp(name=self.data["name"])
            if not vsp.created():
                return None
            self._vsp = vsp
        return self._vsp
