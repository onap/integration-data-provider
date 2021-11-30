"""Project resource module."""
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

from onapsdk.aai.business import Project  # type: ignore
from onapsdk.exceptions import ResourceNotFound  # type: ignore

from .resource import Resource


class ProjectResource(Resource):
    """Project resource class.

    Creates A&AI project.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize project resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._project: Optional[Project] = None

    def create(self) -> None:
        """Create project resource."""
        logging.debug(f"Create Project {self.data['name']}")
        if not self.exists:
            self._project = Project.create(self.data["name"])

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return bool(self.project)

    @property
    def project(self) -> Project:
        """Project property.

        Project which is represented by the data provided by user.

         Returns:
             Project: Project object

        """
        if not self._project:
            try:
                self._project = Project.get_by_name(self.data["name"])
            except ResourceNotFound:
                return None
        return self._project
