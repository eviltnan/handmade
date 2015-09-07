import re


class JsonStorage(object):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def write(self, data):
        with open(self.filename, 'r') as f:
            return f.write(self.filename)


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class ModelStorage(JsonStorage):
    def __init__(self, model_klass):
        filename = "%s.json" % convert(model_klass.__name__)
        super(ModelStorage, self).__init__(filename)
