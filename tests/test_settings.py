import pytest

from handmade.exceptions import ImproperlyConfigured
from handmade.conf import settings


def test_improperly_configured():
    with pytest.raises(ImproperlyConfigured):
        print settings