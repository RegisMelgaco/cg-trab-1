FROM --platform=$BUILDPLATFORM python:3.10 AS builder

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY api.py .
COPY raster.py .

CMD ["python3", "api.py"]
