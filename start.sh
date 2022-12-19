#!/bin/bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install pipenv
alias pipenv=~/.local/bin/pipenv
rm get-pip.py
pipenv shell
pipenv update
apt install mariadb-server