"""Re-code 4 CPL03-orphan rows (MK048, MK058) to their correct canonical CPMK.

Background
----------
Same "empty Sub-CPMK code" audit (2026-07-11, third pass) that produced
restore_missing_subcpmk_from_rps.py found 10 rows referencing undefined CPL03-cluster codes
CPMK0307-CPMK0322. For 6 of them (MK030, MK037, MK057) the same competency was re-authored in
the real RPS under a correct canonical CPMK, so those are handled by restoring the real RPS
row and deleting the orphan (delete_redundant_cpl03_orphans.py).

The remaining 4 rows are different: they hold the ONLY record of a real, curriculum-mandated
CPL03 competency that the course's published RPS never documented:
  - MK048 Proyek Teknologi Terintegrasi, rows 166/167 (CPMK0317/0318): team leadership and
    stakeholder-presentation content for a project course. MK048 is explicitly listed as a
    "MK kunci" for CPMK0302 (team/project management) in docs/kurikulum-2025-cpl-cpmk.md, but
    has no CPMK0302 Sub-CPMK anywhere else in the sheet.
  - MK058 Skripsi, rows 201/202 (CPMK0321/0322): self-management/committee-defense content.
    CPMK0301 (self-management, communication) fits; the row's original "menulis skripsi"
    clause is dropped from the re-coded Sub-CPMK statement because that specific competency
    is already covered by the existing SCPMK0404-05802 row (CPMK0404, writing) - keeping it
    would duplicate content instead of resolving the CPL03 gap.

User-approved approach: re-code rather than delete, since these rows are the only record of
real content, and rather than invent all-new rows, since K-O (Metode/Bentuk/Penilaian/
Kriteria/Materi) were already correctly populated and course-appropriate - only G (Kode CPMK),
H (CPMK description), I (Kode SubCPMK), J (SubCPMK statement) are wrong/missing, plus D/E/F
(CPL/BK context), which had silently inherited STALE values via the sheet's blank-continuation
carry-down convention (row166/167 inherited "(CPL02) ... Systems Analysis & Design" from an
earlier block; row201/202 had inherited CPL03 text but the wrong BK "Social Issues/Metodologi
Penelitian" instead of "Pengembangan Diri", which matches CPMK0301 in every other course).

J (Sub-CPMK statement) is also cleaned up: the original auto-generated text had a garbled
"Mampu menyusun dan mengomunikasikan" prefix spliced onto the CPMK description (H) verbatim -
removed here in favor of a direct, clean statement.

Canonical CPL03/CPMK0302 context (D/E/F) reused verbatim from row194 (MK057 Magang) /
kurikulum-2025-cpl-cpmk.md's own CPMK0302 summary, same as restore_missing_subcpmk_from_rps.py.

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

CPL03_D = (
    "(CPL03)\nMemiliki kemampuan (pengelolaan) manajerial tim dan kerja sama (team "
    "work), manajemen diri, mampu berkomunikasi baik lisan maupun tertulis dengan baik "
    "dan mampu melakukan presentasi."
)
CPL03_E = "BK30"
CPL03_F = "Pengembangan Diri"

CPMK0302_H = (
    "Mampu memimpin dan mengelola tim dalam proyek teknologi terintegrasi secara efektif "
    "melalui perencanaan, koordinasi, dan pengambilan keputusan untuk menyelesaikan "
    "permasalahan nyata dengan menggabungkan berbagai teknologi."
)
CPMK0301_SKRIPSI_H = (
    "Mampu mengelola diri secara profesional dan berkomunikasi efektif dengan dosen "
    "pembimbing serta pihak terkait selama pelaksanaan penelitian tugas akhir."
)

# row -> (new D, new E, new F, new G, new H, new I, new J). K-O are left untouched: they
# were already correctly populated and course-appropriate.
RECODES = {
    166: {
        "D": CPL03_D, "E": CPL03_E, "F": CPL03_F,
        "old_G": "CPMK0317", "new_G": "CPMK0302",
        "new_H": CPMK0302_H,
        "new_I": "SCPMK0302-04810",
        "new_J": "Mampu memimpin dan mengelola tim dalam proyek teknologi terintegrasi "
                 "yang kompleks dengan menggabungkan berbagai teknologi untuk "
                 "menyelesaikan permasalahan nyata serta mengelola konflik, mengambil "
                 "keputusan, dan memfasilitasi kolaborasi tim multidisiplin.",
    },
    167: {
        "D": CPL03_D, "E": CPL03_E, "F": CPL03_F,
        "old_G": "CPMK0318", "new_G": "CPMK0302",
        "new_H": CPMK0302_H,
        "new_I": "SCPMK0302-04811",
        "new_J": "Mampu mempresentasikan solusi teknologi terintegrasi kepada client "
                 "dan stakeholder serta mendokumentasikan dan mengomunikasikan proses "
                 "dan hasil proyek secara komprehensif.",
    },
    201: {
        "D": CPL03_D, "E": CPL03_E, "F": CPL03_F,
        "old_G": "CPMK0321", "new_G": "CPMK0301",
        "new_H": CPMK0301_SKRIPSI_H,
        "new_I": "SCPMK0301-05810",
        "new_J": "Mampu mengelola diri secara mandiri dalam merencanakan, "
                 "melaksanakan, dan menyelesaikan penelitian tugas akhir serta "
                 "berkomunikasi dan berkolaborasi secara profesional dengan dosen "
                 "pembimbing dan pihak terkait.",
    },
    202: {
        "D": CPL03_D, "E": CPL03_E, "F": CPL03_F,
        "old_G": "CPMK0322", "new_G": "CPMK0301",
        "new_H": CPMK0301_SKRIPSI_H,
        "new_I": "SCPMK0301-05811",
        "new_J": "Mampu mempresentasikan hasil penelitian dalam sidang dengan "
                 "argumentasi yang kuat dan sistematis serta merespons pertanyaan dan "
                 "kritik dalam forum ilmiah secara profesional dan argumentatif.",
    },
}


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def replace_cell_value(row_body, col, row_num, new_val):
    """Replace one cell's value in-place, preserving its existing style (s="...")
    attribute. The cell must already exist in row_body (every column D-J is present
    as an explicit, if empty, cell on these 4 rows - confirmed by inspecting the raw
    XML before writing this script)."""
    pattern = re.compile(
        rf'<c r="{col}{row_num}"((?:\s+\w+="[^"]*")*)\s*(?:/>|>.*?</c>)', re.S
    )
    m = pattern.search(row_body)
    assert m, f"row {row_num}: <c r=\"{col}{row_num}\"> cell not found"
    attrs = m.group(1)
    style_m = re.search(r'\s+s="(\d+)"', attrs)
    style_attr = f' s="{style_m.group(1)}"' if style_m else ""
    new_cell = (
        f'<c r="{col}{row_num}"{style_attr} t="inlineStr">'
        f'<is><t xml:space="preserve">{xml_escape(new_val)}</t></is></c>'
    )
    return row_body[: m.start()] + new_cell + row_body[m.end() :]


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    recoded = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            for row_num, spec in RECODES.items():
                assert spec["new_I"] not in text, f"{spec['new_I']} already present"

                row_match = re.compile(
                    rf'<row r="{row_num}">(.*?)</row>', re.S
                ).search(text)
                assert row_match, f"row {row_num} not found"
                row_body = row_match.group(1)

                # Confirm the row currently has the expected (old) CPMK code in G, and
                # an empty I cell (not a populated one - would mean this row isn't the
                # orphan we expect).
                g_match = re.search(rf'<c r="G{row_num}"[^>]*>(.*?)</c>', row_body, re.S)
                assert g_match, f"row {row_num}: G cell not found"
                g_text = re.search(r'<t[^>]*>(.*?)</t>', g_match.group(1), re.S)
                assert g_text and g_text.group(1) == spec["old_G"], (
                    f"row {row_num}: expected G={spec['old_G']!r}, "
                    f"found {g_text.group(1) if g_text else None!r}"
                )
                i_match = re.search(rf'<c r="I{row_num}"[^>]*>(.*?)</c>', row_body, re.S)
                assert i_match, f"row {row_num}: I cell not found"
                i_text = re.search(r'<t[^>]*/?>([^<]*)', i_match.group(1))
                existing_i = i_text.group(1) if i_text else ""
                assert existing_i == "", (
                    f"row {row_num}: I cell already has content {existing_i!r}, "
                    f"expected empty"
                )

                new_body = row_body
                for col in ("D", "E", "F", "G", "H", "I", "J"):
                    new_val = spec.get(f"new_{col}", spec.get(col))
                    new_body = replace_cell_value(new_body, col, row_num, new_val)

                text = text[: row_match.start(1)] + new_body + text[row_match.end(1) :]
                recoded += 1

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return recoded


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    recoded = apply_fix(args.xlsx_path)
    print(f"Re-coded {recoded} rows (expected {len(RECODES)}).")
    print(f"Saved to {args.xlsx_path}")
