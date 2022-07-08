"""Customer resource module."""
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

import logging
from typing import Any, Dict
from onapsdk.cds import Blueprint, BlueprintModel  # type: ignore

from onapsdk.exceptions import ResourceNotFound  # type: ignore
from onap_data_provider.resources.resource import Resource


class BlueprintResourceTemplateResource(Resource):

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)

        self._blueprint: Blueprint = None
        self._blueprint_model: BlueprintModel = None

    def create(self) -> None:
        if self.blueprint:
            self.blueprint.store_resolved_template(
                artifact_name=self.data["artifact-name"],
                data=self.data["data"],
                resolution_key=self.data.get("resolution-key"),
                resource_type=self.data.get("resource-type"),
                resource_id=self.data.get("resource-id")
            )

    @property
    def blueprint_model(self) -> BlueprintModel:
        if not self._blueprint_model:
            try:
                self._blueprint_model = BlueprintModel.get_by_name_and_version(
                    blueprint_name=self.data["blueprint-name"],
                    blueprint_version=self.data["blueprint-version"]
                )
            except ResourceNotFound:
                logging.error(f"No blueprint with {self.data['blueprint-name']} name and {self.data['blueprint-version']} version")
                return None
        return self._blueprint_model

    @property
    def blueprint(self) -> Blueprint:
        if self.blueprint_model and not self._blueprint:
            self._blueprint = self.blueprint_model.get_blueprint()
        return self._blueprint
