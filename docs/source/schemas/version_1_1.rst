Schema v1.1
===========

To use v1.1 schema you need to use:

.. code-block:: yaml

    odpSchemaVersion: 1.1
    resources:
        # List of resources to create

.. |version| replace:: v1.1

.. contents:: Table of Contents
   :local:

.. include:: /schemas/resources/shared/aai_service_design_and_creation_service.rst

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
     - List of `Cloud region's tenants 1.1`_
     - NO
     -
   * - est-system-infos
     - List of `ESR sytem infos 1.1`_
     - NO
     -
   * - complex
     - string
     - NO
     - physical-location-id of the complex to create relationship with
   * - available-zones
     - List of `Availability zones 1.1`_
     - NO
     -

.. _Cloud region's tenants 1.1:

.. include:: /schemas/resources/shared/cloud_region_tenants.rst

.. _ESR sytem infos 1.1:

.. include:: /schemas/resources/shared/cloud_region_esr_system_infos.rst

.. _Availability zones 1.1:

.. include:: /schemas/resources/shared/cloud_region_availability_zones.rst

.. include:: /schemas/resources/shared/complex.rst

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
     - List of `Service subscriptions 1.1`_
     - NO
     -

.. _Service subscriptions 1.1:

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
     - List of `Service subscription tenant relationships 1.1`_
     - NO
     -

.. _Service subscription tenant relationships 1.1:

.. include:: /schemas/resources/shared/customer_service_subscription_tenant_relationship.rst

.. include:: /schemas/resources/shared/vendor.rst

.. include:: /schemas/resources/shared/vsp.rst

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
     - List of `Service resources 1.1`_
     - NO
     -
   * - properties
     - List of `Service properties 1.1`_
     - NO
     -

.. _Service resources 1.1:

.. include:: /schemas/resources/shared/service_resources.rst

.. _Service properties 1.1:

.. include:: /schemas/resources/shared/service_properties.rst

PNF
---

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
   * - vendor
     - string
     - NO
     -
   * - vsp
     - string
     - NO
     -
   * - category
     - string
     - NO
     -
   * - subcategory
     - string
     - NO
     -
   * - deployment_artifact
     - `PNF deployment artifact 1.1`_
     - NO
     -
   * - properties
     - List of `PNF Properties 1.1`_
     - NO
     -

.. _PNF deployment artifact 1.1:

.. include:: /schemas/resources/shared/xnf_deployment_artifact.rst

.. _PNF properties 1.1:

.. include:: /schemas/resources/shared/xnf_property.rst

VNF
---

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
   * - vendor
     - string
     - NO
     -
   * - vsp
     - string
     - NO
     -
   * - category
     - string
     - NO
     -
   * - subcategory
     - string
     - NO
     -
   * - deployment_artifact
     - `VNF deployment artifact 1.1`_
     - NO
     -
   * - properties
     - List of `VNF properties 1.1`_
     - NO
     -

.. _VNF deployment artifact 1.1:

.. include:: /schemas/resources/shared/xnf_deployment_artifact.rst

.. _VNF properties 1.1:

.. include:: /schemas/resources/shared/owning_entity.rst

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
     - List of `Profiles 1.1`_
     - NO
     -

.. _Profiles 1.1:

.. include:: /schemas/resources/shared/msb_profile.rst

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
     - List of `Instantiation parameters 1.1`_
     - YES
     -

.. _Instantiation parameters 1.1:

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
     - List of `VF modules instantiation parameters 1.1`_
     - NO
     -

.. _VF modules instantiation parameters 1.1:

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
