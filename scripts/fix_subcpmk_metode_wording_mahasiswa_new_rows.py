"""Remove the leading "Mahasiswa" from the 13 Sub-CPMK statements added after the
original 149-cell wording pass (fix_subcpmk_metode_wording_mahasiswa.py).

Background
----------
fix_subcpmk_metode_wording_mahasiswa.py (committed earlier this session) applied the
house style - no Sub-CPMK statement starts with "Mahasiswa" - to all 149 cells that
had it at the time. ensure_min2_subcpmk_per_course.py then appended 25 new rows (later
trimmed to 13 kept) whose Sub-CPMK text also starts with "Mahasiswa mampu ...", since
they were transcribed verbatim from real published RPS and never passed through the
wording fix. This applies the identical transformation to just those 13 rows.

Same CELL_PATTERN and transformation as the original script: "Mahasiswa mampu X" ->
"Mampu X" (capitalize the verb, drop the leading subject).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this repo: openpyxl
load_workbook(...).save(...) previously caused data loss in this exact workbook.
"""

import argparse
import os
import re
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"

CELL_PATTERN = re.compile(
    r'<c r="(J\d+)"([^/]*?)t="inlineStr"><is><t xml:space="preserve">'
    r'Mahasiswa (mampu|mengetahui|mengerti)([^<]*)</t></is></c>'
)

EXPECTED_COUNT = 13
EXPECTED_ROWS = {
    "J1151", "J1154", "J1155", "J1158", "J1162", "J1164", "J1167",
    "J1168", "J1169", "J1171", "J1172", "J1174", "J1175",
}


def fix_text(sheet_xml: str):
    audit = []

    def repl(m):
        ref, attrs, verb, rest = m.groups()
        assert ref in EXPECTED_ROWS, f"unexpected cell {ref} matched - not one of the 13 new rows"
        new_text = verb[0].upper() + verb[1:] + rest
        audit.append((ref, f"Mahasiswa {verb}{rest}", new_text))
        return f'<c r="{ref}"{attrs}t="inlineStr"><is><t xml:space="preserve">{new_text}</t></is></c>'

    new_xml, count = CELL_PATTERN.subn(repl, sheet_xml)
    return new_xml, count, audit


def apply_fix(xlsx_path: str):
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    audit = []
    count = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            new_text, count, audit = fix_text(text)
            assert count == EXPECTED_COUNT, (
                f"expected {EXPECTED_COUNT} substitutions, got {count}"
            )
            found_rows = {ref for ref, _, _ in audit}
            assert found_rows == EXPECTED_ROWS, (
                f"row mismatch: missing {EXPECTED_ROWS - found_rows}, "
                f"extra {found_rows - EXPECTED_ROWS}"
            )
            data = new_text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return count, audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    parser.add_argument("--quiet", action="store_true", help="suppress per-row audit output")
    args = parser.parse_args()

    applied, audit = apply_fix(args.xlsx_path)
    print(f"Applied {applied} substitutions (expected {EXPECTED_COUNT}).")
    print(f"Saved to {args.xlsx_path}")
    if not args.quiet:
        print("\nAudit (cell, old, new):")
        for ref, old, new in audit:
            print(f"  {ref}: {old[:60]!r} -> {new[:60]!r}")
