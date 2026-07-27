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

Layout formulas (reverse-engineered from the original 10 diagrams and verified against all
of them before implementing - see the session's plan file for the check):
  - 8 semester columns at x = 1.6, 4.8, 8.0, 11.2, 14.4, 17.6, 20.8, 24.0 (spacing 3.2)
  - within a column, courses stack top-to-bottom starting y=-3.45, step -1.3
  - box height H = 4.1 + (max_rows_in_any_column - 1) * 1.3
  - "CPLxx" side label y = -(2.5 + H) / 2

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

SEM_X = {1: 1.6, 2: 4.8, 3: 8.0, 4: 11.2, 5: 14.4, 6: 17.6, 7: 20.8, 8: 24.0}
YEAR_X = {1: 3.2, 2: 9.6, 3: 16.0, 4: 22.4}
COL_BOUNDARIES = [3.2, 6.4, 9.6, 12.8, 16.0, 19.2, 22.4]
THICK_BOUNDARIES = [6.4, 12.8, 19.2]

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


def build_diagram(cpl, courses, kelompok):
    by_sem = defaultdict(list)
    for c in courses:
        by_sem[c["sem"]].append(c)
    for sem in by_sem:
        by_sem[sem].sort(key=lambda c: c["mknum"])

    max_rows = max(len(v) for v in by_sem.values())
    H = 4.1 + (max_rows - 1) * 1.3
    label_y = (2.5 + H) / 2

    lines = []
    lines.append(f"% ===================== {cpl} =====================")
    lines.append(r"\begin{figure}[H]")
    lines.append(r"\centering")
    lines.append(r"\resizebox{\textwidth}{!}{%")
    lines.append(r"\begin{tikzpicture}[")
    lines.append(r"  mk/.style={draw, rounded corners, fill=headblue, font=\fontsize{6}{7}\selectfont, align=center, text width=2.6cm, minimum height=0.9cm, inner sep=1.5pt},")
    lines.append(r"  soft/.style={draw, rounded corners, fill=softgreen, font=\fontsize{6}{7}\selectfont, align=center, text width=2.6cm, minimum height=0.9cm, inner sep=1.5pt},")
    lines.append(r"  hdr/.style={font=\bfseries\small, align=center},")
    lines.append(r"  ->, >={Stealth[length=1.5mm]}, thick, rounded corners=2pt,")
    lines.append(r"]")
    lines.append(f"\\draw (-2.300,0) rectangle (25.600,-{H:.3f});")
    lines.append(f"\\draw (-2.300,-1.100) -- (25.600,-1.100);")
    lines.append(f"\\draw (-2.300,-1.800) -- (25.600,-1.800);")
    lines.append(f"\\draw (-2.300,-2.500) -- (25.600,-2.500);")
    lines.append(f"\\draw (0,-1.100) -- (0,-{H:.3f});")
    for x in COL_BOUNDARIES:
        lines.append(f"\\draw ({x:.3f},-1.800) -- ({x:.3f},-{H:.3f});")
    for x in THICK_BOUNDARIES:
        lines.append(f"\\draw[thick] ({x:.3f},-1.800) -- ({x:.3f},-{H:.3f});")
    desc = CPL_DESCRIPTIONS[cpl]
    lines.append(f"\\node[align=center, text width=26.900cm, font=\\small] at (11.650,-0.550) {{{cpl}: {desc}}};")
    for yr, x in YEAR_X.items():
        lines.append(f"\\node[hdr] at ({x:.3f},-1.450) {{Tahun {yr}}};")
    lines.append(r"\node[hdr] at (-1.150,-1.450) {CPL};")
    for sem, x in SEM_X.items():
        lines.append(f"\\node[hdr] at ({x:.3f},-2.150) {{Semester {sem}}};")
    lines.append(f"\\node[hdr] at (-1.150,-{label_y:.3f}) {{{cpl}}};")

    node_ids = {}
    for sem in sorted(by_sem):
        x = SEM_X[sem]
        for row, c in enumerate(by_sem[sem]):
            y = 3.45 + row * 1.3
            nid = sanitize_id(c["name"])
            node_ids[c["name"]] = (nid, x, y)
            style = "soft" if kelompok.get(c["name"]) in ("WN", "WP-PT") else "mk"
            lines.append(
                f"\\node[{style}] ({nid}) at ({x:.3f},-{y:.3f}) "
                f"{{{c['name']}\\\\{c['sks']} SKS}};"
            )

    chain = sorted(courses, key=lambda c: (c["sem"], c["mknum"]))
    for prev, cur in zip(chain, chain[1:]):
        pid, px, py = node_ids[prev["name"]]
        cid, cx, cy = node_ids[cur["name"]]
        if px == cx and py == cy:
            continue
        if py == cy:
            lines.append(f"\\draw ({pid}.east) -- ({cid}.west);")
        else:
            midx = (px + cx) / 2
            lines.append(
                f"\\draw ({pid}.east) -- ({midx:.3f},-{py:.3f}) -- "
                f"({midx:.3f},-{cy:.3f}) -- ({cid}.west);"
            )

    lines.append(r"\end{tikzpicture}%")
    lines.append(r"}")
    lines.append(f"\\caption{{Peta Jalan {cpl}}}")
    lines.append(r"\end{figure}")
    return "\n".join(lines)


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
             "setiap Capaian Pembelajaran Lulusan (CPL), disusun per tahun dan semester. "
             "Setiap kotak menampilkan nama mata kuliah beserta bobot SKS-nya, dan anak "
             "panah menunjukkan keterkaitan/urutan antar mata kuliah dalam membangun "
             "capaian tersebut.\n\n")
    outro = (r"\reviewfrompdf{Sepuluh diagram peta jalan CPL di atas memetakan kontribusi "
              r"mata kuliah terhadap setiap CPL, disusun ulang langsung dari "
              r"docs/rti-mk-crosswalk.md (bukan dari sheet CPL-MK (Rev3 fix) yang dipakai "
              r"pada versi sebelumnya dan sudah diketahui memiliki sejumlah mismatch "
              r"terhadap kurikulum 59 mata kuliah). Susunan node dan panah keterkaitan "
              r"ini tetap perlu divalidasi oleh tim kurikulum sebelum dokumen dinyatakan "
              r"final.}" + "\n\n")

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
