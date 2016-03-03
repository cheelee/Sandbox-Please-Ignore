# Sandbox-Please-Ignore
Personal sandbox code for me to exercise and experiment with github + associated features (e.g. travis-ci, waffle.io)

Goals
----

I'm hoping to find ways to elegantly add performance profiling and
regression testing to the Continuous Integration process on github.

Setup
----

The current setup uses python as a (currently non-existent) codebase
with a single dependency on numpy.

Travis-CI
----

This sandbox exercises simple pytest tests using travis-ci.

Notes
----

There exists a cProfile plugin "pytest_profiling" that can be installed via

*pip install pytest_profiling*

However this plugin probably does not provide the flexibility we need
to achieve the goals set out. For example, it currently changes the
test result to issue a warning and I do not really want that. At this
stage of the game however, it is functionally equivalent if not better
than the basic profiler plugin written.
