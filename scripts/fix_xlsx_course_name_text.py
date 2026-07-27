"""Fix 2 course-name text defects in cpl-cpmk-subcpmk.xlsx's Metode sheet.

Background
----------
Found during the second CPL/CPMK/Sub-CPMK consistency pass (2026-07-11):
  - C6: "Critical thinking dan problem solving" - wrong casing (lowercase t/p). The correct
    Title Case ("Critical Thinking dan Problem Solving") is already used everywhere else in
    the repo (RPS title, network diagram, matrix table, and the already-fixed Chapter 5
    Peta Jalan CPL diagram) - only this xlsx cell still has the old casing.
  - C76: "Desain &amp; Pemrograman Web" - a raw, literal HTML entity string baked into the
    cell value (not a rendering artifact - the characters "&amp;" are literally present).
    Every other reference to this course uses "Desain dan Pemrograman Web".

Both are shared strings referenced exactly once in the sheet, safe to convert to inline
strings with the corrected text (shared string table itself untouched).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this repo: openpyxl
load_workbook(...).save(...) previously caused data loss in this exact workbook.
"""

import argparse
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"

REPLACEMENTS = [
    ('<c r="C6" s="154" t="s"><v>131</v></c>',
     '<c r="C6" s="154" t="inlineStr"><is><t xml:space="preserve">'
     'Critical Thinking dan Problem Solving</t></is></c>'),
    ('<c r="C76" s="154" t="s"><v>166</v></c>',
     '<c r="C76" s="154" t="inlineStr"><is><t xml:space="preserve">'
     'Desain dan Pemrograman Web</t></is></c>'),
]


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    applied = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            for old, new in REPLACEMENTS:
                assert text.count(old) == 1, f"not found or not unique: {old!r}"
                text = text.replace(old, new, 1)
                applied += 1

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

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
    print(f"Applied {applied} cell fixes (expected {len(REPLACEMENTS)}).")
    print(f"Saved to {args.xlsx_path}")
