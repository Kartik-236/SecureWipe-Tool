# Changelog

## v1.0 – Current
- Added SSD wipe logic: overwrite + encrypt + delete.
- Updated HDD verification: multi-pass binary sampling.
- Updated `main.py` to integrate new `verify.py`.
- Reports now include:
  - Verification notes (HDD/SSD)
  - SHA256 hash of file
  - Verification code
- Removed `mode` argument from `verify_wipe()`.
- Added `detect_drive_type()` helper for drive detection.
- Updated frontend integration planned.
