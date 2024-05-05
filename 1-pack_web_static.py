#!/usr/bin/python
"""
This module generates a .tgz archive from the contents of the web_static folder
"""


from fabric.api import local, task
from datetime import datetime
import os
from collections.abc import Mapping


# @task
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
