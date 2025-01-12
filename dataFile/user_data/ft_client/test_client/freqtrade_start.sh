#!/bin/bash
while true; do
  # Get the current CPU utilization as an integer
  CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d. -f1)

  # Check if CPU utilization is below 50%
  if [ "$CPU_USAGE" -lt 50 ]; then
    echo "CPU usage is below 50% ($CPU_USAGE%). Starting Freqtrade..."
    supervisorctl start freqtrade
    break
  else
    echo "CPU usage is too high ($CPU_USAGE%). Retrying in 10 seconds..."
    sleep 10
  fi
done
