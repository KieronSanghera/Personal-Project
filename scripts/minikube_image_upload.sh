#!/bin/bash

docker compose --file /Users/kieronsanghera/Projects/Personal-Project/docker/docker-compose.yaml build --no-cache

kubectl scale deployments --replicas=0 --all

sleep 3

minikube image rm file_gateway
minikube image rm file_storage
minikube image rm metadata_storage
minikube image rm file_management

minikube image load file_gateway:latest
minikube image load file_storage:latest
minikube image load metadata_storage:latest
minikube image load file_management:latest

kubectl scale deployments --replicas=1 --all
