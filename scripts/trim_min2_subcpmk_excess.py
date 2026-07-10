"""Trim the over-added Sub-CPMK rows from ensure_min2_subcpmk_per_course.py down to
the minimum needed to bring each course to exactly 2 Sub-CPMK.

Background
----------
The previous pass (ensure_min2_subcpmk_per_course.py, committed in 6e852ee) pulled
EVERY real Sub-CPMK available in each deficient course's published RPS, not just the
minimum needed to reach 2 - e.g. Fisika went from 1 to 5, Pancasila 1 to 4. Per
feedback, this is too much: courses that had 1 should end at exactly 2 (add 1), courses
that had 0 should end at exactly 2 (add 2).

This script deletes 13 rows:
- 12 of the 25 rows appended by the previous pass (rows 1151-1175), keeping only the
  ones selected per course using the principle "prefer extending the CPMK(s) already
  represented" (e.g. MK047: kept -04702, same CPMK0603 as the pre-existing -04704;
  dropped -04701, a different CPMK0209) or, for courses that started at 0, the pair
  that best captures the course's core build+verify competency over more generic
  project-management-adjacent ones already covered elsewhere in the curriculum.
- 1 pre-existing row (row 24, MK009 Fisika's SCPMK0902-00905) - its content is a copy
  from a math course (Matematika Dasar/Aljabar Linier), not a genuine Fisika Sub-CPMK
  (already flagged in docs/subcpmk-wording-review.md SS3a). Dropped entirely rather than
  corrected in place, and replaced by the two genuine physics Sub-CPMK already added
  in the previous pass (-00901, -00902), which are kept.

Final disposition (see the approved plan for full reasoning):
  MK001 Pancasila:  keep -00102                    | drop -00103, -00104
  MK009 Fisika:     keep -00901, -00902 (appended)  | drop -00903, -00904 (appended)
                                                       + -00905 (pre-existing, row 24)
  MK021 Kewarganegaraan: keep -02101                | drop -02102, -02103
  MK047 Pemrograman Berbasis Framework: keep -04702 | drop -04701, -04703
  MK053 Proyek Inovasi: keep -05301, -05304         | drop -05302, -05303
  MK054 Workshop Teknologi Terapan: keep -05401, -05402 | drop -05403
  MK056 Teknologi Terapan: keep -05601, -05602      | drop -05603
  MK059 Bahasa Inggris Persiapan Kerja: keep both   | drop none

Every course ends at exactly 2 Sub-CPMK.

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

# row -> expected Kode SubCPMK, asserted before deletion for safety
ROWS_TO_DELETE = {
    24: "SCPMK0902-00905",     # pre-existing, content-mismatched Fisika row
    1152: "SCPMK0102-00103",   # Pancasila
    1153: "SCPMK0102-00104",
    1156: "SCPMK0902-00903",   # Fisika
    1157: "SCPMK0902-00904",
    1159: "SCPMK0102-02102",   # Kewarganegaraan
    1160: "SCPMK0102-02103",
    1161: "SCPMK0209-04701",   # Pemrograman Berbasis Framework
    1163: "SCPMK0603-04703",
    1165: "SCPMK0803-05302",   # Proyek Inovasi
    1166: "SCPMK0804-05303",
    1170: "SCPMK0803-05403",   # Workshop Teknologi Terapan
    1173: "SCPMK0801-05603",   # Teknologi Terapan
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
            for row, expected_code in ROWS_TO_DELETE.items():
                pattern = re.compile(rf'<row r="{row}"[^>]*>.*?</row>', re.S)
                m = pattern.search(text)
                assert m, f"could not find row {row}"
                row_xml = m.group(0)
                assert expected_code in row_xml, (
                    f"row {row}: expected to contain {expected_code!r}, "
                    f"but it doesn't - refusing to delete: {row_xml[:200]}"
                )
                assert text.count(row_xml) == 1, f"row {row}: not exactly 1 occurrence"
                text = text.replace(row_xml, "", 1)
                deleted += 1

            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

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
