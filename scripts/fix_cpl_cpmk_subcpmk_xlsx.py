"""Fix CPL10's CPMK code inconsistency and 2 missing codes in docs/cpl-cpmk-subcpmk.xlsx.

Background
----------
CPL01-09's CPMK codes were unpadded (CPMK101...CPMK905, i.e. a 1-digit
CPL number + 2-digit sequence). Because CPL10 is 2 digits, naively
concatenating would produce CPMK101 for CPL10's first item, colliding
with CPL01's own CPMK101. The `CPL-CPMK` sheet worked around this with
a dot (CPMK10.1...CPMK10.9) instead of the padded, collision-proof form
(CPMK1001...CPMK1009) that the `(MK-CPMK)-BK-CPL` sheet already used
correctly.

This script:
1. Rewrites `CPL-CPMK` sheet column C rows for CPL10 from the dotted
   form to the padded dotless form.
2. Fills 2 confirmed-by-cross-reference missing Kode CPMK cells in the
   `(MK-CPMK)-BK-CPL` sheet (MK005 Bahasa Inggris 1 -> CPMK303, MK019
   Manajemen Proyek -> CPMK302), found by checking `CPL-CPMK`'s own
   Kode-MK/Nama-MK columns, which already listed those courses under
   those CPMK codes.

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
An earlier attempt used `openpyxl.load_workbook(...).save(...)` to make
these edits. That round-trip silently dropped 23 empty placeholder
drawing objects and a `persons.xml` (threaded-comment metadata) file
from the workbook, and separately reformatted unrelated numeric cells
in *other* sheets (e.g. "1.0" -> "1") plus lost some values entirely in
one column of an untouched sheet. None of that was intentional, so this
script instead edits the exact `<c>` XML elements in place inside the
zip archive, leaving every other byte in the file untouched. Verified
by a full cell-level diff (old vs new workbook) showing exactly the 11
intended cells changed and a byte-level diff of every other file in the
zip showing zero differences.

Status: already applied (commit 944d0f6). Re-running this script now
will fail its own assertions, since the old dotted/blank cell patterns
it looks for no longer exist post-fix — that's intentional, it prevents
accidental double-application. Kept here as the historical record of
what was changed and how, and as a reference for applying the same
surgical-edit technique to similar spreadsheet fixes.
"""

import argparse
import os
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")

# ---- exact string replacements, each must be unique within its file ----
SHEET14_REPLACEMENTS = [
    ('<c r="C61" s="141" t="s"><v>538</v></c>', '<c r="C61" s="141" t="inlineStr"><is><t>CPMK1001</t></is></c>'),
    ('<c r="C62" s="110" t="s"><v>542</v></c>', '<c r="C62" s="110" t="inlineStr"><is><t>CPMK1002</t></is></c>'),
    ('<c r="C63" s="110" t="s"><v>544</v></c>', '<c r="C63" s="110" t="inlineStr"><is><t>CPMK1003</t></is></c>'),
    ('<c r="C64" s="110" t="s"><v>546</v></c>', '<c r="C64" s="110" t="inlineStr"><is><t>CPMK1004</t></is></c>'),
    ('<c r="C65" s="110" t="s"><v>551</v></c>', '<c r="C65" s="110" t="inlineStr"><is><t>CPMK1005</t></is></c>'),
    ('<c r="C66" s="110" t="s"><v>553</v></c>', '<c r="C66" s="110" t="inlineStr"><is><t>CPMK1006</t></is></c>'),
    ('<c r="C67" s="110" t="s"><v>557</v></c>', '<c r="C67" s="110" t="inlineStr"><is><t>CPMK1007</t></is></c>'),
    ('<c r="C68" s="110" t="s"><v>559</v></c>', '<c r="C68" s="110" t="inlineStr"><is><t>CPMK1008</t></is></c>'),
    ('<c r="C69" s="110" t="s"><v>563</v></c>', '<c r="C69" s="110" t="inlineStr"><is><t>CPMK1009</t></is></c>'),
]

SHEET15_REPLACEMENTS = [
    ('<c r="C8" s="101"/>', '<c r="C8" s="101" t="inlineStr"><is><t>CPMK303</t></is></c>'),
    ('<c r="C44" s="153"/>', '<c r="C44" s="153" t="inlineStr"><is><t>CPMK302</t></is></c>'),
]

TARGET_FILES = {
    "xl/worksheets/sheet14.xml": SHEET14_REPLACEMENTS,  # "CPL-CPMK" sheet
    "xl/worksheets/sheet15.xml": SHEET15_REPLACEMENTS,  # "(MK-CPMK)-BK-CPL" sheet
}


def apply_fix(xlsx_path: str) -> int:
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    total_replacements = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in TARGET_FILES:
            text = data.decode("utf-8")
            for old, new in TARGET_FILES[item.filename]:
                count = text.count(old)
                assert count == 1, f"{item.filename}: expected exactly 1 occurrence of {old!r}, found {count}"
                text = text.replace(old, new, 1)
                total_replacements += 1
            data = text.encode("utf-8")
        # preserve original ZipInfo metadata (compression type, date, etc.) exactly
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return total_replacements


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    applied = apply_fix(args.xlsx_path)
    print(f"Applied {applied} surgical replacements (expected 11).")
    print(f"Saved to {args.xlsx_path}")
