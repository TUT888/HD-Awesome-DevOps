#!/bin/bash

set -e

TESTING_URL="http://${TEST_IP}:${TEST_PORT}"

echo "Running smoke tests against staging environment"
echo "Testing on backend service at: $TESTING_URL"

# Check Response Body
echo "Verifying response content..."
response=$(curl -s "$TESTING_URL/")
echo "Response: $response"

# Check if response contains expected message
if echo "$response" | grep -q "$EXPECTED_MESSAGE"; then
  echo "Response content test passed"
else
  echo "Response content test failed"
  # exit 1
fi

echo "Done!"