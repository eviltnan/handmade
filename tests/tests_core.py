from handmade.conf import settings


def test_root_widget():
    from handmade.core import application
    app = application.HandmadeApplication()
    widget = app.build()
    assert settings.ROOT_WIDGET == widget.__module__ + "." + widget.__class__.__name__, \
        'Application root widget is other as specified in settings'
