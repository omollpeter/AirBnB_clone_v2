#!/usr/bin/python3
"""
This module combines archiving and deployment
"""


from fabric.operations import run, local, sudo, put
from fabric.api import env, execute
from fabric.context_managers import cd
from datetime import datetime
import os


env.user = "ubuntu"
env.hosts = ["3.90.85.174", "100.26.159.203"]


def list_dirs():
    """
    Test example
    """
    with cd("~/"):
        run("ls -l")


def do_pack():
    """
    This function generates a .tgz archive from the contents of the
    web_static folder
    """

    if not os.path.exists("versions"):
        os.mkdir("versions")

    current_date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the archive path
    # os.path.join can also be used with directory and filename
    archive_path = "versions/web_static_{}.tgz".format(current_date)

    # Generate the archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None


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


def deploy():
    """
    This function distributes an archive to multiple web servers
    """
    archive_path = do_pack()

    if not os.path.exists(archive_path):
        return False
    do_deploy(archive_path)


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    versions = sorted(os.listdir("versions"), reverse=True)

    to_delete = []
    archives = []

    if number == 1 or number == 0:
        for i in range(1, len(versions)):
            to_delete.append(versions[i])
            archives.append(os.path.splitext(versions[i])[0])
    else:
        for i in range(number, len(versions)):
            to_delete.append(versions[i])
            archives.append(os.path.splitext(versions[i])[0])

    def clean_remote():
        with cd("/data/web_static/releases/"):
            for f in archives:
                sudo("rm -rf {}".format(f))

    execute(clean_remote)

    for f in to_delete:
        if os.path.exists(os.path.join("versions", f)):
            local("rm -f versions/{}".format(f))
