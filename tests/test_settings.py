import pytest

from handmade.exceptions import ImproperlyConfigured

from handmade.utils import empty


def test_improperly_configured():
    from handmade.conf import settings
    old_wrapped_settings = settings._wrapped
    settings._wrapped = empty
    with pytest.raises(ImproperlyConfigured):
        print settings
    settings._wrapped = old_wrapped_settings

def test_configure():
    from handmade.conf import settings
    settings._wrapped = empty
    settings.configure()
    assert not settings.DEBUG
