#!/bin/bash

# Exit immediately if any command fails
set -e

echo "Current environment: $ENVIRONMENT"
echo "Waiting for LoadBalancer IPs to be assigned (up to 5 minutes)..."
NOTES_IP=""
USERS_IP=""

NOTES_PORT=""
USERS_PORT=""

for i in $(seq 1 10); do
  echo "Attempt $i/10 to get IPs..."
  NOTES_IP=$(kubectl get service notes-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}' -n $ENVIRONMENT)
  NOTES_PORT=$(kubectl get service notes-service -o jsonpath='{.spec.ports[0].port}' -n $ENVIRONMENT)
  
  USERS_IP=$(kubectl get service users-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}' -n $ENVIRONMENT)
  USERS_PORT=$(kubectl get service users-service -o jsonpath='{.spec.ports[0].port}' -n $ENVIRONMENT)

  if [[ -n "$NOTES_IP" && -n "$NOTES_PORT" ]]; then
    echo "Note Service LoadBalancer IPs assigned!"
    echo "NOTE Service IP: $NOTES_IP:$NOTES_PORT"
    break
  fi
  
  if [[ -n "$USERS_IP" && -n "$USERS_PORT" ]]; then
    echo "User Service LoadBalancer IPs assigned!"
    echo "NOTE Service IP: $NOTES_IP:$NOTES_PORT"
    echo "USER Service IP: $USERS_IP:$USERS_PORT"
    break
  fi

  sleep 5 # Wait 5 seconds before next attempt
done

if [[ -z "$NOTES_IP" || -z "$NOTES_PORT" || -z "$USERS_IP" || -z "$USERS_PORT" ]]; then
  echo "Error: One or more LoadBalancer IPs not assigned after timeout."
  exit 1 # Fail the job if IPs are not obtained
fi

# These are environment variables for subsequent steps in the *same job*
# And used to set the job outputs
echo "NOTES_IP=$NOTES_IP" >> $GITHUB_ENV
echo "NOTES_PORT=$NOTES_PORT" >> $GITHUB_ENV
echo "USERS_IP=$USERS_IP" >> $GITHUB_ENV
echo "USERS_PORT=$USERS_PORT" >> $GITHUB_ENV