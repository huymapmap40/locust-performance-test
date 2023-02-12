#!/usr/bin/env bash

args=("$@")
set -eou pipefail

readonly LOCUST_SCRIPT="${args[0]}"

source venv/bin/activate

set -x

locust --locustfile "tasks/${LOCUST_SCRIPT}.py"
