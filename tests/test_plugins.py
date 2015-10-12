import os
from handmade.plugins import Plugin
from handmade.resources.managers import image


def test_discover_tasks():
    from test_plugin import plugin
    assert os.path.dirname(plugin.tasks.__file__) == Plugin.get_plugin_path('test_plugin')


def test_register_resources():
    from test_plugin import plugin
    assert image['test_plugin'].logo == "data/test_plugin/data/image/test.png"


def test_post_register_resources():
    from test_plugin import plugin
    raise NotImplementedError()