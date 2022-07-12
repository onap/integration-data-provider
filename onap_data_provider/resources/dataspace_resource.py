"""CPS dataspace resource module."""
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
from onapsdk.cps import Dataspace, SchemaSet  # type: ignore
from onapsdk.exceptions import APIError  # type: ignore

from onap_data_provider.resources.resource import Resource


class DataspaceResource(Resource):
    """DataspaceResource resource class

    Creates CPS dataspace and sub-resources
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize dataspace resource"""
        super().__init__(data)

        self._dataspace: Dataspace = None

    def create(self) -> None:
        try:
            self._dataspace = Dataspace.create(self.data["name"])
        except APIError as api_error:
            # Needs to be fixed when https://gitlab.com/Orange-OpenSource/lfn/onap/python-onapsdk/-/issues/181 is done
            if "409" in str(api_error):
                logging.warning("Dataspace %s already exists", self.data["name"])
                self._dataspace = Dataspace(self.data["name"])
            else:
                raise

        for schema_set_data in self.data.get("schema-sets", []):
            try:
                self._dataspace.get_schema_set(schema_set_data["name"])
            except APIError:
                # Needs to be fixed when https://gitlab.com/Orange-OpenSource/lfn/onap/python-onapsdk/-/issues/181 is done
                with open(schema_set_data["schema-set-file"], "rb") as schema_set_file:
                    self._dataspace.create_schema_set(
                        schema_set_data["name"],
                        schema_set_file
                    )
            else:
                logging.warning("Schema set %s already exists", schema_set_data["name"])

        for anchor_data in self.data.get("anchors", []):
            try:
                self._dataspace.get_anchor(anchor_data["name"])
            except APIError:
                try:
                    schema_set: SchemaSet = self._dataspace.get_schema_set(anchor_data["schema-set-name"])
                except APIError:
                    logging.warning("Schema set %s does not exist, anchor won't be created",
                                    anchor_data["schema-set-name"])
                    continue
                self._dataspace.create_anchor(schema_set,
                                              anchor_data["name"])
            else:
                logging.warning("Anchor %s already exists", anchor_data["name"])
