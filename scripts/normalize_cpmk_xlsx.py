"""Normalize remaining unpadded CPMK codes across all tabs of cpl-cpmk-subcpmk.xlsx.

Background
----------
The zero-padded CPL/CPMK/SubCPMK code convention (CPMK101 -> CPMK0101,
CPMK10.1 -> CPMK1001) was already propagated across every .tex/.md file
in the repo (see propagate_cpmk_padding.py, commit 1d08f2a), and the
MK-CPMK-SubCPMK-Metode sheet's own Kode CPMK/Kode SubCPMK columns were
fixed directly (commits 944d0f6, bcc0c28). But several *other* tabs in
this same workbook still held the old unpadded codes, because they were
never touched by those passes:

  - CPL-CPMK, (MK-CPMK)-BK-CPL, MK-CPMK-SubCPMK, and the
    "backup (MK-CPMK)-BK-CPL" snapshot store their codes as *shared
    strings* (xl/sharedStrings.xml) - a single edit there normalizes
    every one of these sheets at once, since they all reference the
    same string table entries.
  - MK-CPMK-SubCPMK-Metode (sheet16.xml) additionally has 80 inline
    "capaian CPMKxxx" references embedded in free-text SubCPMK
    description cells (column J), which are inline strings, not shared
    strings.
  - (MK-CPMK)-BK-CPL (sheet15.xml) has 2 inline-string cells
    (CPMK303/CPMK302) that were added by fix_cpl_cpmk_subcpmk_xlsx.py
    in commit 944d0f6 - themselves unpadded, since that fix predates
    the zero-padding convention introduced afterward.

This script applies the exact same transform used in
propagate_cpmk_padding.py to all three files, restricted to <t>...</t>
text runs (never touching XML structure/attributes/<v> numeric cells).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
An earlier attempt on this same workbook used
openpyxl.load_workbook(...).save(...) and silently dropped placeholder
drawing/persons.xml files plus reformatted unrelated numeric cells in
other sheets. This script instead rewrites only the exact <t> runs that
match the code patterns inside sharedStrings.xml / sheet15.xml /
sheet16.xml, leaving every other byte in the zip untouched. Verified by
a full-workbook byte-level diff showing only those 3 files changed.

Status: not yet applied as of writing. Running this script twice is a
safe no-op (the regexes require an exact match on the unpadded/dotted
forms, which no longer exist after the first run).
"""

import argparse
import os
import re
import shutil
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")

# Same transform as propagate_cpmk_padding.py.
PAT_UNPADDED_CPL01_09 = re.compile(r"CPMK([1-9])([0-9]{2})(?!\d)")
PAT_DOTTED_CPL10 = re.compile(r"CPMK10\.([0-9])(?!\d)")

# Restrict edits to text runs only, in each of these files.
TARGET_FILES = [
    "xl/sharedStrings.xml",
    "xl/worksheets/sheet15.xml",  # (MK-CPMK)-BK-CPL
    "xl/worksheets/sheet16.xml",  # MK-CPMK-SubCPMK-Metode
]

# Matches both <t>...</t> and <t xml:space="preserve">...</t> text runs,
# whether they're shared-string <si><t>...</t></si> entries or inline
# <is><t>...</t></is> cells - both use the same <t ...>...</t> element.
TEXT_RUN_PATTERN = re.compile(r"(<t\b[^>]*>)(.*?)(</t>)", re.DOTALL)


def transform(text: str) -> tuple[str, int]:
    count = 0

    def sub_unpadded(m: re.Match) -> str:
        nonlocal count
        count += 1
        return f"CPMK0{m.group(1)}{m.group(2)}"

    def sub_dotted(m: re.Match) -> str:
        nonlocal count
        count += 1
        return f"CPMK100{m.group(1)}"

    text = PAT_UNPADDED_CPL01_09.sub(sub_unpadded, text)
    text = PAT_DOTTED_CPL10.sub(sub_dotted, text)
    return text, count


def transform_text_runs(xml: str) -> tuple[str, int]:
    total = 0

    def repl(m: re.Match) -> str:
        nonlocal total
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        new_inner, count = transform(inner)
        total += count
        return f"{open_tag}{new_inner}{close_tag}"

    new_xml = TEXT_RUN_PATTERN.sub(repl, xml)
    return new_xml, total


def apply_fix(xlsx_path: str) -> dict:
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    counts = {}
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in TARGET_FILES:
            xml = data.decode("utf-8")
            new_xml, count = transform_text_runs(xml)
            counts[item.filename] = count
            data = new_xml.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    result = apply_fix(args.xlsx_path)
    total = sum(result.values())
    for filename, count in result.items():
        print(f"{filename}: {count} replacements")
    print(f"Total replacements: {total}")
    print(f"Saved to {args.xlsx_path}")
