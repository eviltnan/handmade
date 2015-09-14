from kivy.properties import NumericProperty
import pytest
from handmade.models.base import JsonStoragedModel
from handmade.models.storages import JsonModelStorage
import os
from handmade.models.widget import ModelWidget


class TestModel(JsonStoragedModel):
    foo = NumericProperty()


def test_base_model_meta():
    from handmade.models.base import BaseModel
    assert BaseModel.DoesNotExist != TestModel.DoesNotExist


def test_storage_creation():
    instance = TestModel()
    assert instance.storage
    instance2 = TestModel()

    assert instance.storage is instance2.storage is TestModel.storage


@pytest.fixture
def json_storage(request):
    storage = JsonModelStorage(TestModel)

    def finalizer():
        if os.path.exists(storage.filename):
            os.remove(storage.filename)

    request.addfinalizer(finalizer)
    return storage


def test_json_storage_filename(json_storage):
    assert json_storage.filename == 'models/test_model.json'


def test_json_storage_create(json_storage):
    instance = TestModel(foo=123)
    json_storage.save(instance)
    assert instance.id == 1, "Instance got unexpected id after saving in json storage: %s" % instance.id
    assert json_storage._json_storage[instance.id]['foo'] == 123


def test_json_storage_update(json_storage):
    instance = TestModel(foo=123)
    json_storage.save(instance)
    instance.foo = 1234
    json_storage.save(instance)
    assert instance.id == 1, "Instance got unexpected id after updating in json storage: %s" % instance.id
    assert json_storage._json_storage[instance.id]['foo'] == 1234


def test_json_storage_create_json_unserializable(json_storage):
    raise NotImplementedError()


def test_json_storage_get_by_id_ok(json_storage):
    instance = TestModel(foo=123)
    json_storage.save(instance)
    got_instance = json_storage.get(instance.id)
    assert instance.id == got_instance.id, 'Instance gotten from the json storage has other id as saved one'
    assert instance.foo == got_instance.foo, \
        'Instance gotten from the json storage has wrong value for field as the saved one'


def test_json_storage_get_by_id_not_found(json_storage):
    with pytest.raises(TestModel.DoesNotExist):
        json_storage.get(10)


def test_json_storage_delete_ok(json_storage):
    instance = TestModel(foo=123)
    json_storage.save(instance)
    id_ = instance.id
    json_storage.delete(instance)
    with pytest.raises(TestModel.DoesNotExist):
        json_storage.get(id_)


def test_json_storage_delete_not_found_pk(json_storage):
    instance = TestModel(foo=123)
    instance.id = 10
    with pytest.raises(TestModel.DoesNotExist):
        json_storage.delete(instance)


def test_json_storage_delete_id_none(json_storage):
    instance = TestModel(foo=123)
    with pytest.raises(RuntimeError):
        json_storage.delete(instance)


class TestModelWidget(ModelWidget):
    model_class = TestModel


@pytest.fixture
def model_instance(json_storage):
    instance = TestModel()
    instance.save()
    return instance


def test_model_widget_creation(model_instance):
    model_widget = TestModelWidget(instance=model_instance)
    assert model_widget.model_instance == model_instance, 'Unexpected model instance while creation of model widget'
    model_widget = TestModelWidget(instance_id=model_instance.id)
    assert model_widget.model_instance == model_instance, 'Unexpected model instance while creation of model widget'


def test_model_widget_properties_bind(model_instance):
    model_widget = TestModelWidget(instance=model_instance)
    assert all(
        model_instance_property in model_widget.properties()
        for model_instance_property in model_instance.properties()
    )

    assert isinstance(model_widget.properties()['foo'], model_instance.properties()['foo'].__class__)
    assert model_widget.properties()['foo'] is model_instance.properties()['foo']

    model_instance.handler_called = False

    def model_prop_handler(caller, value):
        assert isinstance(caller, TestModel)
        caller.handler_called = True

    model_widget.handler_called = False

    def widget_prop_handler(caller, value):
        assert isinstance(caller, TestModelWidget)
        model_widget.handler_called = True

    model_instance.bind(foo=model_prop_handler)
    model_widget.bind(foo=widget_prop_handler)
    model_instance.foo = 2
    assert model_widget.foo == model_instance.foo
    assert model_instance.handler_called, 'Model property handler was not called'
    assert model_widget.handler_called, 'Widget property handler was not called'

    model_widget.foo = 3
    assert model_instance.foo == model_widget.foo


def test_model_widget_naming_collision(model_instance):
    with pytest.raises(AssertionError):
        class TestNamingClashModelWidget(ModelWidget):
            foo = NumericProperty()
            model_class = TestModel


def test_model_widget_class_doesnt_define_model_class():
    with pytest.raises(RuntimeError):
        class TestNoModelClassModelWidget(ModelWidget):
            foo = NumericProperty()


def test_model_widget_from_storage(json_storage):
    instance = TestModel(foo=5)
    instance.save()
    widget = TestModelWidget(instance_id=instance.id)
    assert widget.foo == instance.foo


class TestModelWidget2(ModelWidget):
    model_class = TestModel


def test_multiple_model_widgets_for_one_instance(model_instance):
    widget = TestModelWidget(model_instance)
    widget2 = TestModelWidget2(model_instance)
    widget3 = TestModelWidget(model_instance)
    model_instance.foo = 10
    assert widget.foo == model_instance.foo
    assert widget2.foo == model_instance.foo
    assert widget3.foo == model_instance.foo
