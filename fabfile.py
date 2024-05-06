#!/usr/bin/python
"""
This module generates a .tgz archive from the contents of the web_static folder
"""


from fabric import task, Connection
from datetime import datetime
import os


@task
def dopack(ctx):
    """
    This function generates a .tgz archive from the contents of the
    web_static folder
    """

    if not os.path.exists("versions"):
        os.mkdir("versions")

    current_date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the archive path
    # os.path.join can also be used with directory and filename
    archivepath = "versions/web_static_{}.tgz".format(current_date)

    # Generate the archive
    result = ctx.run("tar -cvzf {} web_static".format(archivepath))

    if result.exited == 0:
        return archivepath
    else:
        return None


@task
def dodeploy(ctx, archivepath=dopack()):
    """
    Distributes an archive to web servers

    This function takes an archivepath as an argument and deploys it to
    multiple web servers. The archivepath should be a path to a .tgz file.

    Parameters:
        archivepath (str): Path to the archive file.

    Returns:
        True if all commands are executed successfully, False otherwise.
    """

    # Check if the archivepath exists
    if not os.path.exists(archivepath):
        return False

    # Define the list of web server hosts
    hosts = ["3.90.85.174", "100.26.159.203"]

    # Remove the file extension from the archivepath
    file_no_ext = os.path.splitext(archivepath)[0]

    # Deploy the archive to each web server
    for host in hosts:
        with Connection(host=host, user="ubuntu") as c:
            # Copy the archive file to the /tmp/ directory on the web server
            c.put("archivepath", "/tmp/")

            # Create the releases directory if it does not exist
            c.sudo("mkdir -p /data/web_static/releases/{}".format(
                file_no_ext
            ))

            # Extract the archive file to the releases directory
            c.sudo("tar -xzf {} -C /data/web_static/releases/{}".format(
                archivepath, file_no_ext
            ))

            # Move the contents of the releases directory to the web_static
            # directory
            c.sudo("mv /data/web_static/releases/{}/web_static/*\
 /data/web_static/releases/{}".format(file_no_ext, file_no_ext))

            # Remove the web_static directory from the releases directory
            c.sudo("rm -rf /data/web_static/releases/{}/web_static".format(
                file_no_ext
            ))

            # Remove the archive file from the /tmp/ directory on the web
            # server
            c.sudo("rm -f /tmp/{}".format(archivepath))

            # Remove the symlink to the current directory
            c.sudo("rm -rf /data/web_static/current")

            # Create a symlink to the newly deployed release
            c.sudo("ln -s /data/web_static/releases/{} /data/web_static/\
current".format(file_no_ext))

    return True
