#!/usr/bin/python3
"""
This module distributes archived files to multiple web servers
"""


from fabric.operations import run, local, sudo, put
from fabric.api import env
from fabric.context_managers import cd, lcd
import os


env.user = "ubuntu"
env.hosts = ["3.90.85.174", "100.26.159.203"]


def list_dirs():
    """
    Test example
    """
    with cd("~/"):
        run("ls -l")


def do_deploy(archive_path):
    """
    Distributes archived contents to multiple servers
    """
    if not os.path.exists(archive_path):
        return False

    archivepath = archive_path.split("/")[-1]
    file_name = os.path.splitext(archivepath)[0]

    put(archive_path, "/tmp/")

    sudo("mkdir -p /data/web_static/releases/{}".format(file_name))

    sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
        archivepath, file_name
    ))

    sudo("mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}".format(file_name, file_name))

    sudo("rm -rf /data/web_static/releases/{}/web_static".format(
        file_name
    ))

    sudo("rm -f /tmp/{}".format(archivepath))

    sudo("rm -rf /data/web_static/current")

    sudo("ln -s /data/web_static/releases/{} /data/web_static/\
current".format(file_name))

    return True
