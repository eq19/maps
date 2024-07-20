ARG FROM=postgres:latest
FROM ${FROM}

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_VERSION="2.26.2"
ARG GH_RUNNER_VERSION
ARG DOCKER_COMPOSE_VERSION="1.27.4"

ENV RUNNER_NAME=""
ENV RUNNER_WORK_DIRECTORY="_work"
ENV RUNNER_TOKEN=""
ENV RUNNER_REPOSITORY_URL=""
ENV RUNNER_LABELS=""
ENV RUNNER_ALLOW_RUNASROOT=true
ENV GITHUB_ACCESS_TOKEN=""
ENV PGLOG log_statement=all

ENV AGENT_TOOLSDIRECTORY=/opt/hostedtoolcache
RUN mkdir -p ${AGENT_TOOLSDIRECTORY}

ADD hooks /opt/runner
RUN chmod +x /opt/runner/*.sh

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

# Start PostgreSQL with custom configuration
COPY conf/pg_hba.conf /etc/postgresql/pg_hba.conf
COPY conf/postgresql.conf /etc/postgresql/postgresql.conf
COPY conf/docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        gcc \
        gettext \
        iputils-ping \
        jq \
        libc-dev \
        libcurl4-openssl-dev \
        liblttng-ust1 \
        libpq-dev \
        musl-dev \            
        openssh-client \
        plocate \
        postgresql-server-dev-all \
        python3 python3-pip python3-dev \
        software-properties-common \
        sudo \
        supervisor \
        unzip \
        wget \
        zlib1g-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Find the most recent 1.1 libssl package in the ubuntu archives
RUN cd /tmp && wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

# Install Docker CLI
RUN curl -fsSL https://get.docker.com -o- | sh && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Install Docker-Compose
RUN curl -L -o /usr/local/bin/docker-compose \
    "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" && \
    chmod +x /usr/local/bin/docker-compose

RUN updatedb
RUN cd /tmp && \
    curl -sL -o git.tgz \
    https://www.kernel.org/pub/software/scm/git/git-${GIT_VERSION}.tar.gz && \
    tar zxf git.tgz  && \
    cd git-${GIT_VERSION}  && \
    ./configure --prefix=/usr  && \
    make && \
    make install && \
    rm -rf /tmp/*

COPY requirements.txt requirements-dev.txt /tmp/pip-tmp/
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt
#RUN pipx install pre-commit ruff && pre-commit install
  
# Install pgvector and make sure the extension can be loaded
#RUN wget https://github.com/pgvector/pgvector/archive/refs/tags/v0.2.1.tar.gz
#RUN tar -xzf v0.2.1.tar.gz && cd pgvector-0.2.1 && make && make install
#RUN echo "shared_preload_libraries = 'vector'" >> /etc/postgresql/postgresql.conf

WORKDIR /home/runner
RUN GH_RUNNER_VERSION=${GH_RUNNER_VERSION:-$(curl --silent "https://api.github.com/repos/actions/runner/releases/latest" | grep tag_name | sed -E 's/.*"v([^"]+)".*/\1/')} && \
    curl -L -O https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz && \
    tar -zxf actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz && \
    rm -f actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz && \
    ./bin/installdependencies.sh && \
    chown -R root: /home/runner && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN chmod a+r /docker-entrypoint-initdb.d/*
RUN chown postgres:postgres /docker-entrypoint-initdb.d/*
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod 644 /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

#USER postgres
