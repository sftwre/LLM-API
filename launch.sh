#!/bin/bash

# startup redis server
service redis-server start

# start uvicorn server
cd api
uvicorn main:app --host '0.0.0.0' --port '8000'