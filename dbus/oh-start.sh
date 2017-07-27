#!/bin/sh

OH_ROOT=$HOME/work/openheating

_message() {
    echo $* 1>&2
}
_debug() {
    _message DEBUG: $*
}
_warn() {
    _message WARN: $*
}
_error() {
    _message ERROR: $*
}

_BUSPID=$OH_ROOT/dbus/run/openheating-dbus-daemon.pid
_BUSSOCKET=$OH_ROOT/dbus/run/openheating-dbus-daemon.socket

_PROCESSES=''
trap 'for p in $_PROCESSES; do kill $p; done' EXIT

_start() {
    command=$*

    $command &
    _PROCESSES="$_PROCESSES $!"
}

_start_bus() {
    if [ -f $_BUSPID ]; then
	pid=$(cat $_BUSPID)
	if kill -0 $pid; then
	    _error bus daemon still running, PID $pid
	    return 1
	fi
	_warn found stale bus daemon PID file $_BUSPID, removing
	rm $_BUSPID
	rm -f $_BUSSOCKET
    fi

    _start dbus-daemon --config-file $OH_ROOT/dbus/busconf/openheating-dbus-daemon.conf

    local nwaits=0
    while [ ! -S $_BUSSOCKET ]; do
	((nwaits++))
	sleep 0.5
	[ $nwaits -ge 3 ] && _warn $_BUSSOCKET not '(yet)' there, waiting ...
    done
}

_start_thermometer_service() {
    _start $OH_ROOT/dbus/dbus-thermometer-service.py
}

_start_bus
_start_thermometer_service

wait
