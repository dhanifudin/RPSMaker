"""Restore 5 real RPS Sub-CPMK missing from MK045/MK046 in the Metode sheet.

Background
----------
Follow-up to the "empty Sub-CPMK code" fix (2026-07-11, third pass). That audit's
undefined-CPMK verification also flagged 4 POPULATED rows (not empty ones) referencing
codes CPMK0313/0314 (MK045 Komunikasi dan Etika Profesi) and CPMK0315/0316 (MK046
Pengembangan Karir) that don't exist anywhere in the canonical CPL-CPMK master. Investigation
showed the exact same pattern as the earlier CPL03 cluster: these are vestigial early-draft
CPMK numbering whose content was later re-authored in the final published RPS under correct
canonical codes (CPMK0101/CPMK0301/CPMK0303 for MK045; CPMK0102/CPMK0303 for MK046) - but the
real Sub-CPMK under those canonical codes were never added to this master sheet.

  MK045 Komunikasi dan Etika Profesi: has SCPMK0101-04501 only. Missing SCPMK0301-04502,
    SCPMK0303-04503 (both defined in the real RPS).
  MK046 Pengembangan Karir: has SCPMK0102-04601 only. Missing all 3 of the real RPS's
    CPMK0303 Sub-CPMK. The RPS itself uses a "-053xx" serial suffix (a copy-paste artifact
    from another course's numbering, unrelated to this fix) - this script uses this sheet's
    own established "-046xx" (matching Kode MK "MK046") serial convention instead, reusing
    the two serials freed up by deleting the orphan rows (04602, 04603) plus one new (04604).

The now-redundant orphan rows (157/158/160/161) are deleted separately by
delete_redundant_orphans_mk045_mk046.py, run AFTER this script - same two-step order as the
original CPL03 cluster fix.

Every new row is fully self-contained (explicit Kode MK/MK/CPL/Kode BK/BK/Kode CPMK/CPMK),
same precaution as every other row addition this session. This also fixes the same stale-
carry-down defect found in the original fix: rows 157/158/160/161 all silently inherited
"(CPL01) ... " context from row155's explicit CPL01 declaration, despite their content being
CPL03 (communication/career) material - the new rows use the correct canonical CPL03 context
instead (D/E/F reused verbatim from row194, MK057 Magang, same as the original fix).

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

MK046_CPMK0303_H = (
    "Mampu mengembangkan diri secara berkelanjutan, berkomunikasi secara profesional, dan "
    "mengelola karir secara sistematis untuk mencapai tujuan karir jangka panjang."
)

NEW_ROWS = [
    # --- MK045 Komunikasi dan Etika Profesi (RTI256001) ---
    {
        "B": "MK045", "C": "Komunikasi Dan Etika Profesi", **CPL03,
        "G": "CPMK0301",
        "H": "Mampu berkomunikasi dan mempresentasikan gagasan teknis secara efektif "
             "dalam konteks kerja profesional.",
        "I": "SCPMK0301-04502",
        "J": "Mampu menyajikan presentasi teknis, menulis laporan profesional, dan "
             "berkolaborasi dalam tim lintas fungsi.",
        "K": "Case Method, simulasi profesional, studi kasus, dan diskusi reflektif",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas, UTS, dan PBL (simulasi profesional)",
        "N": "Ketepatan konsep; kualitas komunikasi; validasi dan dokumentasi.",
        "O": "Teknik komunikasi profesional dan presentasi teknis; penulisan profesional "
             "(email, laporan, proposal teknis); dinamika tim dan kolaborasi lintas fungsi",
    },
    {
        "B": "MK045", "C": "Komunikasi Dan Etika Profesi", **CPL03,
        "G": "CPMK0303",
        "H": "Mampu menyusun rencana pengembangan karir dan portofolio profesional di "
             "bidang TI.",
        "I": "SCPMK0303-04503",
        "J": "Mampu menyusun portofolio profesional dan rencana pengembangan karir "
             "berbasis kompetensi TI.",
        "K": "Case Method, simulasi profesional, studi kasus, dan diskusi reflektif",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "kuis, PBL (portofolio), dan UAS (presentasi portofolio)",
        "N": "Ketepatan konsep; kualitas komunikasi; validasi dan dokumentasi.",
        "O": "Tanggung jawab sosial korporasi di bidang TI; personal branding (LinkedIn, "
             "GitHub, portofolio digital); perencanaan karir dan strategi pencarian "
             "kerja; CV, cover letter, dan teknik wawancara kerja",
    },
    # --- MK046 Pengembangan Karir (RTI256002) ---
    {
        "B": "MK046", "C": "Pengembangan Karir", **CPL03,
        "G": "CPMK0303",
        "H": MK046_CPMK0303_H,
        "I": "SCPMK0303-04602",
        "J": "Mampu mengidentifikasi dan menganalisis minat, bakat, potensi diri, serta "
             "peluang karir sesuai kompetensi dan tren industri informatika.",
        "K": "Ceramah, tanya jawab, studi literatur, diskusi, dan tugas",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas, UTS (presentasi portofolio), dan UAS (evaluasi akhir)",
        "N": "Ketepatan konsep; kedalaman refleksi; kebaruan ide dan gagasan.",
        "O": "Pemetaan minat dan potensi karir; karir mandiri dan fleksibel di era "
             "digital; profesi bidang informatika; karir organisasi vs freelance; karir "
             "era Industri 4.0",
    },
    {
        "B": "MK046", "C": "Pengembangan Karir", **CPL03,
        "G": "CPMK0303",
        "H": MK046_CPMK0303_H,
        "I": "SCPMK0303-04603",
        "J": "Mampu merancang strategi personal branding dan komunikasi profesional yang "
             "efektif untuk pengembangan karir di era digital.",
        "K": "Ceramah, diskusi, dan tugas",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas, UTS (presentasi portofolio), dan UAS (evaluasi akhir)",
        "N": "Ketepatan konsep; kedalaman refleksi; kebaruan ide dan gagasan.",
        "O": "Personal branding profesional; public speaking profesional; pembuatan CV "
             "profesional dan ATS-friendly",
    },
    {
        "B": "MK046", "C": "Pengembangan Karir", **CPL03,
        "G": "CPMK0303",
        "H": MK046_CPMK0303_H,
        "I": "SCPMK0303-04604",
        "J": "Mampu menyusun Career Development Plan (CDP) yang sistematis mencakup "
             "tujuan SMART, analisis gap kompetensi, strategi pengembangan diri, dan "
             "timeline pencapaian.",
        "K": "Ceramah, diskusi, tugas, presentasi proyek individual, dan peer review",
        "L": "Kuliah/Blended Learning (Luring/Daring)",
        "M": "tugas dan PBL (Career Development Plan)",
        "N": "Ketepatan konsep; kedalaman refleksi; kebaruan ide dan gagasan; "
             "kelengkapan CDP; kualitas presentasi dan pertahanan argumen.",
        "O": "Manajemen karir jangka panjang; perencanaan karir (SMART goals dan "
             "roadmap); penilaian kinerja dan KPI; internasionalisasi karir; PBL Career "
             "Development Plan (CDP) menyeluruh",
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
