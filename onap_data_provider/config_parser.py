"""Data parser module."""
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
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
from .config_loader import ConfigLoader
from .resources.resource import Resource
from .resources.resource_creator import ResourceCreator
from .validator import Validator
from .versions import VersionsEnum


class Config:
    """Config class."""

    VERSION_TAG = "odpSchemaVersion"

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize config object.

        Args:
            config (Dict[str, Any]): Entites files content loaded by loader.

        """
        self.config: Dict[str, Any] = config

    @property
    def version(self) -> VersionsEnum:
        """Config file version.

        Files with entities are versioned to keep backward compatibility.
        Each config keep the version number and that value is represented
            by that property.

        Returns:
            VersionsEnum: VersionsEnum class object

        """
        return VersionsEnum.get_version_by_number(
            str(self.config.get(self.VERSION_TAG))
        )

    @property
    def resources(self) -> Dict[str, Any]:
        """Resources dictionary.

        Dictionary with definition of objects to be created in ONAP.

        Returns:
            Dict[str, Any]: Resources dictionary

        """
        if self.version == VersionsEnum.NONE:
            return self.config
        resources: Dict[str, Any] = self.config["resources"]
        return resources


class ConfigParser:
    """Configuration parser class.

    Processes data loaded from resource.
    """

    def __init__(self, config_file_path: List[Path]) -> None:
        """Initialize configuration parser class.

        Args:
            config_file_path (str): Path to yaml data source file.

        """
        self._config_file_path: List[Path] = config_file_path
        self._config_loader: ConfigLoader = ConfigLoader(self._config_file_path)
        self._configs: Optional[List[Config]] = None
        self._validator: Optional[Validator] = None
        self._PRIORITY_ORDER = (
            "complexes",
            "cloud-regions",
            "vendors",
            "vsps",
            "pnfs",
            "vnfs",
            "services",
            "customers",
            "msb-k8s-definitions",
            "aai-services",
            "service-instances",
        )

    def parse(self) -> Iterator[Resource]:
        """Parser method.

        Invokes factory method to create objects from nested data dictionary.

        Returns:
            Iterator[Resource]: Iterator of Resource type objects.

        """
        for config in self.configs:
            for resource in self._get_ordered_resources(config.resources):
                for resource_type, data in resource.items():
                    yield ResourceCreator.create(resource_type, data, config.version)

    def _get_ordered_resources(
        self, resources_data: Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """Resources helper method.

        Generates data in fixed order defined in _PRIORITY_ORDER property.

        Args:
            resources_data (Dict[str, Any]): Dictionary generated from YAML infra file.

        Returns:
            Dict[str, Any]: Iterator of Dict type objects where key is the name
            of resource type, and the value is actual resource data.

        """
        ordered_resources: Dict[str, Any] = OrderedDict.fromkeys(
            self._PRIORITY_ORDER, {}
        )
        ordered_resources.update(resources_data)
        for ordered_resource in ordered_resources.values():
            for resource_data in ordered_resource:
                yield resource_data

    @property
    def configs(self) -> List[Config]:
        """Config loaded using loader.

        Returns:
            Dict[str, Any]: Config

        """
        if self._configs is None:
            self._configs = [Config(config) for config in self._config_loader.load()]
        return self._configs

    @property
    def validator(self) -> Validator:
        """Property which stores validator object.

        Used to validate provided data.

        Returns:
            Validator: Validator object

        """
        if not self._validator:
            self._validator = Validator()
        return self._validator

    def validate(self) -> None:
        """Validate provided resources.

        Checks whether the data provided by the user are correct.
        """
        for config in self.configs:
            self.validator.validate(config.version, config.resources)
