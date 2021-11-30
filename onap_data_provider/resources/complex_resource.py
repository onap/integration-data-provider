"""Complex resource module."""
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

from onapsdk.aai.cloud_infrastructure import Complex  # type: ignore

from .resource import Resource
from onapsdk.exceptions import ResourceNotFound  # type: ignore


class ComplexResource(Resource):
    """Complex resource class."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Complex resource initialization.

        Args:
            data (Dict[str, Any]): Data needed to create complex

        """
        super().__init__(data)
        self._complex: Complex = None

    def create(self) -> None:
        """Create complex resource."""
        if not self.exists:
            self._complex = Complex.create(
                physical_location_id=self.data["physical-location-id"],
                name=self.data.get("complex-name"),
                data_center_code=self.data.get("data-center-code"),
                identity_url=self.data.get("identity-url"),
                physical_location_type=self.data.get("physical-location-type"),
                street1=self.data.get("street1"),
                street2=self.data.get("street2"),
                city=self.data.get("city"),
                state=self.data.get("state"),
                postal_code=self.data.get("postal-code"),
                country=self.data.get("country"),
                region=self.data.get("region"),
                latitude=self.data.get("latitude"),
                longitude=self.data.get("longitude"),
                elevation=self.data.get("elevation"),
                lata=self.data.get("lata"),
            )

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.complex is not None

    @property
    def complex(self) -> Complex:
        """Complex property.

        Returns:
            Complex: Complex object

        """
        if not self._complex:
            try:
                self._complex = next(
                    Complex.get_all(
                        physical_location_id=self.data["physical-location-id"]
                    )
                )
            except ResourceNotFound:
                logging.error(
                    "Complex %s does not exist", self.data["physical-location-id"]
                )
                return None
        return self._complex
