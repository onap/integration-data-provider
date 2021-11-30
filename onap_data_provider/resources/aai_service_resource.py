"""A&AI service model resource module."""
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

from onapsdk.aai.service_design_and_creation import Service as AaiService  # type: ignore
from onapsdk.exceptions import ResourceNotFound  # type: ignore

from .resource import Resource


class AaiServiceResource(Resource):
    """A&AI service model resource class."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize A&AI SDC service resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._aai_service: AaiService = None

    def create(self) -> None:
        """Create aai service resource."""
        if not self.exists:
            logging.debug("Create AaiService %s", self.data["service-id"])
            AaiService.create(
                service_id=self.data["service-id"],
                service_description=self.data["service-description"],
            )

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.aai_service is not None

    @property
    def aai_service(self) -> AaiService:
        """A&AI service property.

        A&AI servic emodel which is represented by the data provided by user.

        Returns:
            AaiService: A&AI service model object

        """
        if not self._aai_service:
            try:
                for aai_service in AaiService.get_all():
                    if (
                        aai_service.service_id == self.data["service-id"]
                        and aai_service.service_description
                        == self.data["service-description"]
                    ):
                        self._aai_service = aai_service
                        return self._aai_service
            except ResourceNotFound:
                logging.error(
                    "A&AI service %s does not exist",
                    self.data["service-id"],
                )
        return self._aai_service
