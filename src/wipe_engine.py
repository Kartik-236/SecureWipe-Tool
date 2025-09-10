# wipe_engine.py

def wipe_file(file_path):
    """
    Mode 1: Securely delete a targeted file/folder.
    Steps:
    1. Overwrite contents.
    2. Delete entry from filesystem.
    3. Verify.
    """
    print(f"[Mode 1] Pretending to wipe file: {file_path}")
    return True


def wipe_partition(partition_name, is_os=False):
    """
    Mode 2b: Wipe a single partition.
    - If OS partition → bootable media required.
    - If non-OS → wipe directly.
    """
    if is_os:
        print(f"[Mode 2.b] Partition {partition_name} contains OS. Bootable media required.")
    else:
        print(f"[Mode 2.b] Pretending to wipe non-OS partition: {partition_name}")
    return True


def wipe_full_device(device_name):
    """
    Mode 2a: Wipe entire device (all partitions).
    Always requires bootable media.
    """
    print(f"[Mode 2.a] Full device wipe initiated on {device_name}. Bootable media required.")
    return True
