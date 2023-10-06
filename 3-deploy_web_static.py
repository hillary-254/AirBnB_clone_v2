#!/usr/bin/python3
# creates and distributes an archive to your web servers

from fabric.api import local, env, run, put
from datetime import datetime
import os

env.hosts = ['54.208.23.186', '18.234.80.12']
env.user = 'ubuntu'

def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    Returns:
        Archive path if successful, None otherwise.
    """
    try:
        current_time = datetime.now()
        archive_name = "web_static_{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}.tgz".format(
            current_time.year, current_time.month, current_time.day,
            current_time.hour, current_time.minute, current_time.second
        )
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None

def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]
        remote_dir = "/data/web_static/releases/{}/".format(archive_no_ext)

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create a new directory for the archive
        run("mkdir -p {}".format(remote_dir))

        # Uncompress the archive to the remote directory
        run("tar -xzf /tmp/{} -C {}".format(archive_name, remote_dir))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_name))

        # Move contents of the uncompressed folder to the new directory
        run("mv {}web_static/* {}".format(remote_dir, remote_dir))

        # Remove the empty web_static directory
        run("rm -rf {}web_static".format(remote_dir))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version
        run("ln -s {} /data/web_static/current".format(remote_dir))

        print("New version deployed!")
        return True
    except Exception:
        return False

def deploy():
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
