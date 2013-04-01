#!/bin/bash

. ./_env.sh

cd src
python manage.py test MomohaFeed
