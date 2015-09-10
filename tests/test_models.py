from kivy.properties import NumericProperty
from handmade.models import BaseModel
from handmade.models.storages import JsonModelStorage


class TestModel(BaseModel):
    foo = NumericProperty()


def test_json_storage_filename():
    storage = JsonModelStorage(TestModel)
    assert storage.filename == 'models/test_model.json'


def test_json_storage_create():
    storage = JsonModelStorage(TestModel)

    instance = TestModel(foo=1)
    storage.create(instance)
    assert instance.id == 1, "Instance didn't get id after saving in json storage"
