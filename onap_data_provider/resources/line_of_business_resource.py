"""Line of business resource module."""
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

from onapsdk.aai.business import LineOfBusiness  # type: ignore
from onapsdk.exceptions import ResourceNotFound  # type: ignore

from .resource import Resource


class LineOfBusinessResource(Resource):
    """Line of business resource class.

    Creates A&AI line of business.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize line of business resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        super().__init__(data)
        self._line_of_business: Optional[LineOfBusiness] = None

    def create(self) -> None:
        """Create line of business resource."""
        logging.debug(f"Create Line of business {self.data['name']}")
        if not self.exists:
            self._line_of_business = LineOfBusiness.create(self.data["name"])

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return bool(self.line_of_business)

    @property
    def line_of_business(self) -> LineOfBusiness:
        """Line of business property.

        Line of business which is represented by the data provided by user.

         Returns:
             LineOfBusiness: Line of business object

        """
        if not self._line_of_business:
            try:
                self._line_of_business = LineOfBusiness.get_by_name(self.data["name"])
            except ResourceNotFound:
                return None
        return self._line_of_business
