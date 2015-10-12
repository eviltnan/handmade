import os
from handmade.plugins import Plugin


def test_discover_tasks():
    from test_plugin import plugin
    assert os.path.dirname(plugin.tasks.__file__) == Plugin.get_plugin_path('test_plugin')


def test_register_resources():
    raise NotImplementedError()
