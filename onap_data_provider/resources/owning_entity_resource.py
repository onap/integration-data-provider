"""Owning entity resource module."""
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

from onapsdk.aai.business import OwningEntity  # type: ignore
from onapsdk.exceptions import ResourceNotFound  # type: ignore

from .resource import Resource


class OwningEntityResource(Resource):
    """Owning entity resource class.

    Creates A&AI line of business.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize line of business resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._owning_entity: Optional[OwningEntity] = None

    def create(self) -> None:
        """Create line of business resource."""
        logging.debug(f"Create Owning entity {self.data['name']}")
        if not self.exists:
            self._owning_entity = OwningEntity.create(self.data["name"])

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return bool(self.owning_entity)

    @property
    def owning_entity(self) -> OwningEntity:
        """Owning entity property.

        Owning entity which is represented by the data provided by user.

         Returns:
             OwningEntity: Owning entity object

        """
        if not self._owning_entity:
            try:
                self._owning_entity = OwningEntity.get_by_owning_entity_name(
                    self.data["name"]
                )
            except ResourceNotFound:
                return None
        return self._owning_entity
