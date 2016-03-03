# conftest.py is executed by py.test prior to collecting test files
#   it can be used to locate plugins.

# Bizarrely, this is how we look for the plugin (.py) file
pytest_plugins = 'common.profiler.basic_profile_plugin'
