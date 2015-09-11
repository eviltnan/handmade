from kivy.properties import NumericProperty
import pytest
from handmade.models.base import JsonStoragedModel
from handmade.models.storages import JsonModelStorage
import os


class TestModel(JsonStoragedModel):
    foo = NumericProperty()


def test_base_model_meta():
    from handmade.models.base import BaseModel
    assert BaseModel.DoesNotExist != TestModel.DoesNotExist


def test_storage_creation():
    instance = TestModel()
    assert instance.storage


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
