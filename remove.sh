#!/bin/bash
TASKS_TARGET_FOLDER="tasks"
namespace=${1:-locust}
echo "namespace: $namespace"

helm uninstall $(cat .RELEASE_NAME) -n $namespace
rm -rf $TASKS_TARGET_FOLDER
