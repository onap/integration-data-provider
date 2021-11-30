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
