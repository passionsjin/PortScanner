#!/bin/bash

docker run -d --env-file .env --network host --name port_scanner port_scanner:latest