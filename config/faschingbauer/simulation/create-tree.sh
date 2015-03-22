#!/bin/sh

set -e

BASEDIR=/tmp/openheating-simulation

message() {
    echo $* 1>&2
}

if [ -d $BASEDIR ]; then
   message $BASEDIR exists, only cleaning dbus pidfile
   rm -f $BASEDIR/openheating-dbus-daemon.pid
   exit
fi

mkdir -p $BASEDIR
mkdir $BASEDIR/thermometers
mkdir $BASEDIR/switches

echo off > $BASEDIR/switches/pumpe-hk
echo off > $BASEDIR/switches/pumpe-ww
echo off > $BASEDIR/switches/oel-enable
echo off > $BASEDIR/switches/oel-burn
echo 20 > $BASEDIR/thermometers/boiler-top
echo 20 > $BASEDIR/thermometers/boiler-middle
echo 20 > $BASEDIR/thermometers/boiler-bottom
echo 20 > $BASEDIR/thermometers/hk-vl
echo 20 > $BASEDIR/thermometers/boiler-vl
echo 20 > $BASEDIR/thermometers/ofen-vl
echo 20 > $BASEDIR/thermometers/ofen
echo 20 > $BASEDIR/thermometers/oel-puffer
echo 20 > $BASEDIR/thermometers/essraum

