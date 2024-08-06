#!/bin/bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install pipenv
alias pipenv=~/.local/bin/pipenv
rm get-pip.py
pipenv shell
# установка пакетов из .lock (заданные версии) без обновления версий окружения
pipenv install
#pipenv run pip install psycopg2-binary
#apt install mariadb-server
mkdir migrations/tmp sandbox/tmp
chmod 777 -Rf migrations/tmp sandbox/tmp

make start

python migrations/execute.py