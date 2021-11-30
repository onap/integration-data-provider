FROM python:3.9-slim AS builder

COPY requirements.txt /opt/app/onap_data_provider/requirements.txt

WORKDIR /opt/app/onap_data_provider/

RUN python -m pip install -r requirements.txt --prefix=/opt/install

FROM nexus3.onap.org:10001/onap/integration-python:9.1.0

COPY --from=builder --chown=onap:onap /opt/install /usr/local

COPY --chown=onap:onap . /opt/app/onap_data_provider

WORKDIR /opt/app/onap_data_provider/

RUN python setup.py install --user

ENV PATH=/home/onap/.local/bin

CMD ["onap-data-provider"]
