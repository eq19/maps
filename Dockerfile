ARG DEBIAN_FRONTEND=noninteractive
ARG FROM=node:lts-bookworm-slim
#ARG FROM=redis/redis-stack-server:latest
FROM ${FROM}

ENV RUNNER_NAME=""
ENV RUNNER_TOKEN=""
ENV RUNNER_LABELS=""
ENV RUNNER_REPOSITORY_URL=""
ENV RUNNER_ALLOW_RUNASROOT="1"     
ENV RUNNER_WORK_DIRECTORY="_work"

ARG IREE_VERSION
ARG GH_RUNNER_VERSION
ENV GITHUB_ACCESS_TOKEN=""
ENV PGLOG log_statement=all
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV PIP_ROOT_USER_ACTION=ignore
#ENV PATH="/usr/local/iree:${PATH}"

ADD . /home/runner
WORKDIR /home/runner
RUN chmod +x /home/runner/hooks/*.sh
RUN chmod +x /home/runner/scripts/*.sh
COPY dataFile/dump.rdb /data/dump.rdb
COPY conf/*.conf /etc/supervisor/conf.d/
RUN chmod 644 /etc/supervisor/conf.d/*.conf

#ENV ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER=false
#ENV ACTIONS_RUNNER_CONTAINER_HOOKS=/opt/runner/index.js
ENV ACTIONS_RUNNER_HOOK_JOB_STARTED=/home/runner/hooks/job_started.sh
ENV ACTIONS_RUNNER_HOOK_JOB_COMPLETED=/home/runner/hooks/job_completed.sh

LABEL maintainer="me@eq19.github.io" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.name="tcardonne/github-runner" \
    org.label-schema.description="Dockerized GitHub Actions runner." \
    org.label-schema.url="https://github.com/tcardonne/docker-github-runner" \
    org.label-schema.vcs-url="https://github.com/tcardonne/docker-github-runner" \
    org.label-schema.vendor="Thomas Cardonne" \
    org.label-schema.docker.cmd="docker run -it tcardonne/github-runner:latest"

# Find the required package in ubuntu
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq -o=Dpkg::Use-Pty=0 > /dev/null 2>&1
RUN sed "s/#.*//" /home/runner/requirements.apt | xargs apt-get install -yq -o=Dpkg::Use-Pty=0 > /dev/null 2>&1
RUN cd /tmp && wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

# Install dependencies
#RUN cd /home/runner && mkdir xml && DOXYGEN=$(doxygen > /dev/null 2>&1)
#RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=./.install
RUN npm install --package-lock-only redis talib pg mathjs gauss commander handlebars object-assign winston xml2js && npm ci

# Install iree-dist
#RUN IREE_VERSION=${IREE_VERSION:-$(curl -s https://api.github.com/repos/iree-org/iree/releases | jq -r 'map(select(.prerelease == true)) | .[0].tag_name' | sed 's/^iree-//')} && \
    #cd /tmp && wget -qO iree-dist.tar.xz https://github.com/iree-org/iree/releases/download/iree-$IREE_VERSION/iree-dist-$IREE_VERSION-linux-x86_64.tar.xz && \
    #mkdir -p /usr/local/iree && tar xf iree-dist.tar.xz -C /usr/local/iree --strip-components=1 && rm iree-dist.tar.xz

# Install only iree-run-module
RUN IREE_VERSION=${IREE_VERSION:-$(curl -s https://api.github.com/repos/iree-org/iree/releases | jq -r 'map(select(.prerelease == true)) | .[0].tag_name' | sed 's/^iree-//')} && \
    cd /tmp && wget -qO iree-dist.tar.xz https://github.com/iree-org/iree/releases/download/iree-$IREE_VERSION/iree-dist-$IREE_VERSION-linux-x86_64.tar.xz && \
    mkdir -p /usr/local/bin && tar -xJf iree-dist.tar.xz --wildcards --no-anchored 'iree-run-module' -O > /usr/local/bin/iree-run-module && \
    chmod +x /usr/local/bin/iree-run-module && rm iree-dist.tar.xz && iree-run-module --help
    
#Install Self host runner for Github Actions
RUN GH_RUNNER_VERSION=${GH_RUNNER_VERSION:-$(curl -s "https://api.github.com/repos/actions/runner/releases/latest" | grep tag_name | sed -E 's/.*"v([^"]+)".*/\1/')} && \
    curl -s -L -O https://github.com/actions/runner/releases/download/v$GH_RUNNER_VERSION/actions-runner-linux-x64-$GH_RUNNER_VERSION.tar.gz && \
    tar -zxf actions-runner-linux-x64-$GH_RUNNER_VERSION.tar.gz && rm -f actions-runner-linux-x64-$GH_RUNNER_VERSION.tar.gz && \
    ./bin/installdependencies.sh && chown -R root: /home/runner && apt-get clean && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/home/runner/scripts/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
