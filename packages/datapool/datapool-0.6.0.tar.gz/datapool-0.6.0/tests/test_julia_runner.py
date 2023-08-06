# encoding: utf-8
from __future__ import absolute_import, division, print_function

import pytest

from datapool.instance.config_handling import guess_config
from datapool.julia_runner import JuliaRunner
from datapool.utils import find_executable

has_julia = find_executable("julia") is not None

# we skip this test file if matlab is not installed on the test system:
# see http://doc.pytest.org/en/latest/skipping.html#skip-all-test-functions-of-a-class-or-module
pytestmark = pytest.mark.skipif(
    not has_julia, reason="no julia interpreter found on your system"
)


@pytest.fixture
def julia_exe(regtest):
    config, messages = guess_config({})
    assert config.julia.executable != "", str(config)
    return config.julia.executable


def test_julia_runner(julia_exe, setup_logger):
    j = JuliaRunner(julia_exe)
    j.start_interpreter()
    assert j.is_alive()
    j.run_command(
        "using DataFrames", verbose=True
    )  # needed in test_landing_zone julia script


def test_julia_exception(julia_exe, regtest_logger):
    j = JuliaRunner(julia_exe)
    j.start_interpreter()
    with regtest_logger():
        assert j.run_command("a = b;") == 1
    assert j.is_alive()


def test_julia_version(julia_exe, setup_logger):
    j = JuliaRunner(julia_exe)
    j.start_interpreter()
    version = j.get_julia_version_string()
    sections = version.split(".")
    for section in sections:
        try:
            int(section)
        except ValueError:
            raise ValueError("not all dot separated sections of %r are ints" % version)
    assert len(sections) == 3

    version = j.get_julia_version_tuple()
    assert len(version) == 3
    assert all(isinstance(vi, int) for vi in version)


def test_julia_with_call_limit_exceeded(julia_exe, regtest_logger):

    with regtest_logger():
        j = JuliaRunner(julia_exe, call_limit=1)
        j.start_interpreter()

        pid_before = j.pid
        j.run_command("1")
        assert j.pid == pid_before

        j.run_command("2")
        assert j.pid != pid_before


def test_julia_with_mem_limit_exceeded(julia_exe, regtest_logger):

    import datapool.interpreter_bridge

    injected_mem_usage = 100

    def patched_used_memory(p):
        return injected_mem_usage

    with regtest_logger():
        j = JuliaRunner(julia_exe, mem_limit=110, used_memory=patched_used_memory)
        j.start_interpreter()

        pid_before = j.pid
        j.run_command("1")
        assert j.pid == pid_before

        injected_mem_usage = 120
        j.run_command("2")
        assert j.pid != pid_before
