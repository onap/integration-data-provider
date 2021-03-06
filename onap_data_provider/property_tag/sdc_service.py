"""SDC property module used by tag to get resource's property"""
"""
   Copyright 2022 Deutsche Telekom AG

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

from typing import Optional

from onapsdk.onap_service import OnapService  # type: ignore
from onapsdk.sdc.service import Service  # type: ignore

from .base import BasePropertyTagResource


class SdcServicePropertyTagResource(BasePropertyTagResource):
    """Class to get property from SDC service module objects."""

    def __init__(self, property_name: str, service_name: str, version: Optional[str] = None) -> None:
        """Initialize object.

        Get the name of the property to get, serivce name and optional version of the service.

        Args:
            property_name (str): Property name
            service_name (str): Service name
            version (Optional[str], optional): Optional version. If no version is given
                the latest version of the service will be loaded. Defaults to None.
        """
        super().__init__(property_name)
        self.service_name: str = service_name
        self.version: Optional[str] = version

    @property
    def resource(self) -> Service:
        """Service resource.

        Returns:
            Service: Service with the provided name and version.

        """
        return Service(self.service_name, version=self.version)
