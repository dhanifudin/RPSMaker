"""Restore 9 real RPS Sub-CPMK missing from cpl-cpmk-subcpmk.xlsx's Metode sheet.

Background
----------
A deep "empty Sub-CPMK code" audit (2026-07-11, third pass) found that 10 rows in the Metode
sheet carry a Kode CPMK but no Kode SubCPMK - all referencing undefined CPL03-cluster codes
CPMK0307-CPMK0322 (canonically CPL03 only has CPMK0301/0302/0303). Cross-referencing each
affected course's real published RPS showed most of the orphan content was already
re-authored in the final RPS under the correct canonical CPMK - but 9 of those real Sub-CPMK
were never added to this master sheet at all:

  MK030 Bahasa Indonesia:       SCPMK0301-03001, SCPMK0401-03002 (course had ZERO real rows)
  MK037 Kewirausahaan:          SCPMK0101-03702, SCPMK0301-03703, SCPMK0301-03704
  MK057 Magang:                 SCPMK0301-05701, SCPMK0303-05702
  MK058 Skripsi:                SCPMK0403-05801, SCPMK0802-05803

This script adds those 9 rows, sourced verbatim from each course's RPS.tex (leading
"Mahasiswa " stripped from the Sub-CPMK statement to match this session's established house
style). The now-redundant orphan rows (102,103,130,131,194,195) are deleted separately by
delete_redundant_cpl03_orphans.py, run AFTER this script.

Every new row is fully self-contained (explicit Kode MK/MK/CPL/Kode BK/BK/Kode CPMK/CPMK) -
same precaution as every other row addition this session, following the row-1162 incident
where an unrelated later edit broke an implicit carry-down chain. This also fixes a separate,
newly-discovered defect: the deleted orphan rows (102,103,130,131) carried STALE CPL/BK
context via blank-continuation (e.g. row102/103 inherited "(CPL06) ... Software Modeling"
from an earlier block, despite their content being CPL03 communication/writing content) -
these new rows use the correct canonical CPL context instead.

Canonical CPL context text (D/E/F) reused verbatim from existing correctly-labeled rows in
this same sheet:
  - CPL03 (D/E="BK30"/F="Pengembangan Diri"): from row194 (MK057 Magang, CPMK0301/0303).
  - CPL04 (D/E="BK01\\nBK31"/F="...Metodologi Penelitian"): from row200 (MK058, CPMK0404).
  - CPL08 (D/E="BK03\\nBK30"/F="Project Management\\nPengembangan Diri"): from row203 (MK058,
    CPMK0804).
  - CPL01 (D/E="BK30"/F="Pengembangan Diri"): from row130's resolved carry-down (MK037,
    CPMK0101), matching row128's own CPMK0101 context.

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

CPL03 = {
    "D": "(CPL03)\nMemiliki kemampuan (pengelolaan) manajerial tim dan kerja sama (team "
         "work), manajemen diri, mampu berkomunikasi baik lisan maupun tertulis dengan baik "
         "dan mampu melakukan presentasi.",
    "E": "BK30",
    "F": "Pengembangan Diri",
}
CPL04 = {
    "D": "(CPL04)\nMenyusun deskripsi saintifik hasil kajian implikasi pengembangan atau "
         "implementasi ilmu pengetahuan teknologi dalam bentuk skripsi atau laporan tugas "
         "akhir atau artikel\nilmiah.",
    "E": "BK01\nBK31",
    "F": "Social Issues and Professional Practice\nMetodologi Penelitian",
}
CPL08 = {
    "D": "(CPL08)\nMampu mengelola proyek teknologi informasi secara profesional dengan "
         "mengoptimalkan sumber daya yang tersedia",
    "E": "BK03\nBK30",
    "F": "Project Management\nPengembangan Diri",
}
CPL01 = {
    "D": "(CPL01) Menginternalisasi ketakwaan kepada Tuhan Yang Maha Esa, menaati hukum, "
         "disiplin, dan menunjukkan profesionalisme melalui etika profesi, pembelajaran "
         "sepanjang hayat, serta respons terhadap isu sosial dan teknologi.",
    "E": "BK30",
    "F": "Pengembangan Diri",
}

MK037_CPMK0101_H = (
    "Mampu menunjukkan profesionalisme melalui penerapan etika profesi TI, keselamatan "
    "kerja, kewirausahaan bertanggung jawab, rekayasa perangkat lunak ramah lingkungan, dan "
    "disiplin dalam penelitian maupun penerapan aplikasi teknologi"
)

NEW_ROWS = [
    # --- MK030 Bahasa Indonesia (RTI254003) ---
    {
        "B": "MK030", "C": "Bahasa Indonesia", **CPL03,
        "G": "CPMK0301",
        "H": "Mampu mengelola diri secara profesional, berkomunikasi efektif lisan dan "
             "tulisan dalam bahasa Indonesia baku untuk keperluan akademik dan profesional.",
        "I": "SCPMK0301-03001",
        "J": "Mampu menulis laporan teknis, makalah, dan proposal dalam bahasa Indonesia "
             "yang baku, sistematis, dan efektif.",
        "K": "Case Method, diskusi, presentasi, dan peer review",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas, kuis, UTS, dan UAS",
        "N": "Ketepatan bahasa; kualitas karya tulis; validasi dan dokumentasi.",
        "O": "Ragam bahasa baku dan tidak baku; EYD V dan tanda baca; diksi dan kalimat "
             "efektif; paragraf: kohesi dan koherensi; penulisan laporan teknis dan "
             "proposal; presentasi dan diskusi ilmiah",
    },
    {
        "B": "MK030", "C": "Bahasa Indonesia", **CPL04,
        "G": "CPMK0401",
        "H": "Mampu menganalisis masalah dan menulis karya ilmiah berbasis data "
             "menggunakan kaidah bahasa Indonesia yang benar.",
        "I": "SCPMK0401-03002",
        "J": "Mampu menyusun karya tulis ilmiah sederhana dengan rumusan masalah, "
             "metodologi, pembahasan, dan kesimpulan yang valid sesuai kaidah akademik.",
        "K": "Case Method, diskusi, presentasi, dan peer review",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas, UTS, kuis, PBL, dan UAS",
        "N": "Ketepatan bahasa; kualitas karya tulis; validasi dan dokumentasi.",
        "O": "Karya tulis ilmiah: struktur dan jenis; rumusan masalah dan tinjauan "
             "pustaka; metodologi penulisan ilmiah; sitasi dan daftar pustaka "
             "(APA/IEEE style); abstrak dan artikel ilmiah; PBL penulisan karya tulis "
             "ilmiah",
    },
    # --- MK037 Kewirausahaan Berbasis Teknologi (RTI255001) ---
    {
        "B": "MK037", "C": "Kewirausahaan Berbasis Teknologi", **CPL01,
        "G": "CPMK0101",
        "H": MK037_CPMK0101_H,
        "I": "SCPMK0101-03702",
        "J": "Mampu menganalisis permintaan pasar, menyusun rencana pemasaran, "
             "mengidentifikasi aspek teknis bisnis, serta menyusun laporan keuangan "
             "dasar dan penetapan harga.",
        "K": "Blended Learning, experiential learning, business simulation, studi "
             "kasus, dan presentasi",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas, kuis, dan UTS",
        "N": "Ketepatan konsep; kualitas artefak/praktik; validasi dan dokumentasi.",
        "O": "Memahami pasar dan rencana pemasaran; aspek-aspek teknis bisnis; "
             "menghitung biaya dan menetapkan harga jual; modal awal dan proyeksi "
             "laporan keuangan; rasio keuangan dasar",
    },
    {
        "B": "MK037", "C": "Kewirausahaan Berbasis Teknologi", **CPL03,
        "G": "CPMK0301",
        "H": "Mampu mengelola diri secara profesional, berkomunikasi efektif, dan "
             "mempresentasikan rencana bisnis teknologi kepada pemangku kepentingan.",
        "I": "SCPMK0301-03703",
        "J": "Mampu merancang Business Model Canvas, menganalisis sumber pendanaan, "
             "aspek hukum, tanggung jawab sosial, manajemen SDM, dan strategi "
             "pengembangan produk baru.",
        "K": "Blended Learning, experiential learning, business simulation, studi "
             "kasus, dan presentasi",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "Case Method (workshop) dan tugas",
        "N": "Ketepatan konsep; kualitas artefak/praktik; validasi dan dokumentasi.",
        "O": "Business Model Canvas; sumber-sumber pendanaan bisnis baru; aspek hukum "
             "dan tanggung jawab sosial; manajemen SDM, jaringan, dan pengembangan "
             "produk baru",
    },
    {
        "B": "MK037", "C": "Kewirausahaan Berbasis Teknologi", **CPL03,
        "G": "CPMK0301",
        "H": "Mampu mengelola diri secara profesional, berkomunikasi efektif, dan "
             "mempresentasikan rencana bisnis teknologi kepada pemangku kepentingan.",
        "I": "SCPMK0301-03704",
        "J": "Mampu menyusun dan mempresentasikan rencana bisnis teknologi secara "
             "profesional dengan argumentasi berbasis data kepada pemangku kepentingan.",
        "K": "Blended Learning, experiential learning, business simulation, studi "
             "kasus, dan presentasi",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "UAS (presentasi rencana bisnis)",
        "N": "Ketepatan konsep; kualitas artefak/praktik; validasi dan dokumentasi.",
        "O": "UAS: presentasi rencana bisnis teknologi",
    },
    # --- MK057 Magang (RTI257001) ---
    {
        "B": "MK057", "C": "Magang", **CPL03,
        "G": "CPMK0301",
        "H": "Mampu berkomunikasi secara profesional lisan dan tulisan dalam "
             "lingkungan kerja industri TI.",
        "I": "SCPMK0301-05701",
        "J": "Mampu berkomunikasi profesional secara lisan dan tulisan selama "
             "kegiatan magang di industri TI.",
        "K": "Praktik industri, monitoring berkala, dan bimbingan pembimbing "
             "akademik/lapangan",
        "L": "Praktik Lapangan dan Bimbingan",
        "M": "logbook dan laporan",
        "N": "Ketepatan waktu; kualitas dokumen; profesionalisme.",
        "O": "Pembekalan magang: orientasi dan etika kerja; monitoring logbook dan "
             "progress report bulanan; logbook final dan evaluasi keseluruhan",
    },
    {
        "B": "MK057", "C": "Magang", **CPL03,
        "G": "CPMK0303",
        "H": "Mampu mempresentasikan hasil kerja dan laporan magang secara efektif "
             "kepada pembimbing dan penguji.",
        "I": "SCPMK0303-05702",
        "J": "Mampu menyusun dan mempresentasikan laporan magang yang komprehensif "
             "kepada pembimbing akademik dan penguji.",
        "K": "Praktik industri, monitoring berkala, dan bimbingan pembimbing "
             "akademik/lapangan",
        "L": "Praktik Lapangan dan Bimbingan",
        "M": "laporan dan sidang",
        "N": "Ketepatan waktu; kualitas dokumen; profesionalisme.",
        "O": "Bimbingan penulisan laporan: struktur dan konten; draft laporan magang "
             "bab I-III; revisi dan finalisasi laporan; persiapan dan pelaksanaan "
             "sidang magang",
    },
    # --- MK058 Skripsi (RTI258001) ---
    {
        "B": "MK058", "C": "Skripsi", **CPL04,
        "G": "CPMK0403",
        "H": "Mampu melaksanakan penelitian/pengembangan TIK secara sistematis dan "
             "mandiri berdasarkan metodologi ilmiah.",
        "I": "SCPMK0403-05801",
        "J": "Mampu melaksanakan penelitian atau pengembangan sistem TIK secara "
             "sistematis sesuai metodologi yang dipilih.",
        "K": "Penelitian/pengembangan mandiri, bimbingan akademik, dan presentasi "
             "ilmiah",
        "L": "Penelitian Mandiri dan Bimbingan",
        "M": "seminar kemajuan dan penilaian pelaksanaan penelitian",
        "N": "Kemajuan penelitian; kualitas dokumen ilmiah; profesionalisme akademis.",
        "O": "Penentuan metodologi penelitian; bimbingan proposal BAB III metodologi; "
             "pelaksanaan penelitian fase 1-2; seminar kemajuan/progress report",
    },
    {
        "B": "MK058", "C": "Skripsi", **CPL08,
        "G": "CPMK0802",
        "H": "Mampu merencanakan dan mengelola jalannya penelitian/pengembangan "
             "skripsi secara profesional.",
        "I": "SCPMK0802-05803",
        "J": "Mampu menyusun proposal penelitian, membuat jadwal, dan mengelola "
             "progress skripsi secara mandiri.",
        "K": "Penelitian/pengembangan mandiri, bimbingan akademik, dan presentasi "
             "ilmiah",
        "L": "Penelitian Mandiri dan Bimbingan",
        "M": "proposal penelitian",
        "N": "Kemajuan penelitian; kualitas dokumen ilmiah; profesionalisme akademis.",
        "O": "Orientasi skripsi: prosedur dan pemilihan pembimbing; bimbingan proposal "
             "BAB I pendahuluan; finalisasi dan pengumpulan proposal; seminar "
             "proposal skripsi",
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

            for row in NEW_ROWS:
                assert row["I"] not in text, f"{row['I']} already present in sheet"

            last_rows = re.findall(r'<row r="(\d+)"', text)
            next_row = max(int(r) for r in last_rows) + 1

            new_rows_xml = ""
            for offset, row_data in enumerate(NEW_ROWS):
                new_rows_xml += build_row_xml(next_row + offset, row_data)
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
