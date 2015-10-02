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


class ImageResource(BaseResource):
    class FileNotFound(Exception):
        pass

    def validate(self, *args, **kwargs):
        if not os.path.exists(self.filename):
            raise ImageResource.FileNotFound("Image %s not found" % self.filename)

    @classmethod
    def default_value(cls, value):
        return {
            "filename": value
        }

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename

    def get(self, *args, **kwargs):
        return self.filename
