from pathlib import Path
import jsonschema
import yaml

with Path("/home/ubuntu/data-provider/onap_data_provider/schemas/infra_2_0.schema").open() as p:
    yschema = yaml.safe_load(p.read())
jsonschema.validate({"witam": "test"}, yschema)
