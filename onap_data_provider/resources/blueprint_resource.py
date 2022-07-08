"""Blueprint resource module."""
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

from onapsdk.exceptions import FileError, ResourceNotFound  # type: ignore
from onap_data_provider.resources.resource import Resource


class BlueprintResource(Resource):

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)

        self._blueprint: Blueprint = None
        self._blueprint_model: BlueprintModel = None

    def create(self) -> None:
        enriched_blueprint: Blueprint = self.blueprint.enrich()
        enriched_blueprint.publish()

    @property
    def blueprint(self) -> Blueprint:
        if not self._blueprint:
            self._blueprint = Blueprint.load_from_file(self.data["blueprint-file-path"])
        return self._blueprint
