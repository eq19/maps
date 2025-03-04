FROM python:3.12.7-slim-bookworm as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PATH=/home/ftuser/.local/bin:$PATH
ENV FT_APP_ENV="docker"

# Prepare environment
RUN mkdir /freqtrade \
  && apt-get update \
  && apt-get -y install sudo libatlas3-base curl sqlite3 libhdf5-serial-dev libgomp1 \
  && apt-get clean \
  && useradd -u 1000 -G sudo -U -m -s /bin/bash ftuser \
  && chown ftuser:ftuser /freqtrade \
  # Allow sudoers
  && echo "ftuser ALL=(ALL) NOPASSWD: /bin/chown" >> /etc/sudoers

WORKDIR /freqtrade

# Install dependencies
FROM base as python-deps
RUN  apt-get update \
  && apt-get -y install build-essential libssl-dev git libffi-dev libgfortran5 pkg-config cmake gcc \
  && apt-get clean \
  && pip install --upgrade pip wheel

# Install TA-lib
ADD user_data/build_helpers/ /tmp/
RUN cd /tmp && ./install_ta-lib.sh > /dev/null 2>&1

# Install dependencies
USER ftuser
ENV LD_LIBRARY_PATH /usr/local/lib
RUN  pip install --user --no-cache-dir "numpy<2.0" \
  && pip install --user --no-cache-dir -r /tmp/requirements-hyperopt.txt

# Copy dependencies to runtime-image
FROM base as runtime-image

COPY --from=python-deps /usr/local/lib /usr/local/lib
COPY --from=python-deps --chown=ftuser:ftuser /home/ftuser/.local /home/ftuser/.local

# Install and execute
USER ftuser

WORKDIR /freqtrade
ENV LD_LIBRARY_PATH /usr/local/lib
RUN pip install --user --no-cache-dir --no-build-isolation freqtrade@https://github.com/KernelPatterns/freqtrade/releases/download/v0.0.56/freqtrade-dev0.0.56-py3-none-any.whl \
  && mkdir /freqtrade/user_data/ \
  && freqtrade install-ui

ENTRYPOINT ["freqtrade"]
# Default to trade mode
CMD [ "trade" ]
