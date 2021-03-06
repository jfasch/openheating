#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.base.error import HeatingError

from openheating.web.faschingbauer_app import FaschingbauerApp
from openheating.web import instance

from systemd.daemon import notify as sd_notify

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
parser.add_argument('--no-notify', action='store_true', 
                    help='Do not notify systemd about readiness (for example when started by hand during development)')
parser.add_argument('--templates', default='./templates', help='Jinja2 templates/ directory (default: ./templates)')
parser.add_argument('--static', default='./static', help='static/ directory (default: ./static)')
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname='org.openheating.http')
instance.app = FaschingbauerApp(
    flask_args = {
        'template_folder': args.templates,
        'static_folder': args.static,
    },
    dbus_connection = dbusutil.bus_from_argparse(args),
)

# notify systemd about readiness
if not args.no_notify:
    if not sd_notify("READY=1"):
        raise HeatingError('failed to notify systemd about readiness')

instance.app.run(host='0.0.0.0')
