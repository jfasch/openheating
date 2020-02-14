from . import locations

import os.path


def create(servicedef, sourcepath, generator_exe):
    lines = [
        '# generated by '+generator_exe,
        '',
        '[Unit]',
        'Description='+servicedef.description,
        'SourcePath='+sourcepath,
        '',
        '[Service]',
        'User=openheating',
        'Environment=PYTHONPATH='+locations.libdir,
        'ExecStart='+' '.join(
            [os.path.join(locations.bindir, servicedef.exe), '--system'] + \
            servicedef.args),
        'Type=dbus',
        'BusName='+servicedef.busname,
        '',
        '[Install]',
        'WantedBy=multi-user.target',
        '',
    ]
    basename, _ = os.path.splitext(servicedef.exe)

    return basename+'.service', servicedef.busname, '\n'.join(lines)
