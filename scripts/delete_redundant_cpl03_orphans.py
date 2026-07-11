"""Delete 6 redundant CPL03-orphan rows made obsolete by restore_missing_subcpmk_from_rps.py.

Background
----------
Same "empty Sub-CPMK code" audit (2026-07-11, third pass). 10 rows in the Metode sheet
referenced undefined CPL03-cluster codes CPMK0307-CPMK0322 with no Kode SubCPMK. For 6 of
them (MK030 rows 102/103; MK037 rows 130/131; MK057 rows 194/195) the same competency was
already re-authored in the course's real published RPS under a correct canonical CPMK -
restore_missing_subcpmk_from_rps.py adds those real rows. This script deletes the now-fully-
redundant orphans. This MUST run after restore_missing_subcpmk_from_rps.py, so the real
content exists in the sheet before the duplicate placeholder is removed.

The other 4 orphan rows (MK048 166/167, MK058 201/202) are NOT touched here - they hold the
only record of real content with no RPS counterpart, so they are re-coded in place by
recode_cpl03_orphans.py instead of deleted.

Row numbers are pinned to the exact CPMK code expected in column G as a safety check (not
just position) - if the sheet has shifted since this script was written (e.g. because
restore_missing_subcpmk_from_rps.py's appended rows go at the END of the sheet, not spliced
in near these rows, so 102/103/130/131/194/195 keep their row numbers), this assertion catches
any mismatch instead of silently deleting the wrong row.

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

# row -> expected Kode CPMK (G), used as a safety check before deleting.
ROWS_TO_DELETE = {
    102: "CPMK0307",  # MK030 Bahasa Indonesia (superseded by SCPMK0301-03001)
    103: "CPMK0308",  # MK030 Bahasa Indonesia (superseded by SCPMK0301-03001)
    130: "CPMK0311",  # MK037 Kewirausahaan (superseded by SCPMK0301-03703)
    131: "CPMK0312",  # MK037 Kewirausahaan (superseded by SCPMK0301-03704)
    194: "CPMK0319",  # MK057 Magang (superseded by SCPMK0301-05701)
    195: "CPMK0320",  # MK057 Magang (superseded by SCPMK0303-05702)
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

            for row_num, expected_g in ROWS_TO_DELETE.items():
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
                if i_match:
                    i_text = re.search(r'<t[^>]*/?>([^<]*)', i_match.group(1), re.S)
                    existing_i = i_text.group(1) if i_text else ""
                    assert existing_i == "", (
                        f"row {row_num}: I cell has content {existing_i!r}, "
                        f"expected empty - refusing to delete a populated row"
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
