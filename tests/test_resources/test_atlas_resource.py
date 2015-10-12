import pytest
from handmade.resources.managers import for_plugin, atlas
from handmade.resources.types import AtlasResource


@pytest.fixture
def atlas_resource(request):
    with for_plugin('test_plugin'):
        atlas.test = 'test_atlas'

    resource = atlas.get('test', 'test_plugin')

    def fin():
        atlas.unregister('test', 'test_plugin')

    resource.process()
    request.addfinalizer(fin)
    return resource


def test_atlas_resource_file_is_directory():
    with pytest.raises(AtlasResource.NotADirectory):
        with for_plugin('test_plugin'):
            atlas.test = 'atlas_not_directory.txt'
            atlas.get('test', 'test_plugin').validate()
    atlas.unregister('test', 'test_plugin')


def test_atlas_resource_directory_empty():
    with pytest.raises(AtlasResource.DirectoryEmpty):
        with for_plugin('test_plugin'):
            atlas.test = 'empty_atlas'
            atlas.get('test', 'test_plugin').validate()
    atlas.unregister('test', 'test_plugin')


def test_atlas_register_dict_notation():
    with for_plugin('test_plugin'):
        atlas.test2 = {
            'filename': 'test_atlas',
            'size': (4, 4)
        }
    resource = atlas.get('test2', 'test_plugin')
    assert resource.size == (4, 4)


def test_atlas_get(atlas_resource):
    atlas_instance = atlas_resource.get()
    assert 'test' in atlas_instance.textures.keys()
    texture = atlas_instance['test']

    from kivy.graphics.texture import TextureRegion
    assert isinstance(texture, TextureRegion)


def test_atlas_process(atlas_resource):
    assert atlas_resource.atlas_filename == 'data/test_plugin/test_atlas.atlas'
