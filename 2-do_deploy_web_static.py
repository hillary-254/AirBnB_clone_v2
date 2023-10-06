#!/usr/bin/python3
# distributes an archive to your web servers

from fabric.api import run, put, env
import os

env.hosts = ['54.208.23.186', '18.234.80.12'] 
env.user = 'ubuntu'

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
