#!/usr/bin/python3
"""
 a Fabric script that generates a .tgz archive
 from the contents of the web_static folder of your
 AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """ Generates a .tgz archive from the folder web_static folder
    """
    local("mkdir -p versions")

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(date)

    result = local("tar -cvzf {} web_static".format(archive_name))
    if result.succeeded:
        return archive_name
    else:
        return None
