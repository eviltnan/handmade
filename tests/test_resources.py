import pytest
from handmade.exceptions import ProgrammingError
from handmade.resources import ResourceManager, BaseResource, register_for_plugin


def test_unknown_resource_type():
    with pytest.raises(ProgrammingError):
        ResourceManager('unknown')


class DummyResource(BaseResource):
    def get(self, *args, **kwargs):
        return self.dummy_parameter

    def process(self, *args, **kwargs):
        pass

    def validate(self, *args, **kwargs):
        pass

    def __init__(self, dummy_parameter, *args, **kwargs):
        self.dummy_parameter = dummy_parameter


@pytest.fixture
def resource_manager():
    return ResourceManager.register_type('dummy', DummyResource)


def test_register_module_not_found(resource_manager):
    resource_manager.register(resource_id='id', module='module', dummy_parameter='test.png')


def test_register_resource_id_already_registered(resource_manager):
    resource_manager.register(resource_id='id', module='module', dummy_parameter='test.png')
    with pytest.raises(ProgrammingError):
        resource_manager.register(resource_id='id', module='module', dummy_parameter='test.png')


def test_get_module_not_found(resource_manager):
    with pytest.raises(ResourceManager.ModuleNotRegistered):
        resource_manager.get('module', 'id')


def test_get_resource_id_not_found(resource_manager):
    resource_manager.register(resource_id='id', module='module', dummy_parameter='test.png')
    with pytest.raises(ResourceManager.IdNotRegistered):
        resource_manager.get('module', 'id2')


def test_get_after_register(resource_manager):
    resource_manager.register(resource_id='id', module='module', dummy_parameter='test.png')
    resource = resource_manager.get('module', 'id')
    assert resource == 'test.png', \
        "Unexpected value of dummy parameter got from registry: %s" % resource.dummy_parameter


def test_attribute_register_wrong_path(resource_manager):
    resource_manager.dummy = 'dummy'


def test_activate_registering_for_plugin():
    assert ResourceManager.current_plugin is None, \
        'ResourceManager has %s plugin activated before entering the context' \
        ' of registering resources' % ResourceManager.current_plugin
    with register_for_plugin('dummy'):
        assert ResourceManager.current_plugin == 'dummy'
    assert ResourceManager.current_plugin is None, \
        'ResourceManager has %s plugin activated after entering the context' \
        ' of registering resources' % ResourceManager.current_plugin


def test_attribute_register():
    raise NotImplementedError()


def test_attribute_register_dict():
    raise NotImplementedError()
