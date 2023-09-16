#!/usr/bin/python3
"""
 a Fabric script (based on the file 2-do_deploy_web_static.py)
 that creates and distributes an archive to your web servers,
 using the function deploy
"""

from fabric.api import *
from os.path import exists
from os import getenv, environ
from datetime import datetime

env.hosts = ['100.25.165.191', '3.83.245.148']
env.user = 'ubuntu'
env.key_filename = '/home/~/.ssh/id_rsa'


@runs_once
def do_pack():
    """ Generates a .tgz archive from the folder web_static folder
    """
    local("mkdir -p versions")

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{date}.tgz"
    print(f"\nCreating a new_version of web_static: {archive_name}")
    result = local(f"tar -cvzf {archive_name} web_static")
    if result.succeeded:
        return archive_name
    else:
        return None


def do_deploy(archive_path):
    """Deploys the web static to the server"""

    if not exists(archive_path):
        return False
    try:
        archive_name = archive_path.split('/')[-1]
        file_name = archive_name.split('.')[0]
        sym_link = "/data/web_static/current"
        release_version = f"/data/web_static/releases/{file_name}/"

        print(f"\nDeploying new_version from {archive_path}\n")

        # deploying locally
        run_locally = getenv("run_locally", None)
        if run_locally is None:
            print(f"Deploying new_version from {archive_path}")
            local(f"sudo mkdir -p {release_version}")
            local(f"sudo tar -xzf {archive_path} \
-C {release_version} --strip-components=1")
            local(f"sudo rm -f {sym_link}")
            local(f"sudo ln -s {release_version} {sym_link}")
            environ['run_locally'] = "True"
            print("Deployed locally\n")

        put(archive_path, f"/tmp/{archive_name}")
        run(f"mkdir -p {release_version}")
        run(f"tar -xzf /tmp/{archive_name} \
-C {release_version} --strip-components=1")
        run(f"rm /tmp/{archive_name}")
        run(f"rm -f {sym_link}")
        run(f"ln -s {release_version} {sym_link}")
        print(f"\nNew Version Deployed --> {release_version}\n")
        return True
    except Exception as e:
        print(f"\nFailed to Deploy New Version -->{release_version}\n{str(e)}")
        return False


def deploy():
    """Fully deploys web_statics to web servers"""
    archive_path = do_pack()

    return do_deploy(archive_path) if archive_path else False
