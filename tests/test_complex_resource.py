from unittest.mock import patch, PropertyMock

from onapsdk.aai.cloud_infrastructure.complex import Complex

from onap_data_provider.resources.complex_resource import ComplexResource
from onapsdk.exceptions import ResourceNotFound


COMPLEX_DATA = {
    "physical-location-id": "123",
    "complex-name": "NB central office 1",
    "data-center-code": "veniam",
    "identity-url": "https://estevan.org",
    "physical-location-type": "centraloffice",
    "street1": "Ravensburgstraße",
    "street2": "123",
    "city": "Neubrandenburg",
    "state": "Mecklenburg-Vorpommern",
    "postal-code": "17034",
    "country": "DE",
    "region": "Mecklenburg Lakeland",
    "latitude": "53.5630015",
    "longitude": "13.2722710",
    "elevation": "100",
    "lata": "dolorem",
}


@patch("onap_data_provider.resources.complex_resource.Complex.get_all")
def test_complex_resource_complex(mock_complex_get_all):
    mock_complex_get_all.side_effect = ResourceNotFound
    mock_complex_get_all.return_value = iter([])
    complex_resource = ComplexResource(COMPLEX_DATA)
    assert complex_resource.complex is None
    mock_complex_get_all.side_effect = None
    mock_complex_get_all.return_value = iter([Complex(physical_location_id="123")])
    assert complex_resource.complex is not None


@patch(
    "onap_data_provider.resources.complex_resource.ComplexResource.complex",
    new_callable=PropertyMock,
)
def test_complex_resource_exists(mock_complex):
    mock_complex.return_value = None
    complex_resource = ComplexResource(COMPLEX_DATA)
    assert complex_resource.exists is False
    mock_complex.return_value = 1  # Anything but not None
    assert complex_resource.exists is True


@patch(
    "onap_data_provider.resources.complex_resource.ComplexResource.exists",
    new_callable=PropertyMock,
)
@patch("onap_data_provider.resources.complex_resource.Complex.create")
def test_complex_resource_create(mock_complex_create, mock_exists):
    mock_exists.return_value = True
    complex_resource = ComplexResource(COMPLEX_DATA)
    complex_resource.create()
    mock_complex_create.assert_not_called()

    mock_exists.return_value = False
    complex_resource.create()
    mock_complex_create.assert_called_once_with(
        physical_location_id="123",
        name="NB central office 1",
        data_center_code="veniam",
        identity_url="https://estevan.org",
        physical_location_type="centraloffice",
        street1="Ravensburgstraße",
        street2="123",
        city="Neubrandenburg",
        state="Mecklenburg-Vorpommern",
        postal_code="17034",
        country="DE",
        region="Mecklenburg Lakeland",
        latitude="53.5630015",
        longitude="13.2722710",
        elevation="100",
        lata="dolorem",
    )
