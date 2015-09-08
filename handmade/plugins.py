from handmade.exceptions import ImproperlyConfigured


def tasks_collections():
    from conf import settings
    import importlib
    for plugin in settings.PLUGINS:
        try:
            importlib.import_module(plugin)
        except ImportError:
            try:
                importlib.import_module("handmade." + plugin)
            except ImportError:
                raise ImproperlyConfigured("Plugin %s is not found" % plugin)
        try:
            tasks = importlib.import_module("handmade.%s.tasks" % plugin)
        except ImportError:
            pass
        else:
            yield plugin, tasks
