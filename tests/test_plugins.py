from handmade.plugins import tasks_collections


def test_task_modules():
    for plugin, task_module in tasks_collections():
        if plugin == 'core':
            from handmade.core import tasks
            assert task_module == tasks, 'Core tasks collection should be from core plugin, but not %s' % task_module

# todo: test import error to improperly configured