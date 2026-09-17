"""Regenerate the 10 "Peta Jalan CPL" TikZ diagrams in book/src/chapters/05-matriks.tex.

Background
----------
A full consistency audit (2026-07-11) found the existing diagrams were generated from the
`CPL-MK (Rev3 fix)` sheet in docs/cpl-cpmk-subcpmk.xlsx, not from the actual curriculum
design data. That sheet predates the 59-course scheme (missing the 4 second-track courses
and Keselamatan dan Kesehatan Kerja) and disagreed with the more current
docs/rti-mk-crosswalk.md on 28 of 54 shown courses' CPL membership.

Per curriculum-owner direction, this script treats docs/rti-mk-crosswalk.md as the sole
source of truth for CPL membership (RPS documents are "a referenced document" only, not
used to decide CPL assignment), and rebuilds all 10 diagrams from scratch rather than
hand-patching 28+ changes across 10 files with hardcoded pixel coordinates.

Layout (2026-09-17 portrait rewrite)
-------------------------------------
The original layout put semesters on a fixed 8-wide horizontal axis (SEM_X below), which
gave every diagram the same fixed natural width of 27.9cm regardless of content -- too wide
to shrink into the book's ~15.8cm portrait \\textwidth without dropping the 7.5pt node font
to an unreadable ~4.2pt. That version rendered the whole section on landscape pages instead.

This version transposes the axes: semesters run top-to-bottom (one fixed-height row band
per semester, 8 rows always drawn even if a CPL has no course in some semester), and the
courses assigned to a semester sit side-by-side within that row. The width driver becomes
"how many courses does this CPL have in its busiest single semester" (1-6 across the 10
diagrams) instead of the fixed 8-semester count, while height is now a near-constant ~19cm
(header band + 8 fixed-height rows) that comfortably fits the portrait page without ever
needing the extra landscape headroom. Each CPL stays exactly one figure/page, in the book's
normal portrait flow -- no \\begin{landscape}, no multi-figure split, no cross-figure
connectors, since each diagram is a single chronological chain with no edges that need to
jump between separate figures.

Node style (mk vs soft) uses docs/kurikulum-2025-distribusi-mk.md's Kelompok column
(WN/WP-PT -> soft, WP/P -> mk) - the cleanest available signal, though not a perfect
match to the original hand-authored diagrams (documented as approximate in the plan;
flagged for curriculum-team validation like the rest of this section already is).

Connectors: the original diagrams' arrow routing encoded specific hand-authored
"builds on" relationships that aren't recoverable from any data source. This script
draws a single deterministic chronological chain per CPL diagram (connect each course to
the previous one in semester order, tie-broken by MK number) - a defensible, simple,
honest baseline given the section's own text already states this is a "concept
relationship, not enrollment prerequisite" map that needs curriculum-team validation.

Why a generator instead of hand-editing the TikZ
--------------------------------------------------
28+ add/remove operations across 54 existing courses, plus 5 new course nodes, spread
over 10 hand-coded diagrams with hardcoded pixel coordinates - hand-patching is
error-prone and hard to verify. A generator makes the output reproducible and the source
data (crosswalk doc) directly auditable against the rendered result.
"""

import argparse
import os
import re
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CROSSWALK_PATH = os.path.join(REPO_ROOT, "docs", "rti-mk-crosswalk.md")
DISTRO_PATH = os.path.join(REPO_ROOT, "docs", "kurikulum-2025-distribusi-mk.md")
CHAPTER_PATH = os.path.join(REPO_ROOT, "book", "src", "chapters", "05-matriks.tex")

CPL_DESCRIPTIONS = {
    "CPL01": "Menginternalisasi ketakwaan kepada Tuhan Yang Maha Esa, menaati hukum, disiplin, dan menunjukkan profesionalisme melalui etika profesi, pembelajaran sepanjang hayat, serta respons terhadap isu sosial dan teknologi.",
    "CPL02": "Menguasai konsep teoritis bidang pengetahuan mengenai berbagai prinsip rekayasa sistem/perangkat lunak dalam merancang solusi aplikasi multi-platform yang relevan dengan kebutuhan stakeholder.",
    "CPL03": "Mampu mengelola tim, manajemen diri, berkomunikasi secara lisan maupun tertulis dengan baik dan mampu melakukan presentasi.",
    "CPL04": "Mampu menyusun deskripsi saintifik hasil kajian implikasi pengembangan atau implementasi ilmu pengetahuan teknologi dalam bentuk skripsi atau laporan tugas akhir atau artikel ilmiah.",
    "CPL05": "Mampu menerapkan solusi teknologi komputasi dan infrastruktur digital dengan mempertimbangkan berbagai teknik/pendekatan yang sesuai dengan kebutuhan.",
    "CPL06": "Mampu merancang, mengimplementasikan, menguji, melakukan deployment, dan memelihara, serta menjamin mutu perangkat lunak yang menjawab permasalahan dan memenuhi kebutuhan stakeholder.",
    "CPL07": "Mampu mengembangkan sistem komputasi cerdas, analisis data dengan menerapkan algoritma dan teknik kecerdasan artifisial secara tepat guna.",
    "CPL08": "Mampu mengelola proyek teknologi informasi secara profesional dengan mengoptimalkan sumber daya yang tersedia.",
    "CPL09": "Memiliki pemahaman yang memadai terkait cara kerja sistem komputer dan berbagai teknik/pendekatan berbasis komputasi untuk memecahkan masalah stakeholder.",
    "CPL10": "Memiliki kompetensi untuk menganalisis persoalan kompleks untuk mengidentifikasi solusi bidang informatika/ilmu komputer dengan mempertimbangkan wawasan ilmu multidisiplin.",
}

# Portrait usable area under the book's default geometry (book/src/preamble.tex:
# left=2.8cm, right=2.4cm, top=2.3cm, bottom=2.2cm on A4 -> 15.8cm wide, ~25.2cm
# tall). PORTRAIT_HEIGHT leaves headroom under that for the caption + spacing,
# matching the constant used in generate_jejaring_kurikulum.py for the same reason.
PORTRAIT_WIDTH = 15.8
PORTRAIT_HEIGHT = 22.5

# ---- Row (semester) / column (course-within-semester) layout ----
ROW_PITCH_Y = 2.0     # vertical distance between semester-row centers
COL_PITCH_X = 2.9     # horizontal distance between course-box centers in a row
HEADER_H = 2.6        # vertical space reserved for the "CPLxx: <description>" banner
BOX_HALF_W = 1.3       # half of the 2.6cm node text width
NODE_X0 = 0.5          # x-center of the first (leftmost) course box in a row
GUTTER_LABEL_X = -1.7  # x-center of the "Sem. N" row labels
SEP_X = -0.85          # x of the vertical rule separating labels from course boxes
FRAME_LEFT = -2.6
RIGHT_PAD = 0.4        # padding beyond the widest row's last box
BOTTOM_PAD = 0.3
MIN_NATURAL_W = 13.6   # frame widens to at least this so the CPL description banner
                        # (which spans the full frame width) never wraps to a cramped
                        # column just because a CPL has few courses in any one semester
ELBOW_NUDGE = 0.15
TAHUN_BOUNDARY_AFTER = {2, 4, 6}  # thick separator after these semesters

CW_NAME_FIX = {
    "Konsep TI": "Konsep Teknologi Informasi",
    "Critical Thinking": "Critical Thinking dan Problem Solving",
    "Prak Dasar Pemrograman": "Praktikum Dasar Pemrograman",
    "K3": "Keselamatan dan Kesehatan Kerja",
    "RPL": "Rekayasa Perangkat Lunak",
    "Prak Basis Data": "Praktikum Basis Data",
    "Prak ASD": "Praktikum Algoritma dan Struktur Data",
    "Prak PBO": "Praktikum Pemrograman Berbasis Objek",
    "Penjaminan Mutu PL": "Penjaminan Mutu Perangkat Lunak",
    "Prak Jaringan Komputer": "Praktikum Jaringan Komputer",
}


def parse_crosswalk(path):
    with open(path, encoding="utf-8") as f:
        md = f.read()
    courses = []
    for line in md.splitlines():
        m = re.match(
            r'^\|\s*\**(RTI\d+)\**\s*\|\s*\**([^|*]+?)\**\s*\|\s*\**(\d+)\**\s*\|'
            r'\s*\**(\d+)\**\s*\|\s*\**(MK\d{3})\**\s*\|\s*\**([^|*]+?)\**\s*\|',
            line,
        )
        if not m:
            continue
        code, name, sks, sem, mknum, cpl_field = m.groups()
        name = CW_NAME_FIX.get(name.strip(), name.strip())
        cpls = sorted(re.findall(r'CPL\d{2}', cpl_field))
        courses.append({
            "code": code, "name": name, "sks": int(sks), "sem": int(sem),
            "mknum": int(mknum[2:]), "cpl": cpls,
        })
    assert len(courses) == 59, f"expected 59 courses in crosswalk, got {len(courses)}"
    return courses


def parse_distro_kelompok(path):
    with open(path, encoding="utf-8") as f:
        md = f.read()
    kelompok = {}
    for line in md.splitlines():
        m = re.match(r'^\|\s*\d+\s*\|\s*RTI\d+\s*\|\s*([^|]+?)\s*\|\s*([\w-]+)\s*\|', line)
        if m:
            name, kel = m.groups()
            kelompok[name.strip()] = kel
    return kelompok


def sanitize_id(name):
    return "n" + re.sub(r'[^a-z0-9]', '', name.lower())


def row_top(sem):
    """Y of the horizontal separator above semester `sem`'s row (sem=9 -> frame bottom)."""
    return -HEADER_H - (sem - 1) * ROW_PITCH_Y


def build_diagram(cpl, courses, kelompok):
    by_sem = defaultdict(list)
    for c in courses:
        by_sem[c["sem"]].append(c)
    for sem in by_sem:
        by_sem[sem].sort(key=lambda c: c["mknum"])

    max_cols = max((len(v) for v in by_sem.values()), default=1)
    grid_right = NODE_X0 + (max_cols - 1) * COL_PITCH_X + BOX_HALF_W + RIGHT_PAD
    frame_right = max(grid_right, FRAME_LEFT + MIN_NATURAL_W)
    frame_bottom = row_top(9)

    natural_w = frame_right - FRAME_LEFT
    natural_h = -frame_bottom + BOTTOM_PAD
    target_w = min(natural_w, PORTRAIT_WIDTH)
    implied_h = natural_h * (target_w / natural_w)
    if implied_h > PORTRAIT_HEIGHT:
        target_w = natural_w * (PORTRAIT_HEIGHT / natural_h)

    lines = []
    lines.append(f"% ===================== {cpl} =====================")
    lines.append(r"\begin{figure}[H]")
    lines.append(r"\centering")
    lines.append(f"\\resizebox{{{target_w:.2f}cm}}{{!}}{{%")
    lines.append(r"\begin{tikzpicture}[")
    lines.append(r"  mk/.style={draw, rounded corners, fill=headblue, font=\fontsize{7.5}{8.5}\selectfont, align=center, text width=2.6cm, minimum height=1.0cm, inner sep=1.5pt},")
    lines.append(r"  soft/.style={draw, rounded corners, fill=softgreen, font=\fontsize{7.5}{8.5}\selectfont, align=center, text width=2.6cm, minimum height=1.0cm, inner sep=1.5pt},")
    lines.append(r"  smhdr/.style={font=\bfseries\footnotesize, align=center},")
    lines.append(r"  ->, >={Stealth[length=1.5mm]}, thick, rounded corners=2pt,")
    lines.append(r"]")

    # Outer frame + header/row separators. Explicit "-" (no arrow tip) since the
    # picture's default style is "->" for the course-chain connectors below --
    # without this override these plain grid/frame lines pick up arrowheads too,
    # which reads as a second, meaningless set of "flow" arrows on the page.
    lines.append(f"\\draw[-] ({FRAME_LEFT:.3f},0.000) rectangle ({frame_right:.3f},{frame_bottom:.3f});")
    lines.append(f"\\draw[-] ({FRAME_LEFT:.3f},{row_top(1):.3f}) -- ({frame_right:.3f},{row_top(1):.3f});")
    for sem in range(2, 9):
        y = row_top(sem)
        style = "-,thick" if (sem - 1) in TAHUN_BOUNDARY_AFTER else "-"
        lines.append(f"\\draw[{style}] ({FRAME_LEFT:.3f},{y:.3f}) -- ({frame_right:.3f},{y:.3f});")
    lines.append(f"\\draw[-] ({SEP_X:.3f},{row_top(1):.3f}) -- ({SEP_X:.3f},{frame_bottom:.3f});")

    # CPL description banner.
    desc = CPL_DESCRIPTIONS[cpl]
    header_text_width = frame_right - FRAME_LEFT - 0.6
    header_x = (FRAME_LEFT + frame_right) / 2
    lines.append(
        f"\\node[align=center, text width={header_text_width:.3f}cm, font=\\small] "
        f"at ({header_x:.3f},{-HEADER_H / 2:.3f}) {{\\textbf{{{cpl}}}: {desc}}};"
    )

    # Row (semester) labels.
    for sem in range(1, 9):
        y = row_top(sem) - ROW_PITCH_Y / 2
        lines.append(f"\\node[smhdr] at ({GUTTER_LABEL_X:.3f},{y:.3f}) {{Sem. {sem}}};")

    node_ids = {}
    for sem in sorted(by_sem):
        y = row_top(sem) - ROW_PITCH_Y / 2
        for col, c in enumerate(by_sem[sem]):
            x = NODE_X0 + col * COL_PITCH_X
            nid = sanitize_id(c["name"])
            node_ids[c["name"]] = (nid, x, y)
            style = "soft" if kelompok.get(c["name"]) in ("WN", "WP-PT") else "mk"
            lines.append(
                f"\\node[{style}] ({nid}) at ({x:.3f},{y:.3f}) "
                f"{{{c['name']}\\\\{c['sks']} SKS}};"
            )

    chain = sorted(courses, key=lambda c: (c["sem"], c["mknum"]))
    for prev, cur in zip(chain, chain[1:]):
        pid, px, py = node_ids[prev["name"]]
        cid, cx, cy = node_ids[cur["name"]]
        if px == cx and py == cy:
            continue
        if py == cy:
            # Same semester row: adjacent boxes, sorted left-to-right by MK number.
            lines.append(f"\\draw ({pid}.east) -- ({cid}.west);")
        elif px == cx:
            # Same column position in different semester rows: plain vertical edge.
            lines.append(f"\\draw ({pid}.south) -- ({cid}.north);")
        else:
            raw_mid = (py + cy) / 2
            midy = raw_mid + ELBOW_NUDGE * (1 if py > cy else -1)
            lines.append(
                f"\\draw ({pid}.south) -- ({px:.3f},{midy:.3f}) -- "
                f"({cx:.3f},{midy:.3f}) -- ({cid}.north);"
            )

    lines.append(r"\end{tikzpicture}%")
    lines.append(r"}")
    lines.append(f"\\caption{{Peta Jalan {cpl}}}")
    lines.append(r"\end{figure}")
    lines.append("")
    lines.append(summarize(cpl, courses, by_sem, kelompok))
    return "\n".join(lines)


def summarize(cpl, courses, by_sem, kelompok):
    """One real, data-derived sentence pair per CPL (not filler): every number here
    is computed from the same course list build_diagram() just drew, so it can
    never drift out of sync with the diagram above it.
    """
    total = len(courses)
    total_sks = sum(c["sks"] for c in courses)
    sem_lo, sem_hi = min(by_sem), max(by_sem)
    busiest_sem = max(sorted(by_sem), key=lambda s: len(by_sem[s]))
    busiest_count = len(by_sem[busiest_sem])
    soft_count = sum(1 for c in courses if kelompok.get(c["name"]) in ("WN", "WP-PT"))
    mk_count = total - soft_count

    if sem_lo == sem_hi:
        span = f"seluruhnya berada pada Semester {sem_lo}"
    else:
        span = f"tersebar dari Semester {sem_lo} hingga Semester {sem_hi}"

    if soft_count == 0:
        breakdown = f"Seluruh {total} mata kuliah tersebut bersifat teknis inti."
    elif mk_count == 0:
        breakdown = f"Seluruh {total} mata kuliah tersebut bersifat pengembangan umum (soft skill)."
    else:
        breakdown = (f"Dari jumlah tersebut, {mk_count} mata kuliah bersifat teknis inti "
                     f"dan {soft_count} bersifat pengembangan umum (soft skill).")

    return (f"{cpl} dipetakan pada {total} mata kuliah ({total_sks} SKS) yang {span}, "
            f"dengan Semester {busiest_sem} sebagai yang terpadat ({busiest_count} mata "
            f"kuliah paralel). {breakdown}")


def generate(courses, kelompok):
    by_cpl = defaultdict(list)
    for c in courses:
        for cpl in c["cpl"]:
            by_cpl[cpl].append(c)
    blocks = []
    for i in range(1, 11):
        cpl = f"CPL{i:02d}"
        blocks.append(build_diagram(cpl, by_cpl[cpl], kelompok))
    return "\n\n".join(blocks) + "\n"


def apply_fix(chapter_path, crosswalk_path, distro_path):
    courses = parse_crosswalk(crosswalk_path)
    kelompok = parse_distro_kelompok(distro_path)
    new_diagrams = generate(courses, kelompok)

    with open(chapter_path, encoding="utf-8") as f:
        text = f.read()

    start_marker = r"\section{Peta Jalan CPL}"
    end_marker = r"\section{Matrik Organisasi"
    start_idx = text.index(start_marker) + len(start_marker)
    end_idx = text.index(end_marker)

    intro = ("\n\nSepuluh diagram berikut memetakan mata kuliah yang berkontribusi pada "
             "setiap Capaian Pembelajaran Lulusan (CPL). Setiap diagram dibaca dari atas ke "
             "bawah mengikuti urutan semester; mata kuliah pada semester yang sama "
             "ditampilkan berdampingan. Setiap kotak menampilkan nama mata kuliah beserta "
             "bobot SKS-nya, dan anak panah menunjukkan keterkaitan/urutan antar mata "
             "kuliah dalam membangun capaian tersebut.\n\n")
    outro = (r"\textit{Sepuluh diagram peta jalan CPL di atas memetakan kontribusi mata "
              r"kuliah terhadap setiap CPL, disusun langsung dari pemetaan mata kuliah-CPL "
              r"Kurikulum 2025 yang telah disinkronkan terhadap kurikulum 59 mata kuliah.}"
              + "\n\n")

    new_text = text[:start_idx] + intro + new_diagrams + "\n" + outro + text[end_idx:]

    with open(chapter_path, "w", encoding="utf-8") as f:
        f.write(new_text)

    return len(courses), sum(len(c["cpl"]) for c in courses)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", default=CHAPTER_PATH)
    parser.add_argument("--crosswalk", default=CROSSWALK_PATH)
    parser.add_argument("--distro", default=DISTRO_PATH)
    args = parser.parse_args()

    n_courses, n_memberships = apply_fix(args.chapter, args.crosswalk, args.distro)
    print(f"Regenerated 10 Peta Jalan CPL diagrams from {n_courses} courses "
          f"({n_memberships} total CPL memberships).")
    print(f"Saved to {args.chapter}")
