import pytest
from handmade.resources.managers import for_plugin, just_file
from handmade.resources.types import FileResource


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
