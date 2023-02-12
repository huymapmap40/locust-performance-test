#!/bin/bash

if [[ "$#" -lt 3 && "$#" -gt 4 ]]; then
  echo "usage: ./install.sh environments/<filename.yaml> <unique_release_name>"
  echo "usage with namespace: ./install.sh environments/<filename.yaml> tasksall/<team's folder> <unique_release_name> <namespace>"
  exit 1
fi

TASKS_TARGET_FOLDER="tasks"
testcase_filepath=$1
task_folder=$2
release_name=$3
namespace=${4:-locust}
echo "$release_name" > .RELEASE_NAME
echo "namespace: $namespace"
echo "task folder: $task_folder"

mkdir -p $TASKS_TARGET_FOLDER
cp -r $task_folder $TASKS_TARGET_FOLDER
helm upgrade --install -f values.yaml -f $testcase_filepath --namespace $namespace $release_name .
