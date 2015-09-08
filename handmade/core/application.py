from kivy.app import App


class HandmadeApplication(App):
    def build(self):
        import importlib
        from handmade.conf import settings
        module, klass = settings.ROOT_WIDGET.rsplit(".", 1)
        klass = getattr(importlib.import_module(module), klass)
        return klass()
