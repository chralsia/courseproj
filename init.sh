#!/usr/bin/env bash
source `which virtualenvwrapper.sh`
workon course
cd ~/Projects/courseproj
if [[ $1 = 'setup' ]]
then
    git pull https://rudenkonastya1996:13011996z@github.com/rudenkonastya1996/courseproj.git
    pip install -r requirements.txt
fi
firefox 127.0.0.1:8000 &
./manage.py runserver
