from handmade.plugins import Plugin


class CorePlugin(Plugin):
    def configure(self):
        import os

        import handmade
        import kivy

        kivy.kivy_data_dir = os.path.join(os.path.dirname(handmade.__file__), 'data')


plugin = Plugin.register('handmade.core', CorePlugin)
