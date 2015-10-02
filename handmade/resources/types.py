import os


class BaseResource(object):
    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def validate(self, *args, **kwargs):
        raise NotImplementedError()

    def process(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def default_value(cls, value):
        raise NotImplementedError()

    def __init__(self):
        self.validate()


class FileResource(BaseResource):
    class FileNotFound(Exception):
        pass

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        super(FileResource, self).__init__()

    def get(self, *args, **kwargs):
        return self.filename

    @classmethod
    def default_value(cls, value):
        return {
            "filename": value
        }

    def process(self, *args, **kwargs):
        app_path = os.getcwd()
        full_path = os.path.join(app_path, self.filename)
        raise NotImplementedError()

    def validate(self, *args, **kwargs):
        if not os.path.exists(self.filename):
            raise FileResource.FileNotFound("Image %s not found" % self.filename)


class ImageResource(FileResource):
    pass
