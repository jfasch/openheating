from . import locations

import os.path


def create(servicedef, sourcepath, generator_exe):
    lines = [
        '# generated by '+generator_exe,
        '',
        '[Unit]',
        'Description='+servicedef.description,
        'SourcePath='+sourcepath,
    ]

    for w in servicedef.wants:
        lines.append('Wants='+w)
        lines.append('After='+w)

    lines += [
        '',
        '[Service]',
        'User=openheating',
        'Environment=PYTHONPATH='+locations.libdir,
        'ExecStart='+' '.join(
            [os.path.join(locations.bindir, servicedef.exe), '--system'] + \
            servicedef.args),
        'Type=dbus',
        'BusName='+servicedef.busname,
    ]

    if len(servicedef.wantedby):
        lines += [
            '',
            '[Install]',
            '# technically, [Install] is not interpreted by systemd,',
            '# but by sytemctl\'s "enable" and "disable" commands (to',
            '# create and remove symlinks). so this is completely ',
            '# irrelevant for generated units',
        ]
        for w in servicedef.wantedby:
            lines.append('WantedBy='+w)

    return '\n'.join(lines)

