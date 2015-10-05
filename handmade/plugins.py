import importlib
import os

from handmade.exceptions import ImproperlyConfigured, ProgrammingError
from kivy import Logger


class Plugin(object):
    plugins = {}

    @classmethod
    def get_plugin_path(cls, plugin_name):
        try:
            module = importlib.import_module(plugin_name)
        except ImportError:
            raise ProgrammingError('Plugin %s is not found' % plugin_name)
        return os.path.dirname(module.__file__)

    @classmethod
    def register(cls, name, klass=None):

        if name in cls.plugins and cls.plugins[name] == klass:
            raise ProgrammingError("Plugin %s is already registered with class %s" % (name, klass))

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
        from resources.managers import for_plugin
        try:
            with for_plugin(self.name):
                importlib.import_module("%s.resources" % self.name)
        except ImportError:
            Logger.debug("Plugins: plugin %s does not declare resources, pass" % self.name)

    def __init__(self, name):
        self.name = name
        self.tasks = None

        self.discover_tasks()
        self.configure()
        self.register_resources()


def discover():
    from conf import settings

    for plugin in settings.PLUGINS:
        Logger.debug("Plugins: discover plugin %s" % plugin)
        try:
            plugin_module = importlib.import_module(plugin)
        except ImportError as ex:
            raise ImproperlyConfigured("Plugin %s is not found, ex: %s" % (plugin, ex))
        if not hasattr(plugin_module, 'plugin'):
            raise ProgrammingError("Plugin %s does not register itself with Plugin.register" % plugin)
