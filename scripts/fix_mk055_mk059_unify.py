"""Correct rows 1174/1175 (Bahasa Inggris Persiapan Kerja) from Kode MK "MK059" to
the internally-established "MK055", and renumber their Kode SubCPMK to avoid colliding
with the pre-existing MK055 block (rows 207-208).

Background
----------
ensure_min2_subcpmk_per_course.py used "MK059" for Bahasa Inggris Persiapan Kerja,
sourced from docs/rti-mk-crosswalk.md (an external reference doc). Per curriculum-owner
direction, re-checked the CPL/CPMK mapping using cpl-cpmk-subcpmk.xlsx's OWN internal
sheets instead of external docs or the published RPS:
  - BK-MK (Rev), sheet3.xml row 57: Kode MK "MK055" = "Bahasa Inggris Persiapan Kerja"
  - (MK-CPMK)-BK-CPL, sheet15.xml row 178: same pairing, with full CPL03/CPMK0303 detail
  - MK-CPMK-SubCPMK (hidden), sheet17.xml row 70: same pairing
  - backup (MK-CPMK)-BK-CPL, sheet18.xml row 159: same pairing
Four independent internal sheets agree MK055 = Bahasa Inggris Persiapan Kerja.
"MK059" does not appear ANYWHERE else in the entire workbook - it has zero internal
corroboration. The crosswalk doc's MK059 was simply wrong for this course.

This relabels rows 1174/1175 to MK055 and renumbers their Kode SubCPMK into that
course's existing serial range (07501/07502... no - MK055's existing rows 207/208 use
-05501/-05502, so the next free serials are -05503/-05504). The four resulting
Sub-CPMK (05501-05504) are judged non-redundant: career planning (05501),
self-presentation/TOEIC (05502), professional document writing (05503), interview
simulation (05504) - four distinct facets of career-prep English, not duplicates.

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
    ('<c r="B1174" t="inlineStr"><is><t xml:space="preserve">MK059</t></is></c>',
     '<c r="B1174" t="inlineStr"><is><t xml:space="preserve">MK055</t></is></c>'),
    ('<c r="B1175" t="inlineStr"><is><t xml:space="preserve">MK059</t></is></c>',
     '<c r="B1175" t="inlineStr"><is><t xml:space="preserve">MK055</t></is></c>'),
    ('<c r="I1174" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05901</t></is></c>',
     '<c r="I1174" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05503</t></is></c>'),
    ('<c r="I1175" t="inlineStr"><is><t xml:space="preserve">SCPMK0102-05902</t></is></c>',
     '<c r="I1175" t="inlineStr"><is><t xml:space="preserve">SCPMK0102-05504</t></is></c>'),
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
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

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
    print(f"Applied {applied} replacements (expected {len(REPLACEMENTS)}).")
    print(f"Saved to {args.xlsx_path}")
