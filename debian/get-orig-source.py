#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020 Pino Toscano <pino@debian.org>
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import git

OSINFO_DB_REPO = 'https://gitlab.com/libosinfo/osinfo-db.git'

scriptdir = os.path.dirname(os.path.realpath(__file__))
uscan_args = ['uscan', '--dehs', '--skip-signature',
              '--watchfile', os.path.join(scriptdir, 'watch')]
uscan_proc = subprocess.run(uscan_args, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
uscan_xml = uscan_proc.stdout.decode('utf-8')
root = ET.fromstring(uscan_xml)
upstream_version = root.find('upstream-version').text
print('Downloading version {} ...'.format(upstream_version))

with tempfile.TemporaryDirectory() as tmpdir:
    repo = git.Repo.clone_from(OSINFO_DB_REPO, os.path.join(tmpdir, 'git'))
    tmparchive = os.path.join(tmpdir, 'archive.tar')
    with open(tmparchive, 'wb') as tmpfile:
        repo.archive(tmpfile, treeish='v{}'.format(upstream_version),
                     prefix='osinfo-db-{}/'.format(upstream_version))
    outarchive = 'osinfo-db_0.{}.orig.tar.xz'.format(upstream_version)
    with open(tmparchive, 'r') as tmpfile, open(outarchive, 'w') as outfile:
        subprocess.run(['xz', '-c'], stdin=tmpfile, stdout=outfile)
    print('Written {}'.format(outarchive))
