#!/bin/bash

# docker run -it -p 8089:8089 -e LOCUST_HOST=http://host.docker.internal:8080 -e LOCUST_LOCUSTFILE=/mnt/locust/test_ecommerce.py -v /Users/siyong/shopback/repo/locust/tasks:/mnt/locust locustio/locust:0.14.5 


docker run --rm -it -v $PWD/tasks:/locust-tasks -e "TARGET_URL=http://host.docker.internal:8080" -e "LOCUSTFILE_PATH=/locust-tasks/test_payment-linked-offers.py" -p 8089:8089 locustio/locust:0.14.5 
