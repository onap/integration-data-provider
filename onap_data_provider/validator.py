"""Infra file schema validatior module."""
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

from typing import Any, Dict

import yaml
from jsonschema import validate  # type: ignore

from .versions import VersionsEnum


class Validator:
    """Validate input schema class."""

    def __init__(self) -> None:
        """Validate class initialization.

        Load schema file.

        """
        self.schemas: Dict[str, Any] = {}

    def validate(self, version: VersionsEnum, input_data: Dict[str, Any]) -> None:
        """Check if given input is valid from schema perspective.

        Args:
            input_data (Dict[str, Any]): Input to check

        Raises:
            ValidationError: Raises if input is invalid

        """
        if not version.value.version_number in self.schemas:
            with open(version.value.schema_path, "r") as schema_file:
                self.schemas[version.value.version_number] = yaml.safe_load(
                    schema_file.read()
                )
        validate(input_data, schema=self.schemas[version.value.version_number])
