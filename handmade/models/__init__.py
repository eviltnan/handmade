from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class BaseModel(EventDispatcher):
    id = NumericProperty(None, allownone=True)
    storage = None

    def save(self):
        raise NotImplementedError("Save is not implemented in base model")

    def delete(self):
        raise NotImplementedError("Delete is not implemented in base model")

# class JsonStorageModel(BaseModel):
