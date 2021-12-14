Service
-------

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - name
     - string
     - YES
     -
   * - resources
     - List of `Service resources`_
     - NO
     -
   * - properties
     - List of `Service properties`_
     - NO
     -

.. _Service resources:

Service resources
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - name
     - string
     - YES
     - Name of existing SDC resource
   * - type
     - string
     - YES
     - Type of existing SDC resource (VF, PNF, etc.)

.. _Service properties:

Service properties
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - name
     - string
     - YES
     -
   * - type
     - string
     - YES
     -
   * - value
     - string
     - YES
     -
