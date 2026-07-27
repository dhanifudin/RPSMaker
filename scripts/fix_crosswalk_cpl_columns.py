"""Fix 28 wrong CPL columns in docs/rti-mk-crosswalk.md.

Background
----------
A fresh CPL/CPMK/Sub-CPMK consistency audit (2026-07-11, second pass) found that
docs/rti-mk-crosswalk.md's CPL column disagreed with docs/kurikulum-2025-cpl-cpmk.md
(the curriculum's CPMK-level "MK kunci" mapping, sourced from the master planning
spreadsheet) on 44% of courses (MK001-052 range), and only agreed with the xlsx's
actually-authored Sub-CPMK content on 43% of courses - compared to 76% agreement between
kurikulum-2025-cpl-cpmk.md and the xlsx. crosswalk.md's CPL column was built from a
narrower "CPMK utama" (primary CPMK only) column, which explains most of the gap.

Per curriculum-owner direction, kurikulum-2025-cpl-cpmk.md is now the canonical source for
CPL membership (MK001-052). For MK053-059 (postdating that doc, added by the earlier
MK053-059 renumbering this session), the canonical value is the union of the xlsx's actual
Sub-CPMK CPMK codes and crosswalk.md's own "CPMK utama" column, both mapped through the
CPMK-code-prefix rule (a CPMK's first digits ARE its parent CPL number - verified with 0
exceptions across all 61 CPMK codes in kurikulum-2025-cpl-cpmk.md).

This matters because docs/rti-mk-crosswalk.md is the direct data source for
scripts/generate_peta_jalan_cpl.py (Chapter 5's "Peta Jalan CPL" diagrams) - fixing this
table is a prerequisite for regenerating that chapter correctly.

Why a Python script instead of hand-editing the markdown table
------------------------------------------------------------------
28 rows, each needing an exact-match old-line -> new-line replacement - same
exact-match-assertion safety pattern as every other fix this session, applied to a
markdown table instead of xlsx XML.
"""

import argparse
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "rti-mk-crosswalk.md")

# (old CPL column text, new CPL column text) - unique substrings within each row line
REPLACEMENTS = [
    ("MK002 | CPL09 |", "MK002 | CPL02, CPL09 |"),
    ("MK006 | CPL09 |", "MK006 | CPL07, CPL09 |"),
    ("MK007 | CPL09 |", "MK007 | CPL07, CPL09 |"),
    ("MK013 | CPL09, CPL05 |", "MK013 | CPL02, CPL05, CPL09 |"),
    ("MK014 | CPL02, CPL06 |", "MK014 | CPL02, CPL06, CPL08 |"),
    ("MK016 | CPL02, CPL07 |", "MK016 | CPL02, CPL07, CPL10 |"),
    ("MK017 | CPL09, CPL07 |", "MK017 | CPL02, CPL09 |"),
    ("MK019 | CPL08, CPL03 |", "MK019 | CPL03, CPL04, CPL08 |"),
    ("**MK020** | **CPL02, CPL06, CPL08** |", "**MK020** | **CPL02, CPL10** |"),
    ("MK022 | CPL02, CPL06 |", "MK022 | CPL02, CPL06, CPL07 |"),
    ("**MK025** | **CPL02, CPL07, CPL09** |", "**MK025** | **CPL02, CPL06, CPL07** |"),
    ("**MK026** | **CPL02, CPL07, CPL09** |", "**MK026** | **CPL02, CPL06, CPL07** |"),
    ("**MK027** | **CPL01, CPL03** |", "**MK027** | **CPL03** |"),
    ("**MK030** | **CPL03, CPL04** |", "**MK030** | **CPL03** |"),
    ("**MK031** | **CPL07, CPL09, CPL10** |", "**MK031** | **CPL07, CPL10** |"),
    ("**MK032** | **CPL05, CPL09, CPL10** |", "**MK032** | **CPL05, CPL09** |"),
    ("**MK035** | **CPL07, CPL09, CPL10** |", "**MK035** | **CPL07, CPL09** |"),
    ("**MK036** | **CPL02, CPL06, CPL08** |", "**MK036** | **CPL03, CPL06, CPL08, CPL10** |"),
    ("MK037 | CPL01, CPL08 |", "MK037 | CPL01, CPL03 |"),
    ("**MK038** | **CPL04, CPL03** |", "**MK038** | **CPL04, CPL10** |"),
    ("MK042 | CPL06 |", "MK042 | CPL05, CPL06, CPL08 |"),
    ("MK047 | CPL02, CPL06, CPL10 |", "MK047 | CPL02, CPL06 |"),
    ("**MK048** | **CPL02, CPL06, CPL08, CPL10** |", "**MK048** | **CPL02, CPL03, CPL06, CPL08** |"),
    ("**MK053** | **CPL08, CPL02, CPL06** |", "**MK053** | **CPL06, CPL08** |"),
    ("**MK054** | **CPL02, CPL06, CPL08** |", "**MK054** | **CPL06, CPL08** |"),
    ("**MK055** | **CPL02, CPL06, CPL10** |", "**MK055** | **CPL02, CPL06** |"),
    ("**MK057** | **CPL03, CPL06, CPL08** |", "**MK057** | **CPL01, CPL03, CPL06, CPL08** |"),
    ("**MK058** | **CPL04, CPL06, CPL08, CPL10** |",
     "**MK058** | **CPL01, CPL02, CPL03, CPL04, CPL06, CPL08, CPL10** |"),
]


def apply_fix(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        text = f.read()

    applied = 0
    for old, new in REPLACEMENTS:
        assert text.count(old) == 1, f"not found or not unique: {old!r}"
        text = text.replace(old, new, 1)
        applied += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return applied


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    applied = apply_fix(args.path)
    print(f"Applied {applied} CPL-column fixes (expected {len(REPLACEMENTS)}).")
    print(f"Saved to {args.path}")
