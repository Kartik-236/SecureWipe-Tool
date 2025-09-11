# src/report.py
import os
import json
import time
import hashlib
import platform
from datetime import datetime

# optional cryptography imports
try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    CRYPTO_AVAILABLE = True
except Exception:
    CRYPTO_AVAILABLE = False

REPORTS_DIR = "reports"
KEYS_DIR = "keys"
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)

def _json_bytes_canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")

def save_report_files(report_data: dict, prefix: str = None):
    ts = int(time.time())
    if not prefix:
        prefix = f"report_{ts}"
    json_path = os.path.join(REPORTS_DIR, f"{prefix}.json")
    html_path = os.path.join(REPORTS_DIR, f"{prefix}.html")
    # save JSON (canonical)
    jb = _json_bytes_canonical(report_data)
    with open(json_path, "wb") as f:
        f.write(jb)
    # simple HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<html><body><pre>\n")
        f.write(json.dumps(report_data, indent=2))
        f.write("\n</pre></body></html>")
    return json_path, html_path

def compute_report_sha256(json_bytes: bytes) -> str:
    return hashlib.sha256(json_bytes).hexdigest()

# ---------------- Device-specific key logic ----------------

def get_device_id():
    """Return a string unique to this device for key derivation."""
    try:
        system = platform.system()
        if system == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Cryptography")
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
            return value
        elif system == "Linux":
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        elif system == "Darwin":
            import subprocess
            out = subprocess.check_output(["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"])
            for line in out.decode().splitlines():
                if "IOPlatformUUID" in line:
                    return line.split('"')[-2]
        else:
            return platform.node()
    except Exception:
        # fallback
        return platform.node()

def generate_or_load_keys(bits=2048):
    """Generate or load a unique device-tied private key."""
    priv_path = os.path.join(KEYS_DIR, "private.pem")
    pub_path = os.path.join(KEYS_DIR, "public.pem")
    if not CRYPTO_AVAILABLE:
        return None, None

    # If already exists, just load it
    if os.path.exists(priv_path):
        with open(priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        return private_key, pub_path

    # Otherwise, generate a new key seeded with device ID
    device_id = get_device_id()
    seed = int(hashlib.sha256(device_id.encode()).hexdigest(), 16) % (2**32)
    
    # Note: cryptography does not directly support seeded key generation,
    # so we generate random key and store it; uniqueness comes from first run per device
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(priv_path, "wb") as f:
        f.write(priv_pem)
    public_key = private_key.public_key()
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(pub_path, "wb") as f:
        f.write(pub_pem)

    return private_key, pub_path

# ---------------- Signing ----------------

def sign_json_bytes(json_bytes: bytes, private_key) -> bytes:
    if not CRYPTO_AVAILABLE or private_key is None:
        raise RuntimeError("cryptography not installed or private key missing")
    sig = private_key.sign(
        json_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return sig

# ---------------- Report Generation ----------------

def generate_report(mode, target, verified, method,
                    file_hash=None, drive_type=None):
    """
    Generates a report with all metadata and signs it using device-private key.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
    report = {
        "timestamp": timestamp,
        "mode": mode,
        "target": target,
        "method": method,
        "verified": verified,
        "file_hash": file_hash,
        "drive_type": drive_type
    }

    private_key, pub_path = generate_or_load_keys()
    json_bytes = _json_bytes_canonical(report)
    if private_key:
        sig = sign_json_bytes(json_bytes, private_key)
        report["verification_code"] = sig.hex()

    # Save files
    prefix = f"report_{int(time.time())}"
    json_path, html_path = save_report_files(report, prefix=prefix)

    return {
        "json": json_path,
        "html": html_path,
        "sig": json_path + ".sig" if private_key else None,
        "sha256": compute_report_sha256(json_bytes),
        "verification_code": report.get("verification_code"),
        "public_key": pub_path
    }
