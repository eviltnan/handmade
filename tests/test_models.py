from kivy.properties import NumericProperty
import pytest
from handmade.models import BaseModel
from handmade.models.storages import JsonModelStorage
import os


class TestModel(BaseModel):
    foo = NumericProperty()


@pytest.fixture
def json_storage(request):
    storage = JsonModelStorage(TestModel)

    def finalizer():
        print storage.filename
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
