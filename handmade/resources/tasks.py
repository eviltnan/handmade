from invoke import ctask as task


@task
def list(c):
    from handmade.resources import ResourceManager
    from handmade.conf import settings
    for plugin in settings.PLUGINS:
        print "%s:\n" % plugin
        for type_key, manager in ResourceManager.managers.items():
            print "%s: %s" % (type_key, manager.registry[plugin].keys())
