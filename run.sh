#!/bin/bash

docker run -d --env-file .env --network host \
-v ./output:/app/output \
--name port_scanner port_scanner:latest