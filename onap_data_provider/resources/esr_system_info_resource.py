"""External system info resource module."""
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

from onapsdk.aai.cloud_infrastructure import CloudRegion, EsrSystemInfo  # type: ignore
from onapsdk.exceptions import APIError  # type: ignore

from .resource import Resource


class EsrSystemInfoResource(Resource):
    """ESR system info resource class."""

    def __init__(self, data: Dict[str, Any], cloud_region: CloudRegion) -> None:
        """ESR system info resource initialization.

        Args:
            data (Dict[str, Any]): Data needed to create esr system info
            cloud_region (CloudRegion): Cloud region for which esr system info is going to be created

        """
        super().__init__(data)
        self.cloud_region: CloudRegion = cloud_region
        self._esr_system_info: EsrSystemInfo = None

    @staticmethod
    def get_esr_info_by_id(
        cloud_region: CloudRegion, esr_syste_info_id: str
    ) -> EsrSystemInfo:
        """Get esr system info from Cloud region by it's ID.

        Iterate through cloud region's esr system infos and check
            if it's already have some with provided ID.

        Args:
            cloud_region (CloudRegion): CloudRegion object to check if esr system info already exists
            esr_syste_info_id (str): ESR system info ID to check.

        Returns:
            EsrSystemInfo: ESR system info object
        """
        for esr_system_info in cloud_region.esr_system_infos:
            if esr_system_info.esr_system_info_id == esr_syste_info_id:
                return esr_system_info

    def create(self) -> None:
        """Create ESR system info resource.

        Add ESR system info to provided cloud region

        """
        logging.debug(
            "Create ESR system info for %s cloud region",
            self.cloud_region.cloud_region_id,
        )
        if not self.exists:
            self.cloud_region.add_esr_system_info(
                esr_system_info_id=self.data["esr-system-info-id"],
                user_name=self.data["user-name"],
                password=self.data["password"],
                system_type=self.data["system-type"],
                service_url=self.data["service-url"],
                system_status="active",
                cloud_domain=self.data["cloud-domain"],
                default_tenant=self.data.get("default-tenant"),
            )
            self._esr_system_info = self.get_esr_info_by_id(
                self.cloud_region, self.data["esr-system-info-id"]
            )

    @property
    def exists(self) -> bool:
        """Determine if resource already exists or not.

        Returns:
            bool: True if object exists, False otherwise

        """
        return self.esr_system_info is not None

    @property
    def esr_system_info(self) -> EsrSystemInfo:
        """External system info property.

        Returns:
            EsrSystemInfo: EsrSystemInfo object

        """
        if self._esr_system_info is None:
            try:
                if (
                    esr_system_info := self.get_esr_info_by_id(
                        self.cloud_region, self.data["esr-system-info-id"]
                    )
                ) is not None:
                    self._esr_system_info = esr_system_info
            except APIError:
                logging.info("No esr system infos")
        return self._esr_system_info
