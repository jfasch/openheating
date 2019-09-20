#!/usr/bin/python3

from openheating import logutil
from openheating.dbus import cmdline
from openheating.dbus.connection import Connection

from openheating.web.default_app import DefaultApp
from openheating.web import instance

from systemd.daemon import notify as sd_notify

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
cmdline.add_dbus_options(parser)
logutil.add_log_options(parser)
parser.add_argument('--no-notify', action='store_true', 
                    help='Do not notify systemd about readiness (for example when started by hand during development)')
parser.add_argument('--templates', default='./templates', help='Jinja2 templates/ directory (default: ./templates)')
parser.add_argument('--static', default='./static', help='static/ directory (default: ./static)')
args = parser.parse_args()

logutil.configure_from_argparse(args)
instance.app = DefaultApp(
    flask_args = {
        'template_folder': args.templates,
        'static_folder': args.static,
    },
    dbus_connection = Connection(is_session=cmdline.is_session(args)),
)

instance.app.setup()

# notify systemd about readiness
if not args.no_notify:
    if not sd_notify("READY=1"):
        raise HeatingError('failed to notify systemd about readiness')

instance.app.run(host='0.0.0.0')
