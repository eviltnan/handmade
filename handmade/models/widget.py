from kivy.properties import partial

from kivy.uix.widget import Widget


class ModelWidget(Widget):
    model_class = None

    def propagate_to_model(self, property_name, model_instance, value):
        setattr(self, property_name, value)

    def propagate_to_widget(self, property_name, widget, value):
        setattr(self.model_instance, property_name, value)

    def bind_model_properties(self):
        for model_property_name, model_property in self.model_instance.properties().items():
            if model_property_name != 'id':
                assert not hasattr(self, model_property_name), \
                    'Model widget %s has attribute named the same as model attribute: %s, value: %s.' \
                    'Model properties will be mapped to widget properties automatically' % (
                        self.__class__.__name__,
                        model_property_name,
                        getattr(self, model_property_name)
                    )

        self.apply_property(**self.model_instance.properties())

        model_bindings = {model_property_name: partial(self.propagate_to_model, model_property_name) for
                          model_property_name in self.model_instance.properties()}

        widget_bindings = {model_property_name: partial(self.propagate_to_widget, model_property_name) for
                           model_property_name in self.model_instance.properties()}

        self.model_instance.bind(**model_bindings)
        self.bind(**widget_bindings)

    def __init__(self, instance=None, instance_id=None, **kwargs):
        assert instance_id or instance, "Model widget should get either instance id to get pick it from storage" \
                                        "or the model instance"
        assert not (instance and instance_id), "You can either specify an instance or instance_id for model widget," \
                                               "both doesn't make sense"
        if not instance:
            self.model_instance = self.model_class.storage.get(id_=instance_id)
        else:
            self.model_instance = instance

        self.bind_model_properties()

        super(ModelWidget, self).__init__(**kwargs)
