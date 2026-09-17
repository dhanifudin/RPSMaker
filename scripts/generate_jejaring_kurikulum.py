"""Regenerate the "Jejaring Kurikulum" diagram in book/src/chapters/05-matriks.tex.

Background
----------
The original hand-authored diagram (\\section{Jejaring Kurikulum}) laid up to 9 course boxes
side by side per semester in a 2-level "ladder" stagger. Its real TikZ bounding box is 44.0cm
wide x 50.3cm tall, but it was squeezed via \\resizebox{\\textwidth}{!} into a ~17.6cm-wide
portrait column -- a ~0.40x shrink that took the 7pt course-box font down to an effective
~2.8pt, unreadable in print.

This script parses a preserved snapshot of that original, hand-authored content --
scripts/data/jejaring-kurikulum-original.tex, saved before any relayout -- so the 61 course/
gate boxes and their 51 hand-curated "concept relationship" edges (4 line styles: solid =
confirmed, dotted = needs validation, dashed = corequisite, green = general/soft-skill track)
are preserved exactly, not redrawn or reinvented. It then lays them out in a much more compact
3-column-per-semester grid (instead of 9-wide) and regenerates the edges to connect the new
positions, split into two figures (Semester 1-4, Semester 5-8) since even the compacted layout
is too tall for one legible page. 21 of the 51 edges cross the Semester 4/5 boundary; since a
line can't be drawn across two separate figures, affected boxes get a small "continues on the
next/previous figure" annotation and the full detail is preserved in a reference table after
Figure 2.

Like scripts/generate_peta_jalan_cpl.py, both figures render on landscape pages (pdflscape)
with \\pagestyle{empty} -- the book's eso-pic/fancyhdr chrome does not rotate correctly under
pdflscape, discovered and fixed the same way for that script.
"""

import argparse
import os
import re
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_PATH = os.path.join(REPO_ROOT, "scripts", "data", "jejaring-kurikulum-original.tex")
CHAPTER_PATH = os.path.join(REPO_ROOT, "book", "src", "chapters", "05-matriks.tex")

COLS = 3
COL_PITCH = 3.6
ROW_PITCH = 2.3
BAND_GAP = 1.8
LABEL_X = -2.3
JOG_STEP = 0.09  # per-edge lane offset so parallel elbow routes don't coincide
LEFT_MARGIN = -1.7  # clear vertical lane left of column 0, never occupied by a box
# Usable area under the BOOK'S DEFAULT geometry (book/src/preamble.tex:
# left=2.8cm, right=2.4cm, top=2.3cm, bottom=2.2cm -- this section used to carry
# its own wider \newgeometry, which needed a \clearpage before it and stranded
# the chapter heading alone on an otherwise-blank page; removed so Section 5.1
# starts right after "BAB 5" like every other section in the book):
# A4 21x29.7cm minus margins = 15.8cm wide, 25.2cm tall; PORTRAIT_HEIGHT leaves
# headroom under that for the caption + spacing.
PORTRAIT_WIDTH = 15.8
PORTRAIT_HEIGHT = 22.5

SEM6_GROUPS = {
    "n256003": "always", "n256001": "always", "n256002": "always",
    "n256104": "reguler", "n256105": "reguler", "n256106": "reguler",
    "n256107": "reguler", "n256108": "reguler",
    "n256204": "magang", "n256205": "magang", "n256206": "magang", "n256207": "magang",
}

STYLE_DRAW = {
    "solid": "",
    "dotted": "dotted, ",
    "dashed": "dashed, ",
    "green": "green!40!black, ",
}


def parse_source(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    tstart = text.index(r"\begin{tikzpicture}[")
    tend = text.index("\\end{tikzpicture}%\n}", tstart) + len("\\end{tikzpicture}%\n}")
    diagram = text[tstart:tend]

    nodes = {}
    sem = None
    for line in diagram.splitlines():
        m = re.match(r"%\s*=+\s*SEMESTER (\d+)\s*=+", line)
        if m:
            sem = int(m.group(1))
            continue
        m = re.match(
            r"\\node\[(mk|soft|gate)\]\s*\((\w+)\)\s*at\s*\(([-\d.]+),(-?[\d.]+)\)\s*\{(.+?)\};",
            line,
        )
        if m:
            style, nid, x, y, label = m.groups()
            nodes[nid] = dict(
                style=style, label=label, sem=sem, orig_x=float(x), orig_y=float(y),
                group=SEM6_GROUPS.get(nid),
            )
    assert len(nodes) == 61, f"expected 61 nodes, parsed {len(nodes)}"

    edges = []
    anchor_re = re.compile(r"\((\w+)\.(\w+)\)")
    for line in diagram.splitlines():
        line = line.strip()
        if not line.startswith(r"\draw"):
            continue
        m = re.match(r"\\draw(\[([^\]]*)\])?", line)
        opts = m.group(2) or ""
        if "green" in opts:
            style = "green"
        elif "dotted" in opts:
            style = "dotted"
        elif "dashed" in opts:
            style = "dashed"
        else:
            style = "solid"
        refs = anchor_re.findall(line)
        if len(refs) < 2:
            continue  # the reguler/magang divider line has no node anchors
        edges.append((refs[0][0], refs[-1][0], style))
    assert len(edges) == 51, f"expected 51 edges, parsed {len(edges)}"

    return nodes, edges


def layout_band(nodes_in_band, top_y):
    """Row-major 3-column grid, reading order = original left-to-right (x) order."""
    order = sorted(nodes_in_band, key=lambda n: nodes_in_band[n]["orig_x"])
    positions = {}
    for i, nid in enumerate(order):
        col, row = i % COLS, i // COLS
        positions[nid] = (col * COL_PITCH, top_y - row * ROW_PITCH)
    rows = (len(order) - 1) // COLS + 1
    bottom_y = top_y - (rows - 1) * ROW_PITCH
    return positions, bottom_y


def layout_sem6(nodes, top_y):
    always = [n for n in nodes if nodes[n]["group"] == "always"]
    reguler = [n for n in nodes if nodes[n]["group"] == "reguler"]
    magang = [n for n in nodes if nodes[n]["group"] == "magang"]
    positions = {}

    always_order = sorted(always, key=lambda n: nodes[n]["orig_x"])
    for i, nid in enumerate(always_order):
        positions[nid] = (i * COL_PITCH, top_y)

    track_top = top_y - ROW_PITCH - 0.9
    divider_gap = 1.2
    reg_x = [0.0, COL_PITCH]
    mag_x = [2 * COL_PITCH + divider_gap, 3 * COL_PITCH + divider_gap]

    reguler_order = sorted(reguler, key=lambda n: nodes[n]["orig_x"])
    for i, nid in enumerate(reguler_order):
        col, row = i % 2, i // 2
        positions[nid] = (reg_x[col], track_top - row * ROW_PITCH)
    reguler_rows = (len(reguler_order) - 1) // 2 + 1

    magang_order = sorted(magang, key=lambda n: nodes[n]["orig_x"])
    for i, nid in enumerate(magang_order):
        col, row = i % 2, i // 2
        positions[nid] = (mag_x[col], track_top - row * ROW_PITCH)
    magang_rows = (len(magang_order) - 1) // 2 + 1

    bottom_y = track_top - (max(reguler_rows, magang_rows) - 1) * ROW_PITCH
    divider_x = 2 * COL_PITCH + divider_gap / 2
    extra = {
        "divider_x": divider_x, "divider_top": track_top + ROW_PITCH * 0.5,
        "divider_bottom": bottom_y - ROW_PITCH * 0.5,
        "reg_label_x": reg_x[0] + COL_PITCH / 2, "mag_label_x": mag_x[0] + COL_PITCH / 2,
        "label_y": (top_y + track_top) / 2,
    }
    return positions, bottom_y, extra


def _path_clear_vertical(all_positions, x, y_lo, y_hi, exclude):
    return not any(
        nid not in exclude and abs(px - x) < 1e-6 and y_lo + 1e-6 < py < y_hi - 1e-6
        for nid, (px, py) in all_positions.items()
    )


def _path_clear_horizontal(all_positions, y, x_lo, x_hi, exclude):
    return not any(
        nid not in exclude and abs(py - y) < 1e-6 and x_lo + 1e-6 < px < x_hi - 1e-6
        for nid, (px, py) in all_positions.items()
    )


def route_edge(nid_a, nid_b, all_positions, style, jog_counter, left_margin, right_margin):
    """Straight edge when source/target are truly adjacent (nothing else shares
    their column/row in between); otherwise route via whichever outer margin
    (never occupied by a box) is nearer, entering/exiting through the row-gap
    immediately beside each node -- both kinds of segment stay in space no box
    ever occupies, so this can't pierce an unrelated node the way a naive
    same-column/same-row straight line can once a grid has more than one row.
    """
    ax, ay = all_positions[nid_a]
    bx, by = all_positions[nid_b]
    opt = STYLE_DRAW[style]
    exclude = {nid_a, nid_b}

    if abs(ax - bx) < 1e-6 and abs(ay - by) > 1e-6:
        y_lo, y_hi = min(ay, by), max(ay, by)
        if _path_clear_vertical(all_positions, ax, y_lo, y_hi, exclude):
            if ay > by:
                return f"\\draw[{opt}->] ({nid_a}.south) -- ({nid_b}.north);"
            return f"\\draw[{opt}->] ({nid_a}.north) -- ({nid_b}.south);"

    if abs(ay - by) < 1e-6 and abs(ax - bx) > 1e-6:
        x_lo, x_hi = min(ax, bx), max(ax, bx)
        if _path_clear_horizontal(all_positions, ay, x_lo, x_hi, exclude):
            if ax < bx:
                return f"\\draw[{opt}->] ({nid_a}.east) -- ({nid_b}.west);"
            return f"\\draw[{opt}->] ({nid_a}.west) -- ({nid_b}.east);"

    downward = ay > by
    exit_side = "south" if downward else "north"
    enter_side = "north" if downward else "south"
    sign = -1 if downward else 1
    src_jog_y = ay + sign * ROW_PITCH * 0.4
    tgt_jog_y = by - sign * ROW_PITCH * 0.4

    use_right = (ax + bx) / 2 >= COL_PITCH
    margin = right_margin if use_right else left_margin
    lane_key = (use_right, downward)
    n = jog_counter[lane_key]
    jog_counter[lane_key] += 1
    margin_x = margin + (n * JOG_STEP if use_right else -n * JOG_STEP)

    return (
        f"\\draw[{opt}->] ({nid_a}.{exit_side}) -- ({ax:.3f},{src_jog_y:.3f}) -- "
        f"({margin_x:.3f},{src_jog_y:.3f}) -- ({margin_x:.3f},{tgt_jog_y:.3f}) -- "
        f"({bx:.3f},{tgt_jog_y:.3f}) -- ({nid_b}.{enter_side});"
    )


def build_figure(fig_nodes, fig_edges, positions, sems, extras, cross_out, cross_in, caption,
                  left_margin, right_margin):
    lines = []
    lines.append(r"\begin{tikzpicture}[")
    lines.append(r"  mk/.style={draw, rounded corners, fill=headblue, font=\fontsize{9}{10}\selectfont, align=center, text width=2.8cm, minimum height=0.9cm, inner sep=2pt},")
    lines.append(r"  soft/.style={draw, rounded corners, fill=softgreen, font=\fontsize{9}{10}\selectfont, align=center, text width=2.8cm, minimum height=0.9cm, inner sep=2pt},")
    lines.append(r"  gate/.style={draw, dashed, rounded corners, fill=headgray, font=\fontsize{9}{10}\selectfont, align=center, text width=2.8cm, minimum height=0.9cm, inner sep=2pt},")
    lines.append(r"  smlabel/.style={font=\bfseries\normalsize, anchor=east},")
    lines.append(r"  thick, rounded corners=2pt,")
    lines.append(r"]")

    for nid in fig_nodes:
        n = fig_nodes[nid]
        x, y = positions[nid]
        label = n["label"]
        if nid in cross_out:
            label += r"\\{\tiny$\rightarrow$ lanjut Gambar berikutnya}"
        if nid in cross_in:
            label = r"{\tiny$\leftarrow$ dari Gambar sebelumnya}\\" + label
        lines.append(f"\\node[{n['style']}] ({nid}) at ({x:.3f},{y:.3f}) {{{label}}};")

    for sem, (label_x, label_y) in sems.items():
        lines.append(f"\\node[smlabel] at ({label_x:.3f},{label_y:.3f}) {{Sem. {sem}}};")

    if extras:
        lines.append(
            f"\\draw[densely dotted, thick] ({extras['divider_x']:.3f},{extras['divider_top']:.3f}) -- "
            f"({extras['divider_x']:.3f},{extras['divider_bottom']:.3f});"
        )
        lines.append(f"\\node[font=\\bfseries\\normalsize] at ({extras['reg_label_x']:.3f},{extras['label_y']:.3f}) {{Jalur Reguler}};")
        lines.append(f"\\node[font=\\bfseries\\normalsize] at ({extras['mag_label_x']:.3f},{extras['label_y']:.3f}) {{Jalur Magang}};")

    jog_counter = defaultdict(int)
    for a, b, style in fig_edges:
        lines.append(route_edge(a, b, positions, style, jog_counter, left_margin, right_margin))

    lines.append(r"\end{tikzpicture}%")
    tikz_body = "\n".join(lines)

    # Fit-to-page: this layout is tall and narrow (many stacked semester bands,
    # only 3 columns wide), the opposite shape of the book's usual wide/short
    # figures -- \resizebox{\textwidth}{!} (width-driven) would blow the height
    # far past the page. Measure the actual coordinate extent of what was just
    # generated and scale by whichever dimension is the binding constraint.
    coords = re.findall(r"\(([-\d.]+),(-?[\d.]+)\)", tikz_body)
    xs = [float(x) for x, _ in coords]
    ys = [float(y) for _, y in coords]
    # pad for box half-extents beyond node-center coordinates, the "Sem. N"
    # label text hanging left of its anchor point, and rounded-corner strokes
    natural_w = (max(xs) - min(xs)) + 3.6
    natural_h = (max(ys) - min(ys)) + 2.2
    scale_w = PORTRAIT_WIDTH / natural_w
    scale_h = PORTRAIT_HEIGHT / natural_h
    if scale_w <= scale_h:
        resize = f"\\resizebox{{{PORTRAIT_WIDTH:.2f}cm}}{{!}}{{%"
    else:
        resize = f"\\resizebox{{!}}{{{PORTRAIT_HEIGHT:.2f}cm}}{{%"

    return (
        "\\begin{figure}[H]\n\\centering\n" + resize + "\n" + tikz_body + "\n}\n"
        f"\\caption{{{caption}}}\n\\end{{figure}}"
    )


def generate(nodes, edges):
    page1_sems = [1, 2, 3, 4]
    page2_bands = [5, 6, 7, 8]

    fig1_edges = [(a, b, s) for a, b, s in edges if nodes[a]["sem"] <= 4 and nodes[b]["sem"] <= 4]
    fig2_edges = [(a, b, s) for a, b, s in edges if nodes[a]["sem"] >= 5 and nodes[b]["sem"] >= 5]
    crossing = [(a, b, s) for a, b, s in edges if nodes[a]["sem"] <= 4 and nodes[b]["sem"] >= 5]
    assert len(fig1_edges) + len(fig2_edges) + len(crossing) == len(edges)

    cross_out = {a for a, _, _ in crossing}
    cross_in = {b for _, b, _ in crossing}

    # ---- Figure 1: Semester 1-4 ----
    positions1 = {}
    sems1 = {}
    y_cursor = 0.0
    for sem in page1_sems:
        band_nodes = {n: nodes[n] for n in nodes if nodes[n]["sem"] == sem}
        pos, bottom_y = layout_band(band_nodes, y_cursor)
        positions1.update(pos)
        sems1[sem] = (LABEL_X, y_cursor - (ROW_PITCH * ((len(band_nodes) - 1) // COLS)) / 2)
        y_cursor = bottom_y - BAND_GAP
    fig1_nodes = {n: nodes[n] for n in nodes if nodes[n]["sem"] <= 4}

    # ---- Figure 2: Semester 5-8 ----
    positions2 = {}
    sems2 = {}
    y_cursor = 0.0
    extras2 = None
    for sem in page2_bands:
        band_nodes = {n: nodes[n] for n in nodes if nodes[n]["sem"] == sem}
        if sem == 6:
            pos, bottom_y, extras2 = layout_sem6(band_nodes, y_cursor)
            sems2[sem] = (LABEL_X, y_cursor - 0.4)
        else:
            pos, bottom_y = layout_band(band_nodes, y_cursor)
            sems2[sem] = (LABEL_X, y_cursor - (ROW_PITCH * ((len(band_nodes) - 1) // COLS)) / 2)
        positions2.update(pos)
        y_cursor = bottom_y - BAND_GAP
    fig2_nodes = {n: nodes[n] for n in nodes if nodes[n]["sem"] >= 5}

    max_x1 = max(x for x, _ in positions1.values())
    max_x2 = max(x for x, _ in positions2.values())

    fig1 = build_figure(
        fig1_nodes, fig1_edges, positions1, sems1, None, cross_out, set(),
        "Jejaring Kurikulum Program Studi D4 Teknik Informatika -- Semester 1--4 (Kurikulum 2025)",
        LEFT_MARGIN, max_x1 + 1.7,
    )
    fig2 = build_figure(
        fig2_nodes, fig2_edges, positions2, sems2, extras2, set(), cross_in,
        "Jejaring Kurikulum Program Studi D4 Teknik Informatika -- Semester 5--8 (Kurikulum 2025)",
        LEFT_MARGIN, max_x2 + 1.7,
    )

    table_rows = []
    for a, b, style in crossing:
        style_label = {"solid": "Terkonfirmasi", "dotted": "Perlu validasi",
                        "dashed": "Korekuisit", "green": "Jalur umum"}[style]
        an = nodes[a]["label"].replace("\\\\", " -- ")
        bn = nodes[b]["label"].replace("\\\\", " -- ")
        table_rows.append(f"{an} & {bn} & {style_label} \\\\")

    return fig1, fig2, table_rows, len(crossing)


def apply_fix(chapter_path, snapshot_path):
    nodes, edges = parse_source(snapshot_path)
    fig1, fig2, table_rows, n_crossing = generate(nodes, edges)

    with open(chapter_path, encoding="utf-8") as f:
        text = f.read()

    start_marker = r"\section{Jejaring Kurikulum}"
    end_marker = r"\section{Peta Jalan CPL}"
    start_idx = text.index(start_marker) + len(start_marker)
    end_idx = text.index(end_marker)

    # Figure 1 needs a full page on its own regardless of what precedes it (it's ~100%
    # page-height even alone), so a short intro just leaves most of ITS OWN preceding
    # page blank -- there's no length that lets intro+Figure 1 share a page. Given
    # that, lean into genuinely explaining the diagram here rather than staying terse:
    # real orientation content the reader needs before a dense diagram, not padding.
    intro = (
        "\n\nJejaring kurikulum berikut menunjukkan keterkaitan antar mata kuliah pada "
        "Kurikulum 2025 Program Studi D4 Teknik Informatika: garis dari mata kuliah A ke B "
        "berarti B secara substansi membangun di atas materi A, disusun per tahun dan "
        "semester agar urutan pembelajaran mudah ditelusuri.\n\n"
        "Perlu dicatat, jejaring ini merepresentasikan peta keterkaitan konsep antar mata "
        "kuliah, bukan mata kuliah prasyarat pendaftaran (\\emph{prerequisite}) dalam "
        "pengertian akademik formal. Mahasiswa Program Studi D4 Teknik Informatika menempuh "
        "satu paket mata kuliah tetap per semester (kecuali percabangan Jalur Reguler/Jalur "
        "Magang pada Semester 6), sehingga urutan pengambilan mata kuliah sudah ditentukan "
        "oleh struktur kurikulum itu sendiri, bukan oleh garis keterkaitan pada diagram "
        "ini.\n\n"
        "Setiap kotak berwarna biru menandai mata kuliah pada jalur teknis/wajib program "
        "studi, sedangkan kotak berwarna hijau menandai mata kuliah umum atau pengembangan "
        "diri (misalnya Pancasila, Agama, Bahasa Inggris, K3); kotak abu-abu bergaris "
        "putus-putus menandai gerbang syarat SKS kumulatif, bukan mata kuliah. Empat gaya "
        "garis panah membedakan jenis keterkaitan: garis penuh untuk keterkaitan konsep yang "
        "terkonfirmasi, garis titik-titik untuk keterkaitan yang masih perlu divalidasi "
        "berdasarkan kesamaan topik/bahan kajian, garis putus-putus untuk korekuisit (mata "
        "kuliah yang ditempuh pada semester yang sama), dan garis hijau untuk jalur mata "
        "kuliah umum/pengembangan diri; lihat pula legenda bergambar di bawah Gambar "
        "kedua.\n\n"
        "Karena rentang delapan semester tidak dapat ditampilkan dalam satu halaman tanpa "
        "mengecilkan kotak mata kuliah hingga sulit dibaca, diagram ini dipecah menjadi dua "
        "Gambar: Semester 1--4 dan Semester 5--8. Kotak yang memiliki keterkaitan menuju atau "
        "berasal dari Gambar lainnya ditandai dengan keterangan kecil "
        "``$\\rightarrow$ lanjut Gambar berikutnya'' atau ``$\\leftarrow$ dari Gambar "
        "sebelumnya''; daftar lengkap seluruh keterkaitan lintas-Gambar tersebut disajikan "
        "pada tabel setelah Gambar kedua.\n\n"
    )

    # This lands in Figure 1's own trailing space (proven to fit cleanly there without
    # pushing Figure 2 off that page).
    bridge = (
        "\n\nGambar 5.1 berikut menunjukkan mata kuliah Semester 1--4, yang "
        "menekankan penguasaan konsep dasar teknologi informasi, pemrograman, struktur data, "
        "basis data, dan rekayasa perangkat lunak sebagai fondasi bersama seluruh mahasiswa. "
        "Gambar berikutnya (Gambar 5.2) melanjutkan ke Semester 5--8, tempat mahasiswa "
        "mendalami topik spesialisasi (kecerdasan artifisial, jaringan, manajemen data, dan "
        "lain-lain) sebelum memasuki proyek terintegrasi, percabangan Jalur Reguler/Magang "
        "pada Semester 6, dan diakhiri dengan magang serta skripsi.\n\n"
    )

    table_intro = (
        "\n\nSebagian besar keterkaitan yang melintasi batas Semester 4--5 pada tabel "
        "berikut adalah lanjutan langsung dari mata kuliah pemrograman, basis data, "
        "atau jaringan pada Semester 1--4 menuju mata kuliah spesialisasi yang sejalan "
        "temanya pada Semester 5--6, sementara beberapa lainnya (ditandai \\emph{Perlu "
        "validasi}) merupakan kesamaan topik yang belum dinyatakan eksplisit pada RPS.\n\n"
    )

    legend = (
        "\n\n\\vspace{2mm}\n"
        "\\resizebox{0.85\\textwidth}{!}{%\n"
        "\\begin{tikzpicture}[font=\\scriptsize, ->, >={Stealth[length=1.5mm]}, thick]\n"
        "\\draw (0,0) -- (0.8,0); \\node[anchor=west] at (0.9,0) {Keterkaitan konsep terkonfirmasi};\n"
        "\\draw[dotted] (6.7,0) -- (7.5,0); \\node[anchor=west] at (7.6,0) {Perlu validasi (kesamaan topik)};\n"
        "\\draw[dashed] (13.3,0) -- (14.1,0); \\node[anchor=west] at (14.2,0) {Korekuisit (satu semester)};\n"
        "\\draw[green!40!black] (18.5,0) -- (19.3,0); \\node[anchor=west] at (19.4,0) {Jalur umum/pengembangan diri};\n"
        "\\end{tikzpicture}%\n}\n\n"
    )

    # longtblr (not plain tblr) so a 21-row table can break across the page boundary
    # instead of being pushed as one non-splittable block onto a fresh page -- the
    # latter stranded the previous page's remaining space mostly blank.
    table = (
        "\\vspace{3mm}\n"
        f"\\textbf{{Keterkaitan lintas Semester 4--5}} ({n_crossing} keterkaitan; lihat kotak bertanda "
        "$\\rightarrow$/$\\leftarrow$ pada kedua Gambar di atas):\n\n"
        "\\begin{longtblr}{width=\\textwidth,colspec={X[l,m]X[l,m]Q[l,m,3.2cm]},hlines,vlines,hspan=minimal,rowsep=2pt,colsep=3pt,row{1}={bg=headblue,font=\\bfseries},rowhead=1}\n"
        "Mata Kuliah Sumber (Semester 1--4) & Mata Kuliah Tujuan (Semester 5--8) & Jenis Keterkaitan \\\\\n"
        + "\n".join(table_rows) + "\n"
        "\\end{longtblr}\n\n"
    )

    outro = (
        r"\reviewfrompdf{Diagram jejaring kurikulum di atas adalah visualisasi baru yang "
        r"disusun dari data Deskripsi Mata Kuliah, Bahan Kajian, dan Matakuliah Syarat pada "
        r"RPS Kurikulum 2025, direpresentasikan sebagai peta keterkaitan konsep (bukan "
        r"prasyarat pendaftaran) mengingat mahasiswa menempuh satu paket mata kuliah tetap "
        r"per semester (kecuali percabangan Jalur Reguler/Jalur Magang pada Semester 6); "
        r"dokumen kurikulum 2020 tidak memiliki data digital yang setara untuk Peta Kurikulum "
        r"dan Pohon Kurikulum. Sejumlah keterkaitan (ditandai garis bertitik) disusun "
        r"berdasarkan kesamaan topik/bahan kajian, bukan pernyataan eksplisit pada RPS, dan "
        r"perlu divalidasi oleh tim kurikulum. Dipecah menjadi dua Gambar (Semester 1--4 dan "
        r"5--8) pada 2026-09-11 agar kotak mata kuliah terbaca saat dicetak; tata letak dan "
        r"penomoran kotak berubah dari versi sebelumnya, isi (59 mata kuliah + 2 gerbang SKS, "
        r"51 keterkaitan) tidak berubah.}" + "\n\n"
    )

    # Each figure is fit-scaled to the section's existing portrait geometry (see
    # PORTRAIT_WIDTH/HEIGHT) -- no landscape/pagestyle workaround needed here,
    # unlike the Peta Jalan CPL diagrams (those are wide, not tall+narrow).
    color_def = "\n\n\\definecolor{softgreen}{HTML}{D9F2DA}\n\n"

    new_text = (
        text[:start_idx] + color_def
        + intro + fig1 + bridge + fig2 + "\n\n" + table_intro + table + legend + outro
        + text[end_idx:]
    )

    with open(chapter_path, "w", encoding="utf-8") as f:
        f.write(new_text)

    return len(nodes), len(edges), n_crossing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", default=CHAPTER_PATH)
    parser.add_argument("--snapshot", default=SNAPSHOT_PATH)
    args = parser.parse_args()

    n_nodes, n_edges, n_crossing = apply_fix(args.chapter, args.snapshot)
    print(f"Regenerated Jejaring Kurikulum: {n_nodes} nodes, {n_edges} edges "
          f"({n_crossing} crossing Semester 4/5), split into 2 figures.")
    print(f"Saved to {args.chapter}")
