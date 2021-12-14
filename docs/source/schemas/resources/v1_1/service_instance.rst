Service instance
----------------

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - service_instance_name
     - string
     - YES
     -
   * - service_name
     - string
     - YES
     -
   * - cloud_region
     - string
     - YES
     -
   * - customer_id
     - string
     - YES
     -
   * - owning_entity
     - string
     - YES
     -
   * - project
     - string
     - YES
     -
   * - platform
     - string
     - YES
     -
   * - line_of_business
     - string
     - YES
     -
   * - cloud_region_id
     - string
     - YES
     -
   * - cloud_owner
     - string
     - YES
     -
   * - timeout
     - number
     - NO
     -
   * - aai_service
     - string
     - YES
     -
   * - service_subscription_type
     - string
     - NO
     -
   * - instantiation_parameters
     - List of `Instantiation parameters`_
     - YES
     -

.. _Instantiation parameters:

Instantiation parameters
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - vnf_name
     - string
     - NO
     -
   * - parameters
     - List of key-value parameters
     - NO
     -
   * - vf_modules
     - List of `VF modules instantiation parameters`_
     - NO
     -

.. _VF modules instantiation parameters:

VF modules instantiation parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - name
     - string
     - NO
     - Name of the vf module
   * - parameters
     - List of key-value parameters
     - NO
     -
