#!/bin/bash

# Exit immediately if any command fails
set -e

echo "Current environment: $ENVIRONMENT"
echo "Waiting for Frontend LoadBalancer IPs to be assigned (up to 5 minutes)..."
FRONTEND_IP=""
FRONTEND_PORT=""

for i in $(seq 1 60); do
  echo "Attempt $i/60 to get IPs..."
  FRONTEND_IP=$(kubectl get service frontend-w10 -o jsonpath='{.status.loadBalancer.ingress[0].ip}' -n $ENVIRONMENT)
  FRONTEND_PORT=$(kubectl get service frontend-w10 -o jsonpath='{.spec.ports[0].port}' -n $ENVIRONMENT)

  if [[ -n "$FRONTEND_IP" && -n "$FRONTEND_PORT" ]]; then
    echo "Frontend LoadBalancer IP assigned!"
    echo "Frontend IP: $FRONTEND_IP:$FRONTEND_PORT"
    break
  fi
  sleep 5 # Wait 5 seconds before next attempt
done

if [[ -z "$FRONTEND_IP" || -z "$FRONTEND_PORT" ]]; then
  echo "Error: One or more LoadBalancer IPs not assigned after timeout."
  exit 1 # Fail the job if IPs are not obtained
fi

# These are environment variables for subsequent steps in the *same job*
# And used to set the job outputs
echo "FRONTEND_IP=$FRONTEND_IP" >> $GITHUB_ENV
echo "FRONTEND_PORT=$FRONTEND_PORT" >> $GITHUB_ENV