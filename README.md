# Secure Wipe Tool

## Description
Local tool to securely delete files or partitions on HDD and SSD drives. Ensures files are overwritten, deleted, and generates verification reports.

## Requirements
- Python 3.9+
- Libraries: `cryptography`, `reportlab` (optional for PDF reports)

## Usage
1. Place your target file in a folder.
2. Run `main.py`:
   ```bash
   python main.py
Enter full path to the file you want to wipe.

Tool will detect drive type (HDD/SSD) and perform the appropriate wipe.

Verification messages are printed:

HDD: shows multi-pass overwrite confirmation.

SSD: warns about wear-leveling traces.

Reports are saved in /reports folder:

JSON, HTML, optional PDF.

SHA256 hash and verification code included.

Notes
Opening a file in another program (e.g., Notepad) may show cached content even after deletion; the file is deleted on disk.

For SSDs, full secure erase may be required for guaranteed unrecoverability.

Future updates may include online verification via public key.

yaml
Copy code

---

## 4️⃣ **test_plan.md**

```markdown
# Test Plan: Secure Wipe Tool

## File-Level Wipe Testing
1. Create a test file (`test_file.txt`) in the project folder.
2. Run `main.py` and enter the full path of the test file.
3. Verify:
   - File gets deleted from the folder.
   - Verification messages appear:
     - HDD: shows multi-pass overwrite check.
     - SSD: shows wear-leveling warning.
   - SHA256 hash matches the original content.
4. Open the `/reports` folder:
   - JSON, HTML, optional PDF are created.
   - Signed report exists (if private key present).
   - Verification code matches the hash.

## SSD vs HDD Testing
1. Run the tool on both HDD and SSD test files.
2. Confirm drive detection is correct.
3. Check messages:
   - HDD: binary verification passes/fails.
   - SSD: existence check + warning printed.

## Optional Edge Tests
- Open test file in another application before wiping.
- Test with small and large files.
- Test multiple consecutive files.
