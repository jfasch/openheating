# -*- shell-script -*-

set -e

OH_USER=openheating
OH_GROUP=openheating
OH_WORKDIR=/var/run/openheating
OH_CONFDIR=/etc/openheating

if [ ! -d $OH_WORKDIR ]; then
    mkdir -p $OH_WORKDIR
    chown $OH_USER $OH_WORKDIR
    chgrp $OH_GROUP $OH_WORKDIR
fi

. /lib/lsb/init-functions
