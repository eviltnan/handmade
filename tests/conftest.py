from _pytest.python import fixture


@fixture(autouse=True)
def settings():
    from handmade.conf import settings
    settings.configure()
