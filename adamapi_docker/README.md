# Docker image for the adam api service

This docker image provides an Ubuntu container with python 3.8 and the adamapi Application Processing Interfaces python library.

## Using the image
Build the image with:
```
cd adamapi_docker
docker build --tag adamapiimg:latest .
```
Start a jupyter server inside a new container:
```
./start_notebook.sh
```
