#!/bin/bash

rm -rf data 
rm sqlite.db

cd src
# python manage.py syncdb --migrate --noinput
python manage.py syncdb --noinput
cat ../dev_init.sh.py.in | python manage.py shell >> /dev/null
