#!/bin/bash

docker run -d --rm --env-file .env --network host \
-v ./output:/app/output \
--name port_scanner port_scanner:latest