"""Restore Pancasila's SCPMK0102-00103 and SCPMK0102-00104 rows into
docs/cpl-cpmk-subcpmk.xlsx, sourced from the real published RPS.

Background
----------
The real RPS (subjects/RTI251001-pancasila/RTI251001 Pancasila - RPS.tex) defines 4 Sub-CPMK
for Pancasila: SCPMK0102-00101 through -00104. The master sheet only had 2 (-00101 original;
-00102 added earlier this session) - the other two were deliberately trimmed down to the
session's minimum-required-count fix (trim_min2_subcpmk_excess.py), not because they were
wrong, but because only 2 were needed to satisfy the "≥2 Sub-CPMK per course" rule at the
time. This restores the full, RPS-accurate set for Pancasila specifically.

Content for the 2 new rows is sourced from RPS lines 19-20 (Sub-CPMK statement, with the
leading "Mahasiswa " stripped to match this session's established house style - "avoid
Mahasiswa as prefix" - same transformation as fix_subcpmk_metode_wording_mahasiswa.py) and
lines 50-57 (weekly breakdown, aggregated per Sub-CPMK the same way -00102 was built earlier
this session): -00103 covers weeks 9-10 (ideologi nasional), -00104 covers weeks 11-16
(HAM/korupsi/pembangunan).

Both new rows are fully self-contained (explicit Kode MK/MK/CPL/Kode BK/BK/Kode CPMK/CPMK),
not relying on carry-down from a distant earlier row - same precaution as every other row
addition this session, following the row-1162 incident where an unrelated later edit broke an
implicit carry-down chain.

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

SHARED_CONTEXT = {
    "B": "MK001",
    "C": "Pancasila",
    "D": "(CPL01) Menginternalisasi ketakwaan kepada Tuhan Yang Maha Esa, menaati hukum, "
         "disiplin, dan menunjukkan profesionalisme melalui etika profesi, pembelajaran "
         "sepanjang hayat, serta respons terhadap isu sosial dan teknologi.",
    "E": "BK30",
    "F": "Pengembangan Diri",
    "G": "CPMK0102",
    "H": "Mampu menginternalisasi nilai ketakwaan kepada Tuhan YME, Pancasila, "
         "kewarganegaraan, dan menunjukkan pembelajaran sepanjang hayat melalui disiplin "
         "diri, tanggung jawab sosial, dan adaptasi karir profesional",
}

NEW_ROWS = [
    {
        "I": "SCPMK0102-00103",
        "J": "Mampu menjelaskan Pancasila sebagai ideologi nasional dan "
             "membandingkannya dengan ideologi lain yang berkembang di dunia [C2, A3].",
        "K": "Ceramah, presentasi, diskusi, tanya jawab, dan kuis",
        "L": "Kuliah/Luring",
        "M": "tes lisan, tugas, dan kuis tertulis",
        "N": "kelancaran dan kesesuaian dalam kerja tim; ketepatan jawaban",
        "O": "Pancasila sebagai ideologi nasional: definisi, fungsi, dan proses "
             "terbentuknya; ideologi lain yang berkembang di dunia: definisi, urgensi "
             "mempelajari ideologi, dan macam-macam ideologi",
    },
    {
        "I": "SCPMK0102-00104",
        "J": "Mampu menginternalisasi nilai Pancasila dalam isu HAM, pencegahan "
             "tindak pidana korupsi, dan Pancasila sebagai paradigma pembangunan [C3, A4].",
        "K": "Ceramah, presentasi, dan tanya jawab; Case Method, FGD, dan diskusi kelompok",
        "L": "Kuliah/Luring",
        "M": "tes lisan, tugas, dan penilaian case method",
        "N": "kelancaran dan kesesuaian dalam kerja tim; ketajaman analisis kasus dan "
             "argumentasi; daya tarik presentasi dan kesesuaian materi",
        "O": "Pancasila dan HAM: definisi, hubungan, implementasi, bentuk-bentuk HAM, dan "
             "contoh penerapannya; pelaksanaan HAM dalam UUD RI 1945; tindak pidana "
             "korupsi: pengertian, jenis-jenis, dan dasar hukum; upaya pencegahan dan "
             "penanggulangan korupsi; Pancasila sebagai paradigma pembangunan; contoh "
             "paradigma pembangunan dan presentasi hasil analisis kasus",
    },
]

COLUMN_ORDER = "ABCDEFGHIJKLMNO"


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_row_xml(row_num, data):
    cells = []
    for col in COLUMN_ORDER:
        val = data.get(col, "")
        if val == "":
            continue
        cells.append(
            f'<c r="{col}{row_num}" t="inlineStr">'
            f'<is><t xml:space="preserve">{xml_escape(val)}</t></is></c>'
        )
    return f'<row r="{row_num}">' + "".join(cells) + "</row>"


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    appended = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            for code in ("SCPMK0102-00103", "SCPMK0102-00104"):
                assert code not in text, f"{code} already present in sheet"

            last_rows = re.findall(r'<row r="(\d+)"', text)
            next_row = max(int(r) for r in last_rows) + 1

            new_rows_xml = ""
            for offset, row_data in enumerate(NEW_ROWS):
                full = dict(SHARED_CONTEXT)
                full.update(row_data)
                new_rows_xml += build_row_xml(next_row + offset, full)
                appended += 1

            assert text.count("</sheetData>") == 1
            text = text.replace("</sheetData>", new_rows_xml + "</sheetData>", 1)

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return appended


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    appended = apply_fix(args.xlsx_path)
    print(f"Appended {appended} rows (expected {len(NEW_ROWS)}).")
    print(f"Saved to {args.xlsx_path}")
