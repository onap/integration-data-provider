"""Data loader module."""
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
from pathlib import Path
from typing import Any, Iterator, List
import yaml
from onap_data_provider.tag_handlers import join, generate_random_uuid, resource_property

# register custom tag handlers in yaml.SafeLoader
yaml.add_constructor("!join", join, yaml.SafeLoader)
yaml.add_constructor("!uuid4", generate_random_uuid, yaml.SafeLoader)
yaml.add_constructor("!onap_resource_property", resource_property, yaml.SafeLoader)


class ConfigLoader:
    """Configuration loader class.

    Loads data from file resource.
    """

    YAML_EXTENSIONS = {".yml", ".yaml"}

    def __init__(self, config_file_path: List[Path]) -> None:
        """Initialize configuration loader class.

        Args:
            config_file_path (str): Path to yaml data source file.

        """
        self.config_file_path: List[Path] = config_file_path

    def _yamls_from_dir(self, dir: Path) -> Iterator[Path]:
        for child in dir.iterdir():  # type: Path
            if child.suffix in self.YAML_EXTENSIONS:
                yield child

    @property
    def _yamls(self) -> Iterator[Path]:
        for config_file_path in self.config_file_path:  # type: Path
            if config_file_path.is_file():
                yield config_file_path
            elif config_file_path.is_dir():
                yield from self._yamls_from_dir(config_file_path)
            else:
                raise ValueError("Provided path is neither file nor directory")

    def load(self) -> Iterator[Any]:
        """Get data from the config file.

        Get data from the config file and return parsed to dictionary resource.

        Returns:
             Any: Data from yaml file.

        """
        for yaml_path in self._yamls:  # type: Path
            with yaml_path.open() as f:
                yield yaml.safe_load(f)
