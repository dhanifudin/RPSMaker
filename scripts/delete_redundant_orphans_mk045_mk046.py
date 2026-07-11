"""Delete 4 redundant orphan rows made obsolete by restore_missing_subcpmk_mk045_mk046.py.

Background
----------
Follow-up to the "empty Sub-CPMK code" fix (2026-07-11, third pass). MK045 (Komunikasi dan
Etika Profesi) rows 157/158 reference undefined CPMK0313/0314, and MK046 (Pengembangan Karir)
rows 160/161 reference undefined CPMK0315/0316 - none of these 4 codes exist in the canonical
CPL-CPMK master or either course's real published RPS. restore_missing_subcpmk_mk045_mk046.py
adds the real RPS Sub-CPMK these orphans duplicate (SCPMK0301-04502/SCPMK0303-04503 for
MK045; 3 SCPMK0303-046xx rows for MK046). This script deletes the now-fully-redundant
orphans. MUST run after restore_missing_subcpmk_mk045_mk046.py, so the real content exists in
the sheet before the duplicate placeholder is removed - same two-step order as the original
CPL03 cluster fix.

Row numbers are pinned to the exact CPMK code expected in column G as a safety check (not
just position), same precaution as delete_redundant_cpl03_orphans.py.

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
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"

# row -> (expected Kode CPMK, expected Kode SubCPMK), used as a safety check before
# deleting. Unlike the original CPL03 cluster, these orphans are POPULATED rows (they
# have a real-looking but undefined Kode SubCPMK) - so the check pins the exact G AND I
# values instead of asserting I is empty.
ROWS_TO_DELETE = {
    157: ("CPMK0313", "SCPMK0313-04505"),  # MK045 (superseded by SCPMK0301-04502)
    158: ("CPMK0314", "SCPMK0314-04506"),  # MK045 (superseded by SCPMK0303-04503)
    160: ("CPMK0315", "SCPMK0315-04602"),  # MK046 (superseded by SCPMK0303-04602)
    161: ("CPMK0316", "SCPMK0316-04603"),  # MK046 (superseded by SCPMK0303-04603/04604)
}


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    deleted = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            for row_num, (expected_g, expected_i) in ROWS_TO_DELETE.items():
                row_match = re.compile(
                    rf'<row r="{row_num}"[^>]*>(.*?)</row>', re.S
                ).search(text)
                assert row_match, f"row {row_num} not found"
                row_body = row_match.group(1)

                g_match = re.search(rf'<c r="G{row_num}"[^>]*>(.*?)</c>', row_body, re.S)
                assert g_match, f"row {row_num}: G cell not found"
                g_text = re.search(r'<t[^>]*>(.*?)</t>', g_match.group(1), re.S)
                assert g_text and g_text.group(1) == expected_g, (
                    f"row {row_num}: expected G={expected_g!r}, "
                    f"found {g_text.group(1) if g_text else None!r} - refusing to delete"
                )
                i_match = re.search(rf'<c r="I{row_num}"[^>]*>(.*?)</c>', row_body, re.S)
                assert i_match, f"row {row_num}: I cell not found"
                i_text = re.search(r'<t[^>]*>(.*?)</t>', i_match.group(1), re.S)
                found_i = i_text.group(1) if i_text else ""
                assert found_i == expected_i, (
                    f"row {row_num}: expected I={expected_i!r}, found {found_i!r} - "
                    f"refusing to delete"
                )

                # row_match.start()/.end() already bound the whole <row ...>...</row>
                # element (the regex's literal <row r="..."> anchors group 0's start).
                text = text[: row_match.start()] + text[row_match.end() :]
                deleted += 1

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return deleted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    deleted = apply_fix(args.xlsx_path)
    print(f"Deleted {deleted} rows (expected {len(ROWS_TO_DELETE)}).")
    print(f"Saved to {args.xlsx_path}")
