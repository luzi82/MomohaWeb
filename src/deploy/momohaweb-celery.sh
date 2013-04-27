#! /bin/sh
### BEGIN INIT INFO
# Provides:          MomohaWeb celery worker and beat
# Required-Start:    networking
# Required-Stop:     networking
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: MomohaWeb celery worker and beat
# Description:       MomohaWeb celery worker and beat
### END INIT INFO
#
#

#### SERVER SPECIFIC CONFIGURATION
PROJECT_ROOT=/opt/momohaweb/MomohaWeb
RUN_AS=momohaweb
RUNFILE=$PROJECT_ROOT/MomohaWebCelery.pid
#### DO NOT CHANGE ANYTHING AFTER THIS LINE!

set -e

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DESC="MomohaWeb Celery"
NAME=$0
SCRIPTNAME=/etc/init.d/$NAME

#
#       Function that starts the daemon/service.
#
d_start()
{
    if [ -f $RUNFILE ]; then
        echo -n " already running"
    else
        start-stop-daemon --start --quiet \
                   --pidfile $RUNFILE \
                   --background \
                   --chuid $RUN_AS --exec /usr/bin/env -- python \
                   $PROJECT_ROOT/src/manage.py \
                   celery worker -B -s $PROJECT_ROOT/celerybeat-schedule \
                   --loglevel=info \
                   --pidfile=$RUNFILE
    fi
}

#
#       Function that stops the daemon/service.
#
d_stop() {
    start-stop-daemon --stop --quiet --pidfile $RUNFILE \
                      || echo -n " not running"
    if [ -f $RUNFILE ]; then
       rm -f $RUNFILE
    fi
}

ACTION="$1"
case "$ACTION" in
    start)
        echo -n "Starting $DESC: $NAME"
        d_start
        echo "."
        ;;

    stop)
        echo -n "Stopping $DESC: $NAME"
        d_stop
        echo "."
        ;;

    restart|force-reload)
        echo -n "Restarting $DESC: $NAME"
        d_stop
        sleep 1
        d_start
        echo "."
        ;;

    *)
        echo "Usage: $NAME {start|stop|restart|force-reload}" >&2
        exit 3
        ;;
esac

exit 0
