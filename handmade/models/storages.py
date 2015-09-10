import re


class BaseModelStorage(object):
    def create(self, instance):
        raise NotImplementedError("Create storage entry for model is not implemented in base storage")

    def delete(self, instance):
        raise NotImplementedError("Delete storage entry for model is not implemented in base storage")

    def update(self, instance):
        raise NotImplementedError("Update storage entry for model is not implemented in base storage")

    def get(self, id, model_class):
        raise NotImplementedError("Get storage entry by id for model class is not implemented in base storage")


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class JsonModelStorage(BaseModelStorage):
    def create(self, instance):
        if instance.id is not None:
            raise NotImplementedError()

        new_key = int(max(self._json_storage.keys() or [0])) + 1
        instance.id = int(new_key)

        data = {}
        for property in instance.properties():
            if property != 'id':
                data[property] = getattr(instance, property)

        self._json_storage.put(new_key, **data)

    def _get_filename(self):
        return "models/%s.json" % convert(self.model_class.__name__)

    def __init__(self, model_class):
        self.model_class = model_class
        self.filename = self._get_filename()
        from kivy.storage.jsonstore import JsonStore
        self._json_storage = JsonStore(self.filename)
        super(JsonModelStorage, self).__init__()
