#!/bin/bash

# Instance details
PROJECT_ID="[YOUR_PROJECT_ID]"
ZONE="[YOUR_INSTANCE_ZONE]" # e.g., us-central1-a
INSTANCE_NAME="spin-1"

# Function to get CPU utilization using gcloud monitoring
get_cpu_usage() {
  # Query the CPU utilization for the last minute
  CPU_USAGE=$(/mnt/disks/deeplearning/usr/bin/gcloud monitoring metrics read \
    "compute.googleapis.com/instance/cpu/utilization" \
    --project="$PROJECT_ID" \
    --filter="metric.labels.instance_name=\"$INSTANCE_NAME\"" \
    --filter="resource.labels.zone=\"$ZONE\"" \
    --format="value(timeseries[0].point.value)" \
    --limit=1 \
    --interval="duration=60s")

  # Check if CPU usage was retrieved
  if [ -z "$CPU_USAGE" ]; then
    echo "Failed to retrieve CPU usage from Cloud Monitoring."
    exit 1
  fi

  # Return CPU usage (percentage)
  echo "$(echo "$CPU_USAGE * 100" | bc)"
}

# Main script
while true; do
  # Get the current CPU usage
  CPU_USAGE=$(get_cpu_usage)

  # Check if CPU usage is below 50%
  if (( $(echo "$CPU_USAGE < 50" | bc -l) )); then
    echo "CPU usage is below 50% ($CPU_USAGE%). Starting Freqtrade via Supervisor..."
    # Start Freqtrade using Supervisor
    supervisorctl start freqtrade
    break
  else
    echo "CPU usage is too high ($CPU_USAGE%). Retrying in 10 seconds..."
    sleep 10
  fi
done
