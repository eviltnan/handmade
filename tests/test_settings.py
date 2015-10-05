import pytest

from handmade.exceptions import ImproperlyConfigured
from handmade.conf import settings
from handmade.utils import empty


def test_improperly_configured():
    from handmade.conf import settings
    settings._wrapped = empty
    with pytest.raises(ImproperlyConfigured):
        print settings


def test_configure():
    settings._wrapped = empty
    settings.configure()
    assert not settings.DEBUG
