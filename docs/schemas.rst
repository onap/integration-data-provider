YAML schemas
============

Data consumed by Data provider needs to be described in `YAML <https://yaml.org/>`_ files. We used specific format:

.. code-block:: yaml

    odpSchemaVersion: # Version
    resources:
        # List of resources to create

.. toctree::
   :maxdepth: 3
   :caption: Available schema versions:

   schemas/version_1_0.rst
   schemas/version_1_1.rst

.. note::
   Versioning was not provided with the very beginning version of the data provider. To keep the backward compatibility
   we keep the old-time schema files support where you don't need to provide the version and resources section, version 1.0
   of schema would be used then by default.
   That format is deprecated and shouldn't be used.
