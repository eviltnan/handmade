from kivy.uix.widget import Widget


class ModelWidget(Widget):
    def copy_properties(self):
        raise NotImplementedError()

    def __init__(self, instance_id, **kwargs):
        super(ModelWidget, self).__init__(**kwargs)
