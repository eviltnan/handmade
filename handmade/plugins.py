import importlib

from handmade.exceptions import ImproperlyConfigured, ProgrammingError
from kivy import Logger


def resources():
    from conf import settings
    from resources import for_plugin
    import importlib
    for plugin in settings.PLUGINS:
        try:
            with for_plugin(plugin):
                importlib.import_module("handmade.%s.resources" % plugin)
        except ImportError:
            pass


class Plugin(object):
    plugins = {}

    @classmethod
    def register(cls, name, klass=None):
        klass = klass or cls
        Logger.debug("Plugins: register plugin %s, class %s" % (name, klass))
        instance = klass(name)
        cls.plugins[name] = instance
        return instance

    def configure(self):
        pass

    def discover_tasks(self):
        try:
            tasks = importlib.import_module("%s.tasks" % self.name)
        except ImportError:
            pass
        else:
            self.tasks = tasks

    def register_resources(self):
        raise NotImplementedError()

    def __init__(self, name):
        self.name = name
        self.tasks = None

        self.discover_tasks()
        self.configure()


def discover():
    from conf import settings

    for plugin in settings.PLUGINS:
        Logger.debug("Plugins: discover plugin %s" % plugin)
        try:
            plugin_module = importlib.import_module(plugin)
        except ImportError:
            raise ImproperlyConfigured("Plugin %s is not found" % plugin)
        if not hasattr(plugin_module, 'plugin'):
            raise ProgrammingError("Plugin %s does not register itself with Plugin.register" % plugin)
