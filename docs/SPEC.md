SIH Project Specification – Secure Wiping & Verification Tool
1. Objective

To design and implement a tool that securely wipes data from drives/partitions/files and generates a digitally signed verification report that proves the data is unrecoverable.

2. Features
Core Features

Selective Wiping

Wipe specific files/folders.

Wipe selected partitions.

Wipe entire drives (including OS if chosen).

Multiple Wiping Methods

Single-pass overwrite (quick).

Multi-pass overwrite (secure, e.g., DoD/Gutmann).

Dry Run Mode

Simulates wiping without touching actual data (for demo and testing).

Verification

Verify that wiped regions contain only chosen patterns/random data.

Generate a detailed report.

Report Generation

JSON/PDF format containing:

Target (file/partition/drive).

Wiping method used.

Timestamp.

Verification result (Success/Failure).

Digital Signing

Report signed with tool’s private key.

Verification possible using public key.

3. Optional / Advanced Features

Bootable USB ISO option (for wiping without OS interference).

Enterprise log export (send reports to central server).

Simple GUI (to replace CLI).

4. Constraints / Safety

Must never wipe system disk by accident.

Require explicit confirmation before destructive actions.

Must support dry run for testing and demo.

Testing must be done only on virtual disks / dummy files.

5. Deliverables

A working tool with:

Wiping engine.

Verification module.

Report generator with digital signatures.

Documentation (design, how-to-use, safety notes).

Demo (safe run on test disk with dry run + real wipe on dummy image).

6. “Done” Criteria

Selective wipe: User can choose a target (file, partition, or disk).

Wiping method: At least 2 overwrite methods available.

Dry run: Produces simulated output + report without touching data.

Verification: Tool scans wiped target and confirms overwrite.

Report: JSON file is generated with all required details.

Digital signing: Report can be verified with a public key.












Wiping Modes-
Mode 1: Targeted File Wiping

Goal: Securely delete selected files/folders.

Steps (User Flow):

User selects one or more files/folders.

Tool overwrites contents with random data / predefined patterns.

Tool deletes the file entry from the filesystem.

Tool verifies deletion (by checking hash or ensuring recovery is impossible).

Generates a report.

👉 This mode never touches partitions/boot sectors. Safe for everyday users.

Mode 2: Partition/Drive Wiping

Has two sub-options:

2.a – Full Device Wipe

Deletes everything from the device.

Important: If the device contains the OS, wiping cannot be done while OS is running.

Tool prompts:

“This drive contains an OS. Please create bootable media to proceed.”

Offers to create a bootable USB using wiping image (ISO).

Runs full wipe on restart via bootable media.

2.b – Single Partition Wipe

User selects a partition.

Tool checks if the partition contains an OS:

Case 1: Non-OS partition → directly wipe it (overwrite + format).

Case 2: OS partition → same as Full Device Wipe → must use bootable media.

🔑 Design Notes

Verification: After wiping, always compute random sector hashes to prove overwrite → attach in report.

Safety: Always prompt warnings (“This action is irreversible”).

Reports: Report format should mention:

Mode used (file wipe / partition wipe / full device wipe)

Method (overwrite passes, patterns used)

Verification status

Timestamp + unique signature
**note - no matter the mode, there will be certificate generation and will be tamper proof with a verifiable public key.






Primary modes:

File-level wipe (targeted files)

Partition-level wipe (full or single partition)

Drive support: HDD and SSD

Wipe methods:

HDD: multi-pass overwrite (0s and 1s, 3 passes)

SSD: overwrite + encrypt + file delete, plus note about wear-leveling

Verification:

HDD: binary sampling of random offsets

SSD: existence check and warning about traces

Report generation:

JSON, HTML, optional PDF

SHA256 hash of file

Signed report with private key

Verification code for public verification