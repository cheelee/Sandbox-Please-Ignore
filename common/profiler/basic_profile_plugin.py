# PyTest plugins for supporting cProfile written by Kevin Katz for OpenWorm
#  late 2015.
# Modified by Chee Wai Lee:
# Last Modified: 3/3/2016
#  - this is a good baseline working example for pytest hooks and plugins.
#  - stolen and modified by Chee Wai Lee for further testing in Sandbox code 3/1/2016.
#  - became aware of a publicly available profiling plugin but it has flexibility issues.
#      pip install pytest_profiling

# This file specified pytest plugins

import cProfile
import pstats
import os
import pytest

# Module level, to pass state across tests.  This is not multiprocessing-safe.
enabled = False

def pytest_addoption(parser):
    profile_group = parser.getgroup('Performance Profiling', description='Uses cProfile to profile the performance of tests.')
    profile_group.addoption('--profile', action='store', help='Enable pytest profiling.')
#    profile_group.addoption('--code-speed-submit', dest='cs_url', action='store',
#                     default=None, help='Submit results as JSON to Codespeed instance at URL. ' + \
#                     "Must be accompanied by --branch, --commit, and --environment arguments.")
#    profile_group.addoption('--branch', dest='branch', action='store',
#                     default=None, help='Specify Codespeed "Branch" setting.')
#    profile_group.addoption('--commit', dest='commit', action='store',
#                     default=None, help='Specify Codespeed "Commit ID" setting.')
#    profile_group.addoption('--environment', dest='env', action='store',
#                     default=None, help='Specify Codespeed "Environment" setting.')


def pytest_configure(config):
    """
    Called before tests are collected.
    """
    global enabled
    enabled = config.getoption('profile') is not None

@pytest.mark.hookwrapper
def pytest_runtest_call(item):
    """
    Calls once per test.
    """
    # item is the test item according to pytest hooks documentation.
    global enabled

    item.enabled = enabled
    item.profiler = cProfile.Profile()

    item.profiler.enable() if item.enabled else None
    # I'm assuming this works because tests in pytest are generators in python
    #   with outcome being a test result object returned by each individual test
    outcome = yield
    item.profiler.disable() if item.enabled else None

    result = None if outcome is None else outcome.get_result()
    # Item's excinfo will indicate any exceptions thrown
    # excinfo does not appear to exist ... removing it for now
    # 3/3 - looks like excinfo is a field with outcome and not with item.
    #if item.enabled and item.excinfo is None:
    if item.enabled and outcome.excinfo is None:
        # item.listnames() returns list of form:
        # [<package name>, <test path>, <test classname>, <test function name>]
        fp = FunctionProfile(profiler=item.profiler, test_function_name=item.listnames()[-1])

def pytest_unconfigure(config):
    """
    Called after all tests are completed.
    """
    global enabled

    if not enabled:
        return

    print 'tests with profiler complete.'

# Very basic profiler, just print the cProfile results if it exists.
class FunctionProfile(object):
    def __init__(self, *args, **kwargs):
        import marshal
        profiler = kwargs.pop("profiler",None)
        test_func = kwargs.pop("test_function_name", None)
        if profiler is not None and test_func is not None:
            stats = pstats.Stats(profiler)
            stats.sort_stats('tottime')
            stats.print_stats(10)
            stats.dump_stats(test_func+'.pstats')

