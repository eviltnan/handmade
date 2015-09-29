import pytest
from handmade.exceptions import ProgrammingError
from handmade.resources import ResourceManager, BaseResource


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


def test_get_after_register():
    raise NotImplementedError()
