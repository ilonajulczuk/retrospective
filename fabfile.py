from fabric.api import local


def hello():
   print("Hello world!")


def prepare_deploy():
    local("git add -p && git commit")
    local("git push")
