"""Versions class."""
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
from collections import namedtuple
from enum import Enum
from pathlib import Path


Version = namedtuple("Version", ["version_number", "schema_path", "deprecated"])


class VersionsEnum(Enum):
    """Class for storing information about supported versions."""

    V1_1 = Version(
        version_number="1.1",
        schema_path=Path(Path(__file__).parent, "schemas/infra_1_1.schema"),
        deprecated=False,
    )
    V1_0 = Version(
        version_number="1.0",
        schema_path=Path(Path(__file__).parent, "schemas/infra.schema"),
        deprecated=False,
    )
    V2_0 = Version(
        version_number="2.0",
        schema_path=Path(Path(__file__).parent, "schemas/infra_2_0.schema"),
        deprecated=False,
    )
    NONE = Version(
        version_number="None",
        schema_path=Path(Path(__file__).parent, "schemas/infra.schema"),
        deprecated=True,
    )

    @classmethod
    def get_version_by_number(cls, version_number: str) -> "VersionsEnum":
        """Get an enum element based on the given string version value.

        Because the version enum elements are not simple objects,
        but also have information about the path to the supported schema and
        whether this version is deprecated this method allows to retrieve
        the version only based on its value stored in the string format.

        Raises:
            ValueError: Provided version number is not supported

        Returns:
            VersionsEnum: The version enum

        """
        for version in cls:
            if version.value.version_number == version_number:
                if version.value.deprecated:
                    logging.warning(
                        f"This version [{version.value.version_number}] is deprecated, consider using the newer one!"
                    )
                return version
        raise ValueError(f"Version number {version_number} not supported")
