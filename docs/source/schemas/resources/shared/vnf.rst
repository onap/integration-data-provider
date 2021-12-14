VNF
---

.. |XNF| replace:: VNF

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
   * - vsp
     - string
     - NO
     -
   * - deployment_artifact
     - `VNF deployment artifact`_
     - NO
     -
   * - properties
     - List of `VNF properties`_
     - NO
     -

.. _VNF deployment artifact:

.. include:: resources/shared/xnf_deployment_artifact.rst

.. _VNF properties:

.. include:: resources/shared/xnf_property.rst