#!/bin/bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install pipenv
alias pipenv=~/.local/bin/pipenv
pipenv update