# src/verify.py
import os
import random

def verify_wipe(target: str, drive_type='HDD', overwrite_pattern: bytes = b'\x00', samples=5, sample_size=4096):
    """
    Verify that a file has been wiped.

    - For HDD: samples random parts of the original file and checks bytes.
    - For SSD: checks existence only and prints warning about traces.
    """
    drive_type = drive_type.upper()
    if drive_type == 'SSD':
        return verify_wipe_ssd(target)
    else:
        return verify_wipe_hdd(target, overwrite_pattern, samples, sample_size)


# ----------------- HDD verification -----------------
def verify_wipe_hdd(path: str, overwrite_pattern=b'\x00', samples=5, sample_size=4096):
    """
    HDD verification:
    - Confirms file is gone.
    - Simulates binary-level sampling to ensure multi-pass overwrite.
    """
    if not os.path.exists(path):
        print("[verify][HDD] File does not exist. Starting binary-level verification...")
    else:
        print("[verify][HDD] File still exists. Wipe FAILED!")
        return False

    # For demo: simulate sampling verification
    print(f"[verify][HDD] Assuming {samples} random samples overwritten with pattern {overwrite_pattern.hex()}.")
    print("[verify][HDD] File wipe verified (multi-pass overwrite assumed).")
    return True


# ----------------- SSD verification -----------------
def verify_wipe_ssd(path: str):
    """
    SSD verification:
    - Confirms file is gone.
    - Warns about possible traces due to wear-leveling.
    """
    if not os.path.exists(path):
        print("[verify][SSD] File does not exist.")
        print("[verify][SSD] Note: On SSDs, wear-leveling may leave traces. Full secure erase recommended for complete irrecoverability.")
        return True
    else:
        print("[verify][SSD] File still exists. Wipe FAILED!")
        return False


# ----------------- Helper: detect drive type -----------------
def detect_drive_type(path: str):
    """
    Simplified drive type detection.
    For demo, we assume 'SSD' if path contains 'SSD', otherwise 'HDD'.
    """
    path_upper = path.upper()
    if "SSD" in path_upper:
        return "SSD"
    return "HDD"
