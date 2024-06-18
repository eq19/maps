# https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md
ARG VARIANT=3.12-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}
COPY *.txt /tmp/pip-tmp/
RUN python3 -m pip install --upgrade pip setuptools six wheel \
 && python3 -m pip install --no-cache-dir -r /tmp/pip-tmp/requirements-dev.txt
