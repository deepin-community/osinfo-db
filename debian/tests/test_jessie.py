#!/usr/bin/python3

import unittest

import gi
gi.require_version('Libosinfo', '1.0')
from gi.repository import Libosinfo as osinfo;

class TestJessie(unittest.TestCase):

    def setUp(self):
        self.loader = osinfo.Loader()
        self.loader.process_default_path()
        self.db = self.loader.get_db()

    def testVirtio(self):
        """
        Make sure jessie has virtio devices
        """
        osid = "http://debian.org/debian/8"
        os = self.db.get_os(osid)
        devs = os.get_all_devices()
        devnames = []

        for idx in range(devs.get_length()):
            devnames.append(devs.get_nth(idx).get_name())

        self.assertIn("virtio-net", devnames)
        self.assertIn("virtio-block", devnames)
        self.assertIn("virtio-rng", devnames)
        self.assertIn("virtio-scsi", devnames)
        self.assertIn("virtio-balloon", devnames)
        self.assertIn("virtio-9p", devnames)

