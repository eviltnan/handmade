from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class BaseModelMeta(type):
    def __new__(cls, *args, **kwargs):
        super_new = super(BaseModelMeta, cls).__new__(cls, *args, **kwargs)

        class DoesNotExist(getattr(super_new, 'DoesNotExist', Exception)):
            pass

        super_new.DoesNotExist = DoesNotExist
        return super_new


class BaseModel(EventDispatcher):
    __metaclass__ = BaseModelMeta
    id = NumericProperty(None, allownone=True)
    storage = None

    def save(self):
        raise NotImplementedError("Save is not implemented in base model")

    def delete(self):
        raise NotImplementedError("Delete is not implemented in base model")

# class JsonStorageModel(BaseModel):
