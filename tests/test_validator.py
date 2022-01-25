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


def test_validator_vnf():
    validator = Validator()
    input_data = {
        "vnfs": [
            {
                "vnf": {
                    "name": "test",
                    "vsp": "testvsp",
                    "inputs": [
                        {"name": "itest", "type": "string", "value": "itest"},
                        {"name": "itest1", "type": "boolean"},
                        {"name": "itest2", "value": True},
                    ],
                }
            }
        ]
    }
    validator.validate(VersionsEnum.V1_0, input_data)
    validator.validate(VersionsEnum.V1_1, input_data)


def test_validator_service():
    validator = Validator()
    input_data = {
        "services": [
            {
                "service": {
                    "name": "test",
                    "resources": [
                        {"name": "test", "type": "test"},
                        {
                            "name": "test1",
                            "type": "test2",
                            "properties": [{"name": "test0", "value": "test1"}],
                        },
                    ],
                    "properties": [
                        {"name": "test", "type": "string", "value": "test"},
                        {"name": "test1", "type": "boolean"},
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
