"""Phase 1 of the 59-course-scheme alignment: fix the Metode sheet's BIPK rows and
add the missing Rekayasa Sistem rows.

Background
----------
The full three-level audit (2026-07-11) found the workbook holds two competing MK
numbering schemes: the stale internal registry (55 courses; MK053=Magang, MK054=Skripsi,
MK055=Bahasa Inggris Persiapan Kerja) vs. the published curriculum (59 courses; MK053-056
= the four second-track RTI2562xx courses, Magang=MK057, Skripsi=MK058, BIPK=MK059).
The workbook's own data already follows the published scheme (Magang rows embed 057xx
serials, Skripsi 058xx), so the curriculum owner confirmed the published scheme as
canonical.

That decision reverses fix_mk055_mk059_unify.py (committed ff697ca), which had trusted
the four stale registry sheets and moved BIPK onto MK055 / 055xx serials - serial space
that belongs to Rekayasa Sistem (its published RPS claims SCPMK0211-05501,
SCPMK0602-05502, SCPMK0609-05503). This script:

1. Reverts rows 1174/1175 to MK059 with codes SCPMK0303-05901 / SCPMK0102-05902.
2. Migrates the two pre-existing BIPK draft rows 207/208 out of Rekayasa Sistem's
   serial space: B207 MK055 -> MK059, I207 -05501 -> -05903, I208 -05502 -> -05904
   (content kept per curriculum-owner decision - career-plan/TOEIC material distinct
   from the -05901/-05902 rows). E207's "BK 30" is normalized to "BK30" in passing.
3. Appends three Rekayasa Sistem rows as MK055 (rows 1176-1178) with its real codes
   05501-05503. Sub-CPMK text from the course's published RPS; CPMK descriptions and
   BK assignments from the master CPL-CPMK sheet (CPMK0211/BK26, CPMK0602/BK10,
   CPMK0609/BK29). All three rows are fully self-contained (course/CPL/BK cells on
   every row, not carry-down) - lesson from the row-1162 incident, where trimming a
   block's header row orphaned its continuation row.

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


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


REPLACEMENTS = [
    # 1. revert rows 1174/1175 to MK059 + published codes
    ('<c r="B1174" t="inlineStr"><is><t xml:space="preserve">MK055</t></is></c>',
     '<c r="B1174" t="inlineStr"><is><t xml:space="preserve">MK059</t></is></c>'),
    ('<c r="B1175" t="inlineStr"><is><t xml:space="preserve">MK055</t></is></c>',
     '<c r="B1175" t="inlineStr"><is><t xml:space="preserve">MK059</t></is></c>'),
    ('<c r="I1174" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05503</t></is></c>',
     '<c r="I1174" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05901</t></is></c>'),
    ('<c r="I1175" t="inlineStr"><is><t xml:space="preserve">SCPMK0102-05504</t></is></c>',
     '<c r="I1175" t="inlineStr"><is><t xml:space="preserve">SCPMK0102-05902</t></is></c>'),
    # 2. migrate pre-existing BIPK drafts (rows 207/208) to MK059 / 059xx serials
    ('<c r="B207" s="153" t="s"><v>230</v></c>',
     '<c r="B207" s="153" t="inlineStr"><is><t xml:space="preserve">MK059</t></is></c>'),
    ('<c r="E207" s="101" t="s"><v>669</v></c>',
     '<c r="E207" s="101" t="inlineStr"><is><t xml:space="preserve">BK30</t></is></c>'),
    ('<c r="I207" s="110" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05501</t></is></c>',
     '<c r="I207" s="110" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05903</t></is></c>'),
    ('<c r="I208" s="40" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05502</t></is></c>',
     '<c r="I208" s="40" t="inlineStr"><is><t xml:space="preserve">SCPMK0303-05904</t></is></c>'),
]

# 3. Rekayasa Sistem rows (fully self-contained), appended as rows 1176-1178.
# tuple: (D CPL text, E Kode BK, F BK, G Kode CPMK, H CPMK desc, I code, J SubCPMK,
#         M bentuk penilaian, O materi)
K_METODE = "Case Method, workshop kolaboratif, presentasi teknis, dan peer review"
L_BENTUK = "Blended Learning (Luring/Daring)"
N_KRITERIA = "Ketepatan konsep; kualitas artefak; validasi dan dokumentasi"

RS_ROWS = [
    ("(CPL02) Menguasai konsep teoritis bidang pengetahuan mengenai berbagai prinsip "
     "rekayasa sistem/perangkat lunak dalam merancang solusi aplikasi multi-platform "
     "yang relevan dengan kebutuhan stakeholder.",
     "BK26", "Systems Analysis & Design",
     "CPMK0211",
     "Mampu menerapkan metodologi analisis dan desain sistem secara terstruktur untuk "
     "mentransformasi kebutuhan stakeholder menjadi spesifikasi teknis yang komprehensif "
     "bagi pengembangan aplikasi multi-platform, dengan menghasilkan artefak desain yang "
     "mencakup aspek fungsional, non-fungsional, dan arsitektural yang dapat diimplementasikan",
     "SCPMK0211-05501",
     "Mampu merancang arsitektur sistem enterprise meliputi komponen, antarmuka, aliran "
     "data, dan ketergantungan antar modul.",
     "Bentuk penilaian: desain arsitektur awal (dokumen arsitektur); implementasi komponen "
     "(Sprint 1-2); finalisasi arsitektur (Sprint 3-4); defense arsitektur (UAS)",
     "Arsitektur sistem enterprise: pola arsitektur, komponen, antarmuka, dan dokumentasi ADR"),
    ("(CPL06) Mampu merancang, mengimplementasikan, menguji, melakukan deployment, dan "
     "memelihara, serta menjamin mutu perangkat lunak yang menjawab permasalahan dan "
     "memenuhi kebutuhan stakeholder.",
     "BK10", "Software Design",
     "CPMK0602",
     "Mampu merancang komponen perangkat lunak secara sistematis menggunakan pola desain "
     "yang sesuai dengan kebutuhan stakeholder",
     "SCPMK0602-05502",
     "Mampu melakukan elicitation, analisis, spesifikasi, dan validasi kebutuhan sistem "
     "yang kompleks.",
     "Bentuk penilaian: kontribusi SRS awal (dokumen arsitektur); presentasi SRS (UTS); "
     "SRS final (laporan)",
     "Requirement elicitation: teknik wawancara, use case, user story, dan spesifikasi kebutuhan"),
    ("(CPL06) Mampu merancang, mengimplementasikan, menguji, melakukan deployment, dan "
     "memelihara, serta menjamin mutu perangkat lunak yang menjawab permasalahan dan "
     "memenuhi kebutuhan stakeholder.",
     "BK29", "Software Modeling and Analysis",
     "CPMK0609",
     "Mampu merancang model pemodelan perangkat lunak yang akurat untuk memastikan desain "
     "teknis memenuhi seluruh spesifikasi kebutuhan stakeholder",
     "SCPMK0609-05503",
     "Mampu merancang dan mengimplementasikan pipeline CI/CD serta strategi deployment "
     "blue-green/canary untuk sistem produksi.",
     "Bentuk penilaian: pipeline CI/CD (Sprint 1-2); deployment strategy (Sprint 3-4); "
     "demo deployment (UAS)",
     "Pipeline CI/CD: automated testing, integrasi, dan strategi deployment (blue-green, "
     "canary); monitoring, observability, dan pemeliharaan sistem produksi"),
]

FIRST_NEW_ROW = 1176


def build_row_xml(row_num, values):
    d, e, f, g, h, i, j, m, o = values
    cells = [
        ("B", "MK055"), ("C", "Rekayasa Sistem"), ("D", d), ("E", e), ("F", f),
        ("G", g), ("H", h), ("I", i), ("J", j),
        ("K", K_METODE), ("L", L_BENTUK), ("M", m), ("N", N_KRITERIA), ("O", o),
    ]
    parts = [f'<row r="{row_num}">']
    for col, val in cells:
        parts.append(
            f'<c r="{col}{row_num}" t="inlineStr">'
            f'<is><t xml:space="preserve">{xml_escape(val)}</t></is></c>'
        )
    parts.append("</row>")
    return "".join(parts)


def apply_fix(xlsx_path: str):
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    replaced = appended = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            for old, new in REPLACEMENTS:
                assert text.count(old) == 1, f"not found or not unique: {old[:80]!r}"
                text = text.replace(old, new, 1)
                replaced += 1

            last_rows = re.findall(r'<row r="(\d+)"', text)
            assert max(int(x) for x in last_rows) == FIRST_NEW_ROW - 1, (
                f"expected last row {FIRST_NEW_ROW - 1}, got {max(int(x) for x in last_rows)}"
            )
            for code in ("SCPMK0211-05501", "SCPMK0602-05502", "SCPMK0609-05503"):
                assert code not in text, f"{code} already present in sheet"

            new_rows_xml = "".join(
                build_row_xml(FIRST_NEW_ROW + idx, vals) for idx, vals in enumerate(RS_ROWS)
            )
            assert text.count("</sheetData>") == 1
            text = text.replace("</sheetData>", new_rows_xml + "</sheetData>", 1)
            appended = len(RS_ROWS)

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return replaced, appended


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    replaced, appended = apply_fix(args.xlsx_path)
    print(f"Applied {replaced} cell replacements (expected {len(REPLACEMENTS)}).")
    print(f"Appended {appended} Rekayasa Sistem rows at {FIRST_NEW_ROW}-{FIRST_NEW_ROW + appended - 1}.")
    print(f"Saved to {args.xlsx_path}")
