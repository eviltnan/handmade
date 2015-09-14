from kivy.uix.widget import Widget


class ModelWidget(Widget):
    model_class = None

    def copy_properties(self):
        raise NotImplementedError()

    def __init__(self, instance=None, instance_id=None, **kwargs):
        assert instance_id or instance, "Model widget should get either instance id to get pick it from storage" \
                                        "or the model instance"
        assert not (instance and instance_id), "You can either specify an instance or instance_id for model widget," \
                                               "both doesn't make sense"
        super(ModelWidget, self).__init__(**kwargs)
        if not instance:
            self.model_instance = self.model_class.storage.get(id_=instance_id)
        else:
            self.model_instance = instance
