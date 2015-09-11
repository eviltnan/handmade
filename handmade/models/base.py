from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from handmade.models.storages import JsonModelStorage


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
    storage_class = None

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        if not self.storage_class:
            raise NotImplementedError("Storage class is not set on %s model" % self.__class__.__name__)
        self.__class__.storage = self.storage_class(self.__class__)

    def save(self):
        self.storage.save(self)

    def delete(self):
        self.storage.delete(self)


class JsonStoragedModel(BaseModel):
    storage_class = JsonModelStorage
