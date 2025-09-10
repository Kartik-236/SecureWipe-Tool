import json
import os
import datetime
from typing import Optional, Dict

# optional cryptography imports
try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except Exception:
    CRYPTO_AVAILABLE = False

# optional PDF generation import
try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas as pdfcanvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# Reports directory
REPORT_DIR = os.path.join(os.getcwd(), 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)

def _now_iso():
    """
    Generate ISO-like timestamp safe for Windows filenames
    (replaces ':' with '-').
    """
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat().replace(":", "-") + 'Z'

def _load_private_key(path: str, password: Optional[bytes] = None):
    if not CRYPTO_AVAILABLE:
        raise RuntimeError('cryptography library is required for signing')
    with open(path, 'rb') as f:
        key_data = f.read()
    return serialization.load_pem_private_key(key_data, password=password, backend=default_backend())

def _sign_data(private_key, data: bytes) -> bytes:
    # Using PKCS1v15 with SHA256 here for compatibility
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def _safe_timestamp(report_obj: Dict) -> str:
    """Extract timestamp and make sure it’s filename-safe."""
    return report_obj.get('timestamp', 'unknown').replace(':', '-')

def save_json_report(report_obj: Dict, filename: Optional[str] = None) -> str:
    if filename is None:
        filename = f"report_{_safe_timestamp(report_obj)}.json"
    out_path = os.path.join(REPORT_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report_obj, f, indent=2)
    return out_path

def save_html_report(report_obj: Dict, filename: Optional[str] = None) -> str:
    if filename is None:
        filename = f"report_{_safe_timestamp(report_obj)}.html"
    out_path = os.path.join(REPORT_DIR, filename)
    html = ["<html><head><meta charset='utf-8'><title>Wipe Report</title></head><body>"]
    html.append(f"<h1>Wipe Report</h1>")
    html.append("<table border='1' cellpadding='6'>")
    for k, v in report_obj.items():
        html.append(f"<tr><th>{k}</th><td>{v}</td></tr>")
    html.append("</table></body></html>")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))
    return out_path

def save_pdf_report(report_obj: Dict, filename: Optional[str] = None) -> Optional[str]:
    if not REPORTLAB_AVAILABLE:
        return None
    if filename is None:
        filename = f"report_{_safe_timestamp(report_obj)}.pdf"
    out_path = os.path.join(REPORT_DIR, filename)
    c = pdfcanvas.Canvas(out_path, pagesize=LETTER)
    width, height = LETTER
    x = 40
    y = height - 60
    c.setFont('Helvetica-Bold', 16)
    c.drawString(x, y, 'Wipe Report')
    c.setFont('Helvetica', 10)
    y -= 30
    for k, v in report_obj.items():
        text = f"{k}: {v}"
        c.drawString(x, y, text)
        y -= 14
        if y < 60:
            c.showPage()
            y = height - 60
    c.save()
    return out_path

def generate_report(mode: str,
                    target: str,
                    verified: bool,
                    method: str = 'overwrite',
                    metadata: Optional[Dict] = None,
                    private_key_path: Optional[str] = None,
                    private_key_password: Optional[bytes] = None) -> Dict:
    """
    Build a structured report and optionally sign it.
    Returns the report object. Also writes JSON/HTML/PDF + signature file (if signing enabled).
    """
    if metadata is None:
        metadata = {}

    report_obj = {
        'timestamp': _now_iso(),
        'mode': mode,
        'target': target,
        'method': method,
        'verified': bool(verified),
        'metadata': metadata
    }

    # Save JSON and HTML immediately
    json_path = save_json_report(report_obj)
    html_path = save_html_report(report_obj)
    pdf_path = None
    if REPORTLAB_AVAILABLE:
        pdf_path = save_pdf_report(report_obj)

    # Sign the JSON report if a private key is provided
    sig_path = None
    if private_key_path:
        if not CRYPTO_AVAILABLE:
            raise RuntimeError('cryptography library required for signing')
        private_key = _load_private_key(private_key_path, password=private_key_password)
        with open(json_path, 'rb') as f:
            data = f.read()
        signature = _sign_data(private_key, data)
        # write signature in binary file
        sig_name = os.path.basename(json_path) + '.sig'
        sig_path = os.path.join(REPORT_DIR, sig_name)
        with open(sig_path, 'wb') as sf:
            sf.write(signature)

    # Add file paths to the returned object for convenience
    report_obj['_files'] = {
        'json': json_path,
        'html': html_path,
        'pdf': pdf_path,
        'sig': sig_path
    }

    return report_obj

# helper: generate an RSA key (for demo only)
def generate_rsa_keypair(out_private: str, out_public: str, key_size: int = 2048, password: Optional[bytes] = None):
    if not CRYPTO_AVAILABLE:
        raise RuntimeError('cryptography library required to generate keys')
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())
    encryption = serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption
    )
    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(out_private, 'wb') as f:
        f.write(priv_pem)
    with open(out_public, 'wb') as f:
        f.write(pub_pem)
    return out_private, out_public

# Quick demo usage when run directly
if __name__ == '__main__':
    # Example: generate a keypair for testing
    try:
        if CRYPTO_AVAILABLE:
            priv, pub = generate_rsa_keypair(os.path.join(REPORT_DIR, 'demo_private.pem'),
                                             os.path.join(REPORT_DIR, 'demo_public.pem'))
            print('Generated demo keypair:', priv, pub)
        else:
            print('cryptography not installed; skipping key generation')
    except Exception as e:
        print('error', e)

    # Example: create a fake report
    r = generate_report(mode='file', target='test.txt', verified=True, private_key_path=None)
    print('Report created:', r)
