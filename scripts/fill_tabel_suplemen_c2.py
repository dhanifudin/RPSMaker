"""Fill Tabel Suplemen C2's assessment-schedule matrix from cpl-cpmk-subcpmk.xlsx.

Background
----------
docs/Interim LINK 04. (Engineering) Lampiran Tabel Suplemen D4TI Polinema.xlsx's
"Tabel Suplemen C2" sheet is a CPP -> CPMK -> Sub-CPMK x Course assessment-schedule
matrix (187 data rows x 61 course columns, 68 total column slots since 7 courses each
span two columns for their Reguler/Jalur Magang track variants). It was ~91% empty
before this script (only 13 rows had any matrix mark at all, verified this session).

Every Sub-CPMK row's `Sub CPMK` text (column C) was matched, via the same normalized
exact-text-matching methodology already validated for the Tabel Suplemen C1 fill this
session (docs/subcpmk-wording-review.md), against cpl-cpmk-subcpmk.xlsx's
MK-CPMK-SubCPMK-Metode sheet, which carries a `Bentuk Penilaian` value for every
Sub-CPMK. Course names were cross-referenced against C2's own two-row header (semester
row + course-name row) after normalizing "&" -> "dan" (one course, "Desain &
Pemrograman Web" in the source vs "Desain dan Pemrograman Web" in C2's header, needed
this) and matched 1:1 in every other case.

Of 187 Sub-CPMK rows: 121 course-column target cells were resolved (112 rows, 9 extra
from the 7 dual-column courses). 2 already had pre-existing content (the "- Pertemuan
ke-4 - Tengah Semester -" style rows from the original ~13 filled examples) and were
left untouched, per instruction not to overwrite existing scheduling-style data. 66 rows
had no matching text in the source at all (same category as C1's 75 unmatched rows -
genuine content gaps, not filled) and 2 rows were genuinely ambiguous (near-identical
"Bahasa Inggris 1" vs "Bahasa Inggris 2" competency text with no way to disambiguate -
one of the two ambiguous rows even has a pre-existing mark in a THIRD, seemingly
unrelated course column ("Praktikum Dasar Pemrograman"), which was left alone rather
than used to guess).

Of the 119 actually-filled targets:
- 47 (REPLACE) had an existing empty self-closing cell (`<c r="K5" s="..."/>`) to fill,
  same technique as fill_tabel_suplemen_c1.py.
- 72 (INSERT) had NO cell element at all for that row/column - this sheet's rows are
  much more sparse than C1's (a row like row 89 has only its A/B/C cells present; every
  unused matrix column is entirely absent from the XML, not even a placeholder). These
  needed a genuinely new <c> element constructed and spliced into the row's cell
  sequence in the correct column-sorted position (OOXML rows are conventionally
  column-ordered) - see `_insert_cell_sorted`. New cells reuse style id 570, the style
  already used by every one of the sheet's ~13 pre-existing matrix-data cells.

Exception - Algoritma Dan Struktur Data (column T) and Praktikum Algoritma Dan Struktur
Data (column U): per instruction, these two courses' cells do NOT use the source
Metode-sheet Bentuk Penilaian (draft data). Instead they use the verbatim "Kriteria &
Bentuk Penilaian" text from that Sub-CPMK's formal-exam week(s) in the REAL, published
RPS (subjects/RTI252008-.../...-RPS.tex and subjects/RTI252009-.../...-RPS.tex, read
directly this session) - the two courses' own RPS is authoritative here, not the draft
workbook. 5 of the 119 targets are this override (rows 33/163 col T, rows 105/122/164
col U).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this repo: openpyxl
load_workbook(...).save(...) previously caused unrelated data loss in the sibling
cpl-cpmk-subcpmk.xlsx workbook.

IMPORTANT lesson carried over from fill_tabel_suplemen_c1.py: that script's first
attempt produced invalid XML (missing whitespace between attributes when converting a
bare self-closing empty cell to an inline-string cell) that zipfile.testzip() alone did
NOT catch - only an explicit ET.fromstring() parse caught it. This script builds that
well-formedness self-check in from the start (see apply_fix's final step) rather than
discovering the same bug the hard way twice.
"""

import argparse
import os
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(
    REPO_ROOT, "docs",
    "Interim LINK 04. (Engineering) Lampiran Tabel Suplemen D4TI Polinema.xlsx",
)
SHEET = "xl/worksheets/sheet13.xml"  # Tabel Suplemen C2
NEW_CELL_STYLE = "570"  # style id used by every pre-existing matrix-data cell in this sheet

# --- REPLACE: (row, col) -> value, for cells that already exist as an empty placeholder ---
REPLACE = {
    (5, "K"): 'Tes Tulis (UTS)',
    (6, "K"): 'Tes Tulis (UAS)',
    (7, "K"): 'Unjuk Kerja (Presentasi)',
    (13, "M"): 'Unjuk Kerja (Presentasi), Quiz, Tes Tulis (UTS)',
    (14, "M"): 'Quiz, Tes Tulis (UAS)',
    (15, "M"): 'studi kasus, esai/refleksi, presentasi, portofolio, dan tes lisan/tulis',
    (19, "AY"): 'Tes Lisan (Tugas Kelompok)',
    (22, "O"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (23, "O"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (24, "R"): 'Observasi (Praktik/ Tugas), Tes Lisan (Tugas Kelompok), Quiz, Unjuk Kerja (Presentasi), Tes Tulis (UTS)',
    (25, "S"): 'Observasi (Praktik/ Tugas), Quiz, Tes Tulis (UTS)',
    (27, "Z"): 'Observasi (Praktik/ Tugas), Quiz, Tes Tulis (UTS)',
    (33, "T"): 'Ujian teori pilihan ganda dan/atau esai, closed book',  # ASD override
    (34, "E"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (35, "AF"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (36, "AF"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (39, "Q"): 'Observasi (Praktik/ Tugas)',
    (40, "AB"): '1. Penilaian Proses (30%): ⏎ - Keaktifan dalam diskusi dan workshop. ⏎ - Peer-assessment dalam kerja kelompok. ⏎ - Kemajuan iteratif dalam pembuatan artefak proyek. ⏎  ⏎ 2. Penilaian Produk (70%): ⏎ - Tugas 1 (Diagram & Dokumen Desain - 30%): Kumpulan diagram kelas UML dengan inheritance yang tepat dan dokumen spesifikasi teknis singkat. ⏎ - Tugas 2 (Implementasi & Presentasi - 40%): Kode prototipe sederhana yang merealisasikan desain, beserta presentasi yang menjelaskan bagaimana inheritance diterapkan untuk memenuhi kebutuhan fungsional/non-fungsional.',
    (42, "AF"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (49, "AD"): 'Observasi (Praktik/ Tugas), Unjuk Kerja (Presentasi), Partisipasi, Quiz, Tes Tulis (UTS), Tes Tulis (UAS)',
    (51, "BT"): 'Observasi (Praktik/ Tugas)',
    (52, "BT"): 'Observasi (Praktik/ Tugas), Unjuk Kerja (Presentasi), Tes Tulis (UTS), Tes Tulis (UAS), Quiz',
    (53, "F"): 'Quiz, Tes Tulis (UTS)',
    (54, "F"): 'Unjuk Kerja (Presentasi), Partisipasi',
    (58, "AW"): 'Partisipasi, Observasi (Praktik/ Tugas)',
    (59, "E"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (63, "AW"): 'Quiz, Observasi (Praktik/ Tugas)',
    (64, "BD"): 'Observasi (Praktik/ Tugas)',
    (64, "BI"): 'Observasi (Praktik/ Tugas)',
    (65, "BD"): 'Observasi (Praktik/ Tugas)',
    (65, "BI"): 'Observasi (Praktik/ Tugas)',
    (66, "BD"): 'Observasi (Praktik/ Tugas)',
    (66, "BI"): 'Observasi (Praktik/ Tugas)',
    (70, "AJ"): 'tugas praktikum, studi kasus, proyek/produk, demonstrasi, dan tes individu',
    (72, "AW"): 'Unjuk Kerja (Presentasi)',
    (73, "AW"): 'Observasi (Praktik/ Tugas)',
    (75, "BD"): 'Observasi (Praktik/ Tugas)',
    (75, "BI"): 'Observasi (Praktik/ Tugas)',
    (76, "BD"): 'Observasi (Praktik/ Tugas)',
    (76, "BI"): 'Observasi (Praktik/ Tugas)',
    (78, "O"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (79, "Q"): 'Observasi (Praktik/ Tugas)',
    (80, "AF"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (81, "AN"): 'Unjuk Kerja (Presentasi), Tes Tulis (UTS)',
    (82, "AN"): 'Unjuk Kerja (Presentasi), Quiz',
    (84, "Y"): 'Observasi (Praktik/ Tugas), Unjuk Kerja (Presentasi)',
    (87, "AZ"): 'Unjuk Kerja (Presentasi), Observasi (Praktik/ Tugas)',
}

# --- INSERT: (row, col) -> value, for cells with no <c> element present at all ---
INSERT = {
    (89, "AB"): '1. Penilaian Proses & Partisipasi (30%): ⏎ - Kontribusi dalam diskusi role-playing dan analisis studi kasus. ⏎ 2. Penilaian Produk & Proyek (70%): ⏎ Menganalisis kode legacy yang diberikan, mengusulkan perbaikan dengan enkapsulasi dan interface, serta membuat rencana deployment incremental',
    (91, "Q"): 'Observasi (Praktik/ Tugas)',
    (92, "AB"): '1. Penilaian Proses & Partisipasi (30%) ⏎ - Kehadiran & Kontribusi Diskusi ⏎ 2. Penilaian Produk Akhir & Ujian (70%) ⏎ - Dokumen Desain (15%): Diagram kelas (dengan interface), diagram arsitektur, skema database. ⏎ - Implementasi Kode (35%): Aplikasi berfungsi dengan GUI, logika bisnis menggunakan interface, dan database persisten. ⏎ - Ujian Praktek Terstruktur (20%): Ujian lab dimana mahasiswa diminta menambahkan fitur baru (misal: integrasi dengan file CSV menggunakan Java I/O API) ke kode dasar yang diberikan, dengan memperhatikan prinsip interface.',
    (94, "AF"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (95, "AN"): 'Unjuk Kerja (Presentasi), Tes Tulis (UAS)',
    (100, "AF"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (101, "S"): 'Observasi (Praktik/ Tugas), Quiz, Tes Tulis (UTS)',
    (102, "Z"): 'Observasi (Praktik/ Tugas), Quiz',
    (105, "U"): 'Ujian praktik di laboratorium, mengerjakan program secara mandiri',  # Praktikum ASD override
    (106, "I"): 'Quiz, Tes Tulis (UTS), Tes Tulis (UAS)',
    (107, "I"): 'tugas praktikum, studi kasus, proyek/produk, demonstrasi, dan tes individu',
    (108, "J"): 'tugas praktikum, studi kasus, proyek/produk, demonstrasi, dan tes individu',
    (109, "J"): 'Observasi (Praktik/ Tugas), Tes Lisan (Tugas Kelompok), Partisipasi',
    (111, "AB"): '1. Penilaian Formatif (40%) ⏎ - Kuis Singkat: Pemahaman konseptual tentang perbedaan class/object, enkapsulasi, dan polimorfisme. ⏎ 2. Penilaian Sumatif (60%) ⏎ - Dokumen Analisis & Desain (20%): Identifikasi kebutuhan dan diagram class.',
    (114, "AT"): 'Quiz, Tes Tulis (UTS), Observasi (Praktik/ Tugas)',
    (115, "AE"): 'Quiz, Observasi (Praktik/ Tugas), Tes Tulis (UTS), Tes Lisan (Tugas Kelompok), Unjuk Kerja (Presentasi)',
    (115, "AV"): 'Quiz, Observasi (Praktik/ Tugas), Tes Tulis (UTS), Tes Lisan (Tugas Kelompok), Unjuk Kerja (Presentasi)',
    (116, "AH"): 'Tes Tulis (UTS)',
    (117, "AH"): 'Observasi (Praktik/ Tugas)',
    (120, "AT"): 'Unjuk Kerja (Presentasi), Observasi (Praktik/ Tugas)',
    (122, "U"): 'Ujian berbasis case method, mengerjakan penyelesaian kasus struktur data linear secara mandiri',  # Praktikum ASD override
    (125, "O"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (126, "O"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (127, "Q"): 'Tes Lisan (Tugas Kelompok)',
    (128, "Q"): 'Tes Lisan (Tugas Kelompok)',
    (129, "Q"): 'Observasi (Praktik/ Tugas)',
    (130, "Q"): 'Observasi (Praktik/ Tugas)',
    (131, "Q"): 'Observasi (Praktik/ Tugas)',
    (132, "Q"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (134, "AN"): 'Unjuk Kerja (Presentasi), Quiz',
    (135, "AN"): 'Unjuk Kerja (Presentasi), Quiz',
    (139, "AN"): 'Unjuk Kerja (Presentasi), Tes Tulis (UAS), Quiz',
    (140, "AN"): 'Unjuk Kerja (Presentasi), Tes Tulis (UAS), Quiz',
    (146, "E"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (150, "G"): 'Quiz, Tes Tulis (UAS), Tes Tulis (UTS)',
    (151, "G"): 'kuis, tugas pemecahan masalah, studi kasus komputasional, UTS, dan UAS',
    (152, "G"): 'kuis, tugas pemecahan masalah, studi kasus komputasional, UTS, dan UAS',
    (153, "L"): 'Tes Tulis (UTS), Tes Tulis (UAS), Quiz',
    (154, "N"): '- Tugas (25%) ⏎ - Kuis 1 (100%) ⏎ - UTS (40%) ⏎ - UAS (20%)',
    (155, "N"): '- Tugas (50%) ⏎ - UTS (60%) ⏎ - Kuis 2 (20%) ⏎ - UAS (50%)',
    (156, "N"): '- Tugas (25%) ⏎ - Kuis 2 (80%) ⏎ - UAS (25%)',
    (157, "AA"): 'Observasi (Praktik/ Tugas), Quiz, Tes Tulis (UTS)',
    (159, "I"): 'Quiz, Tes Tulis (UTS), Tes Tulis (UAS)',
    (160, "I"): 'tugas praktikum, studi kasus, proyek/produk, demonstrasi, dan tes individu',
    (161, "J"): 'Observasi (Praktik/ Tugas), Tes Lisan (Tugas Kelompok), Partisipasi',
    (162, "J"): 'tugas praktikum, studi kasus, proyek/produk, demonstrasi, dan tes individu',
    (163, "T"): 'Ujian teori pilihan ganda dan esai, closed book',  # ASD override
    (164, "U"): 'Ujian praktik di laboratorium, mengerjakan program secara mandiri; Ujian berbasis case method, mengerjakan penyelesaian kasus algoritmik secara mandiri',  # Praktikum ASD override
    (168, "BD"): 'Partisipasi, Observasi (Praktik/ Tugas)',
    (168, "BI"): 'Partisipasi, Observasi (Praktik/ Tugas)',
    (169, "R"): 'Observasi (Praktik/ Tugas), Quiz, Unjuk Kerja (Presentasi), Tes Tulis (UAS)',
    (170, "R"): 'Observasi (Praktik/ Tugas), Tes Lisan (Tugas Kelompok), Quiz, Unjuk Kerja (Presentasi)',
    (171, "S"): 'Observasi (Praktik/ Tugas), Quiz, Tes Tulis (UAS), Tes Lisan (Tugas Kelompok)',
    (172, "W"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (173, "Z"): 'Observasi (Praktik/ Tugas), Unjuk Kerja (Presentasi), Tes Tulis (UAS), Tes Lisan (Tugas Kelompok)',
    (174, "AW"): 'Observasi (Praktik/ Tugas)',
    (175, "AW"): 'Tes Lisan (Tugas Kelompok)',
    (176, "BD"): 'Observasi (Praktik/ Tugas)',
    (176, "BI"): 'Observasi (Praktik/ Tugas)',
    (177, "AS"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (178, "AT"): 'Quiz, Observasi (Praktik/ Tugas), Tes Tulis (UTS)',
    (179, "AE"): 'Quiz, Observasi (Praktik/ Tugas), Unjuk Kerja (Presentasi), Tes Tulis (UTS), Tes Lisan (Tugas Kelompok)',
    (179, "AV"): 'Quiz, Observasi (Praktik/ Tugas), Unjuk Kerja (Presentasi), Tes Tulis (UTS), Tes Lisan (Tugas Kelompok)',
    (180, "AH"): 'Presentasi Proyek, Dokumentasi, UAS',
    (181, "AR"): 'tugas praktikum, studi kasus, proyek/produk, demonstrasi, dan tes individu',
    (182, "AT"): 'Quiz, Observasi (Praktik/ Tugas)',
    (185, "AA"): 'Tes Tulis (UTS), Quiz, Tes Tulis (UAS), Observasi (Praktik/ Tugas)',
    (186, "AN"): 'Unjuk Kerja (Presentasi), Tes Tulis (UAS)',
    (187, "AN"): 'Unjuk Kerja (Presentasi), Tes Tulis (UAS)',
    (188, "BS"): 'proposal, logbook, produk/artefak, laporan, presentasi, dan penilaian kinerja',
    (189, "AP"): 'kuis, tugas terstruktur, studi kasus, presentasi, UTS, dan UAS',
    (190, "BS"): 'proposal, logbook, produk/artefak, laporan, presentasi, dan penilaian kinerja',
}


def col_to_index(col):
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - 64)
    return idx


def xml_escape(value):
    """Escape &, <, > for safe embedding in XML text content.

    Caught the hard way: the first run of this script raised a ParseError from the
    well-formedness self-check because 4 of the REPLACE/INSERT values contain a literal
    "&" (e.g. "Diagram & Dokumen Desain") that was embedded into <t> content unescaped -
    a bare "&" is not valid XML character data on its own. Every value must go through
    this before being placed inside an XML text node.
    """
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_cell_xml(ref, value):
    return f'<c r="{ref}" s="{NEW_CELL_STYLE}" t="inlineStr"><is><t xml:space="preserve">{xml_escape(value)}</t></is></c>'


def apply_replacements(text):
    applied = 0
    for (row, col), value in REPLACE.items():
        ref = f"{col}{row}"
        pattern = re.compile(rf'<c r="{ref}"([^/]*?)/>')
        m = pattern.search(text)
        assert m, f"could not find empty placeholder cell {ref}"
        attrs = m.group(1)
        old_full = m.group(0)
        new_full = f'<c r="{ref}" {attrs.strip()} t="inlineStr"><is><t xml:space="preserve">{xml_escape(value)}</t></is></c>'
        assert text.count(old_full) == 1, f"{ref}: not exactly 1 occurrence"
        text = text.replace(old_full, new_full, 1)
        applied += 1
    return text, applied


def apply_insertions(text):
    """Group inserts by row, then rebuild each row's <c> sequence in column order."""
    from collections import defaultdict
    by_row = defaultdict(dict)
    for (row, col), value in INSERT.items():
        by_row[row][col] = value

    applied = 0
    for row, col_values in by_row.items():
        row_pattern = re.compile(rf'(<row r="{row}"[^>]*>)(.*?)(</row>)', re.S)
        m = row_pattern.search(text)
        assert m, f"could not find row {row}"
        prefix, body, suffix = m.groups()

        # parse existing cells in this row: list of (col_index, col_letter, full_xml)
        existing = []
        for cm in re.finditer(r'<c r="([A-Z]{1,3})\d+"[^>]*(?:/>|>.*?</c>)', body, re.S):
            col_letter = cm.group(1)
            existing.append((col_to_index(col_letter), cm.group(0)))

        for col, value in col_values.items():
            ref = f"{col}{row}"
            assert not re.search(rf'<c r="{ref}"', body), f"{ref}: cell already exists, expected absent"
            existing.append((col_to_index(col), make_cell_xml(ref, value)))
            applied += 1

        existing.sort(key=lambda x: x[0])
        new_body = "".join(xml for _, xml in existing)
        old_full = m.group(0)
        new_full = prefix + new_body + suffix
        assert text.count(old_full) == 1, f"row {row}: not exactly 1 occurrence"
        text = text.replace(old_full, new_full, 1)

    return text, applied


def apply_fix(xlsx_path: str):
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    counts = {"replace": 0, "insert": 0}
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            text, counts["replace"] = apply_replacements(text)
            text, counts["insert"] = apply_insertions(text)

            # Mandatory well-formedness self-check - see module docstring for why.
            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    counts = apply_fix(args.xlsx_path)
    print(f"Replaced (existing empty cell): {counts['replace']} (expected {len(REPLACE)})")
    print(f"Inserted (new cell): {counts['insert']} (expected {len(INSERT)})")
    print(f"Total filled: {counts['replace'] + counts['insert']} (expected {len(REPLACE) + len(INSERT)})")
    print(f"Saved to {args.xlsx_path}")
