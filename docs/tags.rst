ONAP data provider custom YAML tags
===================================

In ONAP data provider we created a few custom YAML tags which could be used (and useful) in entities files.

!join tag
---------

Concatenate multiple strings in YAML value.

`!join [a, b, c]` result is `abc`

`!join ['_', [a, b, c]]` result is `a_b_c`

!uuid4 tag
----------

Generates a random UUID4

`!uuid4` result is random UUID4 value

!onap_resource_property
-----------------------

Gets the property value from the already existing ONAP resources.

Available resources:

* SDC service

`!onap_resource_property service identifier service-model-name` result is a SDC service "service-model-name" model "identifier" property value

`!onap_resource_property service identifier service-model-name 1.0` result is a SDC service "service-model-name" version 1.0 model "identifier" property value
