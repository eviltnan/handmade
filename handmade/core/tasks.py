from invoke import ctask as task
from dispatcher import events


@task
def handmade_reinstall(c):
    # todo: fix this hardcode
    c.run('cd ../handmade; python setup.py install')


@task(pre=[handmade_reinstall])
def run(c):
    events.dispatch('on_initialization')
    from application import HandmadeApplication
    app = HandmadeApplication()
    app.run()


# todo: reinstall should be something like setting
@task(pre=[handmade_reinstall])
def shell(c):
    events.dispatch('on_initialization')
    from IPython import start_ipython
    start_ipython([])
