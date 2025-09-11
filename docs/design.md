High-level architecture:

main.py: orchestrates wiping, verification, report generation

src/wipe_utils.py: actual wipe logic (HDD/SSD)

src/verify.py: verification logic (HDD binary check / SSD warning)

src/report.py: report generation, hash, signature

Flow diagram (optional image or ASCII):

User selects file → main.py

Detect drive type → wipe_utils.wipe()

File wiped → verify.py checks → prints messages

Report generated → JSON/HTML/PDF + signature

Decision points:

HDD vs SSD

File vs partition

Verification method






User -> main.py -> wipe_utils.py -> verify.py -> report.py -> /reports


### Components
- **main.py**: Orchestrates wiping, verification, and report generation.
- **src/wipe_utils.py**: Implements the wiping logic for HDD and SSD.
- **src/verify.py**: Verifies deletion; HDD binary checks, SSD warnings.
- **src/report.py**: Generates reports (JSON/HTML/PDF) with SHA256 hash and optional signature.

## Workflow
1. User provides the path of file/partition.
2. `main.py` detects drive type.
3. File/partition is wiped using `wipe_utils.wipe()`:
   - HDD: multi-pass overwrite.
   - SSD: overwrite + encrypt + delete.
4. Verification:
   - HDD: samples binary data at random offsets.
   - SSD: existence check and warning about wear-leveling.
5. `report.py` generates a report:
   - Includes file hash, verification status, wipe method, drive type.
   - Saves report in `/reports`.
   - Signs report with unique private key.

## Decision Points
- **HDD vs SSD**: Determines wipe and verification method.
- **File vs Partition**: Determines whether bootable media is required.
- **Verification Method**: Multi-pass for HDD; existence/encryption for SSD.

## Notes
- SSD verification cannot fully guarantee unrecoverability due to wear-leveling.
- Future work: integrate online verification portal.