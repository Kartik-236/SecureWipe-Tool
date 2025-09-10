# test_integration.py
import os
from time import sleep

# backend functions (Person 1 + Person 2)
from src.wipe_engine import wipe_file        # expects wipe_file(file_path, passes=3)
from src.verify import verify_wipe           # expects verify_wipe(target, mode='file'|'partition', ...)
from src.report import generate_report       # expects generate_report(mode, target, verified, method, private_key_path=...)

# helper - optional key generator in report.py (many implementations include this)
try:
    from src.report import generate_rsa_keypair
except Exception:
    generate_rsa_keypair = None

# test settings
file_path = "Kartik Kaushik Hall Ticket.pdf"
method_id = "3-pass-random"
private_key = os.path.join("reports", "demo_private.pem")
public_key = os.path.join("reports", "demo_public.pem")

# ensure reports dir
os.makedirs("reports", exist_ok=True)

# create demo keys if helper exists and keys missing
if (not os.path.exists(private_key) or not os.path.exists(public_key)) and generate_rsa_keypair is not None:
    try:
        generate_rsa_keypair(private_key, public_key)
        print("Demo keypair generated:", private_key, public_key)
    except Exception as e:
        print("Keygen helper failed:", e)

# 1) Ensure test file exists
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("this is a test secret\n")
    print("Created test file:", file_path)
else:
    print("Using existing test file:", file_path)

# small wait so file timestamp is stable if needed
sleep(0.2)

# 2) Wipe the file (Person 1)
print("\n==> Calling wipe_file() ...")
res = wipe_file(file_path, passes=3)
print("wipe_file returned:", res)

# 3) Verify (Person 2)
print("\n==> Calling verify_wipe() ...")
verified = verify_wipe(file_path, mode='file')
print("verify_wipe returned:", verified)

# 4) Generate report (Person 2)
print("\n==> Calling generate_report() ...")
try:
    generate_report(
        mode='file',
        target=file_path,
        verified=verified,
        method=method_id,
        private_key_path=private_key  # pass path; module will sign if key exists
    )
    print("report generation called (check /reports).")
except Exception as e:
    print("generate_report failed:", e)

print("\n==> FINISHED. Open the reports/ folder to inspect outputs.")
