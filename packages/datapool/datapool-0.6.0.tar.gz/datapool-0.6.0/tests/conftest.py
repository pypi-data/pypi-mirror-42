# encoding: utf-8
from __future__ import absolute_import, division, print_function

import logging
import os
import re
import sys
import tempfile
import time
from functools import partial
from io import StringIO

import pytest
import pytest_regtest

from datapool.database import setup_db
from datapool.instance.config_handling import (guess_config, is_port_used,
                                               read_ini)

"""
Here we define all the fixtures found in the tests. If pytest sees an argument in a test
procedure, it first runs the corresponding fixture-procedure and passes the return
values to the test as an argument.  Fixture contain the @pytest.fixture annotation and
can be nested.
"""


not_for_root = pytest.mark.skipif(
    os.getuid() == 0, reason="test will fail for roots permissions"
)


@pytest.hookimpl(hookwrapper=True)
def pytest_cmdline_main(config):
    yield
    # beep n times, disabled on CI server where tests run as root
    if os.getuid() > 0:
        for _ in range(1):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(.2)


def _check_pytest_regtest_version(tobe):
    if hasattr(pytest_regtest, "__version__"):
        return pytest_regtest.__version__ >= tuple(map(int, tobe.split(".")))
    return False


@pytest_regtest.register_converter_post
def fix_datapool_version(output, request):
    lines = []
    for line in output.split("\n"):
        line = re.sub(
            r"this is datapool version \d+.\d+.\d+",
            "this is datapool version X.Y.Z",
            line,
        )
        lines.append(line)
    return "\n".join(lines)


@pytest.fixture(scope="session", autouse=True)
def call_ahead_of_alltests(request):
    min_version = "1.0.12"
    if not _check_pytest_regtest_version(min_version):
        session = request.node
        session.items[:] = []  # empty all other tests
        pytest.skip("please install pytest-regtest >= {}".format(min_version))

    if is_port_used(8000):
        pytest.skip("port 8000 is already used, this might break tests")


here = os.path.relpath(os.path.dirname(__file__))
test_config = read_ini(os.path.join(here, "etc", "datapool", "datapool.ini"))

# we fake a /etc folder within the testing folder:
os.environ["ETC"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etc")
os.environ["TMP"] = os.path.realpath(tempfile.mkdtemp())
os.environ["TMP"] = tempfile.mkdtemp()
os.environ["DEVELOPZONE"] = os.path.realpath(tempfile.mkdtemp())


@pytest.fixture
def here(scope="session"):
    """returns the folder containing the test script. """
    return os.path.relpath(os.path.dirname(__file__))


@pytest.fixture
def data_path(here, scope="session"):
    """returns a function to compute the correct path of a file within the tests/data
    folder"""
    return partial(os.path.join, here, "data")


@pytest.fixture
def config(here, monkeypatch, tmpdir, scope="function"):
    """we use the fake /etc folder tests/etc to have an isolated config environment
    which does not interfere with the actual /etc on the machine."""
    from datapool.config import read_ini

    # we patch TMP because this is resolved when calling read_ini and we want to have
    # an isolated enviroment for every test !
    monkeypatch.setenv("TMP", tmpdir.strpath)
    return read_ini(os.path.join(here, "etc", "datapool", "datapool.ini"))


@pytest.fixture(scope="function")
def regtest_logger(_regtest_handler, setup_logger):
    from datapool.logger import replace_handlers

    return partial(replace_handlers, handler=_regtest_handler)


@pytest.yield_fixture
def setup_logger(config):
    from datapool.logger import drop_logger, setup_logger

    drop_logger()
    setup_logger(config)
    yield
    drop_logger()


@pytest.yield_fixture(scope="function")
def _regtest_handler(regtest, tmpdir):
    class RegtestHandler(logging.StreamHandler):
        pass

    handler = RegtestHandler()

    formatter = logging.Formatter("%(levelname)-8s %(name)-15s %(message)s")

    def write(line):
        line = _fix_reg_output(line)
        regtest.write(line)

    handler.stream.write = write
    handler.setFormatter(formatter)

    return handler


def _regtest_list_folders(out, start_folder, recurse):
    for root, dirs, files in sorted(os.walk(start_folder)):
        print(os.path.relpath(root, start_folder), file=out)
        for dir_ in sorted(dirs):
            print("   dir:", dir_, file=out)
        for file in sorted(files):
            print("  file:", file, file=out)
        if not recurse:
            break


@pytest.fixture
def regtest_list_folders(regtest):
    """returns a function to list all files and subfolders of a given path to be
    recoreded for regression tests.
    """
    return partial(_regtest_list_folders, regtest)


def _fix_reg_output(txt):
    fixed = []
    for line in txt.split("\n"):
        if "needed" in line.lower():
            line = re.sub(r"[0-9]*\.[0-9]+", "<TIME>", line)
        if "msec" in line.lower():
            line = re.sub(r"[0-9]+(\.[0-9]+)?", "<TIME>", line)

        line = re.sub(r"\d+ signals per second", "<N> signals per second", line)
        fixed.append(line)
    return "\n".join(fixed)


@pytest.fixture
def regtest_print(regtest):
    def print_(*a, **kw):
        assert "file" not in kw, "you called regtest_print with a file keyword argument"
        fh = StringIO()
        print(*a, file=fh, **kw)
        lines = fh.getvalue()
        fixed = []
        for line in lines.split("\n"):
            line = _fix_reg_output(line)
            fixed.append(line)
        regtest.write("\n".join(fixed))

    return print_


@pytest.fixture(scope="session")
def has_matlab():
    from datapool.utils import find_executable

    return find_executable("matlab") is not None


@pytest.fixture(scope="session")
def has_julia():
    from datapool.utils import find_executable

    return find_executable("julia") is not None


@pytest.fixture(scope="session")
def has_r():
    from datapool.utils import find_executable

    return find_executable("R") is not None


@pytest.fixture
def matlab_exe(regtest):
    config, messages = guess_config({})
    for message in messages:
        print(message, file=regtest)
    assert config.matlab.executable != "", str(config)
    return config.matlab.executable


@pytest.fixture(scope="function")
def lz(tmpdir, data_path):
    """creates a fresh valid landing zone
    """
    from datapool.landing_zone import LandingZone

    lz = LandingZone.create_from(
        tmpdir.join("landing_zone").strpath, data_path("test_landing_zone")
    )
    return lz


@pytest.fixture(scope="function")
def engine(config, setup_logger):
    engine = setup_db(config.db)
    return engine
