# Use official PostgreSQL image
FROM postgres:latest

# Set environment variable for superuser password
# ENV POSTGRES_PASSWORD=password

# Copy initialization script to create database and table
# COPY init-db.sql /docker-entrypoint-initdb.d/
# COPY query-db.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port (optional, but useful for external access)
# EXPOSE 5432

# Set environment variable to log all SQL statements
# ENV PGLOG log_statement=all

# # Copy modified configuration files
COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf

# Run command to start PostgreSQL with custom configuration
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
# CMD ["postgres"]

