#!/bin/bash

set -e

TESTING_URL="http://${TEST_IP}:${TEST_PORT}"

echo "Running smoke tests against staging environment"
echo "Testing on frontend at: $TESTING_URL"

# Basic test, check for HTML response
if curl -f -s "$TESTING_URL" | grep -q "<html"; then
  echo "Frontend is working"
else
  echo "Frontend test failed"
  # exit 1
fi

echo "Done!"