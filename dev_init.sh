#!/bin/bash

rm -rf data 
rm -f sqlite.db

cd src
python manage.py syncdb --migrate --noinput

cat ../_dev_init.sh.py.in | python manage.py shell >> /dev/null
