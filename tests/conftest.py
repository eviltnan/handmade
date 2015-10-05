from _pytest.python import fixture
from handmade.utils import empty


@fixture(autouse=True)
def test_project(request):
    import os
    os.chdir(os.path.join('tests', 'test_project'))

    from handmade.conf import settings
    settings.configure(
        STORAGE_ROOT='tests/test_data/storage'
    )

    def fin():
        settings._wrapped = empty

    request.addfinalizer(fin)
    return settings
