# ONAP data provider

Data ingestion service for ONAP

## Description

Data provider is a project to provide a tool to automate common ONAP resource creation. For many of tasks in ONAP some resources are needed and could be created once, like cloud region, complex or customer in A&AI. With that tool it can be automated to create them for every ONAP instance. It can be also used to create requested resource on already running instance on demand.

## Usage
This project is intended to be included in automation chain, e.g. triggered from the pipeline.
You can also run it locally using Python interpreter or Docker image.

### Installation

To run `onap-data-provider` Python >= 3.8 version is required. Install it using
```
python setup.py install
```
command. You can call then
```
onap-data-provider
```
command.

### Run locally

When installed `onap-data-provider` is ready to work. We need some data to be created. Let's use `samples/vendor.yaml` and create SDC's Vendor resource. Call
```
onap-data-provider -f samples/vendor.yaml
```
and in your ONAP instance Vendor resource should be created. If that resource already exists no new data will be created. Check `samples` directory to get more examples of files which describes resources to create.

You can use multiple files as an input:
```
onap-data-provider -f samples/vendor.yaml -f samples/vsp.yaml
```

Directories could be used as well:
```
onap-data-provider -f samples/
```

### Configuration

Configuration is needed if your environment setup is different that usuall so ONAP components listen on different hosts/ports than default, so are available on other URLs than:

```
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
```

If you want to use another URLs you need to override default `onap-data-provider` settings by create Python file with values you want to use. Example: I want to test `onap-data-provider` data creation on my "test" ONAP instance which is available on "172.17.0.1" IP address, so I need to create `my_test_onap_instance_settings.py` Python file which looks:
```
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
```
and then if I call
```
ONAP_PYTHON_SDK_SETTINGS=my_test_onap_instance_settings onap-data-provider ...
```
all data are going to be created on my local instance.

### Set proxy

ONAP data provider can be run with proxy configured. You need to pass urls you want to use for proxy connection as `--proxy` arguments. Call `onap-data-provider -f <infra-file> --proxy http://localhost:8080 https://localhost:8080` to setup proxy for `http` and `https` on `localhost:8080` address.

## Data verification

You can verify the data provided is correct, before you would try to actually push it
to the ONAP instance. To do so, use the flag `--validate-only`:
```
onap-data-provider -f samples/vendor.yml --validate-only
```
For reference, please see example data files under `samples/` directory.

## Development and testing

The following utilities are used within the project:
 - Black
 - mypy
 - pydocstyle

To run all the tests (unit tests, linter and mypy checks), install tox and then run it:
```
pip install tox
tox .
```

## Licenses

The software that data-provider is built on uses the following licenses.

* Apache 2 License: onapsdk
* MIT license: PyYAML, jsonschema
