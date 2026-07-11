"""Fix 14 garbled "Materi Pembelajaran" (column O) values in cpl-cpmk-subcpmk.xlsx.

Background
----------
Follow-up to a "learning material to support Sub-CPMK" analysis (2026-07-11). Of 218
Sub-CPMK rows in the Metode sheet, 14 (6.4%) had a degenerate column-O value against a
healthy median of ~114 characters: 12 are literally "1" (an enumerate-list rendering
artifact - the same defect class as the isolated `O="1"` glitch fixed incidentally on one
row during the earlier CPL03 cluster work), and 2 are single-word fragments ("Kanban",
"Evolusi PL").

Sourcing, in priority order (same "restore from real source" pattern as every other fix this
session):
  1. 8 rows have a direct per-meeting file (subjects/*/meetings/*.md, tagged with the exact
     sub_cpmk code in frontmatter) - aggregated from each meeting's own "## Materi
     Pembelajaran" section.
  2. 4 rows have no meeting file or RPS occurrence anywhere in the repo, but do have a
     "Materi Pembelajaran Lama" (column Q, legacy content) that's still coherent and
     on-topic - used, scoped to what the row's own SubCPMK statement (column J) covers
     (e.g. row94 narrowed to just the 2 Q items J's "class diagram" wording actually
     references, not the whole 12-item legacy list).
  3. 2 rows (MK014 Rekayasa Perangkat Lunak, rows 48/50) have no meeting file, RPS
     occurrence, or legacy Q content at all - their terse current values are legitimate
     minimal labels, expanded into fuller phrases derived from their own J text.

A separate, pre-existing defect was found and deliberately NOT touched here: row 140's
column J (SubCPMK statement) is about "konsep dasar algoritma" - unrelated content that
doesn't belong to Penjaminan Mutu Perangkat Lunak. It's already present in that row's legacy
column P too, so it predates this session. Flagged for a future look, out of scope for this
column-O-only pass.

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

# row -> (expected current O value, expected Kode SubCPMK, new O value)
FIXES = {
    2: (
        "1", "SCPMK0102-00101",
        "Definisi Pancasila secara historis, kultural, yuridis, dan filosofis; Pancasila "
        "dalam konteks sejarah perjuangan bangsa Indonesia; prinsip-prinsip Pancasila; "
        "Pancasila sebagai sistem filsafat, unsur filsafat, hierarki nilai, dan "
        "penerapannya sehari-hari",
    ),
    11: (
        "1", "SCPMK0303-00501",
        "Computer Applications: kinds of computer applications and their uses; Computer "
        "Architecture: types of computers and hardware functions; Multimedia: hardware "
        "and graphic program toolbox; Computer Network: network hardware and topology; "
        "Websites: features, functions, and types; Careers in IT: jobs and "
        "responsibilities; IT Support Staff: computer problems, solutions, and service "
        "reports; Workstation Health and Safety: work health and safety problems and "
        "advice",
    ),
    38: (
        "1", "SCPMK0206-01302",
        "Perangkat keras dan perintah dasar; dasar input/output; manajemen proses; bash "
        "shell; bash programming; manajemen memori dan system call",
    ),
    48: (
        "Kanban", "SCPMK0802-01411",
        "Manajemen alur kerja visual (Visual Management) dalam tim menggunakan papan "
        "Kanban: kolom status, WIP limit, dan visualisasi progres pekerjaan",
    ),
    50: (
        "Evolusi PL", "SCPMK0802-01413",
        "Evolusi perangkat lunak pasca-rilis: jenis pemeliharaan (corrective, adaptive, "
        "perfective, preventive) dan pengelolaan siklus hidup sistem",
    ),
    67: (
        "1", "SCPMK0903-01905",
        "Konsep proyek dan manajemen proyek; fase dalam manajemen proyek; 10 Knowledge "
        "Area manajemen proyek (integrasi, ruang lingkup, waktu, biaya, kualitas, SDM, "
        "komunikasi, risiko, pengadaan, dan pemangku kepentingan)",
    ),
    75: (
        "1", "SCPMK0102-02104",
        "Wawasan Nusantara: wilayah sebagai ruang hidup dan konsep geopolitik Indonesia; "
        "unsur-unsur dasar wawasan nusantara, penerapan, dan tantangan implementasinya; "
        "Ketahanan Nasional: pengertian, sejarah, unsur-unsur, dan pendekatan asta gatra; "
        "globalisasi dan ketahanan nasional; Integrasi Nasional: pluralitas masyarakat "
        "Indonesia, dinamika, dan strategi integrasi",
    ),
    76: (
        "1", "SCPMK0603-02203",
        "Koneksi PHP-MySQL dan CRUD; autentikasi dasar dan validasi; database dan PHP; "
        "aplikasi web dinamis",
    ),
    87: (
        "1", "SCPMK0211-02604",
        "Konsep Pemrograman Berorientasi Objek; Class dan Object; Enkapsulasi; "
        "Inheritance; Polimorfisme; Abstract Class dan Interface; Java API; pengenalan "
        "GUI dan database (JDBC)",
    ),
    94: (
        "1", "SCPMK0208-02904",
        "Class diagram: pengenalan class dan struktur logis sistem; advanced class "
        "diagram sebagai blueprint desain berorientasi objek yang modular, maintainable, "
        "dan scalable",
    ),
    112: (
        "1", "SCPMK1006-03403",
        "Testing dan debugging; kuis/review kualitas Laravel; review kode dan "
        "refactoring; deployment preparation; validasi proyek Laravel (UAS)",
    ),
    136: (
        "1", "SCPMK0706-04001",
        "Pengantar ML: paradigma, pipeline, dan ekosistem Python; EDA dan preprocessing; "
        "linear/logistic regression; decision tree dan random forest; SVM dan k-NN; "
        "unsupervised learning (k-Means, DBSCAN); dimensionality reduction (PCA); "
        "ensemble methods (Gradient Boosting, XGBoost); pengantar deep learning (ANN, "
        "backpropagation); PBL end-to-end ML project",
    ),
    138: (
        "1", "SCPMK0705-04101",
        "Pengantar BI: konsep, arsitektur, dan ekosistem; data warehouse (skema bintang "
        "dan dimensi-fakta); ETL (Extract, Transform, Load); OLAP (slice, dice, "
        "drill-down, roll-up); self-service BI dan data governance",
    ),
    140: (
        "1", "SCPMK0508-04205",
        "Pengantar Penjaminan Perangkat Lunak dan ISO; pendekatan, tipe, dan level "
        "pengujian; test planning, test scenario, dan test case; test monitoring, test "
        "control, dan test completion; functional testing; non-functional testing",
    ),
}


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    fixed = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            for row_num, (expected_old_o, expected_i, new_o) in FIXES.items():
                row_match = re.compile(
                    rf'<row r="{row_num}"[^>]*>(.*?)</row>', re.S
                ).search(text)
                assert row_match, f"row {row_num} not found"
                row_body = row_match.group(1)

                i_match = re.search(rf'<c r="I{row_num}"[^>]*>(.*?)</c>', row_body, re.S)
                assert i_match, f"row {row_num}: I cell not found"
                i_text = re.search(r'<t[^>]*>(.*?)</t>', i_match.group(1), re.S)
                found_i = i_text.group(1) if i_text else ""
                assert found_i == expected_i, (
                    f"row {row_num}: expected I={expected_i!r}, found {found_i!r} - "
                    f"refusing to edit"
                )

                o_pattern = re.compile(
                    rf'<c r="O{row_num}"((?:\s+\w+="[^"]*")*)\s*(?:/>|>.*?</c>)', re.S
                )
                o_match = o_pattern.search(row_body)
                assert o_match, f"row {row_num}: O cell not found"
                attrs = o_match.group(1)
                style_m = re.search(r'\s+s="(\d+)"', attrs)
                style_attr = f' s="{style_m.group(1)}"' if style_m else ""

                # Verify the O cell's current text matches what we expect before touching it.
                current_text_m = re.search(r'<t[^>]*>(.*?)</t>', o_match.group(0), re.S)
                current_o = current_text_m.group(1) if current_text_m else ""
                assert current_o == expected_old_o, (
                    f"row {row_num}: expected current O={expected_old_o!r}, "
                    f"found {current_o!r} - refusing to edit"
                )

                new_cell = (
                    f'<c r="O{row_num}"{style_attr} t="inlineStr">'
                    f'<is><t xml:space="preserve">{xml_escape(new_o)}</t></is></c>'
                )
                row_body = (
                    row_body[: o_match.start()] + new_cell + row_body[o_match.end() :]
                )
                text = text[: row_match.start(1)] + row_body + text[row_match.end(1) :]
                fixed += 1

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return fixed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    fixed = apply_fix(args.xlsx_path)
    print(f"Fixed {fixed} cells (expected {len(FIXES)}).")
    print(f"Saved to {args.xlsx_path}")
