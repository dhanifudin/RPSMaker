"""Fill empty Kode SubCPMK cells in the MK-CPMK-SubCPMK-Metode sheet.

Background
----------
85 rows in this sheet had a Kode CPMK (col G) and a SubCPMK description
(col J) but an EMPTY Kode SubCPMK (col I). Each row was correlated
against its own course's already-published `subjects/*/* - RPS.tex`
file (the authoritative source) by matching the row's Kode CPMK number
against that course's published SCPMK<cpmk>-<serial> codes:

  - 41 rows had exactly one published code sharing that CPMK number ->
    filled deterministically.
  - 8 rows had multiple published codes sharing that CPMK number ->
    disambiguated by picking whichever published SubCPMK description
    is textually most similar to the row's own col-J description.
  - 36 rows had a Kode CPMK that does not appear AT ALL in that course's
    published RPS (draft CPMK design that was revised before
    publishing) - these were deliberately left empty; no reliable code
    could be derived from either code-matching or description
    similarity. See FLAGGED_ROWS below.

Only the Kode SubCPMK column is touched here - the Kode CPMK column's
divergence for the 36 flagged rows is a separate, not-yet-addressed
concern.

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as the other normalize/fix scripts in this directory:
openpyxl.load_workbook(...).save(...) previously caused unrelated data
loss elsewhere in this exact workbook. This script instead edits only
the 49 specific <c r="I{row}"> inline-string cells (each currently an
empty `<is><t xml:space="preserve" /></is>`), leaving every other byte
in the zip untouched.

Status: not yet applied as of writing. Re-running this script after it
succeeds once will fail its own assertions (the empty placeholder cells
will already contain the filled values) - that's intentional, it
prevents accidental double-application.
"""

import argparse
import os
import re
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"  # MK-CPMK-SubCPMK-Metode

# row -> Kode SubCPMK to fill in column I
FILLS = {
    38: "SCPMK0206-01302",
    39: "SCPMK0901-01301",
    40: "SCPMK0502-01303",
    41: "SCPMK0502-01303",
    42: "SCPMK0502-01303",
    51: "SCPMK0802-01401",
    68: "SCPMK0302-01903",
    70: "SCPMK0402-01904",
    71: "SCPMK0801-01901",
    72: "SCPMK0803-01902",
    75: "SCPMK0102-02104",
    76: "SCPMK0603-02203",
    77: "SCPMK0704-02201",
    81: "SCPMK0902-03503",
    82: "SCPMK1007-03504",
    84: "SCPMK0704-02502",
    88: "SCPMK0704-02602",
    108: "SCPMK0901-03202",
    109: "SCPMK0504-03201",
    110: "SCPMK0901-03303",
    111: "SCPMK0504-03302",
    112: "SCPMK1006-03403",
    113: "SCPMK0603-03402",
    115: "SCPMK0707-03501",
    128: "SCPMK0101-03701",
    134: "SCPMK1006-03903",
    135: "SCPMK0603-03902",
    136: "SCPMK0706-04001",
    137: "SCPMK1005-04002",
    138: "SCPMK0705-04101",
    139: "SCPMK1004-04103",
    142: "SCPMK0608-04203",
    149: "SCPMK0501-04401",
    150: "SCPMK0502-04401",
    152: "SCPMK0505-04401",
    169: "SCPMK0801-04801",
    170: "SCPMK0802-04802",
    171: "SCPMK0803-04803",
    172: "SCPMK0804-04804",
    173: "SCPMK0607-04805",
    174: "SCPMK0204-04901",
    176: "SCPMK0503-04902",
    191: "SCPMK0101-05201",
    192: "SCPMK0509-05202",
    196: "SCPMK0607-05704",
    197: "SCPMK0804-05703",
    200: "SCPMK0404-05802",
    203: "SCPMK0804-05804",
    205: "SCPMK1009-05805",
}

# Rows deliberately left empty: Kode CPMK not found in the course's
# published RPS at all. Kept here for documentation / future follow-up.
FLAGGED_ROWS = [
    67, 73, 74, 83, 85, 86, 87, 89, 102, 103, 129, 130, 131, 140, 141,
    143, 144, 151, 153, 154, 163, 164, 165, 166, 167, 168, 175, 193,
    194, 195, 198, 199, 201, 202, 204, 206,
]


def apply_fix(xlsx_path: str) -> int:
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    applied = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            for row, code in FILLS.items():
                ref = f"I{row}"
                pattern = re.compile(
                    rf'<c r="{ref}"([^/]*?)t="inlineStr"><is><t xml:space="preserve" /></is></c>'
                )
                m = pattern.search(text)
                assert m, f"could not find empty placeholder cell {ref}"
                attrs = m.group(1)
                old_full = m.group(0)
                new_full = f'<c r="{ref}"{attrs}t="inlineStr"><is><t xml:space="preserve">{code}</t></is></c>'
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
    print(f"Applied {applied} surgical replacements (expected {len(FILLS)}).")
    print(f"Saved to {args.xlsx_path}")
