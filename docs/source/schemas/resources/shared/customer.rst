Customer
--------

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - global-customer-id
     - string
     - YES
     -
   * - subscriber-name
     - string
     - YES
     -
   * - subscriber-type
     - string
     - YES
     -
   * - service-subscriptions
     - List of `Service subscriptions`_
     - NO
     -

.. _Service subscriptions:

Service subscription
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - service-type
     - string
     - YES
     -
   * - tenants
     - List of `Service subscription tenant relationships`_
     - NO
     -

.. _Service subscription tenant relationships:

Service subscription tenant relationship
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - tenant-id
     - string
     - YES
     -
   * - cloud-owner
     - string
     - YES
     -
   * - cloud-region-id
     - string
     - YES
     -
