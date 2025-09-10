# utils.py

def is_os_partition(partition_name):
    """
    Dummy function: checks if partition contains OS.
    Later: detect OS files (Windows/System32, Linux /boot).
    """
    if "C:" in partition_name or "root" in partition_name:
        return True
    return False
