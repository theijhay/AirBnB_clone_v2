#!/usr/bin/python3
"""
Distributes an archive to your web servers, using the function do_deploy
"""
import os
from datetime import datetime
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["52.86.36.200", "100.26.232.204"]


def do_pack():
    """Compress files from web_static directory"""
    try:
        if not os.path.isdir("versions"):
            os.makedirs("versions")
        date = datetime.now()
        file = "versions/web_static_{0}{1}{2}{3}{4}{5}".format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
        )
        file += ".tgz"
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy archive

    Args:
        - archive_path(str, optional): Path of the archive
    """
    try:
        if not os.path.isfile(archive_path):
            return False
        path = archive_path.split("/")[1]
        name = path.split(".")[0]
        put(archive_path, "/tmp/{0}".format(path))
        run("sudo mkdir -p /data/web_static/releases/{}/".format(name))
        source = "sudo tar -xzf /tmp/{0} -C".format(path)
        dest = "/data/web_static/releases/{0}/".format(name)
        run(source + " " + dest)
        run("sudo rm /tmp/{0}".format(path))
        source = (
            "sudo mv /data/web_static/releases/{0}/web_static/*".format(name)
        )
        dest = "/data/web_static/releases/{0}/".format(name)
        run(source + " " + dest)
        run(
            "sudo rm -rf /data/web_static/releases/{0}/web_static".format(name)
        )
        run("sudo rm -rf /data/web_static/current")
        source = "sudo ln -s /data/web_static/releases/{0}/".format(name)
        dest = "/data/web_static/current"
        run(source + " " + dest)
        return True
    except Exception:
        return False
