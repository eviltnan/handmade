import pytest

from handmade.exceptions import ProgrammingError
from handmade.resources.managers import ResourceManager, for_plugin, just_file, atlas
from handmade.resources.types import BaseResource, FileResource, AtlasResource


def test_unknown_resource_type():
    with pytest.raises(ProgrammingError):
        ResourceManager('unknown')


class DummyResource(BaseResource):
    @classmethod
    def default_value(cls, value):
        return {
            "dummy_parameter": value
        }

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
    resource_manager.register(resource_id='id', plugin='module', dummy_parameter='test.png')


def test_register_resource_id_already_registered(resource_manager):
    resource_manager.register(resource_id='id', plugin='module', dummy_parameter='test.png')
    with pytest.raises(ProgrammingError):
        resource_manager.register(resource_id='id', plugin='module', dummy_parameter='test.png')


def test_get_module_not_found(resource_manager):
    with pytest.raises(ResourceManager.ModuleNotRegistered):
        resource_manager.get('id', 'module')


def test_get_resource_id_not_found(resource_manager):
    resource_manager.register(resource_id='id', plugin='module', dummy_parameter='test.png')
    with pytest.raises(ResourceManager.IdNotRegistered):
        resource_manager.get('id2', 'module')


def test_get_after_register(resource_manager):
    resource_manager.register(resource_id='id', plugin='module', dummy_parameter='test.png')
    resource = resource_manager.get('id', 'module')
    assert resource.dummy_parameter == 'test.png', \
        "Unexpected value of dummy parameter got from registry: %s" % resource.dummy_parameter


def test_activate_registering_for_plugin():
    assert ResourceManager.current_plugin is None, \
        'ResourceManager has %s plugin activated before entering the context' \
        ' of registering resources' % ResourceManager.current_plugin
    with for_plugin('dummy'):
        assert ResourceManager.current_plugin == 'dummy'
    assert ResourceManager.current_plugin is None, \
        'ResourceManager has %s plugin activated after entering the context' \
        ' of registering resources' % ResourceManager.current_plugin


def test_attribute_register_not_in_context(resource_manager):
    with pytest.raises(ResourceManager.CurrentPluginNotSet):
        resource_manager.dummy = 'dummy.png'


def test_attribute_register_default_value(resource_manager):
    with for_plugin('dummy'):
        resource_manager.dummy = 'test.png'
        assert resource_manager.get('dummy', 'dummy').dummy_parameter == 'test.png', \
            'Unexpected resource value after registering %s' % resource_manager.get('dummy', 'dummy')


def test_resource_unregister(resource_manager):
    with for_plugin('dummy'):
        resource_manager.dummy = 'test.png'
    resource_manager.unregister('dummy', 'dummy')
    with pytest.raises(ResourceManager.IdNotRegistered):
        resource_manager['dummy'].dummy


def test_attribute_register_dict(resource_manager):
    with for_plugin('dummy'):
        resource_manager.dummy = {
            'dummy_parameter': 'test.png'
        }
    assert resource_manager.get('dummy', 'dummy').dummy_parameter == 'test.png', \
        'Unexpected resource value after registering %s' % resource_manager.get('dummy', 'dummy')


def test_get_attribute_not_in_module_context(resource_manager):
    with for_plugin('dummy'):
        resource_manager.dummy = 'dummy'
    with pytest.raises(ResourceManager.CurrentPluginNotSet):
        resource_manager.dummy


def test_get_attribute_not_found(resource_manager):
    with for_plugin('dummy'):
        resource_manager.dummy = 'dummy'
        with pytest.raises(ResourceManager.IdNotRegistered):
            resource_manager.dummy2


def test_get_attribute_ok():
    with for_plugin('dummy'):
        resource_manager.dummy = 'dummy'
        assert resource_manager.dummy == 'dummy', \
            "Unexpected value of attribute style get resource %s" % resource_manager['dummy'].dummy


def test_get_attribute_item_notation(resource_manager):
    with for_plugin('test_plugin'):
        resource_manager.dummy = 'dummy'
    assert resource_manager['test_plugin'].dummy == 'dummy', \
        "Unexpected value of attribute style get resource %s" % resource_manager['test_plugin'].dummy


@pytest.fixture
def file_resource(request):
    with for_plugin('test_plugin'):
        just_file.test = 'image/test.png'

    resource = just_file.get('test', 'test_plugin')

    def fin():
        just_file.unregister('test', 'test_plugin')

    request.addfinalizer(fin)
    return resource


def test_file_resource_validate():
    with pytest.raises(FileResource.FileNotFound):
        with for_plugin('test_plugin'):
            just_file.test = 'not_found.png'


def test_file_resource_process(file_resource):
    file_resource.process()


def test_file_resource_get(file_resource):
    assert file_resource.get() == file_resource.destination_path


@pytest.fixture
def atlas_resource(request):
    with for_plugin('test_plugin'):
        atlas.test = 'test_atlas'

    resource = atlas.get('test', 'test_plugin')

    def fin():
        atlas.unregister('test', 'test_plugin')

    request.addfinalizer(fin)
    return resource


def test_atlas_resource_file_is_directory():
    with pytest.raises(AtlasResource.NotADirectory):
        with for_plugin('test_plugin'):
            atlas.test = 'test_atlas_not_directory.txt'


def test_atlas_resource_directory_empty():
    with pytest.raises(AtlasResource.DirectoryEmpty):
        with for_plugin('test_plugin'):
            atlas.test = 'empty_atlas'


def test_atlas_process(atlas_resource):
    atlas_resource.process()
    assert atlas_resource.atlas_filename == 'data/test_plugin/test_atlas.atlas'
    assert 'test' in atlas_resource.atlas_meta['test_atlas-0.png']
    assert 'test2' in atlas_resource.atlas_meta['test_atlas-0.png']


def test_atlas_register_dict_notation():
    with for_plugin('test_plugin'):
        atlas.test = {
            'filename': 'test_atlas',
            'size': (4, 4)
        }
    resource = atlas.get('test', 'test_plugin')
    assert resource.size == (4, 4)


def test_atlas_get():
    raise NotImplementedError()
