Requirements
============

python-dev (required by django-celery)

# apt-get install python-dev

Django

# pip install Django==1.4.5

django-celery

# pip install django-celery==3.0.11

feedparser

# pip install feedparser==5.1.3

pytz

# pip install pytz

lxml

# apt-get install gcc libxml2-dev libxslt-dev
# pip install lxml

south

# easy_install South


Deploy in Ubuntu 12.04 server
=============================

using nginx, PostgreSQL

# apt-get install python-pip python-dev gcc libxml2-dev libxslt-dev nginx python-flup git postgresql rabbitmq-server
# pip install Django==1.4.5 django-celery==3.0.11 feedparser==5.1.3 pytz lxml South psycopg2
# adduser --disabled-password momohaweb
# sudo -u postgres createuser -d -R -S momohaweb
# rabbitmqctl add_user momohaweb [password]
# rabbitmqctl add_vhost momohaweb_vhost
# rabbitmqctl set_permissions -p momohaweb_vhost momohaweb ".*" ".*" ".*"
# mkdir /opt/momohaweb
# chown momohaweb:momohaweb -R /opt/momohaweb 
# (create /etc/nginx/sites-available/momohaweb.conf)

server {
    listen 80;
    server_name [domain.com];
    access_log /var/log/nginx/momohaweb.access.log;
    error_log /var/log/nginx/momohaweb.error.log;

    location / {
        alias /opt/momohaweb/MomohaWeb/src/static/;
        expires 30d;
    }

    location /data/ {
        alias /opt/momohaweb/MomohaWeb/data/;
        expires 30d;
    }

    location /api/ {
        include fastcgi_params;
        fastcgi_pass 127.0.0.1:8080;
    }

}

# ln -s /etc/nginx/sites-available/hiauntie.conf /etc/nginx/sites-enabled/
# su - momohaweb

$ createdb momohaweb
$ (gen ssh key for github)
$ cd /opt/momohaweb
$ git clone --recurse-submodules git@github.com:luzi82/MomohaWeb.git
$ cd /opt/momohaweb/MomohaWeb
$ (create and modify /opt/momohaweb/MomohaWeb/src/MomohaWeb/secret.py from secret.py.example)
$ (modify /opt/momohaweb/MomohaWeb/src/MomohaWeb/settings.py)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'momohaweb',                      
        'USER': 'momohaweb',
        'PASSWORD': '[password]',
        'HOST': ''
    }
}

BROKER_URL = 'amqp://momohaweb:[password]@localhost:5672/momohaweb_vhost'

# cp /opt/momohaweb/MomohaWeb/src/deploy/momohaweb-django.sh /etc/init.d/momohaweb-django.sh
# update-rc.d momohaweb-django.sh defaults 90

$ cd /opt/momohaweb/MomohaWeb/src
$ python manage.py syncdb --migrate
$ python manage.py runfcgi host=127.0.0.1 port=8080


Get source code
===============

$ git clone --recurse-submodules git@github.com:luzi82/MomohaWeb.git


Coding conventions
==================

For date-time type, use int64, ms from 1970+UTC0.  Software date-time type is trouble.


Acknowledge
===========

Facebook share icon, from http://www.iconfinder.com/icondetails/43141/16/facebook_social_mediadhdydm_icon , by Paul Robert Lloyd

Twitter share icon, from http://www.iconfinder.com/icondetails/43178/16/social_media_twitter_icon , by Paul Robert Lloyd


Special thanks
==============

Google Reader Team.  Created one of the most useful web app ever.

Google.  Shut down Google Reader, give up the most powerful weapon in social network war, give MomohaFeed chance of rising.

Aaron Swartz.  He is the man.
