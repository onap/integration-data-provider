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
from pathlib import Path

from onap_data_provider.config_loader import ConfigLoader


def test_config_loader_no_dirs():
    config_loader = ConfigLoader([Path(Path(__file__).parent, "test-data.yml")])
    configs = list(config_loader.load())
    assert len(configs) == 1

    config_loader = ConfigLoader([Path(Path(__file__).parent, "test-data.yml"),
                                  Path(Path(__file__).parent, "test-data-version.yml")])
    configs = list(config_loader.load())
    assert len(configs) == 2

def test_config_loader_dir():
    config_loader = ConfigLoader([Path(Path(__file__).parent, "config_dirs")])
    configs = list(config_loader.load())
    assert len(configs) == 2

def test_config_loader_both_dirs_and_files():
    config_loader = ConfigLoader([Path(Path(__file__).parent, "test-data.yml"),
                                  Path(Path(__file__).parent, "test-data-version.yml"),
                                  Path(Path(__file__).parent, "config_dirs")])
    configs = list(config_loader.load())
    assert len(configs) == 4
