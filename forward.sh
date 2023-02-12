#!/bin/bash

release_name=$(cat .RELEASE_NAME)
echo "Forwarding $release_name"

namespace=${1:-locust}
echo "namespace: $namespace"

counter=0
until [ $counter -gt 5 ] || nc -z localhost 8089 > /dev/null 2>&1; do ((counter++)); sleep 1; done && open 'http://localhost:8089' &
kubectl port-forward -n $namespace svc/$(cat .RELEASE_NAME) 8089:8089
