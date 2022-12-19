"""CPS resources module."""
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
from abc import ABC
from typing import Any, Dict

from onapsdk.cps import Anchor, Dataspace, SchemaSet  # type: ignore
from onapsdk.exceptions import APIError, ResourceNotFound  # type: ignore

from onap_data_provider.resources.resource import Resource


class DataspaceSubresource(Resource, ABC):
    """Abstract dataspace subresource class."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize dataspace subresource"""
        super().__init__(data)

        self._dataspace: Dataspace = None
        self._schema_set: SchemaSet = None

    @property
    def dataspace(self) -> Dataspace:
        """Dataspace property.

        Return dataspace object by it name.

        Returns:
            Dataspace: Dataspace object.

        """
        return Dataspace(self.data["dataspace-name"])

    @property
    def schema_set(self) -> SchemaSet:
        """Schema set property.

        Raises:
            ValueError: Dataspace which name was used to get schema-set object doesn't exist

        Returns:
            SchemaSet: Schema set object

        """
        if not self._schema_set:
            try:
                self._schema_set = self.dataspace.get_schema_set(self.data["schema-set-name"])
            except APIError as api_error:
                # Needs to be fixed when https://gitlab.com/Orange-OpenSource/lfn/onap/python-onapsdk/-/issues/181 is done
                if "Dataspace not found" in str(api_error):
                    logging.error("Dataspace %s does not exist, create it before", self.data["dataspace-name"])
                    raise ValueError("Dataspace %s does not exist, create it before", self.data["dataspace-name"])
                elif "Schema Set not found" in str(api_error):
                    logging.info("Schema set %s not found", self.data["schema-set-name"])
                    return None
                else:
                    raise
        return self._schema_set


class AnchorResource(DataspaceSubresource):
    """Anchor resource class

    Creates CPS anchor
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize anchor resource"""
        super().__init__(data)

        self._anchor: Anchor = None

    def create(self) -> None:
        """Create anchor.

        Raises:
            ValueError: Schema set doesn't exist

        """
        if not self.schema_set:
            raise ValueError("Schema set %s does not exist, create it first", self.data["schema-set-name"])
        if not self.anchor:
            self.dataspace.create_anchor(self.schema_set, self.data["anchor-name"])

    @property
    def anchor(self) -> Anchor:
        """Anchor property.

        Tries to get anchor from dataspace.

        Returns:
            Anchor: Anchor object, if anchor already exists. None otherwise.

        """
        if not self._anchor:
            try:
                self._anchor = self.dataspace.get_anchor(self.data["anchor-name"])
            except APIError as api_error:
                if "Anchor not found" in str(api_error):
                    return None
                else:
                    raise
        return self._anchor


class SchemaSetResource(DataspaceSubresource):
    """Schema set resource class

    Creates CPS schema set and
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize schema set resource"""
        super().__init__(data)

    def create(self) -> None:
        """Create schema set resource."""
        if not self.schema_set:
            with open(self.data["schema-set-file"], "rb") as schema_set_file:
                self.dataspace.create_schema_set(self.data["schema-set-name"], schema_set_file)


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
            self._dataspace = Dataspace.create(self.data["dataspace-name"])
        except APIError as api_error:
            # Needs to be fixed when https://gitlab.com/Orange-OpenSource/lfn/onap/python-onapsdk/-/issues/181 is done
            if "409" in str(api_error):
                logging.warning("Dataspace %s already exists", self.data["dataspace-name"])
                self._dataspace = Dataspace(self.data["dataspace-name"])
            else:
                raise

        for schema_set_data in self.data.get("schema-sets", []):
            try:
                self._dataspace.get_schema_set(schema_set_data["schema-set-name"])
            except APIError:
                # Needs to be fixed when https://gitlab.com/Orange-OpenSource/lfn/onap/python-onapsdk/-/issues/181 is done
                with open(schema_set_data["schema-set-file"], "rb") as schema_set_file:
                    self._dataspace.create_schema_set(
                        schema_set_data["schema-set-name"],
                        schema_set_file
                    )
            else:
                logging.warning("Schema set %s already exists", schema_set_data["schema-set-name"])

        for anchor_data in self.data.get("anchors", []):
            try:
                self._dataspace.get_anchor(anchor_data["anchor-name"])
            except APIError:
                try:
                    schema_set: SchemaSet = self._dataspace.get_schema_set(anchor_data["schema-set-name"])
                except APIError:
                    logging.warning("Schema set %s does not exist, anchor won't be created",
                                    anchor_data["schema-set-name"])
                    continue
                self._dataspace.create_anchor(schema_set,
                                              anchor_data["anchor-name"])
            else:
                logging.warning("Anchor %s already exists", anchor_data["anchor-name"])

class AnchorNodeResource(DataspaceSubresource):
    """Anchor node resource class

    Creates CPS anchor node
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize anchor resource"""
        super().__init__(data)

        self._anchor: Anchor = None

    def create(self) -> None:
        """Create anchor node.

        Raises:
            ValueError: Schema set doesn't exist

        """
        if not self.schema_set:
            raise ValueError("Schema set %s does not exist, create it first", self.data["schema-set-name"])
        if not self.anchor:
            self._anchor.create_node(self.schema_set, self.data["anchor-name"])

    @property
    def anchor(self) -> Anchor:
        """Anchor property.

        Tries to get anchor from dataspace.

        Returns:
            Anchor: Anchor object, if anchor already exists. None otherwise.

        """
        if not self._anchor:
            try:
                self._anchor = self.dataspace.get_anchor(self.data["anchor-name"])
            except APIError as api_error:
                if "Anchor not found" in str(api_error):
                    return None
                else:
                    raise
        return self._anchor
