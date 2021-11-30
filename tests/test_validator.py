from pytest import raises
from jsonschema import ValidationError

from onap_data_provider.validator import Validator
from onap_data_provider.versions import VersionsEnum


def test_validator_customer():
    validator = Validator()
    input_data = {
        "customers": [
            {
                "customer": {
                    "global-customer-id": "test",
                    "subscriber-name": "test",
                    "subscriber-type": "test",
                }
            }
        ]
    }
    validator.validate(VersionsEnum.NONE, input_data)
    input_data = {
        "customers": [
            {
                "customer": {
                    "global-customer-id": "test",
                    "subscriber-name": "test",
                    "subscriber-type": "test",
                }
            }
        ]
    }
    validator.validate(VersionsEnum.V1_0, input_data)

    invalid_input_data = {  # Missing subscriber-type
        "customers": [
            {"customer": {"global-customer-id": "test", "subscriber-name": "test"}}
        ]
    }
    with raises(ValidationError):
        validator.validate(VersionsEnum.V1_0, invalid_input_data)


def test_validator_vsps():
    validator = Validator()
    input_data = {
        "vsps": [
            {
                "vsp": {
                    "name": "test",
                    "vendor": "test",
                    "package": "test",
                }
            }
        ]
    }
    validator.validate(VersionsEnum.NONE, input_data)

    input_data = {
        "vsps": [
            {
                "vsp": {
                    "name": "test",
                    "vendor": "test",
                    "package": "test",
                }
            }
        ]
    }
    validator.validate(VersionsEnum.V1_0, input_data)

    input_data = {
        "vsps": [
            {
                "vsp": {
                    "name": "test",
                }
            }
        ]
    }
    with raises(ValidationError):
        validator.validate(VersionsEnum.V1_0, input_data)


def test_validator_service():
    validator = Validator()
    input_data = {
        "services": [
            {
                "service": {
                    "name": "test",
                    "resources": [
                        {"name": "test", "type": "test"},
                        {"name": "test1", "type": "test2"},
                    ],
                    "properties": [
                        {"name": "test", "type": "test", "value": "test"},
                        {"name": "test1", "type": "test1"},
                    ],
                }
            }
        ]
    }
    validator.validate(VersionsEnum.NONE, input_data)

    input_data = {
        "services": [
            {
                "service": {
                    "name": "test",
                    "resources": [
                        {"name": "test", "type": "test"},
                        {"name": "test1", "type": "test2"},
                    ],
                    "properties": [
                        {"name": "test", "type": "test", "value": "test"},
                        {"name": "test1", "type": "test1"},
                    ],
                }
            }
        ]
    }
    validator.validate(VersionsEnum.V1_0, input_data)
