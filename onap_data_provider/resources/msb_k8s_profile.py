"""MSB K8S definition profile resource module."""
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
from onapsdk.msb.k8s.definition import Definition, Profile  # type: ignore

from .resource import Resource


class MsbK8SProfileResource(Resource):
    """Profile resource class.

    Creates MSB Kubernetes plugin's profile
    """

    def __init__(self, data: Dict[str, Any], definition: Definition) -> None:
        """Initialize definition resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._profile: Optional[Profile] = None
        self.definition: Definition = definition

    def create(self) -> None:
        """Create profile if not already exists."""
        if not self.exists:
            self._profile = self.definition.create_profile(
                self.data["name"], self.data["namespace"], self.data["k8s-version"]
            )
            with open(self.data["artifact"], "rb") as artifact:
                self._profile.upload_artifact(artifact.read())

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.profile is not None

    @property
    def profile(self) -> Optional[Profile]:
        """Profile property.

        Profile which is represented by the data provided by user.

        Returns:
            Profile: Profile object

        """
        if not self._profile:
            try:
                self._profile = self.definition.get_profile_by_name(
                    self.data["rb-name"]
                )
            except ResourceNotFound:
                logging.error("Profile %s not found", self.data["name"])
        return self._profile
