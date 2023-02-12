#!/usr/bin/env bash

if [[ $# -lt 2 ]]
  then
    echo "Usage: local_start.sh <target host> <test script>"
    exit 1
fi

args=("$@")

readonly TARGET_HOST="${args[0]}"
readonly TEST_SCRIPT="${args[1]}"
readonly TASKS_ROOT="${args[2]:-tasks}"

echo "Target Host: ${TARGET_HOST}"
echo "Test Script: ${TEST_SCRIPT}.py"
echo "Task Root: ${TASKS_ROOT}"
docker run --rm -it -v "$PWD/${TASKS_ROOT}:/locust-tasks" -e "LOCUST_HOST=http://${TARGET_HOST}" -e "LOCUST_LOCUSTFILE=/locust-tasks/${TEST_SCRIPT}.py" -p 8089:8089 locustio/locust:1.2.3
