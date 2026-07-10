"""Normalize the remaining non-conforming Kode SubCPMK codes in MK-CPMK-SubCPMK-Metode.

Background
----------
Prior passes (fix_subcpmk_metode_codes.py, fix_subcpmk_metode_codes_v2.py) fixed specific
duplicate-code collisions and orphan (missing-code) rows. This is a comprehensive follow-up:
a full-sheet scan found 54 more Kode SubCPMK values that don't conform to the documented
format (docs/rti-mk-crosswalk.md: `SCPMK<cpmk>-<MKnum3digit><seq2digit>`) - 10 of those 54
turned out to need no fix (see below), leaving 44 corrected here. Two categories:

1. Malformed length (14 rows) - doesn't match `SCPMK\\d{4}-\\d{3}\\d{2}` at all:
   - MK003 rows 6-7, MK029 rows 94-101: 3-digit serial instead of 2-digit (course-number
     segment was already correct in these).
   - MK051 rows 184-189: the 3-digit course-number segment is missing entirely.

2. Well-formed but wrong embedded course-number (30 rows) - the code embeds a DIFFERENT
   course's number than the row's own Kode MK column (confirmed against
   docs/rti-mk-crosswalk.md, which matches each row's own Kode MK/Nama MK columns in
   every case here): MK009 (embeds 006), MK014 (embeds 050 - and rows 45/46 currently
   collide byte-for-byte with MK050 Big Data's own real published codes), MK023 (embeds
   016), MK024 (embeds 035 - a bug that also exists in MK024's own published RPS, out of
   scope here), MK035 (embeds 001), MK036 (embeds 001), MK045 rows 157/158 (embeds 001 -
   see note below), MK047 (embeds 001).

NOT touched, by design:
- MK014 row 51 and MK023 row 78 already use the correct prefix and match the real
  published RPS exactly.
- MK053/MK054-LABELED rows (10 rows) need no code fix: their `Kode MK` column is stale
  (says MK053/MK054) but the rows are genuinely about Magang/Skripsi, and their codes
  already correctly embed 057/058 - the real numbers for those courses. Only the label
  is wrong, which is a separate, already-documented, cosmetic-only issue.
- The 10 already-flagged invalid-CPMK rows from the original fill_subcpmk_metode.py pass
  remain empty and untouched.

On MK045 rows 157/158 specifically: this fix corrects ONLY the course-number segment
(001 -> 045) to match the row's own actual course. It does not touch or validate the
CPMK0313/CPMK0314 reference itself - neither code exists in the master CPL-CPMK sheet,
so their legitimacy as Sub-CPMK parents remains a separate, open curriculum-owner
question (same class as the 10 already-flagged rows). Confirmed in-scope with the user
before applying.

Every corrected code below reprefixes to the row's own correct course number and assigns
a serial strictly greater than that course's actual highest-used serial (real published
max, or the highest serial among already-correct draft rows, whichever is greater) -
never reusing a real published serial, even where a row's CPMK might plausibly match a
specific published position, since content-alignment can't be assumed (see
docs/subcpmk-wording-review.md SS3a: a prior "plausible position match by serial number"
turned out, on reading the actual Sub-CPMK text, to be about an unrelated topic).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this directory: openpyxl
load_workbook(...).save(...) previously caused unrelated data loss elsewhere in this
exact workbook.
"""

import argparse
import os
import re
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"  # MK-CPMK-SubCPMK-Metode

# row -> (old code currently in the cell, corrected code)
CORRECTIONS = {
    # MK003 Critical Thinking dan Problem Solving - malformed 3-digit serial -> 2-digit,
    # continuing past the real published max (03).
    6: ("SCPMK0401-003001", "SCPMK0401-00304"),
    7: ("SCPMK0401-003002", "SCPMK0401-00305"),

    # MK009 Fisika - wrong embedded course-number (006 -> 009), continuing past real max (04).
    24: ("SCPMK0902-00601", "SCPMK0902-00905"),

    # MK014 Rekayasa Perangkat Lunak - wrong embedded course-number (050 -> 014), continuing
    # past real max (05) plus the already-correct row 51 (serial 01). Rows 45/46 currently
    # collide byte-for-byte with MK050 Big Data's real codes - this fix also resolves that.
    43: ("SCPMK0205-05001", "SCPMK0205-01406"),
    44: ("SCPMK0211-05001", "SCPMK0211-01407"),
    45: ("SCPMK0802-05001", "SCPMK0802-01408"),
    46: ("SCPMK0802-05002", "SCPMK0802-01409"),
    47: ("SCPMK0802-05003", "SCPMK0802-01410"),
    48: ("SCPMK0802-05004", "SCPMK0802-01411"),
    49: ("SCPMK0802-05005", "SCPMK0802-01412"),
    50: ("SCPMK0802-05006", "SCPMK0802-01413"),
    52: ("SCPMK0602-05001", "SCPMK0602-01414"),
    53: ("SCPMK0607-05001", "SCPMK0607-01415"),

    # MK023 Basis Data Lanjut - wrong embedded course-number (016 -> 023), continuing past
    # real max (04) plus the already-correct row 78 (serial 01).
    79: ("SCPMK0701-01603", "SCPMK0701-02305"),
    80: ("SCPMK1001-01604", "SCPMK1001-02306"),

    # MK024 Metode Numerik - wrong embedded course-number (035 -> 024). No genuine code has
    # ever correctly used 024 (the published RPS itself has this same bug), so the space is
    # virgin - start fresh at 01.
    81: ("SCPMK0902-03503", "SCPMK0902-02401"),
    82: ("SCPMK1007-03504", "SCPMK1007-02402"),

    # MK029 Analisis Dan Desain Berorientasi Objek - malformed 3-digit serial -> 2-digit,
    # continuing past the real published max (03).
    94: ("SCPMK0208-029001", "SCPMK0208-02904"),
    95: ("SCPMK0208-029002", "SCPMK0208-02905"),
    96: ("SCPMK0211-029001", "SCPMK0211-02906"),
    97: ("SCPMK0602-029001", "SCPMK0602-02907"),
    100: ("SCPMK0607-029001", "SCPMK0607-02908"),
    101: ("SCPMK0609-029001", "SCPMK0609-02909"),

    # MK035 Statistik Komputasi - wrong embedded course-number (001 -> 035). Continuing
    # past real max (02) alone gives 03, but MK024 Metode Numerik's OWN published RPS has
    # a pre-existing bug that reuses the "035" prefix (see the MK024 note above) - its real
    # published codes occupy 03501-03504 too. To avoid colliding with that published text,
    # this must skip past MK024's real max in this prefix space (04) as well, landing on 05.
    114: ("SCPMK0902-00101", "SCPMK0902-03505"),

    # MK036 Proyek Sistem Informasi - wrong embedded course-number (001 -> 036), continuing
    # past real max (04).
    116: ("SCPMK0301-00101", "SCPMK0301-03605"),
    117: ("SCPMK0301-00102", "SCPMK0301-03606"),
    119: ("SCPMK0602-00101", "SCPMK0602-03607"),
    120: ("SCPMK0602-00102", "SCPMK0602-03608"),
    121: ("SCPMK0802-00101", "SCPMK0802-03609"),
    122: ("SCPMK0802-00102", "SCPMK0802-03610"),
    123: ("SCPMK0803-00101", "SCPMK0803-03611"),
    124: ("SCPMK0803-00102", "SCPMK0803-03612"),
    125: ("SCPMK1008-00101", "SCPMK1008-03613"),
    126: ("SCPMK1008-00102", "SCPMK1008-03614"),
    127: ("SCPMK0607-00101", "SCPMK0607-03615"),

    # MK045 Komunikasi Dan Etika Profesi, rows 157/158 - wrong embedded course-number
    # (001 -> 045), continuing past the current max (04504, set by fix_subcpmk_metode_codes_v2.py).
    # CPMK0313/CPMK0314 validity itself is untouched - see module docstring.
    157: ("SCPMK0313-00101", "SCPMK0313-04505"),
    158: ("SCPMK0314-00101", "SCPMK0314-04506"),

    # MK047 Pemrograman Berbasis Framework - wrong embedded course-number (001 -> 047),
    # continuing past real max (03).
    162: ("SCPMK0603-00104", "SCPMK0603-04704"),

    # MK051 Cloud Computing - course-number segment missing entirely, continuing past real
    # max (03).
    184: ("SCPMK0905-01", "SCPMK0905-05104"),
    185: ("SCPMK0502-01", "SCPMK0502-05105"),
    186: ("SCPMK0502-02", "SCPMK0502-05106"),
    187: ("SCPMK0502-03", "SCPMK0502-05107"),
    188: ("SCPMK0509-01", "SCPMK0509-05108"),
    189: ("SCPMK0509-02", "SCPMK0509-05109"),
}


def apply_fix(xlsx_path: str) -> int:
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    applied = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            for row, (old_code, new_code) in CORRECTIONS.items():
                ref = f"I{row}"
                pattern = re.compile(
                    rf'<c r="{ref}"([^/]*?)t="inlineStr"><is><t xml:space="preserve">{re.escape(old_code)}</t></is></c>'
                )
                m = pattern.search(text)
                assert m, f"could not find {ref} still containing {old_code}"
                attrs = m.group(1)
                old_full = m.group(0)
                new_full = f'<c r="{ref}"{attrs}t="inlineStr"><is><t xml:space="preserve">{new_code}</t></is></c>'
                count = text.count(old_full)
                assert count == 1, f"{ref}: expected exactly 1 occurrence, found {count}"
                text = text.replace(old_full, new_full, 1)
                applied += 1
            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return applied


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    applied = apply_fix(args.xlsx_path)
    print(f"Applied {applied} corrections (expected {len(CORRECTIONS)}).")
    print(f"Saved to {args.xlsx_path}")
