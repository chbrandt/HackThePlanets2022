FROM ubuntu:20.04

LABEL maintainer="leonardo.baroncelli@inaf.it"
LABEL version="0.1"
LABEL description="This is custom Docker Image that encapsulate the adam api."

WORKDIR /shared_dir

RUN apt update
RUN apt upgrade -y

# Install python 3.8
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.8 -y
RUN apt install python3-pip -y

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
RUN update-alternatives --set python /usr/bin/python3.8 

RUN python -m pip install --upgrade pip && \
    apt-get install python3-gdal gdal-bin -y && \
    apt install python3.8-venv -y

RUN python -m venv /opt/venv/adamapienv
ENV VENVNAME="/opt/venv/adamapienv"
ENV PATH="${VENVNAME}/bin:$PATH"
RUN pip install adamapi==2.0.9 jupyter
RUN ln -s "/usr/lib/python3/dist-packages/osgeo" "${VENVNAME}/lib/python3.8/site-packages/osgeo"

RUN pip install pandas matplotlib tqdm

RUN pip install geopandas shapely rasterio

RUN pip install tensorflow tensorflow_datasets

RUN pip install astropy

RUN echo "which python"
RUN echo "source ${VENVNAME}/bin/activate && jupyter notebook --ip='*' --port=8888 --no-browser --allow-root" >> /app/start_notebook.sh
