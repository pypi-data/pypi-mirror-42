# encoding: utf-8
from __future__ import absolute_import, division, print_function

import sys
import time
from queue import Queue

import pytest

from datapool.observer import CREATED_EVENT, ILLEGAL_EVENT, Observer


def test_call_back(tmpdir, setup_logger):

    changes = Queue()

    def call_back(event, rel_path, timestamp):
        changes.put((event, rel_path, timestamp))

    o = Observer(tmpdir.strpath, call_back)
    o.start()

    # create yaml file
    fh = open(tmpdir.join("site.yaml").strpath, "w")
    fh.write("x")
    fh.close()

    time.sleep(.1)

    for i in range(5):

        time.sleep(.1)
        # create raw file "inwrite" mode, must not trigger event:
        fh = open(tmpdir.join("data.raw.inwrite").strpath, "w")
        fh.write("abc")
        fh.close()

        # should trigger a file creation event
        tmpdir.join("data.raw.inwrite").rename(tmpdir.join("data-%03d.raw" % i))

    time.sleep(.1)

    tmpdir.join("site.yaml").remove()

    # average latency on linux is 500 msec, on mac it is faster:
    time.sleep(.7)

    o.stop()

    CE = CREATED_EVENT
    IE = ILLEGAL_EVENT

    changes = sorted(changes.queue, key=lambda t: t[2])
    events, rel_paths, timestamps = zip(*changes)

    assert events == (CE, CE, CE, CE, CE, CE, IE)
    assert rel_paths == (
        "site.yaml",
        "data-000.raw",
        "data-001.raw",
        "data-002.raw",
        "data-003.raw",
        "data-004.raw",
        "site.yaml",
    )


def test_exception_propagation(tmpdir, setup_logger):
    def call_back(event, rel_path, timestamp):
        pass

    # we check if excdeptions are passed from background observer thread to main thread:
    o = Observer(tmpdir.join("nonexisting_subfolder").strpath, call_back)
    with pytest.raises((FileNotFoundError, OSError)):
        o.start()


def test_schedule_old_files(setup_logger, lz, regtest):
    changes = Queue()

    def call_back(event, rel_path, timestamp):
        changes.put((event, rel_path, timestamp))

    o = Observer(lz.root_folder, call_back)
    o.start(schedule_old_files=True)
    time.sleep(.5)
    for (event, rel_path, _) in sorted(changes.queue):
        print(event, rel_path, file=regtest)
