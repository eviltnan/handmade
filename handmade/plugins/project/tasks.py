from invoke import ctask as task


@task
def start(c):
    print "project start called"
