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
    @classmethod
    def default_value(cls, value):
        return {
            "filename": value
        }

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename

    def get(self, *args, **kwargs):
        return self.filename
