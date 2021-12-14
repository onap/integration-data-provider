MSB k8s definition
------------------

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
   * - version
     - string
     - YES
     -
   * - chart-name
     - string
     - NO
     -
   * - description
     - string
     - NO
     -
   * - artifact
     - string
     - YES
     - Path to the artifact file
   * - profiles
     - List of `Profiles`_
     - NO
     -


.. _Profiles:

MSB k8s profile
---------------

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
   * - namespace
     - string
     - YES
     -
   * - k8s-version
     - string
     - YES
     -
   * - artifact
     - string
     - YES
     - Path to the profile artifact
