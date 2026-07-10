"""Fix the MK053/MK054 Kode-MK label collision in cpl-cpmk-subcpmk.xlsx.

Background
----------
Rows 193 (block 193-197) and 198 (block 198-206) in the MK-CPMK-SubCPMK-Metode
sheet are labeled Kode MK "MK053" / "MK054" in column B, but their content is
actually Magang and Skripsi respectively (real codes MK057/MK058 per
docs/rti-mk-crosswalk.md) - a stale mislabeling flagged early in the session and
judged harmless at the time because the embedded Sub-CPMK codes themselves
already correctly used the 057/058 prefix.

That mislabeling stopped being harmless once ensure_min2_subcpmk_per_course.py
(6e852ee) appended genuinely-MK053 (Proyek Inovasi) and genuinely-MK054
(Workshop Teknologi Terapan) rows later in the same sheet: the literal string
"MK053" now ambiguously refers to two different courses, likewise "MK054".

This script corrects the two populated Kode MK cells:
  B193: "MK053" -> "MK057" (Magang)
  B198: "MK054" -> "MK058" (Skripsi)

Only these two cells are populated for their blocks - rows 194-197 and
199-206 leave column B blank (continuation) - confirmed by direct inspection.
Both source values are shared strings (index 226 "MK053", index 228 "MK054"),
each referenced by exactly one cell in the whole sheet, so converting just
these two cells to inline strings with the corrected value is safe and leaves
the shared string table (and every other cell) untouched.

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

# cell -> (expected shared-string <v> old text, new inline text)
FIXES = {
    "B193": ("MK053", "MK057"),  # Magang
    "B198": ("MK054", "MK058"),  # Skripsi
}


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    fixed = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            for ref, (old_val, new_val) in FIXES.items():
                pattern = re.compile(
                    rf'<c r="{ref}"([^>]*) t="s"><v>\d+</v></c>'
                )
                m = pattern.search(text)
                assert m, f"could not find shared-string cell {ref}"
                attrs = m.group(1).strip()
                old_full = m.group(0)
                assert text.count(old_full) == 1, f"{ref}: not exactly 1 occurrence"
                new_full = (
                    f'<c r="{ref}" {attrs} t="inlineStr">'
                    f'<is><t xml:space="preserve">{new_val}</t></is></c>'
                )
                text = text.replace(old_full, new_full, 1)
                fixed += 1

            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return fixed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    fixed = apply_fix(args.xlsx_path)
    print(f"Fixed {fixed} cells (expected {len(FIXES)}).")
    print(f"Saved to {args.xlsx_path}")
