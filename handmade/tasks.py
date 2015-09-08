import os

os.environ.setdefault("HANDMADE_SETTINGS_MODULE", "settings")
from invoke import Collection
from handmade.core import tasks as core_tasks
from plugins import tasks_collections

ns = Collection.from_module(core_tasks, name='core')

for plugin, module in tasks_collections():
    ns.add_collection(Collection.from_module(module), name=plugin)
