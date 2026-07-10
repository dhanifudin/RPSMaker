"""Fix duplicate and missing Kode SubCPMK values in the MK-CPMK-SubCPMK-Metode sheet.

Background
----------
A wording review (docs/subcpmk-wording-review.md) found two classes of
Kode SubCPMK (column I) defects in this sheet, on top of the 36 rows
already left deliberately empty by scripts/fill_subcpmk_metode.py
(commit 5544b91) because their Kode CPMK isn't validated against the
course's published RPS:

1. Duplicate codes: the exact same Kode SubCPMK string was reused for
   genuinely different Sub-CPMK statements.
     - `SCPMK0706-03101` (Kecerdasan Artifisial, MK031) was used for
       THREE different Sub-CPMK statements (rows 104, 105, 106) instead
       of three distinct serials under CPMK0706.
     - `SCPMK0102-00101` was used for BOTH Pancasila (MK001, row 2 -
       correct, matches its course's own local numbering) AND
       Komunikasi Dan Etika Profesi (MK045, row 156 - wrong; that
       course's other three rows, 155/157/158, all correctly use its
       own local "001" prefix + a distinct serial per CPMK, so row 156
       just picked an already-taken serial for CPMK0102).
   (NOT touched: `SCPMK0502-01303` appears 3x for Sistem Operasi
   rows 40-42, but this is intentional - one Sub-CPMK spanning three
   weekly sessions with three different Bentuk Pembelajaran, matching
   the same one-code-many-meetings pattern already used in the
   published RPS. It was assigned deliberately by
   scripts/fill_subcpmk_metode.py's FILLS dict, not left as a bug.)

2. Fixable orphans: of the 36 rows left empty by the prior script, 26
   have a Kode CPMK that IS valid (exists in the master CPL-CPMK sheet)
   - it's just not the CPMK that course's published RPS happened to
     use. These can get a mechanically-derived code following each
     course's own established local numbering (observed from sibling
     rows already coded in the same course block - several courses use
     a legacy/renumbered 3-digit prefix that no longer matches their
     current Kode MK, e.g. MK053/MK054 rows use prefix "057"/"058", not
     "053"/"054"; the fix follows the LOCAL convention already present
     in that block for internal consistency, not the current Kode MK).
   The remaining 10 rows have a Kode CPMK that does not exist ANYWHERE
   in the master CPL-CPMK list (Bahasa Indonesia CPMK0307/0308,
   Kewirausahaan CPMK0311/0312, Proyek Teknologi Terintegrasi
   CPMK0317/0318, Magang CPMK0319/0320, Skripsi CPMK0321/0322) -
   assigning a code would encode a fabricated CPMK reference, so these
   are deliberately left untouched pending a human decision on which
   real CPMK each should be remapped to (see docs/gap-analysis note /
   memory `metode-sheet-cpmk-column-findings`).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this directory:
openpyxl.load_workbook(...).save(...) previously caused unrelated data
loss elsewhere in this exact workbook.
"""

import argparse
import os
import re
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"  # MK-CPMK-SubCPMK-Metode

# row -> (old code, new code): cells that already contain a duplicate value
COLLISION_FIXES = {
    105: ("SCPMK0706-03101", "SCPMK0706-03102"),
    106: ("SCPMK0706-03101", "SCPMK0706-03103"),
    156: ("SCPMK0102-00101", "SCPMK0102-00102"),
}

# row -> new code: empty <is><t xml:space="preserve" /></is> placeholder cells
ORPHAN_FILLS = {
    67: "SCPMK0903-01901",
    73: "SCPMK0203-02001",
    74: "SCPMK1001-02001",
    83: "SCPMK0211-02501",
    85: "SCPMK0606-02501",
    86: "SCPMK0607-02501",
    87: "SCPMK0211-02601",
    89: "SCPMK0607-02601",
    129: "SCPMK0102-03701",
    140: "SCPMK0508-04201",
    141: "SCPMK0605-04201",
    143: "SCPMK0606-04201",
    144: "SCPMK0802-04201",
    151: "SCPMK0504-04401",
    153: "SCPMK1002-04401",
    154: "SCPMK1003-04401",
    163: "SCPMK0201-04801",
    164: "SCPMK0205-04801",
    165: "SCPMK0211-04801",
    168: "SCPMK0602-04801",
    175: "SCPMK0206-04901",
    193: "SCPMK0102-05701",
    198: "SCPMK0101-05801",
    199: "SCPMK0211-05801",
    204: "SCPMK1008-05801",
    206: "SCPMK0607-05801",
}

# Rows deliberately left empty: Kode CPMK does not exist in the master
# CPL-CPMK sheet at all. Needs a human decision on the correct CPMK
# remap before a code can be assigned.
STILL_FLAGGED_ROWS = [102, 103, 130, 131, 166, 167, 194, 195, 201, 202]


def apply_fix(xlsx_path: str) -> tuple[int, int]:
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    collisions_applied = 0
    orphans_applied = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            for row, (old_code, new_code) in COLLISION_FIXES.items():
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
                collisions_applied += 1

            for row, code in ORPHAN_FILLS.items():
                ref = f"I{row}"
                pattern = re.compile(
                    rf'<c r="{ref}"([^/]*?)t="inlineStr"><is><t xml:space="preserve" /></is></c>'
                )
                m = pattern.search(text)
                assert m, f"could not find empty placeholder cell {ref}"
                attrs = m.group(1)
                old_full = m.group(0)
                new_full = f'<c r="{ref}"{attrs}t="inlineStr"><is><t xml:space="preserve">{code}</t></is></c>'
                count = text.count(old_full)
                assert count == 1, f"{ref}: expected exactly 1 occurrence, found {count}"
                text = text.replace(old_full, new_full, 1)
                orphans_applied += 1

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return collisions_applied, orphans_applied


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    collisions, orphans = apply_fix(args.xlsx_path)
    print(f"Applied {collisions} collision fixes (expected {len(COLLISION_FIXES)}).")
    print(f"Applied {orphans} orphan-code fills (expected {len(ORPHAN_FILLS)}).")
    print(f"{len(STILL_FLAGGED_ROWS)} rows still left empty (invalid Kode CPMK, needs human remap): {STILL_FLAGGED_ROWS}")
    print(f"Saved to {args.xlsx_path}")
