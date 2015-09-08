from invoke import ctask as task
from invoke import Collection
from handmade.project import tasks as project_tasks
from handmade.core import tasks as core_tasks


@task(default=True)
def probe(c):
    print "probe called"


ns = Collection(probe)
ns.add_collection(Collection.from_module(project_tasks, name='project'))
ns.add_collection(Collection.from_module(core_tasks, name='core'))
