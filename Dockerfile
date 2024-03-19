ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.04-py3
FROM ${BASE_IMAGE} as base-image

# Install Ray
RUN pip install "ray[default]==2.8.0"
RUN pip install "ray[serve]==2.8.0"

RUN pip install typing_extensions==4.4.0