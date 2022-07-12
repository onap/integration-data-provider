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
