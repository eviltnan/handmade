from invoke import ctask as task


@task
def run(c):
    from application import HandmadeApplication
    app = HandmadeApplication()
    app.run()
