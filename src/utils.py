# src/utils.py
import os
import sys
import uuid
import random

CHUNK_SIZE = 4 * 1024 * 1024  # 4 MiB

# locking helpers
if os.name == "nt":
    import msvcrt
else:
    import fcntl

def acquire_lock_fileobj(fileobj):
    """Try to acquire exclusive non-blocking lock. Return True/False."""
    fd = fileobj.fileno()
    if os.name == "nt":
        try:
            # lock one byte (workaround)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            return True
        except Exception:
            return False
    else:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False
        except Exception:
            return False

def release_lock_fileobj(fileobj):
    fd = fileobj.fileno()
    if os.name == "nt":
        try:
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        except Exception:
            pass
    else:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except Exception:
            pass

def is_probably_ssd(path):
    """Best-effort SSD detection on Linux; returns True/False/None."""
    try:
        if sys.platform.startswith("linux"):
            st = os.stat(path)
            major = os.major(st.st_dev)
            minor = os.minor(st.st_dev)
            rot_path = f"/sys/dev/block/{major}:{minor}/queue/rotational"
            if os.path.exists(rot_path):
                with open(rot_path, "r") as f:
                    val = f.read().strip()
                return (val == "0")
    except Exception:
        pass
    return None

def random_name_in_same_dir(path):
    d = os.path.dirname(os.path.abspath(path)) or "."
    return os.path.join(d, f".wipe_{uuid.uuid4().hex}")
