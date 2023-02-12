#!/usr/bin/env bash

#######################################################
# Initiate an environment to run the test
#
# Usage   : ./setup.sh <your-service>
# Example : ./setup.sh challenge-service
#######################################################

args=("$@")
set -eou pipefail

readonly SERVICE_NAME="${args[0]}"

readonly NAMESPACE="locust"
readonly RELEASE_NAME="${NAMESPACE}-${SERVICE_NAME}"
readonly PORT="8089"

printf "\n\nAccessing Locust Dashboard using http://127.0.0.1:%s\n\n\n" "${PORT}"

set -x

cd ..

helm upgrade --install \
  --values="values.yaml" \
  --values="environments/test_${SERVICE_NAME}.yaml" \
  --namespace="${NAMESPACE}" \
  "${RELEASE_NAME}" .

sleep 15s

kubectl port-forward \
  --namespace="${NAMESPACE}" \
  "svc/${RELEASE_NAME}" "${PORT}:${PORT}"
