from handmade.models import BaseModel
from handmade.models.storages import ModelStorage


class TestModel(BaseModel):
    pass


def test_model_storage_no_file():
    storage = ModelStorage(TestModel)
    storage.read()
