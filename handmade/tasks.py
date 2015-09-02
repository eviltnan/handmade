from invoke import ctask as task
from invoke import Collection
from plugins.project import tasks as project_tasks


@task(default=True)
def probe(c):
    print "probe called"


ns = Collection(probe)
ns.add_collection(Collection.from_module(project_tasks, name='project'))
