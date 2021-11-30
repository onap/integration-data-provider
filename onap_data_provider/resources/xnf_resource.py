"""Xnf resource module."""
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

from abc import ABC
from typing import Any, Dict
from onapsdk.sdc.vsp import Vsp  # type: ignore
from onapsdk.sdc.sdc_resource import SdcResource  # type: ignore
from onapsdk.sdc.properties import Property  # type: ignore


class XnfResource(ABC):
    """Xnf resource class.

    Network function base class.
    """

    def __init__(self) -> None:
        """Initialize xnf resource."""
        self._xnf: SdcResource = None

    def onboard_resource_with_properties(self, data: Dict[str, Any]) -> None:
        """Set properties provided and instantiate SDC resource.

        Args:
            data (Dict[str, Any]): Data needed to create resource.

        """
        if (vsp_name := data.get("vsp")) is not None:
            self._xnf.vsp = Vsp(vsp_name)
        self._xnf.create()
        if (artifact_data := data.get("deployment_artifact")) is not None:
            self._xnf.add_deployment_artifact(
                artifact_type=data["deployment_artifact"]["artifact_type"],
                artifact_name=data["deployment_artifact"]["artifact_name"],
                artifact_label=data["deployment_artifact"]["artifact_label"],
                artifact=data["deployment_artifact"]["artifact_file_name"],
            )
        for property_data in data.get("properties", []):
            self._xnf.add_property(
                Property(
                    name=property_data["name"],
                    property_type=property_data["type"],
                    value=property_data.get("value"),
                )
            )
        self._xnf.onboard()
