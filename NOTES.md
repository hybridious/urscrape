# Notes on setting up the virtual environment for the first time

cd urscrape
pyvenv .
source bin/activate [or run custom activate]

sudo apt-get install libxml2-dev libxslt-dev
pip install lxml
pip install -e .
