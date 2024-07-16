# ---- Build the PostgreSQL Base ----
FROM postgres:latest AS postgres-base

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=postgresDB

# ---- Build the Python App ----
FROM python:3.12-bookworm

# Install supervisor
RUN apt-get update && \
    apt-get install -y supervisor

#WORKDIR /workspace

COPY . /maps

# Copy initialization script to create database and table
COPY conf/init-db.sql /docker-entrypoint-initdb.d/
COPY conf/query-db.sql /docker-entrypoint-initdb.d/

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /maps/requirements.txt

# Copy PostgreSQL binaries from the first stage
COPY --from=postgres-base /usr/local/bin /usr/local/bin
COPY --from=postgres-base /usr/lib/postgresql /usr/lib/postgresql
COPY --from=postgres-base /usr/share/postgresql /usr/share/postgresql
COPY --from=postgres-base /var/lib/postgresql /var/lib/postgresql

# Expose PostgreSQL port (optional, but useful for external access)
EXPOSE 5432 5455 8080

# Set environment variable to log all SQL statements
ENV PGLOG log_statement=all

# # Copy modified configuration files
COPY conf/postgresql.conf /etc/postgresql/postgresql.conf
COPY conf/pg_hba.conf /etc/postgresql/pg_hba.conf

# Add supervisord config
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]

# Run command to start PostgreSQL with custom configuration
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
