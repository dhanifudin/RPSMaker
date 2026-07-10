"""Correct the Kode SubCPMK values wrongly assigned by fix_subcpmk_metode_codes.py.

Background
----------
scripts/fix_subcpmk_metode_codes.py (v1) fixed 3 duplicate-code collisions and 26
orphan (missing-code) rows in the MK-CPMK-SubCPMK-Metode sheet, but used the wrong
scoping rule to pick each new code's trailing 2-digit serial: it picked "next free
serial for this (CPMK, course-prefix) pair", usually landing on 01.

The REAL, documented convention (docs/rti-mk-crosswalk.md: "Format:
SCPMK<cpmk>-<MKnum3digit><seq2digit>") is that the serial is a SINGLE RUNNING COUNTER
PER COURSE across all of that course's CPMKs, not a counter that resets per CPMK. This
was confirmed against every affected course's actual published subjects/*/*-RPS.tex.

Consequence: every one of v1's 26 orphan fills, plus 2 of its 3 collision fixes, ended
up colliding with a real, already-published Sub-CPMK code - worse than the original
empty-cell gap, since the sheet now visibly contradicts the published curriculum. This
script corrects all of it, anchored to each course's real published maximum serial
(gathered by grepping subjects/*/*-RPS.tex for every affected course - see the
per-course "collides with" evidence in the corrected-plan writeup this script
implements).

Additionally fixes MK045 (Komunikasi Dan Etika Profesi) rows 155/156, which v1 never
touched correctly:
  - row 155 (CPMK0101): this CPMK IS published for MK045 (subjects/RTI256001-.../
    ...-RPS.tex uses SCPMK0101-04501) - correct the draft's wrong SCPMK0101-00101
    (wrong prefix: 001 is Pancasila's number, not MK045's 045) to the real code.
  - row 156 (CPMK0102): this CPMK is NOT in MK045's published RPS, but IS currently,
    officially assigned to MK045 in the master CPL-CPMK sheet (row 3's Kode MK list
    includes MK045) - same "valid but unused" class as the 26 orphan rows. Assign a
    provisional code continuing MK045's real sequence past its published max (04503).
  - rows 157/158 (CPMK0313/CPMK0314) are deliberately NOT touched here: neither code
    exists anywhere in the master CPL-CPMK sheet (confirmed by direct lookup), so - like
    the 10 already-flagged invalid-CPMK rows from fill_subcpmk_metode.py - they need a
    curriculum-owner decision, not a mechanical fix. They still carry the wrong `001`
    prefix; that's a known, documented, left-open issue.

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this directory: openpyxl
load_workbook(...).save(...) previously caused unrelated data loss elsewhere in this
exact workbook.
"""

import argparse
import os
import re
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"  # MK-CPMK-SubCPMK-Metode

# row -> (old code currently in the cell, corrected code)
CORRECTIONS = {
    # Issue 1: Kecerdasan Artifisial (MK031) - row 107 (untouched) already legitimately
    # owns serial 02 (SCPMK1005-03102), so rows 105/106 must continue past it.
    105: ("SCPMK0706-03102", "SCPMK0706-03103"),
    106: ("SCPMK0706-03103", "SCPMK0706-03104"),

    # Issue 4: the 26 orphan-fill rows, corrected to continue past each course's real
    # published maximum serial instead of restarting at 01 per CPMK.
    67: ("SCPMK0903-01901", "SCPMK0903-01905"),
    73: ("SCPMK0203-02001", "SCPMK0203-02005"),
    74: ("SCPMK1001-02001", "SCPMK1001-02006"),
    83: ("SCPMK0211-02501", "SCPMK0211-02504"),
    85: ("SCPMK0606-02501", "SCPMK0606-02505"),
    86: ("SCPMK0607-02501", "SCPMK0607-02506"),
    87: ("SCPMK0211-02601", "SCPMK0211-02604"),
    89: ("SCPMK0607-02601", "SCPMK0607-02605"),
    129: ("SCPMK0102-03701", "SCPMK0102-03705"),
    140: ("SCPMK0508-04201", "SCPMK0508-04205"),
    141: ("SCPMK0605-04201", "SCPMK0605-04206"),
    143: ("SCPMK0606-04201", "SCPMK0606-04207"),
    144: ("SCPMK0802-04201", "SCPMK0802-04208"),
    151: ("SCPMK0504-04401", "SCPMK0504-04403"),
    153: ("SCPMK1002-04401", "SCPMK1002-04404"),
    154: ("SCPMK1003-04401", "SCPMK1003-04405"),
    163: ("SCPMK0201-04801", "SCPMK0201-04806"),
    164: ("SCPMK0205-04801", "SCPMK0205-04807"),
    165: ("SCPMK0211-04801", "SCPMK0211-04808"),
    168: ("SCPMK0602-04801", "SCPMK0602-04809"),
    175: ("SCPMK0206-04901", "SCPMK0206-04904"),
    193: ("SCPMK0102-05701", "SCPMK0102-05705"),
    198: ("SCPMK0101-05801", "SCPMK0101-05806"),
    199: ("SCPMK0211-05801", "SCPMK0211-05807"),
    204: ("SCPMK1008-05801", "SCPMK1008-05808"),
    206: ("SCPMK0607-05801", "SCPMK0607-05809"),

    # Issue 2: MK045 rows 155/156, corrected via the master CPL-CPMK cross-check.
    155: ("SCPMK0101-00101", "SCPMK0101-04501"),  # correct to the real published code
    156: ("SCPMK0102-00102", "SCPMK0102-04504"),  # provisional, continues real sequence
}

# Rows deliberately left untouched: CPMK doesn't exist anywhere in the master
# CPL-CPMK sheet, so no code can be derived without a curriculum-owner decision.
STILL_FLAGGED_ROWS_MK045 = [157, 158]  # CPMK0313, CPMK0314 - not in master list


def apply_fix(xlsx_path: str) -> int:
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    applied = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            for row, (old_code, new_code) in CORRECTIONS.items():
                ref = f"I{row}"
                pattern = re.compile(
                    rf'<c r="{ref}"([^/]*?)t="inlineStr"><is><t xml:space="preserve">{re.escape(old_code)}</t></is></c>'
                )
                m = pattern.search(text)
                assert m, f"could not find {ref} still containing {old_code}"
                attrs = m.group(1)
                old_full = m.group(0)
                new_full = f'<c r="{ref}"{attrs}t="inlineStr"><is><t xml:space="preserve">{new_code}</t></is></c>'
                count = text.count(old_full)
                assert count == 1, f"{ref}: expected exactly 1 occurrence, found {count}"
                text = text.replace(old_full, new_full, 1)
                applied += 1
            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return applied


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    applied = apply_fix(args.xlsx_path)
    print(f"Applied {applied} corrections (expected {len(CORRECTIONS)}).")
    print(f"Rows {STILL_FLAGGED_ROWS_MK045} (MK045, CPMK0313/CPMK0314) left untouched - "
          f"not in master CPL-CPMK list, needs curriculum-owner decision.")
    print(f"Saved to {args.xlsx_path}")
