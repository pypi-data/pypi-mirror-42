# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 -- Lars Heuer.
# All rights reserved.
#
# License: BSD License
#
"""\
Script um eine fischertechnik-App für die Community Firmware zu erstellen.

Das Script erstellt das Manifest, sowie ein Standard-Icon und ein Python-Script.
"""
from __future__ import absolute_import, print_function
import os
import io
import re
import uuid
import base64
import datetime
import click
try:
    # Py 2
    open = io.open
    str = unicode
except NameError:
    pass

__version__ = '0.0.1'

_ICON = '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'

_SCRIPT = u'''#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""fischertechnik App - Copyright (c) {year} -- {author}
"""
import sys
from TouchStyle import *


class FtcGuiApplication(TouchApplication):
    """{descr}
    """
    def __init__(self, args):
        super(FtcGuiApplication, self).__init__(args)
        win = TouchWindow("{app_name}")
        win.show()
        self.exec_()


if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
'''


def _validate_app_name(ctx, param, value):
    u"""\
    Überprüfe, ob der name zu lang ist.
    """
    if len(value) > 15:
        raise click.BadParameter(u'Bitte wähle einen kürzeren Namen (max. 15 Zeichen)')
    return value


def _validate_script_name(ctx, param, value):
    u"""\
    Überprüfe, ob der Name des Scripts okay ist.
    """
    if not re.match(r'^[a-zA-Z][\w]*\.py$', value):
        raise click.BadParameter(u'Bitte wähle einen anderen Namen für das Script')
    return value


def _validate_directory(ctx, param, value):
    u"""\
    Überprüfe, ob das Verzeichnis existiert. Sofern es existiert, überprüfe,
    ob es leer ist.
    """
    directory = os.path.abspath(value)
    if os.path.exists(directory):
        if len(os.listdir(directory)):
            raise click.BadParameter(u'Das Verzeichnis ist nicht leer')
    return directory



@click.command()
@click.option('--name', prompt='Name der App', help='Name der Applikation', callback=_validate_app_name)
@click.option('--descr', prompt='Beschreibung der App', help='Beschreibung der Applikation')
@click.option('--author', prompt='Autor', help='Autor der Applikation', default='')
@click.option('--url', prompt='App-URL', help='Homepage der Applikation', default='')
@click.option('--script', prompt='Script-Name', help='Name des Spripts', default='app.py', callback=_validate_script_name)
@click.option('--version', prompt='Version', help='Versions-Nummer', default='1.0.0')
@click.option('--firmware', prompt='CFW-Firmware', help='Welche Firmware nutzt Du', default='0.9')
@click.option('--category', prompt='App-Kategorie', help='Unter welcher Kategorie soll die App einsortiert werden', default='')
@click.option('--html', prompt='HTML-Seite', help=u'Steht die App in der Web-UI zur Verfügung?', default='')
@click.argument('directory', type=click.Path(), callback=_validate_directory)
def cli(name, descr, author, url, script, version, firmware, category, html, directory):
    items = (('name', name), ('category', category), ('author', author),
            ('icon', 'icon.png'), ('desc', descr), ('version', version),
            ('url', url), ('exec', script), ('uuid', str(uuid.uuid4())),
            ('managed', 'yes'), ('firmware', firmware), ('html', html))
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, 'manifest'), 'wt', encoding='utf-8') as f:
        f.write(u'[app]\n')
        for k, v in items:
            v = v.strip()
            if v:
                f.write(u'{0} = {1}\n'.format(k, v))
    with open(os.path.join(directory, script), 'wt', encoding='utf-8') as f:
        f.write(_SCRIPT.format(author=author, app_name=name, descr=descr,
                            year=datetime.date.today().year))
    with open(os.path.join(directory, 'icon.png'), 'wb') as f:
        f.write(base64.b64decode(_ICON))


if __name__ == '__main__':
    cli()
