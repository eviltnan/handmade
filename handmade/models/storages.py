import os
import re
from handmade.exceptions import ProgrammingError
from handmade.conf import settings


class BaseModelStorage(object):
    def save(self, instance):
        raise NotImplementedError("Create storage entry for model is not implemented in base storage")

    def delete(self, instance):
        raise NotImplementedError("Delete storage entry for model is not implemented in base storage")

    def get(self, id_):
        raise NotImplementedError("Get storage entry by id for model class is not implemented in base storage")

    def __init__(self, model_class):
        self.model_class = model_class


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class JsonModelStorage(BaseModelStorage):
    def delete(self, instance):
        if not instance.id:
            raise RuntimeError("Can't delete unsaved instance")

        try:
            self._json_storage.delete(instance.id)
        except KeyError:
            raise self.model_class.DoesNotExist(
                "%s with id %s is not found in the storage" % (
                    self.model_class.__name__,
                    instance.id
                )
            )

    def get(self, id_):
        try:
            data = self._json_storage[id_]
        except KeyError:
            raise self.model_class.DoesNotExist(
                "%s with id %s is not found in the storage" % (
                    self.model_class.__name__,
                    id_
                )
            )
        return self.model_class(id=id_, **data)

    def save(self, instance):
        if instance.id is None:
            id_ = int(max(self._json_storage.keys() or [0])) + 1
            instance.id = int(id_)
        else:
            id_ = instance.id

        data = {}
        for property_ in instance.properties():
            if property_ != 'id':
                data[property_] = getattr(instance, property_)
        try:
            self._json_storage.put(id_, **data)
        except TypeError as ex:
            raise ProgrammingError("Object of model %s can't be serialized, "
                                   "be careful while using object properties: %s" % (self.__class__.__name__, ex))

    def _get_filename(self):
        path = os.path.join(settings.STORAGE_ROOT, "models")

        if not os.path.exists(path):
            os.makedirs(path)
        return "%s/models/%s.json" % (
            settings.STORAGE_ROOT,
            convert(self.model_class.__name__)
        )

    def __init__(self, model_class):
        super(JsonModelStorage, self).__init__(model_class)
        self.filename = self._get_filename()
        from kivy.storage.jsonstore import JsonStore
        self._json_storage = JsonStore(self.filename)
