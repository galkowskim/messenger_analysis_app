#!/bin/bash

read -p "Enter the name of the Docker image: " IMAGE_NAME
read -p "Enter the name for the container: " CONTAINER_NAME
docker run -d -it -p 8080:8080 --name $CONTAINER_NAME -v "$(pwd)":/app $IMAGE_NAME
docker exec -it $CONTAINER_NAME bash