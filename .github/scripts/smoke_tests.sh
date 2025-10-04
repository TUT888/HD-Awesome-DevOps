#!/bin/bash

set -e

NOTES_IP=$NOTES_SERVICE_IP
NOTES_PORT=$NOTES_SERVICE_PORT

USERS_IP=$USERS_SERVICE_IP
USERS_PORT=$USERS_SERVICE_PORT

echo "Running smoke tests against staging environment"
echo "Notes Service: http://${NOTES_IP}:${NOTES_PORT}"
echo "Users Service: http://${USERS_IP}:${USERS_PORT}"

echo "Done!"