"""Fill Tabel Suplemen C1 gaps from the corrected cpl-cpmk-subcpmk.xlsx knowledge base.

Background
----------
docs/Interim LINK 04. (Engineering) Lampiran Tabel Suplemen D4TI Polinema.xlsx is the
IABEE accreditation Lampiran document. Its "Tabel Suplemen C1" sheet is a CPL -> CPMK ->
Course -> Sub-CPMK -> assessment-method table - structurally the same content as
docs/cpl-cpmk-subcpmk.xlsx's MK-CPMK-SubCPMK-Metode sheet, which this repo's other scripts
(fill_subcpmk_metode.py, fix_subcpmk_metode_codes*.py, fix_subcpmk_metode_wording_*.py)
already spent extensive work correcting: orphan Sub-CPMK codes filled, duplicate/collision
codes fixed, code format normalized to SCPMK<CPMK>-<3-digit MK><2-digit seq>, and CPMK/
SCPMK codes zero-padded (CPMK101 -> CPMK0101, CPMK10.1 -> CPMK1001) everywhere else in the
repo (scripts/propagate_cpmk_padding.py).

C1 was exported from an OLDER, unfixed snapshot of that same underlying data and was never
resynced - it still uses the pre-padding code convention throughout, and is missing the
`Kode Sub CPMK` value on most of its rows. This script closes those gaps using the now-
corrected cpl-cpmk-subcpmk.xlsx as the source of truth, applying three distinct, narrowly-
scoped fixes:

1. CODE_PAD (`Kode CPMK`, column B, 61 rows): mechanical zero-padding, same rule as
   scripts/propagate_cpmk_padding.py (CPMK101 -> CPMK0101, CPMK10.1 -> CPMK1001). Every
   filled Kode CPMK cell in C1 needed this - the whole sheet predates the padding
   convention.
2. SUBCODE_PAD (`Kode Sub CPMK`, column E, 15 rows): same padding rule applied to the 15
   rows that already had SOME Kode Sub CPMK value (e.g. SCPMK101-00801 -> SCPMK0101-00801).
3. SUBCODE_FILL (`Kode Sub CPMK`, column E, 110 rows): fills cells that were entirely
   empty. Built by exact-text matching every C1 row with a filled `Sub CPMK` statement but
   an empty `Kode Sub CPMK` (188 such rows) against cpl-cpmk-subcpmk.xlsx's
   MK-CPMK-SubCPMK-Metode column J, normalized for whitespace/`\\n` noise and the
   now-removed leading "Mahasiswa" (this session's own wording fix stripped 149 of those
   from the source - matching had to account for both pre- and post-fix phrasing).
   - 113 rows matched confidently (105 same course name; 8 more after normalizing an
     obvious C1 course-name typo/trailing-whitespace, e.g. "Algoritma & Struktur Data" vs
     the correct "Algoritma Dan Struktur Data" - each of those 8 matched exactly ONE
     source row, so there was no ambiguity to resolve).
   - Of those 113, THREE map to a code that was about to be assigned to two different C1
     rows at once (rows 13/14, 16/58, 157/158) - in every case the two C1 rows have
     byte-identical Sub-CPMK text, but the corrected source has only ONE matching row for
     that text. This is a genuine duplicate ROW within C1 itself (confirmed absent from
     the source - e.g. source MK010 Agama has exactly 3 Sub-CPMK rows, not 4), not a
     matching bug. Filling both with the same code would recreate the exact
     duplicate-code collision class this session spent significant effort eliminating
     from the source workbook. Only the FIRST occurrence of each pair is filled here; the
     second is left empty and flagged in DUPLICATE_ROWS_NOT_FILLED for a human dedup
     decision. Net: 110 rows filled.
   - 75 rows have NO matching text anywhere in the source at all - genuine content gaps,
     left empty, listed in UNMATCHED_ROWS for follow-up (likely needs manual
     reconciliation against the original RPS files or curriculum-owner input, same
     category of judgment call as the CPL03/invalid-CPMK rows already flagged in
     docs/subcpmk-wording-review.md).

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this repo: openpyxl
load_workbook(...).save(...) previously caused unrelated data loss in the sibling
cpl-cpmk-subcpmk.xlsx workbook. Treating this second workbook with the same caution.

Note on cell types: unlike cpl-cpmk-subcpmk.xlsx (which stores its Sub-CPMK text as
inline strings), this workbook stores filled cells as SHARED strings (t="s", <v>index</v>)
and empty cells as bare self-closing tags with no `t` attribute at all
(<c r="E13" s="512"/>). This script converts every touched cell to an inline string
(t="inlineStr") - for filled cells this avoids ever mutating xl/sharedStrings.xml (a
shared string may be referenced by other cells for unrelated purposes); for empty cells
it matches the same inline-string-insertion pattern used by fill_subcpmk_metode.py.
"""

import argparse
import os
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(
    REPO_ROOT, "docs",
    "Interim LINK 04. (Engineering) Lampiran Tabel Suplemen D4TI Polinema.xlsx",
)
SHEET = "xl/worksheets/sheet12.xml"  # Tabel Suplemen C1

# --- 1. CODE_PAD: Kode CPMK (column B) zero-padding, 61 rows ---
CODE_PAD = {
    2: ("CPMK101\n", "CPMK0101\n"), 9: ("CPMK102", "CPMK0102"),
    18: ("CPMK201", "CPMK0201"), 21: ("CPMK202", "CPMK0202"),
    23: ("CPMK203", "CPMK0203"), 27: ("CPMK204", "CPMK0204"),
    28: ("CPMK205", "CPMK0205"), 31: ("CPMK206", "CPMK0206"),
    33: ("CPMK207", "CPMK0207"), 34: ("CPMK208", "CPMK0208"),
    37: ("CPMK209", "CPMK0209"), 38: ("CPMK210", "CPMK0210"),
    39: ("CPMK211", "CPMK0211"), 45: ("CPMK301", "CPMK0301"),
    53: ("CPMK302", "CPMK0302"), 58: ("CPMK303", "CPMK0303"),
    68: ("CPMK401", "CPMK0401"), 70: ("CPMK402", "CPMK0402"),
    71: ("CPMK403", "CPMK0403"), 72: ("CPMK404", "CPMK0404"),
    73: ("CPMK501", "CPMK0501"), 74: ("CPMK502", "CPMK0502"),
    81: ("CPMK503", "CPMK0503"), 84: ("CPMK504", "CPMK0504"),
    87: ("CPMK505", "CPMK0505"), 88: ("CPMK508", "CPMK0508"),
    89: ("CPMK509", "CPMK0509"), 92: ("CPMK601", "CPMK0601"),
    93: ("CPMK602", "CPMK0602"), 99: ("CPMK603", "CPMK0603"),
    103: ("CPMK605", "CPMK0605"), 104: ("CPMK606", "CPMK0606"),
    106: ("CPMK607", "CPMK0607"), 113: ("CPMK608", "CPMK0608"),
    114: ("CPMK609", "CPMK0609"), 115: ("CPMK701", "CPMK0701"),
    117: ("CPMK702", "CPMK0702"), 119: ("CPMK703", "CPMK0703"),
    120: ("CPMK704", "CPMK0704"), 127: ("CPMK705", "CPMK0705"),
    129: ("CPMK706", "CPMK0706"), 135: ("CPMK707", "CPMK0707"),
    136: ("CPMK708", "CPMK0708"), 137: ("CPMK801", "CPMK0801"),
    140: ("CPMK802", "CPMK0802"), 154: ("CPMK803", "CPMK0803"),
    159: ("CPMK804", "CPMK0804"), 162: ("CPMK901", "CPMK0901"),
    166: ("CPMK902", "CPMK0902"), 176: ("CPMK903", "CPMK0903"),
    183: ("CPMK904", "CPMK0904"), 185: ("CPMK905", "CPMK0905"),
    186: ("CPMK10.1", "CPMK1001"), 191: ("CPMK10.2", "CPMK1002"),
    192: ("CPMK10.3", "CPMK1003"), 194: ("CPMK10.4", "CPMK1004"),
    196: ("CPMK10.5", "CPMK1005"), 200: ("CPMK10.6", "CPMK1006"),
    202: ("CPMK10.7", "CPMK1007"), 203: ("CPMK10.8", "CPMK1008"),
    206: ("CPMK10.9", "CPMK1009"),
}

# --- 2. SUBCODE_PAD: Kode Sub CPMK (column E) zero-padding for already-filled cells, 15 rows ---
SUBCODE_PAD = {
    2: ("SCPMK101-00801", "SCPMK0101-00801"),
    3: ("SCPMK101-00802", "SCPMK0101-00802"),
    4: ("SCPMK101-00803\n", "SCPMK0101-00803\n"),
    5: ("SCPMK101-00101", "SCPMK0101-00101"),
    6: ("SCPMK101-00102", "SCPMK0101-00102"),
    7: ("SCPMK101-00103", "SCPMK0101-00103"),
    8: ("SCPMK101-00105", "SCPMK0101-00105"),
    9: ("SCPMK101-00104", "SCPMK0101-00104"),
    10: ("SCPMK102-00101", "SCPMK0102-00101"),
    18: ("SCPMK201-00101", "SCPMK0201-00101"),
    45: ("SCPMK311-00101", "SCPMK0311-00101"),
    46: ("SCPMK313-00101", "SCPMK0313-00101"),
    47: ("SCPMK314-00101\n", "SCPMK0314-00101\n"),
    53: ("SCPMK312-00101\n", "SCPMK0312-00101\n"),
    89: ("SCPMK509-00101\n", "SCPMK0509-00101\n"),
}

# --- 3. SUBCODE_FILL: Kode Sub CPMK (column E) fills for empty cells, 110 rows ---
SUBCODE_FILL = {
    12: "SCPMK0102-01001", 13: "SCPMK0102-01002", 16: "SCPMK0102-04601",
    21: "SCPMK0202-01201", 22: "SCPMK0202-01202", 23: "SCPMK0203-01501",
    24: "SCPMK0203-01601", 26: "SCPMK0203-02301", 29: "SCPMK0205-01406",
    33: "SCPMK0207-01701", 34: "SCPMK0208-00201", 35: "SCPMK0208-02904",
    36: "SCPMK0208-02905", 40: "SCPMK0211-02906", 41: "SCPMK0211-01407",
    42: "SCPMK0211-02504", 51: "SCPMK0301-03605", 52: "SCPMK0301-03606",
    59: "SCPMK0316-04603", 62: "SCPMK0303-00501", 63: "SCPMK0303-00502",
    64: "SCPMK0303-02701", 65: "SCPMK0303-02702", 68: "SCPMK0401-00304",
    69: "SCPMK0401-00305", 73: "SCPMK0501-04401", 76: "SCPMK0502-00201",
    77: "SCPMK0502-04401", 78: "SCPMK0502-05105", 79: "SCPMK0502-05106",
    80: "SCPMK0502-05107", 84: "SCPMK0504-04403", 85: "SCPMK0504-03201",
    87: "SCPMK0505-04401", 90: "SCPMK0509-05108", 91: "SCPMK0509-05109",
    92: "SCPMK0601-01201", 94: "SCPMK0602-01414", 95: "SCPMK0602-02907",
    97: "SCPMK0602-03607", 98: "SCPMK0602-03608", 99: "SCPMK0603-02203",
    102: "SCPMK0603-04704", 104: "SCPMK0606-02505", 108: "SCPMK0607-01415",
    109: "SCPMK0607-02908", 110: "SCPMK0607-02506", 112: "SCPMK0607-03615",
    114: "SCPMK0609-02909", 115: "SCPMK0701-01601", 116: "SCPMK0701-02305",
    119: "SCPMK0703-01801", 121: "SCPMK0704-02502", 123: "SCPMK0704-00601",
    124: "SCPMK0704-00602", 125: "SCPMK0704-00701", 126: "SCPMK0704-00702",
    128: "SCPMK0705-04301", 129: "SCPMK0706-04301", 130: "SCPMK0706-02801",
    131: "SCPMK0706-03101", 132: "SCPMK0706-03103", 136: "SCPMK0708-01801",
    142: "SCPMK0802-01201", 143: "SCPMK0802-01202", 144: "SCPMK0802-01408",
    145: "SCPMK0802-01409", 146: "SCPMK0802-01410", 147: "SCPMK0802-01411",
    148: "SCPMK0802-01412", 149: "SCPMK0802-01413", 151: "SCPMK0802-03609",
    152: "SCPMK0802-03610", 157: "SCPMK0803-03611", 163: "SCPMK0901-00201",
    167: "SCPMK0902-00401", 168: "SCPMK0902-00402", 169: "SCPMK0902-00403",
    170: "SCPMK0902-00905", 171: "SCPMK0902-01101", 172: "SCPMK0902-01102",
    173: "SCPMK0902-01103", 174: "SCPMK0902-02401", 176: "SCPMK0903-01701",
    178: "SCPMK0903-01801", 179: "SCPMK0903-00601", 180: "SCPMK0903-00602",
    181: "SCPMK0903-00701", 182: "SCPMK0903-00702", 185: "SCPMK0905-05104",
    186: "SCPMK1001-01501", 187: "SCPMK1001-01502", 188: "SCPMK1001-01601",
    189: "SCPMK1001-02006", 190: "SCPMK1001-02306", 191: "SCPMK1002-04404",
    192: "SCPMK1003-04405", 193: "SCPMK1003-05103", 194: "SCPMK1004-04103",
    195: "SCPMK1004-04301", 196: "SCPMK1005-04301", 197: "SCPMK1005-02802",
    198: "SCPMK1005-03102", 199: "SCPMK1005-04002", 202: "SCPMK1007-02402",
    203: "SCPMK1008-05808", 204: "SCPMK1008-03613", 205: "SCPMK1008-03614",
    206: "SCPMK1009-05805", 207: "SCPMK1009-03802",
}

# Second occurrence of a duplicate C1 row (byte-identical Sub-CPMK text to the row noted,
# confirmed NOT duplicated in the source) - left empty, not auto-filled. row -> dup-of row.
DUPLICATE_ROWS_NOT_FILLED = {14: 13, 58: 16, 158: 157}

# The 75 rows with Sub-CPMK text but no matching source row at all - left empty.
UNMATCHED_ROWS = [
    11, 15, 17, 19, 20, 25, 27, 28, 30, 31, 32, 39, 43, 44, 48, 49, 50,
    54, 55, 56, 57, 60, 61, 66, 67, 70, 71, 72, 74, 75, 81, 82, 83, 86, 88,
    93, 96, 100, 101, 103, 105, 106, 107, 111, 113, 117, 118, 120, 122, 127,
    133, 134, 135, 137, 138, 139, 140, 141, 150, 153, 154, 155, 156, 159, 160,
    161, 162, 164, 165, 166, 177, 183, 184, 200, 201,
]


def load_shared_strings(z):
    NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(f"{NS}t")) for si in root.findall(f"{NS}si")]


def resolve_shared(cell_xml, shared):
    """Resolve a t="s" cell's displayed text via the shared strings table."""
    m = re.search(r'<v>(\d+)</v>', cell_xml)
    return shared[int(m.group(1))] if m else None


def apply_fix(xlsx_path: str):
    zin = zipfile.ZipFile(xlsx_path, "r")
    shared = load_shared_strings(zin)
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    counts = {"pad_b": 0, "pad_e": 0, "fill_e": 0}
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")

            # 1 & 2: shared-string cells needing padding (column B or E)
            for col, table, key in (("B", CODE_PAD, "pad_b"), ("E", SUBCODE_PAD, "pad_e")):
                for row, (old_val, new_val) in table.items():
                    ref = f"{col}{row}"
                    pattern = re.compile(rf'<c r="{ref}"([^/]*?)t="s"><v>(\d+)</v></c>')
                    m = pattern.search(text)
                    assert m, f"could not find shared-string cell {ref}"
                    attrs = m.group(1)
                    resolved = shared[int(m.group(2))]
                    assert resolved == old_val, (
                        f"{ref}: expected old value {old_val!r}, sheet has {resolved!r}"
                    )
                    old_full = m.group(0)
                    # attrs.rstrip() + explicit space: guarantees exactly one space before
                    # t="inlineStr" regardless of whether the captured attrs already ended
                    # in whitespace (it does here, since attrs was captured right up to a
                    # literal `t="s"`, but keep this robust rather than assume it).
                    new_full = f'<c r="{ref}" {attrs.strip()} t="inlineStr"><is><t xml:space="preserve">{new_val}</t></is></c>'
                    assert text.count(old_full) == 1, f"{ref}: not exactly 1 occurrence"
                    text = text.replace(old_full, new_full, 1)
                    counts[key] += 1

            # 3: empty column-E cells being filled for the first time. NOTE: unlike
            # cpl-cpmk-subcpmk.xlsx, this workbook's empty cells are bare self-closing tags
            # with NO trailing space before `/>` (e.g. `<c r="E33" s="525"/>`) - the captured
            # `attrs` group here does NOT end in whitespace, so a naive
            # f'{attrs}t="inlineStr"' would produce invalid XML like `s="525"t="inlineStr"`
            # (missing space between attributes). This was caught during verification (the
            # first attempt produced a sheet12.xml that failed ET.fromstring parsing) -
            # always insert an explicit space before t="inlineStr" instead of relying on
            # attrs to already have one.
            for row, new_val in SUBCODE_FILL.items():
                ref = f"E{row}"
                pattern = re.compile(rf'<c r="{ref}"([^/]*?)/>')
                m = pattern.search(text)
                assert m, f"could not find empty placeholder cell {ref}"
                attrs = m.group(1)
                old_full = m.group(0)
                new_full = f'<c r="{ref}" {attrs.strip()} t="inlineStr"><is><t xml:space="preserve">{new_val}</t></is></c>'
                assert text.count(old_full) == 1, f"{ref}: not exactly 1 occurrence"
                text = text.replace(old_full, new_full, 1)
                counts["fill_e"] += 1

            # Self-check: confirm the edited sheet is still well-formed XML before
            # writing it out. A first attempt at this script produced invalid XML here
            # (missing whitespace between attributes) that only zipfile.testzip() alone
            # would NOT have caught - that check verifies the zip container's CRCs, not
            # the XML content inside it.
            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    counts = apply_fix(args.xlsx_path)
    print(f"Kode CPMK (col B) padded: {counts['pad_b']} (expected {len(CODE_PAD)})")
    print(f"Kode Sub CPMK (col E) padded: {counts['pad_e']} (expected {len(SUBCODE_PAD)})")
    print(f"Kode Sub CPMK (col E) filled: {counts['fill_e']} (expected {len(SUBCODE_FILL)})")
    print(f"Duplicate rows left empty (flagged): {DUPLICATE_ROWS_NOT_FILLED}")
    print(f"Unmatched rows left empty ({len(UNMATCHED_ROWS)}): {UNMATCHED_ROWS}")
    print(f"Saved to {args.xlsx_path}")
