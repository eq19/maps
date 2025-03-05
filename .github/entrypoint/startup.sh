#!/bin/bash

# Fetch the config.json from Google Secret Manager
/mnt/disks/deeplearning/usr/bin/gcloud secrets versions access latest --secret=freqtrade-config > /home/runner/config.json

# Start Freqtrade
freqtrade trade --config /home/runner/config.json
