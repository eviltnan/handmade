import pytest
from handmade.exceptions import ImproperlyConfigured
from handmade.plugins import tasks_collections


def test_task_modules():
    for plugin, task_module in tasks_collections():
        if plugin == 'project':
            from handmade.project import tasks
            assert task_module == tasks, 'Project tasks collection should be from core plugin, but not %s' % task_module


def test_plugin_not_found():
    from handmade.conf import settings
    settings.PLUGINS = ['unknown']
    with pytest.raises(ImproperlyConfigured):
        list(tasks_collections())
