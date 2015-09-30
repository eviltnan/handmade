# coding=utf-8
from invoke import ctask as task


@task
def all(c):
    from handmade.resources.managers import ResourceManager
    from handmade.conf import settings
    for plugin in settings.PLUGINS:
        print "%s:" % plugin
        for type_key, manager in ResourceManager.managers.items():
            ids = manager.registry[plugin].keys()
            if ids:
                print u"╚%s: %s" % (type_key, ",".join(ids))
