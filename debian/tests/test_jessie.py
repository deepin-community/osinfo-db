#!/usr/bin/python3

import pytest

import gi
gi.require_version('Libosinfo', '1.0')
from gi.repository import Libosinfo as osinfo;


@pytest.fixture(scope="session")
def db():
    loader = osinfo.Loader()
    loader.process_default_path()
    return loader.get_db()


def testVirtio(db):
    """
    Make sure jessie has virtio devices
    """
    osid = "http://debian.org/debian/8"
    os = db.get_os(osid)
    devs = os.get_all_devices()
    devnames = []

    for idx in range(devs.get_length()):
        devnames.append(devs.get_nth(idx).get_name())

    assert "virtio-net" in devnames
    assert "virtio-block" in devnames
    assert "virtio-rng" in devnames
    assert "virtio-scsi" in devnames
    assert "virtio-balloon" in devnames
    assert "virtio-9p" in devnames
