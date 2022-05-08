## Dependencies
```
sudo apt-get install python3-gdal gdal-bin
```

## Installation

```
VENVNAME="hackenv"
python3 -m venv "${VENVNAME}"
PYTHONVERSION=$(ls ${VENVNAME}/lib/)
source "${VENVNAME}/bin/activate"
python3 -m pip install --upgrade pip
pip install -r requirements.txt
ln -s "/usr/lib/python3/dist-packages/osgeo" "${VENVNAME}/lib/${PYTHONVERSION}/site-packages/osgeo"
```