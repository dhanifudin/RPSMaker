"""Restore row 1162's missing Course/CPL/Bahan-Kajian cells (Pemrograman Berbasis Framework).

Background
----------
ensure_min2_subcpmk_per_course.py (6e852ee) appended a 3-row block for MK047
Pemrograman Berbasis Framework: row 1161 (header - sets Kode MK, MK, CPL,
Kode BK, BK) and rows 1162/1163 (continuation rows - leave those 4 columns
blank by design, relying on the header row immediately above for carry-down
reading, same convention used throughout the pre-existing sheet).

trim_min2_subcpmk_excess.py (561ce8e) then deleted row 1161 (the header) and
row 1163, keeping only row 1162 - which broke the carry-down chain: row 1162's
C/D/E/F cells are now genuinely absent (not just blank), so any reader
resolving them by carry-down inherits the WRONG course's data (Kewarganegaraan,
from row 1158, since everything between 1158 and 1162 was also deleted).

This script inserts row 1162's C/D/E/F cells with the exact values row 1161
held before deletion (sourced from ensure_min2_subcpmk_per_course.py's
NEW_ROWS tuple, lines 144-146), making row 1162 self-contained like every
other single-surviving-row course block in this sheet.

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this repo: openpyxl
load_workbook(...).save(...) previously caused data loss in this exact
workbook.
"""

import argparse
import os
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"

ROW = 1162
VALUES = {
    "C": "Pemrograman Berbasis Framework",
    "D": "(CPL06) Mampu merancang, mengimplementasikan, menguji, melakukan "
         "deployment, dan memelihara, serta menjamin mutu perangkat lunak "
         "yang menjawab permasalahan dan memenuhi kebutuhan stakeholder",
    "E": "BK19",
    "F": "Platform-based Development",
}


def make_cell(col, row, value):
    return f'<c r="{col}{row}" t="inlineStr"><is><t xml:space="preserve">{value}</t></is></c>'


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    inserted = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            pattern = re.compile(rf'<row r="{ROW}"[^>]*>.*?</row>', re.S)
            m = pattern.search(text)
            assert m, f"could not find row {ROW}"
            row_xml = m.group(0)

            # row currently has B, G, H, I, J, K, L, M, N, O - no C/D/E/F.
            for col in ("C", "D", "E", "F"):
                assert f'r="{col}{ROW}"' not in row_xml, f"{col}{ROW} already present"

            b_cell_pattern = re.compile(rf'<c r="B{ROW}"[^/]*?/?>(?:.*?</c>)?')
            m2 = b_cell_pattern.search(row_xml)
            assert m2, f"could not find B{ROW} cell"
            b_cell = m2.group(0)

            new_cells = "".join(make_cell(col, ROW, VALUES[col]) for col in ("C", "D", "E", "F"))
            new_row_xml = row_xml.replace(b_cell, b_cell + new_cells, 1)
            inserted = len(VALUES)

            assert text.count(row_xml) == 1, f"row {ROW}: not exactly 1 occurrence"
            text = text.replace(row_xml, new_row_xml, 1)

            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    inserted = apply_fix(args.xlsx_path)
    print(f"Inserted {inserted} cells into row {ROW}.")
    print(f"Saved to {args.xlsx_path}")
