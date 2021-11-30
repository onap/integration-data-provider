"""MSB K8S definition resource module."""
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
from typing import Any, Dict, Optional

from onapsdk.exceptions import ResourceNotFound  # type: ignore
from onapsdk.msb.k8s.definition import Definition  # type: ignore

from .msb_k8s_profile import MsbK8SProfileResource
from .resource import Resource


class MsbK8SDefinitionResource(Resource):
    """Definition resource class.

    Creates MSB Kubernetes plugin's definition.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize definition resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._definition: Optional[Definition] = None

    def create(self) -> None:
        """Create definition if not already exists."""
        if not self.exists:
            self._definition = Definition.create(
                self.data["name"],
                self.data["version"],
                self.data.get("chart-name"),
                self.data.get("description"),
            )
            with open(self.data["artifact"], "rb") as artifact:
                self._definition.upload_artifact(artifact.read())
        for profile_data in self.data.get("profiles", []):
            MsbK8SProfileResource(profile_data, self.definition).create()

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.definition is not None

    @property
    def definition(self) -> Optional[Definition]:
        """Definition property.

        Definition which is represented by the data provided by user.

        Returns:
            Definition: Definition object

        """
        if not self._definition:
            try:
                self._definition = Definition.get_definition_by_name_version(
                    self.data["name"], self.data["version"]
                )
            except ResourceNotFound:
                logging.error("Definition %s does not exist", self.data["rb-name"])
        return self._definition
