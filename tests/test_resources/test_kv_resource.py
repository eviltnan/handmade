from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
import pytest
from handmade.resources.managers import for_plugin, kv


@pytest.fixture
def kv_resource(request):
    with for_plugin('test_plugin'):
        kv.test = 'kv/test.kv'

    resource = kv.get('test', 'test_plugin')

    def fin():
        kv.unregister('test', 'test_plugin')

    resource.process()
    request.addfinalizer(fin)
    return resource


class TestWidget(Widget):
    test_property = NumericProperty()


def test_kv_resource_get_ok(kv_resource):
    rules = kv_resource.get()
    assert rules[0][0].key == 'notexistingwidget'


def test_kv_resource_get_already_loaded(kv_resource):
    kv_resource.get()
    kv_resource.get()


def test_kv_resource_rule_application(kv_resource):
    kv_resource.get()
    test_widget = TestWidget()
    assert test_widget.test_property == 1
