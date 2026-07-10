"""Resolve the SCPMK0502-01303 triple-collision in MK013 Sistem Operasi (rows 40-42).

Background
----------
Rechecked against the real master CPL-CPMK sheet ("CPL-CPMK", sheet14.xml - NOT the
hidden "backup (MK-CPMK)-BK-CPL" sheet18.xml a previous pass in this session mistakenly
treated as the master). CPMK0502 is confirmed to legitimately belong to MK013 (Sistem
Operasi), among 3 other courses, per that sheet's row 27 (Kode MK column lists MK013,
MK044, MK051, MK002).

Per curriculum-owner direction, this resolution does NOT use the published RPS as the
priority source - it uses the workbook's own internal content/wording to judge which
rows represent genuinely distinct Sub-CPMK vs. duplicates:
  - Row 40: a near-verbatim copy of CPMK0502's own master-level description (sheet14
    row 27, column D) with a "sesuai konteks ... capaian CPMK0502" suffix appended -
    the auto-generated-boilerplate pattern already documented for ~86 rows in
    docs/subcpmk-wording-review.md SS1. Distinct in scope from rows 41/42 (broader:
    identify + analyze + apply, across OS/network/cloud).
  - Rows 41 and 42: byte-identical Sub-CPMK statement (J), identical M/N/O - only the
    teaching method (K) differs. A genuine duplicate entry, not two distinct
    competencies.

Resolution: keep row 40 as-is (-01303). Merge row 41 and row 42 into a single row -
combine their K (method) values, matching the sheet's existing convention for
multi-method delivery of one Sub-CPMK (e.g. row 2's comma-separated method list) -
renumber the surviving row to -01304 (MK013's next free serial: row 38 has -01302,
row 39 has -01301, so -01304 is unused), and delete the redundant row 42.

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

MERGED_K = "Demonstrasi &amp; Tutorial Terpandu, Pembelajaran Kolaboratif (Collaborative Learning/CL)"


def apply_fix(xlsx_path: str) -> None:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            # 1. renumber row 41's Kode SubCPMK: -01303 -> -01304
            old_i41 = '<c r="I41" s="38" t="inlineStr"><is><t xml:space="preserve">SCPMK0502-01303</t></is></c>'
            new_i41 = '<c r="I41" s="38" t="inlineStr"><is><t xml:space="preserve">SCPMK0502-01304</t></is></c>'
            assert text.count(old_i41) == 1, "I41 not found or not unique"
            text = text.replace(old_i41, new_i41, 1)

            # 2. merge row 42's method into row 41's K cell
            old_k41 = '<c r="K41" s="217" t="inlineStr"><is><t xml:space="preserve">Demonstrasi &amp; Tutorial Terpandu</t></is></c>'
            new_k41 = f'<c r="K41" s="217" t="inlineStr"><is><t xml:space="preserve">{MERGED_K}</t></is></c>'
            assert text.count(old_k41) == 1, "K41 not found or not unique"
            text = text.replace(old_k41, new_k41, 1)

            # 3. delete row 42 entirely
            pattern42 = re.compile(r'<row r="42"[^>]*>.*?</row>', re.S)
            m = pattern42.search(text)
            assert m, "row 42 not found"
            row42_xml = m.group(0)
            assert "SCPMK0502-01303" in row42_xml, "row 42 doesn't contain expected code"
            assert text.count(row42_xml) == 1, "row 42: not exactly 1 occurrence"
            text = text.replace(row42_xml, "", 1)

            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    apply_fix(args.xlsx_path)
    print("Renumbered row 41 to SCPMK0502-01304, merged row 42's method into it, deleted row 42.")
    print(f"Saved to {args.xlsx_path}")
