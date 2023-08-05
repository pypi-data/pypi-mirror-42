import errno
import os
import subprocess
import sys
from .helpers import prepare_subprocess_env


# POSIX-only, from borg 1.1 platform.base
def sync_dir(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    except OSError as os_error:
        # Some network filesystems don't support this and fail with EINVAL.
        # Other error codes (e.g. EIO) shouldn't be silenced.
        if os_error.errno != errno.EINVAL:
            raise
    finally:
        os.close(fd)


# most POSIX platforms (but not Linux), see also borg 1.1 platform.base
def umount(mountpoint):
    env = prepare_subprocess_env(system=True)
    return subprocess.call(['umount', mountpoint], env=env)


if sys.platform.startswith('linux'):  # pragma: linux only
    from .platform_linux import acl_get, acl_set, umount, API_VERSION
elif sys.platform.startswith('freebsd'):  # pragma: freebsd only
    from .platform_freebsd import acl_get, acl_set, API_VERSION
elif sys.platform == 'darwin':  # pragma: darwin only
    from .platform_darwin import acl_get, acl_set, API_VERSION
else:  # pragma: unknown platform only
    API_VERSION = '1.0_01'

    def acl_get(path, item, st, numeric_owner=False):
        pass

    def acl_set(path, item, numeric_owner=False):
        pass
