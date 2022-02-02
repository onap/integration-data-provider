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
import logging
from typing import Any, Dict
from onapsdk.sdc.vsp import Vsp  # type: ignore
from onapsdk.sdc.sdc_resource import SdcResource  # type: ignore
from onapsdk.sdc.properties import Property  # type: ignore
from onapsdk.sdc.vfc import Vfc  # type: ignore

from .sdc_properties_mixins import SdcPropertiesMixins


class XnfResource(ABC, SdcPropertiesMixins):
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
        if data.get("deployment_artifact") is not None:
            self._xnf.add_deployment_artifact(
                artifact_type=data["deployment_artifact"]["artifact_type"],
                artifact_name=data["deployment_artifact"]["artifact_name"],
                artifact_label=data["deployment_artifact"]["artifact_label"],
                artifact=data["deployment_artifact"]["artifact_file_name"],
            )
        if (resources := data.get("resources")) is not None:
            for resource_data in resources:
                if resource_data["xnf_type"] == "VFC":
                    self._xnf.add_resource(Vfc(name=resource_data["name"]))
                else:
                    logging.warning(
                        f"Provided xNF resource of type {resource_data['xnf_type']} is not supported."
                    )
        self.set_properties(self._xnf, data.get("properties", []))
        self.set_inputs(self._xnf, data.get("inputs", []))
        self._xnf.onboard()
