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

from onap_data_provider.resources.cloud_region_resource import CloudRegionResource
from onap_data_provider.config_parser import ConfigParser


def test_create_cloud_region_resource():
    parser = ConfigParser([Path("tests/test-data.yml")])
    parsed_objects = list(parser.parse())
    assert isinstance(parsed_objects[1], CloudRegionResource)
    assert parsed_objects[1].data['cloud-owner'] == 'AMIST'
    assert parsed_objects[1].data['tenants'][0]['tenant-id'] == '-'.join(
        [parsed_objects[1].data['cloud-owner'], 'TENANT', '1'])
    assert parsed_objects[1].data['tenants'][1]['tenant-id'] == ''.join(
        [parsed_objects[1].data['cloud-owner'], '-', 'TENANT', '-', '2'])


def test_config_parser_versioning():
    parser = ConfigParser([Path("tests/test-data.yml")])
    config = parser.configs[0]
    assert config.version.value.version_number == "None"
    parsed_objects = list(parser.parse())
    assert isinstance(parsed_objects[1], CloudRegionResource)
    assert parsed_objects[1].data['cloud-owner'] == 'AMIST'
    assert parsed_objects[1].data['tenants'][0]['tenant-id'] == '-'.join(
        [parsed_objects[1].data['cloud-owner'], 'TENANT', '1'])
    assert parsed_objects[1].data['tenants'][1]['tenant-id'] == ''.join(
        [parsed_objects[1].data['cloud-owner'], '-', 'TENANT', '-', '2'])

    parser = ConfigParser([Path("tests/test-data-version.yml")])
    config = parser.configs[0]
    assert config.version.value.version_number == "1.0"
    parsed_objects = list(parser.parse())
    assert isinstance(parsed_objects[1], CloudRegionResource)
    assert parsed_objects[1].data['cloud-owner'] == 'AMIST'
    assert parsed_objects[1].data['tenants'][0]['tenant-id'] == '-'.join(
        [parsed_objects[1].data['cloud-owner'], 'TENANT', '1'])
    assert parsed_objects[1].data['tenants'][1]['tenant-id'] == ''.join(
        [parsed_objects[1].data['cloud-owner'], '-', 'TENANT', '-', '2'])

    parser = ConfigParser([Path("tests/test-data.yml"), Path("tests/test-data-version.yml")])
    assert parser.configs[0].version.value.version_number == "None"
    assert parser.configs[1].version.value.version_number == "1.0"
    parsed_objects = list(parser.parse())
    assert isinstance(parsed_objects[1], CloudRegionResource)
    assert parsed_objects[1].data['cloud-owner'] == 'AMIST'
    assert parsed_objects[1].data['tenants'][0]['tenant-id'] == '-'.join(
        [parsed_objects[1].data['cloud-owner'], 'TENANT', '1'])
    assert parsed_objects[1].data['tenants'][1]['tenant-id'] == ''.join(
        [parsed_objects[1].data['cloud-owner'], '-', 'TENANT', '-', '2'])

    parser = ConfigParser([Path("tests/test-data-2-0-version.yaml")])
    assert parser.configs[0].version.value.version_number == "2.0"