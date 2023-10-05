from fabric.api import local
from datetime import datetime

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
