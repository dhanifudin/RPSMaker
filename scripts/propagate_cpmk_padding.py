"""Propagate the zero-padded CPL/CPMK/SubCPMK code convention across the whole repo.

Background
----------
`docs/cpl-cpmk-subcpmk.xlsx` (see fix_cpl_cpmk_subcpmk_xlsx.py) was
corrected to use a consistent, collision-proof code format:

    CPMK101   -> CPMK0101   (CPL01..09: pad the CPL number to 2 digits)
    CPMK905   -> CPMK0905
    CPMK10.1  -> CPMK1001   (CPL10: drop the dot, pad the sequence to 2 digits)
    CPMK10.9  -> CPMK1009

Already-correct dotless CPL10 codes (CPMK1001, CPMK1005, CPMK1007,
independently adopted by a handful of courses before this fix) are left
untouched by construction: the regexes below require an exact match on
the *old* (unpadded / dotted) forms, which these values don't have.

Same transform applies to the CPMK-code portion embedded inside every
`SCPMK<code>-<serial>` reference (e.g. SCPMK102-05902 -> SCPMK0102-05902),
since that's just a substring of the surrounding text, not a separate
pattern.

This script rewrites every reference to these codes across:
  - book/src/chapters/04-cpl.tex          (the master CPL/CPMK table)
  - subjects/*/*.tex RPS and Rubrik files (all 59 courses)
  - subjects/*/meetings/*.md and rubrics/*.md working notes

Both regexes were unit-tested for idempotency (running twice is a
no-op) and for not misfiring on the 4-digit CPL10 forms before this was
run for real - see the session history for the test cases used.

Status: already applied (commit 1d08f2a; 1357 files, 5751
replacements). Running it again is a safe no-op - matching content has
already been rewritten, so the regexes simply find nothing left to
change in files that were already processed. Kept here as the
reference implementation for the code-padding convention itself, and
in case new course files are added later using the old unpadded style.
"""

import argparse
import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CPL01-09: bare 3-char codes (1-digit CPL + 2-digit sequence) -> 4-char padded.
# (?!\d) ensures this never matches inside a 4-digit CPL10 code like CPMK1001.
PAT_UNPADDED_CPL01_09 = re.compile(r"CPMK([1-9])([0-9]{2})(?!\d)")

# CPL10: dotted form (CPMK10.1 .. CPMK10.9) -> dotless padded form.
PAT_DOTTED_CPL10 = re.compile(r"CPMK10\.([0-9])(?!\d)")


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


def target_files(repo_root: str) -> list[str]:
    files = [os.path.join(repo_root, "book", "src", "chapters", "04-cpl.tex")]
    files += glob.glob(os.path.join(repo_root, "subjects", "*", "* - RPS.tex"))
    files += glob.glob(os.path.join(repo_root, "subjects", "*", "* - Rubrik.tex"))
    files += glob.glob(os.path.join(repo_root, "subjects", "*", "meetings", "*.md"))
    files += glob.glob(os.path.join(repo_root, "subjects", "*", "rubrics", "*.md"))
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT)
    args = parser.parse_args()

    targets = target_files(args.repo_root)
    print(f"Total candidate files: {len(targets)}")

    files_changed = 0
    total_replacements = 0
    for path in targets:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content, count = transform(content)
        if count > 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            files_changed += 1
            total_replacements += count

    print(f"Files changed: {files_changed}")
    print(f"Total replacements: {total_replacements}")
