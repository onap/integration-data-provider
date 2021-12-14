Usage
=====

This project is intended to be included in automation chain, e.g. triggered from the pipeline.
You can also run it locally using Python interpreter or Docker image.

Installation
------------

To run `onap-data-provider` Python >= 3.8 version is required. Install it using

.. code-block:: bash

    python setup.py install

command. You can call then

.. code-block:: bash

    onap-data-provider

command.

Run locally
^^^^^^^^^^^

When installed `onap-data-provider` is ready to work. We need some data to be created. Let's use `samples/vendor.yaml` and create SDC's Vendor resource. Call

.. code-block:: bash

    onap-data-provider -f samples/vendor.yaml

and in your ONAP instance Vendor resource should be created. If that resource already exists no new data will be created. Check `samples` directory to get more examples of files which describes resources to create.

You can use multiple files as an input:

.. code-block:: bash

    onap-data-provider -f samples/vendor.yaml -f samples/vsp.yaml

Directories could be used as well:

.. code-block:: bash

    onap-data-provider -f samples/

Configuration
^^^^^^^^^^^^^

Configuration is needed if your environment setup is different that usuall so ONAP components
listen on different hosts/ports than default, so are available on other URLs than:

.. code-block:: python

    AAI_URL     = "https://aai.api.sparky.simpledemo.onap.org:30233"
    CDS_URL     = "http://portal.api.simpledemo.onap.org:30449"
    MSB_URL     = "https://msb.api.simpledemo.onap.org:30283"
    SDC_BE_URL  = "https://sdc.api.be.simpledemo.onap.org:30204"
    SDC_FE_URL  = "https://sdc.api.fe.simpledemo.onap.org:30207"
    SDNC_URL    = "https://sdnc.api.simpledemo.onap.org:30267"
    SO_URL      = "http://so.api.simpledemo.onap.org:30277"
    VID_URL     = "https://vid.api.simpledemo.onap.org:30200"
    CLAMP_URL   = "https://clamp.api.simpledemo.onap.org:30258"
    VES_URL     = "http://ves.api.simpledemo.onap.org:30417"
    DMAAP_URL   = "http://dmaap.api.simpledemo.onap.org:3904"

If you want to use another URLs you need to override default `onap-data-provider` settings by create Python file with values you want to use.
Example: I want to test `onap-data-provider` data creation on my "test" ONAP instance which is available on "172.17.0.1" IP address,
so I need to create `my_test_onap_instance_settings.py` Python file which looks:

.. code-block:: python

    AAI_URL     = "https://172.17.0.1:30233"
    CDS_URL     = "http://172.17.0.1:30449"
    MSB_URL     = "https://172.17.0.1:30283"
    SDC_BE_URL  = "https://172.17.0.1:30204"
    SDC_FE_URL  = "https://172.17.0.1:30207"
    SDNC_URL    = "https://172.17.0.1:30267"
    SO_URL      = "http://172.17.0.1:30277"
    VID_URL     = "https://172.17.0.1:30200"
    CLAMP_URL   = "https://172.17.0.1:30258"
    VES_URL     = "http://172.17.0.1:30417"
    DMAAP_URL   = "http://172.17.0.1:3904"

and then if I call

.. code-block:: bash

    ONAP_PYTHON_SDK_SETTINGS=my_test_onap_instance_settings onap-data-provider ...

all data are going to be created on my local instance.

Set proxy
^^^^^^^^^

ONAP data provider can be run with proxy configured. You need to pass urls you want to use for proxy connection as `--proxy` arguments. Call `onap-data-provider -f <infra-file> --proxy http://localhost:8080 https://localhost:8080` to setup proxy for `http` and `https` on `localhost:8080` address.

Data verification
^^^^^^^^^^^^^^^^^

You can verify the data provided is correct, before you would try to actually push it
to the ONAP instance. To do so, use the flag `--validate-only`:

.. code-block:: bash

    onap-data-provider -f samples/vendor.yml --validate-only
