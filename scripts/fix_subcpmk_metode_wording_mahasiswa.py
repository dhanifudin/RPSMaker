"""Remove "Mahasiswa" as the leading word of every Sub-CPMK statement.

Background
----------
docs/subcpmk-wording-review.md SS2A found the workbook's Sub-CPMK statements (column J of
the MK-CPMK-SubCPMK-Metode sheet) inconsistently start with either "Mahasiswa mampu ..."
or "Mampu ...". The house-style decision (confirmed with the curriculum owner) is to drop
"Mahasiswa" - no Sub-CPMK statement should start with it.

A pre-fix scan found 149 of the 198 filled Sub-CPMK text cells start with "Mahasiswa":
  - 147 as "Mahasiswa mampu <verb>..." -> becomes "Mampu <verb>..."
  - 2 as "Mahasiswa <other verb>..." (SCPMK0101-00802 "Mahasiswa mengetahui...",
    SCPMK0101-00803 "Mahasiswa mengerti..." - the already-flagged weak-verb rows) ->
    becomes "Mengetahui..."/"Mengerti...". This pass only removes the leading subject; the
    weak-verb problem itself stays flagged separately (SS2B of the review doc).

NOT touched: 4 separate MID-SENTENCE "Mahasiswa" occurrences (rows 24, 76, 162, 174) where
a second "Mahasiswa mampu..." clause appears after a period or bullet inside one cell
(bundled multi-part statements). These aren't leading prefixes; fixing them means
splitting/restructuring the statement, which is the separate bundled-multi-competency
cleanup already flagged in SS2C, not a simple prefix removal.

Applied uniformly to all 149 rows, including the 86 rows already flagged in SS1 as
auto-generated/truncated boilerplate needing a full rewrite later - removing the wrong
leading subject is correct and additive regardless of what else needs fixing in those
cells' content.

Why a generic regex substitution instead of a per-row dict
------------------------------------------------------------
Unlike the prior code-format fixes (each row needed an individually-computed, bespoke new
value), this is ONE uniform rule applied across many, sometimes-long text cells. Rather
than hand-transcribing 149 strings into an explicit dict (verbose, token-heavy, and risks
transcription typos corrupting content), this applies one regex substitution across the
sheet XML directly and prints a full (row, old, new) audit list as output so the change
stays traceable without bloating the script source.

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

# Matches a J-column inlineStr cell whose text starts with "Mahasiswa " followed by one of
# the three verbs seen in the pre-fix scan (mampu/mengetahui/mengerti). Captures:
#   1) the <c ...> attributes before t="inlineStr"
#   2) the rest of the text after "Mahasiswa " (starting with the verb, lowercase)
CELL_PATTERN = re.compile(
    r'<c r="(J\d+)"([^/]*?)t="inlineStr"><is><t xml:space="preserve">'
    r'Mahasiswa (mampu|mengetahui|mengerti)([^<]*)</t></is></c>'
)

EXPECTED_COUNT = 149


def fix_text(sheet_xml: str):
    audit = []

    def repl(m):
        ref, attrs, verb, rest = m.groups()
        new_text = verb[0].upper() + verb[1:] + rest
        audit.append((ref, f"Mahasiswa {verb}{rest}", new_text))
        return f'<c r="{ref}"{attrs}t="inlineStr"><is><t xml:space="preserve">{new_text}</t></is></c>'

    new_xml, count = CELL_PATTERN.subn(repl, sheet_xml)
    return new_xml, count, audit


def apply_fix(xlsx_path: str):
    tmp_path = xlsx_path + ".tmp"
    zin = zipfile.ZipFile(xlsx_path, "r")
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    audit = []
    count = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            new_text, count, audit = fix_text(text)
            assert count == EXPECTED_COUNT, (
                f"expected {EXPECTED_COUNT} substitutions, got {count}"
            )
            data = new_text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return count, audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    parser.add_argument("--quiet", action="store_true", help="suppress per-row audit output")
    args = parser.parse_args()

    applied, audit = apply_fix(args.xlsx_path)
    print(f"Applied {applied} substitutions (expected {EXPECTED_COUNT}).")
    print(f"Saved to {args.xlsx_path}")
    if not args.quiet:
        print("\nAudit (cell, old, new):")
        for ref, old, new in audit:
            print(f"  {ref}: {old[:60]!r} -> {new[:60]!r}")
