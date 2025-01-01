#!/bin/bash

# Start PostgreSQL in the background
docker-entrypoint.sh postgres &

# Run freqtrade application
freqtrade trade
