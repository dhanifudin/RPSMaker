"""Phase 3 of the 59-course-scheme alignment: modernize the internal registry sheets
to the published 59-course scheme.

Touches three sheets:

1. `BK-MK (Rev)` (sheet3) - the course registry / BK matrix:
   - Relabels the tail: row 55 Magang MK053->MK057 (A 53->57), row 56 Skripsi
     MK054->MK058 (A 54->58), row 57 BIPK MK055->MK059 (A 55->59).
   - Deletes 4 empty style-only rows (59-62), moves the COUNTA totals row from 58 to
     62 (extending its shared-formula range E3:E57 -> E3:E61 and updating the cached
     values), and writes 4 new course rows 58-61: MK053 Proyek Inovasi, MK054 Workshop
     Teknologi Terapan, MK055 Rekayasa Sistem, MK056 Teknologi Terapan (semester 6,
     BK checkmarks derived from their CPMKs' BK per the master CPL-CPMK sheet).

2. Master `CPL-CPMK` (sheet14) - col E/F course lists per CPMK:
   - Renames every MK053->MK057, MK054->MK058, MK055->MK059 token in col E (10 cells:
     CPMK0101, 0102, 0211, 0301, 0303, 0404, 0607, 0804, 1008, 1009). Course names in
     col F are unchanged by renames (same courses, new codes).
   - Appends the second-track courses to the CPMK rows the Metode sheet assigns them
     (E code + parallel F name): Proyek Inovasi -> 0801, 0607; Workshop Teknologi
     Terapan -> 0603, 0802; Rekayasa Sistem -> 0211, 0602, 0609; Teknologi Terapan ->
     0204, 0503.
   - Repairs a pre-existing E/F parity defect on the CPMK0303 row (F19): the E list
     had 8 course codes but the F name list only 7 - "Bahasa Inggris Persiapan Kerja"
     was never added to the names. Appended.

3. `(MK-CPMK)-BK-CPL` (sheet15) - block header cells: A164 MK053->MK057 (Magang),
   A169 MK054->MK058 (Skripsi), A178 MK055->MK059 (BIPK).

Shared-string cells are converted to inline strings (shared table untouched); each
shared index touched is referenced exactly once in its sheet (verified during audit).

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

RENAMES = {"MK053": "MK057", "MK054": "MK058", "MK055": "MK059"}

# CPMK -> (new MK code, course name) additions for sheet14 E/F lists
ADDITIONS = {
    "CPMK0801": ("MK053", "Proyek Inovasi"),
    "CPMK0607": ("MK053", "Proyek Inovasi"),
    "CPMK0603": ("MK054", "Workshop Teknologi Terapan"),
    "CPMK0802": ("MK054", "Workshop Teknologi Terapan"),
    "CPMK0211": ("MK055", "Rekayasa Sistem"),
    "CPMK0602": ("MK055", "Rekayasa Sistem"),
    "CPMK0609": ("MK055", "Rekayasa Sistem"),
    "CPMK0204": ("MK056", "Teknologi Terapan"),
    "CPMK0503": ("MK056", "Teknologi Terapan"),
}
EXPECTED_RENAMED_E_CELLS = 10

# sheet3 new course rows (written at rows 58-61): (A, code, name, semester, mark cols, AJ)
# Mark columns derived from master BK per CPMK:
#  PI: CPMK0801 (BK03->G, BK26->AD) + CPMK0607 (BK26->AD)          -> G, AD
#  WTT: CPMK0603 (BK19->W) + CPMK0802 (BK10->N, BK22->Z, BK24->AB, BK25->AC, BK28->AF, BK29->AG)
#  RS: CPMK0211 (BK26->AD) + CPMK0602 (BK10->N) + CPMK0609 (BK29->AG)
#  TT: CPMK0204/0503 (BK07->K)
SHEET3_NEW_ROWS = [
    ("53.0", "MK053", "Proyek Inovasi", "6.0", ["G", "AD"], 2),
    ("54.0", "MK054", "Workshop Teknologi Terapan", "6.0", ["N", "W", "Z", "AB", "AC", "AF", "AG"], 7),
    ("55.0", "MK055", "Rekayasa Sistem", "6.0", ["N", "AD", "AG"], 3),
    ("56.0", "MK056", "Teknologi Terapan", "6.0", ["K"], 1),
]
SHEET3_MARK_COLS = ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                    "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE",
                    "AF", "AG", "AH", "AI"]
# totals cached-value bumps per column (from the 13 new marks above)
SHEET3_TOTAL_BUMPS = {"G": 1, "K": 1, "N": 2, "W": 1, "Z": 1, "AB": 1, "AC": 1,
                      "AD": 2, "AF": 1, "AG": 2}


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def xml_unescape(value):
    return (value.replace("&amp;", "&").replace("&lt;", "<")
                 .replace("&gt;", ">").replace("&#13;", "\r"))


def rename_tokens(text):
    return re.sub(r'\bMK05[345]\b', lambda m: RENAMES[m.group(0)], text)


def fix_sheet3(text):
    # 1. relabel rows 55-57
    swaps = [
        ('<c r="A55" s="29"><v>53.0</v></c>', '<c r="A55" s="29"><v>57.0</v></c>'),
        ('<c r="B55" s="30" t="s"><v>226</v></c>',
         '<c r="B55" s="30" t="inlineStr"><is><t xml:space="preserve">MK057</t></is></c>'),
        ('<c r="A56" s="29"><v>54.0</v></c>', '<c r="A56" s="29"><v>58.0</v></c>'),
        ('<c r="B56" s="30" t="s"><v>228</v></c>',
         '<c r="B56" s="30" t="inlineStr"><is><t xml:space="preserve">MK058</t></is></c>'),
        ('<c r="A57" s="29"><v>55.0</v></c>', '<c r="A57" s="29"><v>59.0</v></c>'),
        ('<c r="B57" s="30" t="s"><v>230</v></c>',
         '<c r="B57" s="30" t="inlineStr"><is><t xml:space="preserve">MK059</t></is></c>'),
    ]
    for old, new in swaps:
        assert text.count(old) == 1, f"sheet3: not found or not unique: {old[:60]!r}"
        text = text.replace(old, new, 1)

    # 2. delete empty style-only rows 59-62
    for r in (59, 60, 61, 62):
        m = re.search(rf'<row r="{r}"[^>]*>.*?</row>', text, re.S)
        assert m, f"sheet3: row {r} not found"
        row_xml = m.group(0)
        assert "<v>" not in row_xml and "<is>" not in row_xml and "<f" not in row_xml, (
            f"sheet3: row {r} is not empty, refusing to delete"
        )
        assert text.count(row_xml) >= 1
        text = text.replace(row_xml, "", 1)

    # 3. move totals row 58 -> 62, extend COUNTA range, bump cached values
    m = re.search(r'<row r="58"[^>]*>.*?</row>', text, re.S)
    assert m, "sheet3: totals row 58 not found"
    old_totals = m.group(0)
    assert 'COUNTA(E3:E57)' in old_totals, "sheet3: row 58 is not the COUNTA totals row"
    new_totals = old_totals.replace('r="58"', 'r="62"')
    new_totals = re.sub(r'r="([A-Z]+)58"', r'r="\g<1>62"', new_totals)
    new_totals = new_totals.replace('ref="E58:AI58"', 'ref="E62:AI62"')
    new_totals = new_totals.replace('COUNTA(E3:E57)', 'COUNTA(E3:E61)')
    for col, bump in SHEET3_TOTAL_BUMPS.items():
        cm = re.search(rf'<c r="{col}62"[^>]*><f[^>]*/?>(?:</f>)?<v>(\d+)</v></c>', new_totals)
        assert cm, f"sheet3: totals cell {col}62 not found"
        old_cell = cm.group(0)
        new_cell = old_cell.replace(f'<v>{cm.group(1)}</v>', f'<v>{int(cm.group(1)) + bump}</v>')
        new_totals = new_totals.replace(old_cell, new_cell, 1)
    text = text.replace(old_totals, new_totals, 1)

    # 4. build and insert new course rows 58-61 (before the moved totals row)
    new_rows = []
    for a, code, name, sem, marks, aj in SHEET3_NEW_ROWS:
        cells = [
            f'<row r="{58 + len(new_rows)}">',
            f'<c r="A{58 + len(new_rows)}" s="29"><v>{a}</v></c>',
            f'<c r="B{58 + len(new_rows)}" s="30" t="inlineStr"><is><t xml:space="preserve">{code}</t></is></c>',
            f'<c r="C{58 + len(new_rows)}" s="31" t="inlineStr"><is><t xml:space="preserve">{xml_escape(name)}</t></is></c>',
            f'<c r="D{58 + len(new_rows)}" s="32"><v>{sem}</v></c>',
        ]
        for col in SHEET3_MARK_COLS:
            if col in marks:
                cells.append(f'<c r="{col}{58 + len(new_rows)}" s="33" t="inlineStr">'
                             f'<is><t xml:space="preserve">v</t></is></c>')
            else:
                cells.append(f'<c r="{col}{58 + len(new_rows)}" s="33"/>')
        cells.append(f'<c r="AJ{58 + len(new_rows)}" s="28"><v>{aj}</v></c>')
        cells.append('</row>')
        new_rows.append("".join(cells))
    text = text.replace(new_totals, "".join(new_rows) + new_totals, 1)
    return text


def fix_sheet14(text, si_text):
    CELL = re.compile(r'<c r="([CEF])(\d+)"([^>]*?)( t="s"><v>(\d+)</v>'
                      r'|( t="inlineStr")><is><t[^>]*>((?:(?!</t>).)*)</t></is>)</c>', re.S)

    # collect cell values by (col,row)
    cells = {}
    for m in CELL.finditer(text):
        col, row, attrs = m.group(1), int(m.group(2)), m.group(3)
        if m.group(5) is not None:
            val = si_text(int(m.group(5)))
        else:
            val = xml_unescape(m.group(7))
        cells[(col, row)] = (m.group(0), attrs, val)

    # map row -> normalized CPMK code (col C)
    row_code = {}
    for (col, row), (_, _, val) in cells.items():
        if col == "C":
            cm = re.match(r'^(CPMK\d{4})\b', val.strip())
            if cm:
                row_code[row] = cm.group(1)

    renamed = 0
    added_e = added_f = 0
    for (col, row), (cell_xml, attrs, val) in sorted(cells.items()):
        if col == "C":
            continue
        code = row_code.get(row)
        new_val = val
        if col == "E" and re.search(r'\bMK05[345]\b', new_val):
            new_val = rename_tokens(new_val)
            renamed += 1
        if code in ADDITIONS:
            add_code, add_name = ADDITIONS[code]
            if col == "E":
                assert add_code not in new_val, f"sheet14 E{row}: {add_code} already present"
                new_val = new_val.rstrip() + "\n" + add_code
                added_e += 1
            elif col == "F":
                new_val = new_val.rstrip() + "\n" + add_name
                added_f += 1
        if new_val != val:
            new_cell = (f'<c r="{col}{row}"{attrs.replace(chr(34)+">", chr(34))} '
                        f't="inlineStr"><is><t xml:space="preserve">{xml_escape(new_val)}</t></is></c>')
            # attrs may carry style etc.; rebuild cleanly
            style = re.search(r's="\d+"', attrs)
            style_part = f' {style.group(0)}' if style else ""
            new_cell = (f'<c r="{col}{row}"{style_part} t="inlineStr">'
                        f'<is><t xml:space="preserve">{xml_escape(new_val)}</t></is></c>')
            assert text.count(cell_xml) == 1, f"sheet14 {col}{row}: not exactly 1 occurrence"
            text = text.replace(cell_xml, new_cell, 1)

    assert renamed == EXPECTED_RENAMED_E_CELLS, f"expected {EXPECTED_RENAMED_E_CELLS} renamed E cells, got {renamed}"
    assert added_e == len(ADDITIONS), f"expected {len(ADDITIONS)} E additions, got {added_e}"
    assert added_f == len(ADDITIONS), f"expected {len(ADDITIONS)} F additions, got {added_f}"

    # E/F parity repair on the CPMK0303 row: E lists 8 codes, F named only 7 -
    # "Bahasa Inggris Persiapan Kerja" was missing from the F name list all along.
    f19_old = '<c r="F19" s="109" t="s"><v>399</v></c>'
    f19_new = ('<c r="F19" s="109" t="inlineStr"><is><t xml:space="preserve">'
               'Bahasa Inggris 1\nBahasa Inggris 2\nBahasa Indonesia\n'
               'Kewirausahaan Berbasis Teknologi\nKomunikasi Dan Etika Profesi\n'
               'Pengembangan Karir\nMagang\nBahasa Inggris Persiapan Kerja</t></is></c>')
    assert text.count(f19_old) == 1, "sheet14: F19 shared[399] not found"
    text = text.replace(f19_old, f19_new, 1)
    return text


def fix_sheet15(text):
    swaps = [
        (164, 226, "MK057"),
        (169, 228, "MK058"),
        (178, 230, "MK059"),
    ]
    for row, idx, new_code in swaps:
        pattern = re.compile(rf'<c r="A{row}"([^>]*) t="s"><v>{idx}</v></c>')
        m = pattern.search(text)
        assert m, f"sheet15: A{row} shared[{idx}] not found"
        assert text.count(m.group(0)) == 1
        new_cell = (f'<c r="A{row}"{m.group(1)} t="inlineStr">'
                    f'<is><t xml:space="preserve">{new_code}</t></is></c>')
        text = text.replace(m.group(0), new_cell, 1)
    return text


def apply_fix(xlsx_path: str):
    zin = zipfile.ZipFile(xlsx_path, "r")
    shared_raw = zin.read("xl/sharedStrings.xml").decode("utf-8")
    si_list = re.findall(r'<si>(.*?)</si>', shared_raw, re.S)

    def si_text(i):
        return xml_unescape("".join(re.findall(r'<t[^>]*>([^<]*)</t>', si_list[i], re.S)))

    handlers = {
        "xl/worksheets/sheet3.xml": lambda t: fix_sheet3(t),
        "xl/worksheets/sheet14.xml": lambda t: fix_sheet14(t, si_text),
        "xl/worksheets/sheet15.xml": lambda t: fix_sheet15(t),
    }

    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in handlers:
            text = handlers[item.filename](data.decode("utf-8"))
            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                raise AssertionError(f"edited {item.filename} is not well-formed XML: {exc}")
            data = text.encode("utf-8")
        zout.writestr(item, data)
    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    apply_fix(args.xlsx_path)
    print("Phase 3 applied: sheet3 registry relabeled+extended, sheet14 E/F lists "
          "renamed+extended, sheet15 headers relabeled.")
    print(f"Saved to {args.xlsx_path}")
