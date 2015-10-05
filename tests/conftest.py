from _pytest.python import fixture
from handmade.utils import empty


@fixture(autouse=True)
def test_project(request):
    import os

    old_cwd = os.getcwd()
    os.chdir(os.path.join('tests', 'test_project'))

    from handmade.conf import settings
    settings.configure()

    def fin():
        settings._wrapped = empty
        os.chdir(old_cwd)
    request.addfinalizer(fin)
    return settings
