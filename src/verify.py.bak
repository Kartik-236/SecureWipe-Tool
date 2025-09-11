import os
import json
from datetime import datetime

# ===== Optional crypto imports =====
try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except Exception:
    CRYPTO_AVAILABLE = False

# ===== Optional PDF generation imports =====
try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas as pdfcanvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# ===== Paths =====
REPORT_DIR = os.path.join(os.getcwd(), 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)

# ===== Helpers =====
def _now_iso():
    """Generate ISO-like timestamp safe for Windows filenames."""
    return datetime.utcnow().replace(microsecond=0).isoformat().replace(":", "-") + 'Z'

def _generate_demo_keypair():
    """Generate demo RSA keypair if cryptography available."""
    if not CRYPTO_AVAILABLE:
        return None, None

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Save to files
    private_path = os.path.join(REPORT_DIR, "demo_private.pem")
    public_path = os.path.join(REPORT_DIR, "demo_public.pem")

    with open(private_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(public_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Generated demo keypair: {private_path} {public_path}")
    return private_path, public_path

# ===== Save JSON report =====
def save_json_report(report_obj):
    json_path = os.path.join(REPORT_DIR, f"report_{_now_iso()}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report_obj, f, indent=2)
    return json_path

# ===== Save PDF report =====
def save_pdf_report(report_obj):
    if not REPORTLAB_AVAILABLE:
        return None

    pdf_path = os.path.join(REPORT_DIR, f"report_{_now_iso()}.pdf")
    c = pdfcanvas.Canvas(pdf_path, pagesize=LETTER)
    c.setFont("Helvetica", 12)
    y = 750
    c.drawString(50, y, "Data Wipe Tool Report")
    y -= 20
    for k, v in report_obj.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 15
    c.save()
    return pdf_path

# ===== Verification helpers =====
def _verify_wipe_file(file_path, pattern_byte=b'\x00'):
    """
    Reads back a file and checks that it only contains the pattern_byte.
    Returns True if verified, False otherwise.
    """
    if not os.path.exists(file_path):
        # If file removed completely after wiping, consider verified
        return True
    try:
        with open(file_path, 'rb') as f:
            chunk_size = 4096
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                if any(b != pattern_byte[0] for b in data):
                    return False
        return True
    except Exception:
        return False

# ===== Main function to generate a report =====
def generate_report(mode='file', target=None, verified=False, private_key_path=None):
    """Generate a JSON (and optionally PDF) report."""
    # Construct report object
    report_obj = {
        'mode': mode,
        'target': target,
        'verified': verified,
        'timestamp': _now_iso()
    }

    json_path = save_json_report(report_obj)
    pdf_path = save_pdf_report(report_obj)

    print(f"Report saved as JSON: {json_path}")
    if pdf_path:
        print(f"Report saved as PDF: {pdf_path}")

    return {
        'json': json_path,
        'pdf': pdf_path
    }

# ===== Public API: verify_wipe =====
def verify_wipe(target, mode='file', pattern_byte=b'\x00'):
    """
    Verify that a file or partition was wiped.
    For files: read back and check all bytes match pattern_byte or file is deleted.
    For partitions: currently not implemented.
    """
    if mode == 'file':
        is_verified = _verify_wipe_file(target, pattern_byte=pattern_byte)
    else:
        # Placeholder for partition-level verification
        is_verified = False

    report_obj = {
        'mode': mode,
        'target': target,
        'verified': is_verified,
        'timestamp': _now_iso()
    }

    json_path = save_json_report(report_obj)
    pdf_path = save_pdf_report(report_obj)

    return {
        'verified': is_verified,
        'json': json_path,
        'pdf': pdf_path,
        'report': report_obj
    }

# ===== Entry point =====
if __name__ == "__main__":
    # Generate demo keypair first
    _generate_demo_keypair()

    # Example usage of verify_wipe
    test_file = "test_wipe_file.txt"
    # Create a file and overwrite it to mimic a wipe
    with open(test_file, 'wb') as f:
        f.write(b'\x00' * 1024)  # 1KB zeros
    # Now verify
    result = verify_wipe(test_file, mode='file')
    print("Verification result:", result)
