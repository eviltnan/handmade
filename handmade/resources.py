from collections import defaultdict
from contextlib import contextmanager
from handmade.exceptions import ProgrammingError


class BaseResource(object):
    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def validate(self, *args, **kwargs):
        raise NotImplementedError()

    def process(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def default_value(cls, value):
        raise NotImplementedError()


class ImageResource(BaseResource):
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename

    def get(self, *args, **kwargs):
        return self.filename


class ResourceManager(object):
    RESOURCE_TYPE_MAPPING = {
    }
    current_plugin = None

    class ModuleNotRegistered(ProgrammingError):
        pass

    class IdNotRegistered(ProgrammingError):
        pass

    class CurrentPluginNotSet(ProgrammingError):
        pass

    @classmethod
    def register_type(cls, type_key, klass):
        cls.RESOURCE_TYPE_MAPPING[type_key] = klass
        return cls(type_key)

    def __init__(self, resource_type):

        if resource_type not in ResourceManager.RESOURCE_TYPE_MAPPING:
            raise ProgrammingError("Unknown resource type %s" % resource_type)
        with register_for_plugin('handmade.resources'):
            self.resource_type = resource_type
            self.registry = defaultdict(dict)

    def register(self, resource_id, module, *args, **kwargs):
        if resource_id in self.registry[module]:
            raise ProgrammingError("Resource id %(resource_id)s is already registered for module %(module)s" % {
                "resource_id": resource_id,
                "module": module
            })
        self.registry[module][resource_id] = self.RESOURCE_TYPE_MAPPING[self.resource_type](*args, **kwargs)

    def get(self, resource_id, module, *args, **kwargs):

        if module not in self.registry:
            raise ResourceManager.ModuleNotRegistered("Module %s is not found in resource registry" % module)

        if resource_id not in self.registry[module]:
            raise ResourceManager.IdNotRegistered(
                "Resource %(resource_id)s is not found in %(module)s resource registry" % {
                    "resource_id": resource_id,
                    "module": module
                })

        return self.registry[module][resource_id].get(*args, **kwargs)

    @classmethod
    def start_register_for_plugin(cls, plugin_name):
        cls.current_plugin = plugin_name

    @classmethod
    def finish_register_for_plugin(cls):
        cls.current_plugin = None

    def __setattr__(self, key, value):

        if ResourceManager.current_plugin == 'handmade.resources':
            return super(ResourceManager, self).__setattr__(key, value)

        if ResourceManager.current_plugin is None:
            raise ResourceManager.CurrentPluginNotSet(
                "Current plugin is not set. You should register resources only in resources module")

        if not isinstance(value, dict):
            value = ResourceManager.RESOURCE_TYPE_MAPPING[self.resource_type].default_value(value)

        self.register(key, ResourceManager.current_plugin, **value)

    def __getattr__(self, item):
        if ResourceManager.current_plugin == 'handmade.resources':
            return super(ResourceManager, self).__getattr__(item)

        if ResourceManager.current_plugin is None:
            raise ResourceManager.CurrentPluginNotSet(
                "Current plugin is not set. You can't use attribute notation, use syntax manager[module].%s" % item)

        return self.get(item, ResourceManager.current_plugin)


@contextmanager
def register_for_plugin(plugin_name):
    ResourceManager.start_register_for_plugin(plugin_name)
    try:
        yield
    finally:
        ResourceManager.finish_register_for_plugin()


image = ResourceManager.register_type('image', ImageResource)

# image.icon <-- in context
# image['core'].icon <-- not in context
# image['core'].icon['xxxhdpi']['android'] <-- modifiers, resource level
# image.icon = "images/hello.png" <-- registering non dict style
# image.icon = {"filename": "images/hello.png"}
