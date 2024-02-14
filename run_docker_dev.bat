@echo off
set /p IMAGE_NAME="Enter the name of the Docker image: "
set /p CONTAINER_NAME="Enter the name for the container: "
docker run -d -it -p 8080:8080 --name %CONTAINER_NAME% -v "%cd%:/app" %IMAGE_NAME%
docker exec -it %CONTAINER_NAME% bash