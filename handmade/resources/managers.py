from collections import defaultdict
from contextlib import contextmanager

from handmade.exceptions import ProgrammingError
from handmade.resources.types import ImageResource, FileResource, AtlasResource, KvResource
from kivy import Logger


class ItemNotationWrapper(object):
    def __init__(self, plugin, manager):
        self.plugin = plugin
        self.manager = manager

    def __getattr__(self, item):
        with for_plugin(self.plugin):
            return getattr(self.manager, item)


class ResourceManager(object):
    RESOURCE_TYPE_MAPPING = {
    }
    managers = {}
    current_plugin = None
    _registration_stack = []

    class ModuleNotRegistered(ProgrammingError):
        pass

    class IdNotRegistered(ProgrammingError):
        pass

    class CurrentPluginNotSet(ProgrammingError):
        pass

    class SelfNestedResourceRegistration(ProgrammingError):
        pass

    @classmethod
    def register_type(cls, type_key, klass):
        cls.RESOURCE_TYPE_MAPPING[type_key] = klass
        cls.managers[type_key] = cls(type_key)
        return cls.managers[type_key]

    def __init__(self, resource_type):

        if resource_type not in ResourceManager.RESOURCE_TYPE_MAPPING:
            raise ProgrammingError("Unknown resource type %s" % resource_type)
        with for_plugin('handmade.resources'):
            self.resource_type = resource_type
            self.registry = defaultdict(dict)

    def register(self, resource_id, plugin, *args, **kwargs):
        if resource_id in self.registry[plugin]:
            raise ProgrammingError("%(resource_name)s resource id \"%(resource_id)s\" "
                                   "is already registered for plugin \"%(module)s\"" % {
                                       "resource_name": self.resource_type.capitalize(),
                                       "resource_id": resource_id,
                                       "module": plugin
                                   })
        self.registry[plugin][resource_id] = self.RESOURCE_TYPE_MAPPING[self.resource_type](
            plugin=plugin, *args, **kwargs
        )

    def unregister(self, resource_id, plugin):
        if not resource_id in self.registry[plugin]:
            raise ProgrammingError("Resource id %(resource_id)s is not "
                                   "registered for module %(module)s, can't unregister" % {
                                       "resource_id": resource_id,
                                       "module": plugin
                                   })
        del self.registry[plugin][resource_id]

    def get(self, resource_id, plugin, *args, **kwargs):

        if plugin not in self.registry:
            raise ResourceManager.ModuleNotRegistered("Module %s is not found in resource registry" % plugin)

        if resource_id not in self.registry[plugin]:
            raise ResourceManager.IdNotRegistered(
                "Resource %(resource_id)s is not found in %(module)s resource registry" % {
                    "resource_id": resource_id,
                    "module": plugin
                })

        return self.registry[plugin][resource_id]

    @classmethod
    def enter_plugin_context(cls, plugin):
        if cls.current_plugin:

            cls._registration_stack.append(cls.current_plugin)
            if plugin in cls._registration_stack:
                raise ResourceManager.SelfNestedResourceRegistration(
                    "You try to nest registering of resources of plugin "
                    "%s while already registering the resources for this plugin" % plugin
                )

        Logger.debug("Resources: enter in plugin context of %s" % plugin)
        cls.current_plugin = plugin

    @classmethod
    def exit_plugin_context(cls):
        Logger.debug("Resources: exit plugin context")
        if cls._registration_stack:
            cls.current_plugin = cls._registration_stack.pop()
        else:
            cls.current_plugin = None

    def __setattr__(self, key, value):

        if ResourceManager.current_plugin == 'handmade.resources':
            return super(ResourceManager, self).__setattr__(key, value)

        if ResourceManager.current_plugin is None:
            raise ResourceManager.CurrentPluginNotSet(
                "Current plugin is not set. You should register resources only in resources module "
                "or with for_plugin decorator")

        if not isinstance(value, dict):
            value = ResourceManager.RESOURCE_TYPE_MAPPING[self.resource_type].default_value(value)

        self.register(key, ResourceManager.current_plugin, **value)

    def __getattr__(self, item):
        if ResourceManager.current_plugin == 'handmade.resources':
            return super(ResourceManager, self).__getattr__(item)

        if ResourceManager.current_plugin is None:
            raise ResourceManager.CurrentPluginNotSet(
                "Current plugin is not set. You can't use attribute notation, use syntax manager[module].%s" % item)

        return self.get(item, ResourceManager.current_plugin).get()

    def __getitem__(self, item):

        return ItemNotationWrapper(item, self)


@contextmanager
def for_plugin(plugin_name):
    ResourceManager.enter_plugin_context(plugin_name)
    try:
        yield
    finally:
        ResourceManager.exit_plugin_context()


just_file = ResourceManager.register_type('file', FileResource)
image = ResourceManager.register_type('image', ImageResource)
atlas = ResourceManager.register_type('atlas', AtlasResource)
kv = ResourceManager.register_type('kv', KvResource)
