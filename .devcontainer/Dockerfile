# https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md
ARG VARIANT=3.12-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ADD . /syntax

# ENV GIT_DISCOVERY_ACROSS_FILESYSTEM=1
# RUN apk update && apk upgrade
# RUN apk add -U bash curl github-cli jq yq

RUN python3 -m pip install --upgrade pip setuptools six wheel \
 && python3 -m pip install --no-cache-dir -r /syntax/requirements-dev.txt

ENV PATH=${PATH}:/syntax/.devcontainer/scripts
RUN chmod -R +x /syntax/.devcontainer/scripts
#ENTRYPOINT ["entrypoint.sh"]
