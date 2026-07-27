"""Phase 2 of the 59-course-scheme alignment: format hygiene on the master CPL-CPMK
sheet (sheet14).

Fixes three defect families found by the 2026-07-11 three-level audit:

1. Annotated CPMK codes in col C that break exact-match lookups (these caused 22
   false-positive "orphan" reports earlier in the session):
     C56 "CPMK0901 - cara kerja sistem komputer" -> "CPMK0901"
     C57 "CPMK0902 - teknik komputasi"           -> "CPMK0902"
     C58 "CPMK0903 - komputasi"                  -> "CPMK0903"
     C60 "CPMK0905 - komputasi"                  -> "CPMK0905"
2. "Mahasiswa mampu ..." description stems in col D (house style: "Mampu ..."), same
   transformation as fix_subcpmk_metode_wording_mahasiswa.py:
     D50 (CPMK0707), D56-D60 (CPMK0901-0905)
3. CRLF (\r\n) separators in the col E Kode-MK lists, normalized to LF and stripped of
   trailing newlines: E12 (CPMK0209), E61 (CPMK1001), E65 (CPMK1005), E68 (CPMK1008).

All 14 target cells are shared-string references, each used exactly once in sheet14;
they are converted to inline strings with the corrected text (shared table untouched),
the same pattern as every prior fix. Texts are read from the shared-string table at
runtime and transformed programmatically, so no long strings are transcribed by hand.

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
SHEET = "xl/worksheets/sheet14.xml"


def strip_annotation(text):
    m = re.match(r'^(CPMK\d{4})\b', text)
    assert m and text != m.group(1), f"no annotation to strip in {text!r}"
    return m.group(1)


def strip_mahasiswa(text):
    m = re.match(r'^Mahasiswa (\w)(.*)$', text, re.S)
    assert m, f"no Mahasiswa stem in {text[:60]!r}"
    return m.group(1).upper() + m.group(2)


def normalize_crlf(text):
    assert '\r' in text, f"no CR in {text!r}"
    return text.replace('\r\n', '\n').replace('\r', '\n').rstrip('\n')


# (cell ref, shared-string index, transform)
TARGETS = [
    ("C56", 511, strip_annotation),
    ("C57", 518, strip_annotation),
    ("C58", 523, strip_annotation),
    ("C60", 534, strip_annotation),
    ("D50", 484, strip_mahasiswa),
    ("D56", 512, strip_mahasiswa),
    ("D57", 519, strip_mahasiswa),
    ("D58", 524, strip_mahasiswa),
    ("D59", 530, strip_mahasiswa),
    ("D60", 535, strip_mahasiswa),
    ("E12", 311, normalize_crlf),
    ("E61", 291, normalize_crlf),
    ("E65", 310, normalize_crlf),
    ("E68", 561, normalize_crlf),
]


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def apply_fix(xlsx_path: str):
    zin = zipfile.ZipFile(xlsx_path, "r")

    shared_raw = zin.read("xl/sharedStrings.xml").decode("utf-8")
    si_list = re.findall(r'<si>(.*?)</si>', shared_raw, re.S)

    def si_text(i):
        parts = re.findall(r'<t[^>]*>([^<]*)</t>', si_list[i], re.S)
        text = "".join(parts)
        return (text.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&#13;", "\r"))

    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    applied = 0
    audit = []
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            for ref, idx, transform in TARGETS:
                pattern = re.compile(rf'<c r="{ref}"([^>]*) t="s"><v>{idx}</v></c>')
                m = pattern.search(text)
                assert m, f"cell {ref} with shared index {idx} not found"
                old_val = si_text(idx)
                new_val = transform(old_val)
                attrs = m.group(1).strip()
                attrs_part = f" {attrs}" if attrs else ""
                new_cell = (
                    f'<c r="{ref}"{attrs_part} t="inlineStr">'
                    f'<is><t xml:space="preserve">{xml_escape(new_val)}</t></is></c>'
                )
                assert text.count(m.group(0)) == 1, f"{ref}: not exactly 1 occurrence"
                text = text.replace(m.group(0), new_cell, 1)
                applied += 1
                audit.append((ref, old_val, new_val))

            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {exc}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return applied, audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    applied, audit = apply_fix(args.xlsx_path)
    print(f"Applied {applied} cell fixes (expected {len(TARGETS)}).")
    print(f"Saved to {args.xlsx_path}")
    print("\nAudit (cell, old -> new):")
    for ref, old, new in audit:
        print(f"  {ref}: {old[:55]!r} -> {new[:55]!r}")
