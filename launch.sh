#!/bin/bash

# startup redis server
service redis-server start

# start uvicorn server
uvicorn api.main:app --host '0.0.0.0' --port '8000'