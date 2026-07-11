"""Build docs/kurikulum-2025.xlsx: a clean, reordered rewrite of the core CPL/CPMK/Sub-CPMK
table from docs/cpl-cpmk-subcpmk.xlsx, with a second CPL-centric tab for a different POV.

Background
----------
The source sheet (MK-CPMK-SubCPMK-Metode) accumulated fixes throughout a long session
(code-format normalization, MK053-059 scheme migration, min-2-per-course additions, text
fixes). New rows were appended at the end (rows 1151-1178) rather than inserted next to their
course's original block, so 8 courses (MK001, MK009, MK021, MK047, MK053, MK054, MK056,
MK059) have their Sub-CPMK rows split across two non-adjacent locations. Course order overall
isn't numerically sorted either.

Tab 1 (MK-CPMK-SubCPMK) groups rows by course (Kode MK, ascending MK001->MK059) with each
course's rows consolidated into one contiguous block, sorted by Kode CPMK then by the Kode
SubCPMK's embedded 2-digit serial within each course.

Tab 2 (CPL-CPMK) is the source workbook's CPL-CPMK master sheet (CPL -> CPMK -> [MK] mapping,
already CPL-block-ascending there) - a genuinely different, CPL-centric point of view on the
same curriculum, added per user request.

Discovery made while implementing tab 1 (changes the row-count expectation from the original
plan): of the 1163 physical data rows in the source Metode sheet, only 202 are real Sub-CPMK
entries (have a Kode SubCPMK) and 10 are the already-known CPL03-cluster orphan CPMK rows
(Kode CPMK defined, described, but no Sub-CPMK ever authored). The remaining 951 rows are
fully empty (or, in one case, a course-label-only row with no CPMK/SubCPMK content at all) -
spreadsheet artifacts with zero information. A genuine "clean rewrite" drops these rather than
preserving them as blank filler. Same pattern holds for the CPL-CPMK sheet: only 61 of its
1050 rows carry a real CPMK code.

v2 fix: mixed Dosen (lecturer) values
--------------------------------------
v1 forward-filled column A (Dosen) in raw physical order, same as the other carry-down
columns. But the appended rows (1151+) never had column A set at all (confirmed: A1151,
A1158, A1162 cells are entirely absent in the source XML) - so they silently inherited
whatever Dosen was last set hundreds of rows earlier for a *different, unrelated* course.
Fix: resolve Dosen per-course instead - scan the whole sheet for rows where Kode MK (B) and
Dosen (A) are *both* explicitly non-blank on the same row (not carried), and use that as the
canonical Dosen for every row of that course. Verified zero courses have more than one such
genuine value (the earlier "mixed" appearance was purely the carry-down leak); 7 courses have
no Dosen recorded anywhere in the source and are left blank rather than guessing.

v2 addition: real merged cells instead of repeating values
--------------------------------------------------------------
v1 wrote every row fully self-contained (no blank continuation cells) specifically to avoid
reintroducing the *implicit positional* carry-down convention that caused a real bug earlier
this session (a header row's deletion silently broke a later row's carry-down chain,
misattributing its course - only caught by a later audit). That risk doesn't apply to
*explicit* `<mergeCells>` XML generated fresh from the final resolved+sorted row order on
every rebuild - there's no "chain" to silently break since the merge ranges are recomputed
from scratch each time, not left to positional inference. So this version merges A/B/C
(Dosen/Kode MK/MK) vertically across each course block, and D/E/F/G/H (CPL/Kode BK/BK/Kode
CPMK/CPMK) vertically across each contiguous same-CPMK sub-block within a course - mirroring
the source's own carry-down granularity, just made explicit/robust instead of positional.

Why raw zip/XML construction instead of openpyxl
-----------------------------------------------------
openpyxl is not installed in this environment (checked). Also consistent with every other
xlsx-touching script in this repo, which avoids openpyxl entirely (it previously caused data
loss when round-tripping the complex source workbook) - here we're not round-tripping that
workbook at all, just reading it, and hand-building a new minimal multi-sheet OOXML package
from scratch for the output.
"""

import argparse
import os
import re
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_PATH = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
DEFAULT_OUTPUT = os.path.join(REPO_ROOT, "docs", "kurikulum-2025.xlsx")

METODE_SHEET = "xl/worksheets/sheet16.xml"
CPLCPMK_SHEET = "xl/worksheets/sheet14.xml"

METODE_COLUMNS = list("ABCDEFGHIJKLMNOPQR")
METODE_HEADERS = [
    "Dosen", "Kode MK", "MK", "CPL", "Kode BK", "BK", "Kode CPMK", "CPMK",
    "Kode SubCPMK", "SubCPMK", "MetodePembelajaran", "Bentuk Pembelajaran",
    "Bentuk Penilaian", "Kriteria Penilaian", "Materi Pembelajaran",
    "SubCPMK Lama", "Materi Pembelajaran Lama", "Deskripsi",
]
# B/C are course-level carry-down, D/E/F/H are CPMK-level carry-down. G (Kode CPMK) is never
# blank on a meaningful row - read directly per row, not forward-filled, and used as the
# meaningfulness filter. A (Dosen) is resolved separately (see fix_dosen), not carried here.
METODE_CARRY_DOWN_COLS = "BCDEFH"

CPLCPMK_COLUMNS = list("ABCDEFGHIJ")
CPLCPMK_HEADERS = [
    "CPL", "Deskripsi CPL", "CPMK", "Deskripsi CPMK", "Kode MK", "Nama MK",
    "Kode BK", "Nama BK", "", "CPMK Lama IABEE",
]
# A/B are CPL-level carry-down. C (CPMK) is never blank on a meaningful row.
CPLCPMK_CARRY_DOWN_COLS = "AB"


def xml_unescape(value):
    # order matters: &amp; must be last so it doesn't re-mangle e.g. &amp;lt; -> &lt;
    return (value.replace("&lt;", "<").replace("&gt;", ">")
                 .replace("&quot;", '"').replace("&apos;", "'")
                 .replace("&#10;", "\n").replace("&#13;", "\r")
                 .replace("&amp;", "&"))


def xml_escape(value):
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                 .replace('"', "&quot;"))


def read_sheet_rows(source_path, sheet_part):
    z = zipfile.ZipFile(source_path)
    shared_raw = z.read("xl/sharedStrings.xml").decode("utf-8")
    si_list = re.findall(r'<si>(.*?)</si>', shared_raw, re.S)

    def si_text(i):
        raw = "".join(re.findall(r'<t[^>]*>([^<]*)</t>', si_list[i], re.S)).strip()
        return xml_unescape(raw)

    cell_re = re.compile(r'<c r="([A-Z]+)\d+"([^>]*?)(/>|>(.*?)</c>)', re.S)

    def parse_row(body):
        colmap = {}
        for col, attrs, closer, inner in cell_re.findall(body):
            if closer == '/>':
                colmap[col] = ""
                continue
            if 't="s"' in attrs:
                mm = re.search(r'<v>(\d+)</v>', inner)
                val = si_text(int(mm.group(1))) if mm else ""
            elif 't="inlineStr"' in attrs:
                mm = re.search(r'<t[^>]*>((?:(?!</t>).)*)</t>', inner, re.S)
                val = xml_unescape(mm.group(1).strip()) if mm else ""
            else:
                mm = re.search(r'<v>([^<]*)</v>', inner)
                val = xml_unescape(mm.group(1)) if mm else ""
            colmap[col] = val
        return colmap

    text = z.read(sheet_part).decode("utf-8")
    raw_rows = re.findall(r'<row r="(\d+)"[^>]*>(.*?)</row>', text, re.S)
    return [(int(r), parse_row(body)) for r, body in raw_rows[1:]]  # skip header row


def resolve_and_filter(raw_rows, columns, carry_down_cols, meaningful_col):
    carry = {c: "" for c in carry_down_cols}
    resolved = []
    for _, cm in raw_rows:
        for c in carry_down_cols:
            if cm.get(c, "").strip():
                carry[c] = cm[c]
        full = dict(carry)
        for c in columns:
            if c not in carry_down_cols:
                full[c] = cm.get(c, "")
        if full.get(meaningful_col, "").strip():
            resolved.append(full)
    return resolved


def build_dosen_map(raw_rows):
    """Kode MK -> Dosen, resolved from rows where both are explicitly stated together
    (not carried) - avoids leaking an unrelated course's Dosen via positional forward-fill."""
    dosen = {}
    for _, cm in raw_rows:
        mk = cm.get("B", "").strip()
        a = cm.get("A", "").strip()
        if mk and a:
            assert dosen.get(mk, a) == a, f"{mk}: conflicting Dosen values {dosen[mk]!r} vs {a!r}"
            dosen[mk] = a
    return dosen


def metode_sort_key(row):
    mk_num = int(re.sub(r'\D', '', row.get("B", "")) or 0)
    cpmk = row.get("G", "")
    subcpmk = row.get("I", "")
    m = re.match(r'^SCPMK\d{4}-\d{3}(\d{2})$', subcpmk)
    serial = int(m.group(1)) if m else -1  # orphan CPMK rows sort first in their CPMK group
    return (mk_num, cpmk, serial)


def cplcpmk_sort_key(row):
    cpl_num = int(re.sub(r'\D', '', row.get("A", "")) or 0)
    return (cpl_num, row.get("C", ""))


def col_letter(n):
    letters = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def compute_merge_ranges(rows, key_func, merge_columns, start_row=2):
    """Contiguous runs (length > 1) where key_func(row) stays constant are candidates for
    merging. Within each such run, each column in merge_columns is merged independently -
    only across the sub-run where that column's OWN value also stays identical. This matters
    because two rows can share a group key (e.g. same course+CPMK) while genuinely differing
    in a "carried" column's actual text (source data drift) - merging on key alone would
    silently discard the differing content when the non-top rows get masked blank.
    Returns list of (column_key, first_row, last_row)."""
    ranges = []
    group_start = 0
    n = len(rows)
    for i in range(1, n + 1):
        if i == n or key_func(rows[i]) != key_func(rows[group_start]):
            for col in merge_columns:
                sub_start = group_start
                for j in range(group_start + 1, i + 1):
                    if j == i or rows[j].get(col, "") != rows[sub_start].get(col, ""):
                        if j - sub_start > 1:
                            ranges.append((col, sub_start + start_row, (j - 1) + start_row))
                        sub_start = j
            group_start = i
    return ranges


def mask_merged_values(rows, merge_ranges, start_row=2):
    """Blank out a column's value on every row of a merge range except the first, so only
    the top-left cell of each merged range carries the value (OOXML convention)."""
    masked = [dict(r) for r in rows]
    for col, r0, r1 in merge_ranges:
        for row_num in range(r0 + 1, r1 + 1):
            masked[row_num - start_row][col] = ""
    return masked


def build_sheet_xml(rows, headers, columns, merge_ranges):
    col_idx = {c: i + 1 for i, c in enumerate(columns)}
    parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             '<sheetData>']

    def row_xml(row_num, values):
        cells = []
        for i, val in enumerate(values, start=1):
            if val == "":
                continue
            col = col_letter(i)
            cells.append(
                f'<c r="{col}{row_num}" t="inlineStr">'
                f'<is><t xml:space="preserve">{xml_escape(val)}</t></is></c>'
            )
        return f'<row r="{row_num}">' + "".join(cells) + "</row>"

    parts.append(row_xml(1, headers))
    for idx, row in enumerate(rows, start=2):
        parts.append(row_xml(idx, [row.get(c, "") for c in columns]))
    parts.append('</sheetData>')

    if merge_ranges:
        parts.append(f'<mergeCells count="{len(merge_ranges)}">')
        for col, r0, r1 in merge_ranges:
            letter = col_letter(col_idx[col])
            parts.append(f'<mergeCell ref="{letter}{r0}:{letter}{r1}"/>')
        parts.append('</mergeCells>')

    parts.append('</worksheet>')
    return "".join(parts)


CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
    'relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-'
    'officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.'
    'openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.'
    'openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '</Types>'
)

ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships/officeDocument" Target="xl/workbook.xml"/>'
    '</Relationships>'
)

WORKBOOK_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<sheets>'
    '<sheet name="MK-CPMK-SubCPMK" sheetId="1" r:id="rId1"/>'
    '<sheet name="CPL-CPMK" sheetId="2" r:id="rId2"/>'
    '</sheets>'
    '</workbook>'
)

WORKBOOK_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="worksheets/sheet1.xml"/>'
    '<Relationship Id="rId2" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="worksheets/sheet2.xml"/>'
    '</Relationships>'
)


def build_metode_tab(source_path):
    raw_rows = read_sheet_rows(source_path, METODE_SHEET)
    dosen_map = build_dosen_map(raw_rows)

    resolved = resolve_and_filter(raw_rows, METODE_COLUMNS, METODE_CARRY_DOWN_COLS, "G")
    for row in resolved:
        row["A"] = dosen_map.get(row.get("B", ""), "")
    resolved.sort(key=metode_sort_key)

    course_merges = compute_merge_ranges(resolved, lambda r: r.get("B", ""), "ABC")
    cpmk_merges = compute_merge_ranges(
        resolved, lambda r: (r.get("B", ""), r.get("G", "")), "DEFGH")
    merges = course_merges + cpmk_merges
    masked = mask_merged_values(resolved, merges)

    sheet_xml = build_sheet_xml(masked, METODE_HEADERS, METODE_COLUMNS, merges)
    return sheet_xml, len(raw_rows), len(resolved)


def build_cplcpmk_tab(source_path):
    raw_rows = read_sheet_rows(source_path, CPLCPMK_SHEET)
    resolved = resolve_and_filter(raw_rows, CPLCPMK_COLUMNS, CPLCPMK_CARRY_DOWN_COLS, "C")
    resolved.sort(key=cplcpmk_sort_key)

    merges = compute_merge_ranges(resolved, lambda r: r.get("A", ""), "AB")
    masked = mask_merged_values(resolved, merges)

    sheet_xml = build_sheet_xml(masked, CPLCPMK_HEADERS, CPLCPMK_COLUMNS, merges)
    return sheet_xml, len(raw_rows), len(resolved)


def build(source_path, output_path):
    sheet1_xml, n1_raw, n1_out = build_metode_tab(source_path)
    sheet2_xml, n2_raw, n2_out = build_cplcpmk_tab(source_path)

    ET.fromstring(sheet1_xml)
    ET.fromstring(sheet2_xml)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("[Content_Types].xml", CONTENT_TYPES)
        zout.writestr("_rels/.rels", ROOT_RELS)
        zout.writestr("xl/workbook.xml", WORKBOOK_XML)
        zout.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        zout.writestr("xl/worksheets/sheet1.xml", sheet1_xml)
        zout.writestr("xl/worksheets/sheet2.xml", sheet2_xml)

    return (n1_raw, n1_out), (n2_raw, n2_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=SOURCE_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    (n1_raw, n1_out), (n2_raw, n2_out) = build(args.source, args.output)
    print(f"Tab 1 MK-CPMK-SubCPMK: {n1_raw} physical rows -> {n1_out} meaningful rows "
          f"(dropped {n1_raw - n1_out}).")
    print(f"Tab 2 CPL-CPMK: {n2_raw} physical rows -> {n2_out} meaningful rows "
          f"(dropped {n2_raw - n2_out}).")
    print(f"Saved to {args.output}")
