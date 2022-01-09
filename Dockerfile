FROM python:3.6

COPY requirements.txt /

RUN pip install -r requirements.txt

ENV CONTAINER_VERSION=1.1

RUN pip install xtract-sdk==0.0.7a11 funcx funcx_endpoint
COPY xtract_hdf_main.py /
# COPY A002_Aerogel_025C_att0_Lq0_001_0001-5000.hdf /
