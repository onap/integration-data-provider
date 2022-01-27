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
from onapsdk.cds import DataDictionarySet  # type: ignore

from onapsdk.exceptions import FileError  # type: ignore
from onap_data_provider.resources.resource import Resource


class DataDictionarySetResource(Resource):
    """DataDictionarySet resource class

    creates Data Dictionaries
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize data dictionary set resource

        Args:
            data (Dict[str, Any]): Data needed to create resource.
        """
        super().__init__(data)
        self._data_dictionaries: DataDictionarySet = None

    def create(self) -> None:
        """Create data dictionaries.

        Create data dictionaries from input data.
        """
        if self.data_dictionaries:
            self.data_dictionaries.upload()

    @property
    def data_dictionaries(self) -> DataDictionarySet:
        """Get DataDictionarySet.

        Returns:
            DataDictionarySet: Created DataDictionarySet containing DataDictionary instances.
        """
        if not self._data_dictionaries:
            try:
                self._data_dictionaries = DataDictionarySet.load_from_file(
                    self.data.get("file-path")
                )
            except FileError:
                logging.error(
                    f"Error when reading from file {self.data.get('file-path')}"
                )
                return None
        return self._data_dictionaries
