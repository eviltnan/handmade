from kivy.properties import partial, Property

from kivy.uix.widget import Widget, WidgetMetaclass


def propagate_to_model(widget, property_name, model_instance, value):
    setattr(widget, property_name, value)


def propagate_to_widget(property_name, widget, value):
    setattr(widget.model_instance, property_name, value)


class ModelWidgetMeta(WidgetMetaclass):
    def __new__(cls, klass, parents, *args, **kwargs):
        super_new = super(ModelWidgetMeta, cls).__new__(cls, klass, parents, *args, **kwargs)
        if super_new.model_class:
            properties = {}
            for field in super_new.model_class.__dict__.keys():
                field_value = getattr(super_new.model_class, field)
                if isinstance(field_value, Property):
                    properties[field] = field_value
            for model_property_name, model_property in properties.items():
                if model_property_name != 'id':
                    assert not hasattr(super_new, model_property_name), \
                        'Model widget %s has attribute named the same as model attribute: %s, value: %s.' \
                        'Model properties will be mapped to widget properties automatically' % (
                            super_new.__class__.__name__,
                            model_property_name,
                            getattr(super_new, model_property_name)
                        )
                    setattr(super_new, model_property_name, model_property)
        else:
            if Widget not in parents:
                raise RuntimeError("Model widget class %s doesn't define a model class" % super_new.__name__)
        return super_new


class ModelWidget(Widget):
    model_class = None
    __metaclass__ = ModelWidgetMeta

    def bind_properties(self):
        properties = self.model_instance.properties()
        self.apply_property(**properties)
        model_bindings = {model_property_name: partial(propagate_to_model, self, model_property_name) for
                          model_property_name in properties}
        self.model_instance.bind(**model_bindings)

        widget_bindings = {model_property_name: partial(propagate_to_widget, model_property_name) for
                           model_property_name in properties}
        self.bind(**widget_bindings)

    def assign_model_properties(self):
        for model_property_name in self.model_instance.properties():
            if model_property_name != 'id':
                setattr(self, model_property_name, getattr(self.model_instance, model_property_name))

    def __init__(self, instance=None, instance_id=None, **kwargs):
        assert instance_id or instance, "Model widget should get either instance id to get pick it from storage" \
                                        "or the model instance"
        assert not (instance and instance_id), "You can either specify an instance or instance_id for model widget," \
                                               "both doesn't make sense"
        if not instance:
            self.model_instance = self.model_class.storage.get(id_=instance_id)
        else:
            self.model_instance = instance

        self.bind_properties()
        self.assign_model_properties()
        super(ModelWidget, self).__init__(**kwargs)

        # todo: rename id? the same prop for widget, not good
