# coding=utf-8
from invoke import ctask as task
from handmade.resources.managers import ResourceManager
from handmade.conf import settings


@task
def all(c):
    for plugin in settings.PLUGINS:
        print "%s:" % plugin
        for type_key, manager in ResourceManager.managers.items():
            ids = manager.registry[plugin].keys()
            if ids:
                print u"╚%s: %s" % (type_key, ",".join(ids))


@task
def validate(c):
    for plugin in settings.PLUGINS:
        print u"%s:" % plugin
        for resource_type, manager in ResourceManager.managers.items():
            print u"╚%s:" % resource_type
            for resource_id, resource in manager.registry[plugin].items():
                print u" ╚%s:" % resource_id
                resource.validate()
