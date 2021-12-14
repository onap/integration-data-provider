Cloud region
------------

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - cloud-owner
     - string
     - YES
     -
   * - cloud-region-id
     - string
     - YES
     -
   * - orchestration-disabled
     - string
     - YES
     -
   * - in-maint
     - string
     - YES
     -
   * - cloud-type
     - string
     - NO
     -
   * - kube-config
     - string
     - NO
     - Path to kubernetes config file
   * - tenants
     - List of `Cloud region's tenants`_
     - NO
     -
   * - est-system-infos
     - List of `ESR sytem infos`_
     - NO
     -
   * - complex
     - string
     - NO
     - physical-location-id of the complex to create relationship with
   * - available-zones
     - List of `Availability zones`_
     - NO
     -

.. _Cloud region's tenants:

Cloud region's tenant
^^^^^^^^^^^^^^^^^^^^^

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
   * - tenant-name
     - string
     - YES
     -
   * - tenant-context
     - string
     - NO
     -

.. _ESR sytem infos:

ESR sytem info
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - esr-system-info-id
     - string
     - YES
     -
   * - user-name
     - string
     - YES
     -
   * - password
     - string
     - YES
     -
   * - system-type
     - string
     - YES
     -
   * - service-url
     - string
     - YES
     -
   * - cloud-domain
     - string
     - YES
     -
   * - default-tenant
     - string
     - NO
     -

.. _Availability zones:

Availability zone
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Required
     - Comment
   * - availability-zone-name
     - string
     - YES
     -
   * - hypervisor-type
     - string
     - YES
     -
