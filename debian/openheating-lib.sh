# -*- shell-script -*-

. /lib/lsb/init-functions

OH_USER=openheating
OH_GROUP=openheating
OH_WORKDIR=/var/run/openheating
OH_CONFDIR=/etc/openheating

openheating_run_service() {
    local servicename=$1
    shift
    local description=$1
    shift
    local program=$1
    shift
    local program_args=$1
    shift

    local pidfile=$OH_WORKDIR/$servicename.pid
    local scriptname=/etc/init.d/$servicename

    [ -x "$program" ] || exit 1

    case "$1" in
	start)
	    log_daemon_msg "$description" "$servicename"
	    if [ ! -d $OH_WORKDIR ]; then
		mkdir -p $OH_WORKDIR
		chown $OH_USER $OH_WORKDIR
		chgrp $OH_GROUP $OH_WORKDIR
	    fi
	    start-stop-daemon --start --background --chuid=$OH_USER:$OH_GROUP --pidfile $pidfile --exec $program -- $program_args
	    ;;
	stop)
	    log_daemon_msg "Stopping $description" "$servicename"
	    start-stop-daemon --stop --pidfile $pidfile
	    ;;
	restart|force-reload)
	    $0 stop
	    $0 start
	    ;;
	status)
	    status_of_proc -p $pidfile $program $servicename && exit 0 || exit $?
	    ;;
	*)
	    echo "Usage: $scriptname {start|stop|rotate|restart|force-reload|status}" >&2
	    exit 3
	    ;;
    esac
}
