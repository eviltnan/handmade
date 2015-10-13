import os

# hack for kivy not being run
os.environ["KIVY_NO_ARGS"] = '1'
from kivy.config import Config

Config.set('kivy', 'log_level', 'debug')

from invoke import Collection

from handmade.plugins import discover, Plugin

discover()
from handmade.conf import settings

ns = Collection.from_module(Plugin.plugins['handmade.core'].tasks, name='core')

for plugin_name in settings.PLUGINS:
    if plugin_name == 'handmade.core':
        continue
    plugin = Plugin.plugins[plugin_name]
    collection_name = plugin_name.replace("handmade.", "")  # built in plugins won't have prefix
    collection_name = collection_name.replace(".", "_")  # period causes invoke crash
    if plugin.tasks:
        ns.add_collection(Collection.from_module(plugin.tasks), name=collection_name)
