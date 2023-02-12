#!/usr/bin/env bash

#######################################################
# Cleanup the environment after completing the test
#######################################################

set -eou pipefail

readonly NAMESPACE="locust"

readarray -t RELEASES < <(
  helm list --namespace="${NAMESPACE}" --output=json |
    jq --compact-output ".[]"
)

declare -ra RELEASES

uninstall() {
  local -r release_name=$(echo "$1" | jq --raw-output ".name")
  local -r command="helm uninstall ${release_name} --namespace=${NAMESPACE}"

  # Execute the $command
  echo "+ ${command}"
  ${command} && sleep 5s
}

for release in "${RELEASES[@]}"; do
  uninstall "$release"
done
