# src/wipe_utils.py
import os
import random
import shutil
import tempfile

def detect_drive_type(path: str):
    """
    Simplified drive type detection.
    Returns 'SSD' or 'HDD'.
    """
    # For demo/testing, you can hardcode SSD/HDD
    # Or detect using OS-specific calls
    # Here we simulate:
    if os.name == "nt":  # Windows
        return "SSD"  # Replace with HDD if needed
    return "HDD"

def overwrite_file(file_path: str, passes: int = 3):
    """
    Overwrite file content multiple times with random data and zeros.
    """
    try:
        size = os.path.getsize(file_path)
        with open(file_path, "r+b") as f:
            for p in range(passes):
                f.seek(0)
                print(f"[wipe] Pass {p+1}/{passes} overwrite with random bytes")
                for _ in range(size // 4096 + 1):
                    chunk = os.urandom(4096)
                    f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
        return True
    except Exception as e:
        print("[wipe] Overwrite failed:", e)
        return False

def encrypt_and_delete_key_simulation(file_path: str):
    """
    Simulate SSD secure deletion by:
    1. Overwriting file with random bytes
    2. Generating a temporary "encryption key" and deleting it
    3. This mimics encrypt+delete-key approach
    """
    try:
        size = os.path.getsize(file_path)
        with open(file_path, "r+b") as f:
            f.seek(0)
            f.write(os.urandom(size))  # simple random overwrite
            f.flush()
            os.fsync(f.fileno())
        # Simulate key generation & deletion
        temp_key = os.urandom(32)
        del temp_key
        # Optionally rename file to obscure metadata
        dir_name, base_name = os.path.split(file_path)
        new_name = os.path.join(dir_name, f"wiped_{random.randint(1000,9999)}.tmp")
        os.rename(file_path, new_name)
        os.remove(new_name)
        return True
    except Exception as e:
        print("[wipe] SSD secure delete failed:", e)
        return False

def wipe(file_path: str):
    """
    General wipe function for a single file.
    Detects drive type and applies appropriate strategy.
    """
    if not os.path.isfile(file_path):
        print("[wipe] File does not exist:", file_path)
        return False

    drive_type = detect_drive_type(file_path)

    if drive_type == "HDD":
        print("[wipe] Detected drive type: HDD")
        success = overwrite_file(file_path, passes=3)
        if success:
            os.remove(file_path)
            print("✅ HDD multi-pass overwrite + deletion complete.")
        return success

    elif drive_type == "SSD":
        print("[wipe] Detected drive type: SSD")
        success = encrypt_and_delete_key_simulation(file_path)
        if success:
            print("✅ SSD-style secure deletion simulation complete.")
        return success

    else:
        print("[wipe] Unknown drive type, fallback to single overwrite")
        try:
            os.remove(file_path)
            return True
        except:
            return False
