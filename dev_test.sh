#!/bin/bash

. ./_env.sh

cd src

if [ "$#" = "0" ]; then
	python manage.py test MomohaFeed
elif [ "$#" = "1" ]; then
	python manage.py test MomohaFeed.SimpleTest.${1}
fi
