import shutil
from _pytest.python import fixture
from handmade.utils import empty


@fixture(autouse=True)
def test_project(request):
    import os

    old_cwd = os.getcwd()
    os.chdir(os.path.join('tests', 'test_project'))

    from handmade.conf import settings
    from handmade.plugins import discover
    discover()

    def fin():
        shutil.rmtree(settings.RESOURCES_ROOT, ignore_errors=True)
        shutil.rmtree(settings.STORAGE_ROOT, ignore_errors=True)
        settings._wrapped = empty
        os.chdir(old_cwd)

        from handmade.resources.managers import ResourceManager
        ResourceManager.current_plugin = None
        ResourceManager._registration_stack = []

    request.addfinalizer(fin)
    return settings
