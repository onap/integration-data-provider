import warnings

from onap_data_provider.versions import VersionsEnum


def test_versions_init():
    v_none = VersionsEnum.get_version_by_number("None")
    assert v_none == VersionsEnum.NONE
    assert v_none.value.version_number == "None"
    assert v_none.value.schema_path

    v_1_0 = VersionsEnum.get_version_by_number("1.0")
    assert v_1_0 == VersionsEnum.V1_0
    assert v_1_0.value.version_number == "1.0"
    assert v_1_0.value.schema_path
