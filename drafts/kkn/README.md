# KKN Tematik (Kuliah Kerja Nyata Tematik) — draft RPS, three concept versions

**Status: draft for comparison only.** Not wired into the 2025 curriculum yet —
`docs/rti-mk-crosswalk.md`, `docs/kurikulum-2025-distribusi-mk.md`, and the book
chapters/appendix are all untouched. Nothing here is picked up by `make rps` or
`make book` (both only scan `subjects/` and `book/`, respectively).

## Dasar (why KKN Tematik is now mandatory)

`docs/nota-dinas-kurikulum-kkn.pdf` — **Nota Dinas Wakil Direktur I No.
11/WADIR I/KM/2026** (15 Jan 2026, basis Permendiktisaintek No. 39 Tahun 2025 tentang
SPMPT), effective Semester Ganjil T.A. 2026/2027 for all angkatan — mandates, at
point (d): **"Kuliah Kerja Nyata Tematik sebanyak 2 sks di Semester Ganjil atau
Genap bagi Prodi Sarjana Terapan."** It sits in the same IKU "kegiatan mahasiswa di
luar Prodi" bucket as Penelitian/Proyek Independen/Magang Penelitian (point d, first
bullet). This fixes the course's name (**Kuliah Kerja Nyata Tematik**, not plain
"KKN"), its SKS (**2**, not a free 2–3 choice), and its mandatory status; semester
(Ganjil or Genap) is left to the Prodi.

KKN Tematik does not exist in the current 2025 curriculum build. It was a course in
the legacy 2019/2020 curriculum (`RTI207003`, "KKN Tematik", an MBKM "hak belajar"
option) but was dropped when the 2025 rebuild consolidated off-campus/fieldwork into
**Magang** (`RTI257001`, Semester 7, 20 SKS). The Nota Dinas now requires bringing it
back as its own course. These three drafts model *what it should actually teach* —
the directive mandates the course exists, not its pedagogical emphasis.

> **Broader compliance flag (out of scope here):** the same Nota Dinas caps Prodi
> Sarjana Terapan at **144–150 SKS total** and Semester 1–2 at 20 SKS each. The
> current 2025 D4 TI curriculum is ~152 SKS (`docs/kurikulum-2025-distribusi-mk.md`,
> S1/S2 = 21 SKS each) — already over cap before adding KKN Tematik's +2 SKS. Points
> (e)–(g) of the Nota Dinas (penciri-Polinema courses, *capstone design*, *basic
> science* ≥6 SKS, Tugas Akhir SKS bounds) add further curriculum-wide obligations.
> Full compliance implies a curriculum-wide SKS rebalance — a separate, larger task,
> not folded into this KKN RPS work.

## Provisional identity (shared by all three drafts)

| Field | Value | Note |
|---|---|---|
| Nama | Kuliah Kerja Nyata Tematik | Per Nota Dinas point (d); formal name, not just "KKN". |
| Kode | `RTI257002` | Placeholder — sits as a fieldwork sibling of Magang (`RTI257001`); the real code and semester slot are decided when a version is chosen and integrated. |
| SKS | 2 SKS / 4 jam per minggu | Fixed by the Nota Dinas (was a guessed 3 SKS before the directive was found); same 2 jam/SKS/minggu ratio as Magang's 20 SKS/40 jam. |
| Semester | 6/7 (provisional) | Nota Dinas allows Ganjil *or* Genap for Prodi Sarjana Terapan — Prodi's choice. Real slot decided later, together with the SKS-cap rebalance above. |
| Struktur mingguan | 16 minggu | Pembekalan → observasi/analisis kebutuhan mitra → penyusunan proposal → seminar proposal (wk 5) → pelaksanaan → monev tengah (wk 8) → lanjutan pelaksanaan → laporan → seminar hasil (wk 16). Kept as 16 weekly rows relabeled to 2 SKS (estimasi waktu trimmed from 3 to 2 jam tatap muka in weeks 1–2) rather than restructured into a block/period format. |
| Matakuliah Syarat | Lulus minimal 90 SKS | Placed mid-late program, before Magang's 120-SKS gate. |

All three share the identical **weekly Bobot Penilaian** distribution (by week/moment,
sums to 100): `2,2,3,5,15,3,3,15,3,3,3,3,5,5,5,25`. They differ in *what* each week
and rubric block is grading — the CPL/CPMK anchors and assessment forms below.

## The three versions

| | **A — Solusi TI** | **B — Pengabdian & Sikap** | **C — Seimbang** |
|---|---|---|---|
| Folder | `A-solusi-ti/` | `B-pengabdian-sikap/` | `C-seimbang/` |
| Focus | Deliver a working IT artifact/system to the partner | Social responsibility, engagement, teamwork, communication — impact over artifact | Both community engagement *and* a concrete deliverable, weighted evenly |
| CPL-Prodi | CPL01, CPL03, CPL06, CPL08 | CPL01, CPL03, CPL08 | CPL01, CPL03, CPL06, CPL08 |
| CPMK | CPMK0101, CPMK0301, CPMK0803, CPMK0607 | CPMK0101, CPMK0102, CPMK0301, CPMK0302 | CPMK0102, CPMK0301, CPMK0803, CPMK0607 |
| Rubric blocks (bobot) | Proposal Program Kerja (15) · Produk/Solusi TI (40) · Laporan KKN (25) · Seminar Hasil (20) | Proposal Program Kerja (20) · Logbook & Keterlibatan Sosial (30) · Penilaian Mitra/DPL (25) · Laporan & Seminar Hasil (25) | Proposal Program Kerja (20) · Pelaksanaan & Keterlibatan (30) · Luaran KKN (20) · Laporan & Seminar Hasil (30) |
| Week 16 luaran | Solusi TI berjalan + laporan | Dampak sosial + laporan | Luaran KKN (TI dan/atau kegiatan) + laporan |

### CPL/CPMK reasoning (why these anchors)

Modeled on **Magang** (`subjects/RTI257001-magang/`), the closest existing analog
(CPL01/03/06/08 → CPMK0301/0303/0804/0607), extended with **CPMK0102** (tanggung
jawab sosial, under CPL01) and **CPMK0302** (manajemen tim, under CPL03) to
foreground the community/teamwork emphasis a fieldwork-service course needs beyond
Magang's industry-placement framing. CPL06/CPMK0607 (delivering a real solution) is
included only in versions where a concrete artifact is graded (A, C) — version B
deliberately excludes it since its luaran is social impact, not a technical product.

All six CPMK codes used (`CPMK0101`, `CPMK0102`, `CPMK0301`, `CPMK0302`,
`CPMK0607`, `CPMK0803`) are genuine, pre-existing entries in
`book/src/chapters/04-cpl.tex` — no new CPMK was invented. **The CPMK row text in
each `- RPS.tex` CP block quotes Ch4 verbatim, unmodified** — CPMK is a shared,
program-level statement and should read identically wherever it's cited. Only the
**Sub-CPMK** rows (`SCPMK…-060xx`) are tailored to the KKN/fieldwork context — that
tailoring is what Sub-CPMK exists for. Do not reintroduce paraphrased CPMK text if
this file is edited further.

## How to build each PDF

From the repo root (paths use spaces/parentheses — quote them):

```sh
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory "drafts/kkn/A-solusi-ti" \
  "drafts/kkn/A-solusi-ti/KKN (A) Solusi TI.tex"

pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory "drafts/kkn/B-pengabdian-sikap" \
  "drafts/kkn/B-pengabdian-sikap/KKN (B) Pengabdian dan Sikap.tex"

pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory "drafts/kkn/C-seimbang" \
  "drafts/kkn/C-seimbang/KKN (C) Seimbang.tex"
```

Each produces a 5-page PDF: RPS identity + CP header + penilaian matrix (p.1),
16-week plan (p.2–3), RTM/rubric blocks (p.4–5), signature block (last page). All
three have been verified to compile cleanly with weights summing to 100 throughout.

## What's deliberately NOT here

- `meetings/*.md` and `rubrics/*.md` mirrors — authored later, only for the chosen
  version, once it has its final course code.
- Any edit to `docs/rti-mk-crosswalk.md`, `docs/kurikulum-2025-distribusi-mk.md`,
  `book/src/chapters/**`, or `book/src/appendices/01-pedoman-akademik.tex` — that
  wiring (real course code, semester slot, SKS-total impact, CPL peta-jalan diagram
  placement) is a separate follow-up task once a version is picked.
- A decision on which version to adopt — that's for the department to make.

## Next step

Pick A, B, or C (or ask for a blend). Once decided, the follow-up task is: assign
the real course code/semester, move the package into `subjects/RTI2…-kkn/`, add
`meetings/*.md` + `rubrics/*.md`, and wire it into the crosswalk + book chapters.
