ARG VARIANT=3.12-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}
# https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md

ADD . /syntax

ARG GH_RUNNER_VERSION
ARG GIT_VERSION="2.26.2"
ARG DOCKER_COMPOSE_VERSION="1.27.4"
ARG DEBIAN_FRONTEND=noninteractive

ENV RUNNER_NAME=""
ENV RUNNER_TOKEN=""
ENV RUNNER_LABELS=""
ENV GITHUB_ACCESS_TOKEN=""
ENV RUNNER_REPOSITORY_URL=""
ENV RUNNER_ALLOW_RUNASROOT=true
ENV RUNNER_WORK_DIRECTORY="_work"
ENV PIP_ROOT_USER_ACTION=ignore
ENV AGENT_TOOLSDIRECTORY=/opt/hostedtoolcache
ENV PATH=${PATH}:/syntax/.devcontainer/scripts
RUN chmod -R +x /syntax/.devcontainer/scripts

LABEL maintainer="me@tcardonne.fr" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.name="tcardonne/github-runner" \
    org.label-schema.description="Dockerized GitHub Actions runner." \
    org.label-schema.url="https://github.com/tcardonne/docker-github-runner" \
    org.label-schema.vcs-url="https://github.com/tcardonne/docker-github-runner" \
    org.label-schema.vendor="Thomas Cardonne" \
    org.label-schema.docker.cmd="docker run -it tcardonne/github-runner:latest"

#RUN apt-get update && \
    #apt-get install -y \
RUN sudo DEBIAN_FRONTEND=noninteractive apt-get -qy update && \
    sudo DEBIAN_FRONTEND=noninteractive apt-get -qy install \
        #sudo \
        #curl \
        #unzip \
        #apt-transport-https \
        #ca-certificates \
        #software-properties-common \
        #jq \
        #iputils-ping \
        #build-essential \
        #zlib1g-dev \
        #gettext \
        #libcurl4-openssl-dev \
        #openssh-client \
        #liblttng-ust1 \
        supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN sudo cp /syntax/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN sudo chmod 644 /etc/supervisor/conf.d/supervisord.conf
RUN sudo ls -alR /etc/supervisor

#RUN python3 -m pip install --upgrade pip setuptools six wheel && \
    #python3 -m pip install -r /syntax/requirements-dev.txt

RUN cd /tmp && \
    wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

# Install Docker CLI
#RUN curl -fsSL https://get.docker.com -o- | sh && \
    #rm -rf /var/lib/apt/lists/* && \
    #apt-get clean

# Install Docker-Compose
#RUN curl -L -o /usr/local/bin/docker-compose \
    #"https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" && \
    #chmod +x /usr/local/bin/docker-compose

#RUN cd /tmp && \
    #curl -sL -o git.tgz \
    #https://www.kernel.org/pub/software/scm/git/git-${GIT_VERSION}.tar.gz && \
    #tar zxf git.tgz  && \
    #cd git-${GIT_VERSION}  && \
    #./configure --prefix=/usr  && \
    #make && \
    #make install && \
    #rm -rf /tmp/*

RUN mkdir -p /home/runner ${AGENT_TOOLSDIRECTORY}

WORKDIR /home/runner

RUN GH_RUNNER_VERSION=${GH_RUNNER_VERSION:-$(curl --silent "https://api.github.com/repos/actions/runner/releases/latest" | grep tag_name | sed -E 's/.*"v([^"]+)".*/\1/')} \
    && curl -L -O https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
    && tar -zxf actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
    && rm -f actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
    && ./bin/installdependencies.sh \
    && chown -R root: /home/runner \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

ENTRYPOINT ["entrypoint.sh"]
CMD ["sudo", "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
