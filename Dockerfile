FROM python:3.8-slim

COPY . /opt/app/onap_data_provider/

WORKDIR /opt/app/onap_data_provider/

RUN python -m pip install -r requirements.txt

ENV PYTHONPATH=.

RUN python setup.py install

CMD ["onap-data-provider"]
