# main.py
import os
import hashlib
from src.wipe_utils import wipe, detect_drive_type
from src.verify import verify_wipe
from src.report import generate_report

def compute_file_hash(file_path):
    """Compute SHA256 hash of the file before wiping."""
    sha = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sha.update(chunk)
    return sha.hexdigest()

def main():
    print("DEBUG: Inside main()")
    print("==== Secure Wipe Tool ====")
    
    target = input("Enter the full path of the file to wipe: ").strip()
    
    if not os.path.exists(target):
        print("[main] File not found.")
        return

    # Compute hash before wiping
    file_hash = compute_file_hash(target)
    # Detect drive type
    drive_type = detect_drive_type(target)

    # Verify wipe
    verified = verify_wipe(target, drive_type=drive_type)


    print(f"[main] File hash: {file_hash}")
    print(f"[main] Drive type: {drive_type}")

    # Wipe file
    print("[main] Starting wipe...")
    success = wipe(target)
    if not success:
        print("[main] Wipe failed.")
        return

    # Verify deletion
    print("[main] Verifying deletion...")
    drive_type = detect_drive_type(target)
    verified = verify_wipe(target, drive_type=drive_type)

    print(f"[main] Verified deletion: {verified}")

    # Choose method string based on drive type
    method = "multi-pass-overwrite" if drive_type == "HDD" else "single-pass-trim"

    # Generate signed report
    report = generate_report(
        mode='file',
        target=target,
        verified=verified,
        method=method,
        file_hash=file_hash,
        drive_type=drive_type
    )

    print("[main] Report generated:")
    print(f"  JSON: {report['json']}")
    print(f"  HTML: {report['html']}")
    if report.get('sig'):
        print(f"  Signature: {report['sig']}")
    if report.get('verification_code'):
        print(f"  Verification code: {report['verification_code']}")
    if report.get('public_key'):
        print(f"  Public key path: {report['public_key']}")

# ===== Ensure main() runs =====
if __name__ == "__main__":
    print("DEBUG: Calling main()")
    main()
