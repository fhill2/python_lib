#!/usr/bin/env sh

# note: this can be installed/updated directly from the git repo:
# https://stackoverflow.com/a/56483981

# create the virtual environment
rm -rf .venv
python3 -m venv .venv
source ./.venv/bin/activate

# had to run this to avoid .egg error
pip install --upgrade setuptools pip


# python3 -m venv ~/.venv/python_lib/

# https://stackoverflow.com/a/49414977
# why install pyenv to 


# -e -> installs as editable mode
# installs cwd packages into the venv 
pip install -e .
# pip install -r requirements/starfarm.txt
