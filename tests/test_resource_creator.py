import pytest

from onap_data_provider.resources.cloud_region_resource import CloudRegionResource
from onap_data_provider.resources.complex_resource import ComplexResource
from onap_data_provider.resources.resource_creator import ResourceCreator
from onap_data_provider.versions import VersionsEnum


def test_create_cloud_region_resource():
    cloud_region_resource = ResourceCreator.create("cloud-region", {"a": "B"}, VersionsEnum.NONE)
    assert isinstance(cloud_region_resource, CloudRegionResource)
    assert cloud_region_resource.data == {"a": "B"}
    cloud_region_resource = ResourceCreator.create("cloud-region", {"a": "B"}, VersionsEnum.V1_0)
    assert isinstance(cloud_region_resource, CloudRegionResource)
    assert cloud_region_resource.data == {"a": "B"}


def test_create_complex_resource():
    complex_resource = ResourceCreator.create("complex", {"a": "B"}, VersionsEnum.NONE)
    assert isinstance(complex_resource, ComplexResource)
    assert complex_resource.data == {"a": "B"}
    complex_resource = ResourceCreator.create("complex", {"a": "B"}, VersionsEnum.V1_0)
    assert isinstance(complex_resource, ComplexResource)
    assert complex_resource.data == {"a": "B"}


def test_create_invalid_resource():
    with pytest.raises(ValueError):
        ResourceCreator.create("invalid", {}, VersionsEnum.NONE)
    with pytest.raises(ValueError):
        ResourceCreator.create("invalid", {}, VersionsEnum.V1_0)
