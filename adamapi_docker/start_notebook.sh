 #!/bin/bash 

if [[ -z "${SHARED_VOLUME}" ]]; then
    printf "\n\n\t> Please export an environment variable called 'SHARED_VOLUME' to run the container!\n\n"
else
    docker run --rm -it -p 8888:8888 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "${SHARED_VOLUME}":/shared_volume \
    -v $PWD/notebooks:/shared_dir \
    adamapiimg:latest /bin/bash -c \
    "source /opt/venv/adamapienv/bin/activate && jupyter notebook --ip='*' --port=8888 --no-browser --allow-root --notebook-dir='/shared_dir' --NotebookApp.token='' --NotebookApp.password=''"
fi