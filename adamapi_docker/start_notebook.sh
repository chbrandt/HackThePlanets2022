#!/usr/bin/env bash 

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

NBPORT=8881

if [[ -z "${SHARED_VOLUME}" ]]; then
    printf "\n\n\t> Please export an environment variable called 'SHARED_VOLUME' to run the container!\n\n"
else
    docker run --rm -it -p $NBPORT:$NBPORT \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "${SHARED_VOLUME}":/shared_volume \
    -v $script_dir/../notebooks:/shared_dir/notebooks \
    -v $script_dir/../data:/shared_dir/data \
    -v $script_dir/../hackp:/shared_dir/hackp \
    adamapiimg:latest /bin/bash -c \
    "source /opt/venv/adamapienv/bin/activate && jupyter notebook --ip='*' --port=$NBPORT --no-browser --allow-root --notebook-dir='/shared_dir/notebooks' --NotebookApp.token='' --NotebookApp.password=''"
fi
