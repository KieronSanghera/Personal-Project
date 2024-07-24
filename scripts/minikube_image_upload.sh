#!/bin/bash

docker compose --file /Users/kieronsanghera/Projects/Personal-Project/docker/docker-compose.yaml build --no-cache

minikube image load file_gateway:latest
minikube image load file_storage:latest
minikube image load metadata_storage:latest
minikube image load file_release:latest

