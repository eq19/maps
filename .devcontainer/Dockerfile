ARG FROM=node:lts-bookworm-slim
FROM ${FROM}

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_VERSION="2.26.2"
ARG GH_RUNNER_VERSION
ARG DOCKER_COMPOSE_VERSION="1.27.4"

ENV RUNNER_NAME=""
ENV RUNNER_TOKEN=""
ENV RUNNER_LABELS=""
ENV RUNNER_REPOSITORY_URL=""
ENV RUNNER_WORK_DIRECTORY="_w"
ENV RUNNER_ALLOW_RUNASROOT=true

#ENV ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER=false
#ENV ACTIONS_RUNNER_CONTAINER_HOOKS=/opt/runner/index.js
ENV ACTIONS_RUNNER_HOOK_JOB_STARTED=/opt/runner/job_started.sh
ENV ACTIONS_RUNNER_HOOK_JOB_COMPLETED=/opt/runner/job_completed.sh

ENV GITHUB_ACCESS_TOKEN=""
ENV PGLOG log_statement=all
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV PIP_ROOT_USER_ACTION=ignore
#ENV AGENT_TOOLSDIRECTORY=/opt/hostedtoolcache

ADD hooks /opt/runner
RUN chmod +x /opt/runner/*.sh
#RUN mkdir -p ${AGENT_TOOLSDIRECTORY}

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
#COPY conf/pg_hba.conf /etc/postgresql/pg_hba.conf
#COPY conf/postgresql.conf /etc/postgresql/postgresql.conf
#COPY conf/docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/        

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && apt-get install -y \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        #docker.io \
        gettext \
        gh \
        git \
        iputils-ping \
        liblttng-ust1 \
        libcurl4-openssl-dev \
        libpq-dev \
        iputils-ping \
        jq \
        #npm \
        openssh-client \
        plocate \
        #postgresql \
        python3-pip \
        software-properties-common \
        sudo \
        supervisor \
        unzip \
        wget \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Find the most recent 1.1 libssl package in the ubuntu archives
RUN cd /tmp && wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

# Install Docker Engine
#RUN curl -fsSL https://get.docker.com -o- | sh && \
    #apt-get clean && \
    #rm -rf /var/lib/apt/lists/*

COPY *.txt /tmp/pip-tmp/
RUN python3 -m pip install --upgrade pip
RUN rm -rf /usr/lib/python3.*/EXTERNALLY-MANAGED
RUN pip install -r /tmp/pip-tmp/requirements-dev.txt
  
# Install pgvector and make sure the extension can be loaded
#RUN wget https://github.com/pgvector/pgvector/archive/refs/tags/v0.2.1.tar.gz
#RUN tar -xzf v0.2.1.tar.gz && cd pgvector-0.2.1 && make && make install
#RUN echo "shared_preload_libraries = 'vector'" >> /etc/postgresql/postgresql.conf

RUN updatedb
WORKDIR /home/runner
RUN GH_RUNNER_VERSION=${GH_RUNNER_VERSION:-$(curl --silent "https://api.github.com/repos/actions/runner/releases/latest" | grep tag_name | sed -E 's/.*"v([^"]+)".*/\1/')} && \
    curl -L -O https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz && \
    tar -zxf actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz && \
    rm -f actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz && \
    ./bin/installdependencies.sh && \
    chown -R root: /home/runner && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY scripts/entrypoint.sh /home/runner/entrypoint.sh
RUN chmod +x /home/runner/entrypoint.sh
ENTRYPOINT ["/home/runner/entrypoint.sh"]

#RUN chmod a+r /docker-entrypoint-initdb.d/*
#RUN chown postgres:postgres /docker-entrypoint-initdb.d/*
#CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod 644 /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
