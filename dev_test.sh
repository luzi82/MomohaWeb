#!/bin/bash

. ./_env.sh

cd src

if [ "$#" = "0" ]; then
	python manage.py test MomohaFeed
	python manage.py test KyubeyUser
elif [ "$#" = "2" ]; then
	python manage.py test ${1}.SimpleTest.${2}
fi
