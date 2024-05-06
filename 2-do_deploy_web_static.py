#!/usr/bin/python3
"""
This module distributes an archive to your web servers
"""

from fabric import task, Connection
import os


@task
def do_deploy(archive_path):
    """
    Deploys a given archive to web servers using Fabric.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        None if archive path, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    
    # env.hosts = ["3.90.85.174", "100.26.159.203"]

    # try:
    #     with Connection(env.hosts) as c:
    #         c.put(archive_path, "/tmp/")
            