# Gap Analysis: 2020 Curriculum Document vs. 2025 Curriculum Book

**Method:** built with [graphify](https://github.com/sponsors/safishamsi) — the 2020 reference
PDF (`docs/Dokumen Kurikulum D4 TI 2020 OBE - compressed.pdf`, 1101 pages) was split by
chapter/lampiran and the 2025 book's narrative sources (`book/src/chapters/*.tex`,
`book/src/appendices/{01-pedoman-akademik,02-rps/index,03-penilaian/index}.tex`,
`book/main.tex`) were extracted into one knowledge graph (456 nodes, 632 edges, 19
communities). Every gap below was confirmed by a `graphify query` traversal, not
just inferred from headings — see the query evidence cited per row. Raw outputs:
`graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`.

**Refresh note (2026-07-16):** statuses below were re-verified directly against the
current `book/src/*` sources (grepping for surviving `\todoitem`/`\reviewfrompdf`
markers and reading the surrounding content) — not a full graphify re-run, since the
underlying book content has moved substantially since the original pass (new tracer
study data, new diagrams, a restructured Lampiran 3, a filled-in approval page, etc.).
Where a row's status changed, the original graphify-era note is kept for history and a
new line documents the current state.

**"Fillable" classification used throughout:**
- ✅ **Fillable from 2020** — the content physically exists in the 2020 PDF and is
  portable to 2025 (verbatim, or with a mechanical update like renamed course
  titles/codes).
- 🎨 **Fillable, but needs re-creation, not copy-paste** — the underlying data is
  available (in 2025 sources or the 2020 text), but the deliverable itself (a
  diagram, a redrawn table) doesn't exist as portable text in either document.
- ⛔ **NOT fillable from 2020 — needs fresh 2025 input** — 2020 is not an
  authoritative source for this content (it predates 2025, or the book already
  copied 2020's version and that's precisely the problem).
- ❓ **Unverified** — my corpus sample didn't include this section of the 2020 PDF;
  flagged so a follow-up pass can check it specifically.

---

## Section-by-section

### BAB I — Identitas Program Studi
**Book:** `book/src/chapters/01-identitas.tex` · **2020 source:** pages 6–8

| Item | Status | Evidence |
|---|---|---|
| Visi/Misi/Tujuan (Jurusan & Prodi) | Already populated, real content | community 15 — book & 2020 visi/misi are `semantically_similar_to` (already carried over correctly) |
| SK Pendirian PS, SK Izin Operasional, dates | ⛔ Verify, not fill | The exact 2020 values (`SK DIKTI No 50/D/O/2010`, 21 Mei 2010) are already copied into the book via `\reviewfrompdf` — copying again from 2020 changes nothing. The open question is whether these numbers changed since 2020, which only the institution (not either document) can answer. |
| Nilai Akreditasi ("B"), No. SK BAN-PT (`1810/SK-BAN-PT/AkRED/Dipl-IV/VII/2018`) | ⛔ Verify, not fill | Same as above — this is 2018-vintage data already ported from the 2020 doc; a newer accreditation cycle (if any) is external to both documents. |
| Gelar Lulusan (`S.ST`) | ⛔ Verify, not fill | Book flags: "Konfirmasi apakah gelar lulusan berubah pada kurikulum 2025" — 2020 says S.ST, cannot self-confirm whether the 2025 program kept it. |

### BAB II — Evaluasi Kurikulum dan Tracer Studi
**Book:** `book/src/chapters/02-evaluasi.tex` · **2020 source:** pages 9–28

| Item | Status | Evidence |
|---|---|---|
| Kuesioner Dosen (21 dosen), FGD Industri narrative | Already populated, real 2020 content, appropriately historical | community 6 |
| **Tracer Study Alumni** (participant counts, employment stats, charts) | ✅ **Resolved 2026-07-16 (real 2022–2024 data)** — was ⛔ NOT fillable from 2020 | *Original finding:* query `"tracer study alumni terbaru visualisasi"` showed the book's tracer-study node was the *exact same* 199-participant, 2017/2018–2019/2020 dataset as the 2020 PDF. *Current state:* `book/src/chapters/02-evaluasi.tex` now opens with a genuine, current dataset — "tracer study resmi yang dilaksanakan terhadap alumni lulusan tahun 2022, 2023, dan 2024, dengan total **344 responden**" (102 + 127 + 115 by year). The old 199-participant 2017–2020 findings are retained only as a `\reviewfrompdf`-flagged historical/qualitative supplement, explicitly not primary data anymore. Remaining gap: the new 2022–2024 survey doesn't cover hard-skill/soft-skill competency assessment, per the same marker — that specific sub-item is still open. |
| Tracer study **visualizations/charts** (2020 PDF has `Gambar 1`–`Gambar 13` per the Daftar Gambar) | ⛔ Still not fillable from 2020 (unchanged) | Same reasoning as before — the 2020 charts describe 2017–2020 alumni, not usable as 2025 visuals. The new 2022–2024 tracer data (see row above) would need its own fresh charts if desired. |

### BAB III — Landasan Perancangan
**Book:** `book/src/chapters/03-landasan.tex` · **2020 source:** pages 29–36

| Item | Status | Evidence |
|---|---|---|
| Filosofis/Sosiologis/Psikologis/Yuridis (existing four subsections) | Already populated, thin but real | hyperedge `mbkm_legal_philosophical_foundation`, community 12/14/17 |
| "Post-2020 legal bases" (`\todoitem`: check for regulation after Permendikbud 3/2020) | ⛔ NOT fillable from 2020 | By construction — the 2020 doc cannot contain post-2020 legal updates. Needs a fresh regulatory check (Permendikbud/Kepmendikbud issued 2021–2025). |

### BAB IV — Standar Kompetensi Lulusan (Profil Lulusan, CPL)
**Book:** `book/src/chapters/04-cpl.tex` · **2020 source:** pages 37–41

| Item | Status | Evidence |
|---|---|---|
| CPL01–CPL10 + CPMK tables | Already populated, real 2025 content | — |
| Profil Lulusan (4 roles: IT Project Manager, IT Team Leader, Programmer, System Analyst) | ⛔ Already sourced from 2020, needs *fresh* validation not a 2020 refill | Book's own flag: "diadopsi dari template 2020 sebagai draft awal... validasi final perlu dilakukan berdasarkan berita acara FGD atau keputusan rapat kurikulum terbaru." The 2020 doc's dosen questionnaire (community 6) actually suggests *additional* profiles beyond these 4 (QA/Tester, Technical Writer, DevOps Engineer, Data Integrator, System Implementator, ERP background) that were never folded in — worth revisiting as a specific input, but still requires a fresh 2025 FGD/decision, not a 2020 copy. |

### BAB V — Matrik Distribusi Matakuliah (matriks, peta, pohon)
**Book:** `book/src/chapters/05-matriks.tex` · **2020 source:** pages 42–45

| Item | Status | Evidence |
|---|---|---|
| Matriks BK ↔ Mata Kuliah (2025, text-table form) | Already populated | community 1/7/10 |
| **Peta Kurikulum** (§5.3) diagram | ✅ **Resolved 2026-07-16** — was 🎨 Fillable, needs re-creation | *Original finding:* the 2020 PDF pages for §5.3/§5.4 extract to almost no text — they are images, not portable text, but the underlying data (BK codes, semester distribution) already existed in the book's own §5/§6. *Current state:* `book/src/chapters/05-matriks.tex` now contains a built "diagram jejaring kurikulum" (concept map from Deskripsi Mata Kuliah/Bahan Kajian/Matakuliah Syarat in the 2025 RPS, not from 2020 — confirmed via its own `\reviewfrompdf` note that 2020 has no equivalent digital data for this), plus ten CPL "peta jalan" diagrams built directly from `docs/rti-mk-crosswalk.md`. Both still carry a `\reviewfrompdf` flag for curriculum-team validation of the depicted relationships (some edges are topic-similarity inferences, not explicit RPS prerequisites) — not a content gap anymore, but not yet formally signed off either. |
| **Pohon Kurikulum** (§5.4) diagram | ✅ **Resolved 2026-07-16** — was 🎨 Fillable, needs re-creation | Same file, same resolution as above: a "Matrik Organisasi Mata Kuliah" table (mata kuliah per semester, Jalur Reguler/Magang marked `(R)`/`(M)` for Semester 6) has been built using 2025 data, adapted from the 2020 doc's visual *concept* only (per its own `\reviewfrompdf` note) since 2020 had no portable digital source. Also still flagged for curriculum-team validation, same as the row above. |

### BAB VI — Rancangan Kurikulum Implementasi
**Book:** `book/src/chapters/06-rancangan-kurikulum.tex` · **2020 source:** pages 46–53

Fully populated with real 2025 content (semester 1–8 tables, SKS recap).

**New gap found 2026-07-16** (not present when this analysis was first written — the file
had no markers at all at that time): a `\reviewfrompdf` now flags an SKS mismatch between
the RPS and this chapter's distribution table for 5 courses. The distribution table's
values were kept (they're internally consistent with each semester's SKS total), but which
number is actually correct needs curriculum-team confirmation:

| RTI code | Course | RPS says | Distribution table says |
|---|---|---|---|
| RTI253005 | Basis Data Lanjut | 2 SKS | 3 SKS |
| RTI255008 | Administrasi dan Keamanan Jaringan | 3 SKS | 2 SKS |
| RTI256205 | Workshop Teknologi Terapan | 6 SKS | 3 SKS |
| RTI256206 | Rekayasa Sistem | 6 SKS | 3 SKS |
| RTI256207 | Teknologi Terapan | 6 SKS | 2 SKS |

This is a ⛔ **NOT fillable from 2020** item either way — it's a 2025-internal
RPS-vs-distribution consistency question, not something the 2020 document can resolve.

### BAB VII — Rekonstruksi Kurikulum
**Book:** `book/src/chapters/07-rekonstruksi.tex` · **2020 source:** pages 54–74

| Item | Status | Evidence |
|---|---|---|
| Ringkasan struktur 2018/2019/2020 rows | 🟡 **Still only one-line summaries — original recommendation not (yet) applied** | *Original finding:* query `"rekonstruksi perubahan mata kuliah narasi 2025"` surfaced full itemized 2020 detail — `7.1`/`7.2`/`7.3` each with complete "a. Dihapus / b. Berubah Nama / c. Baru" course-by-course lists. *Current state (2026-07-16):* `book/src/chapters/07-rekonstruksi.tex` still carries only a one-line `\reviewfrompdf` summary per year (e.g. 2018: "Penambahan skema magang, pengembangan karir, dan penyesuaian struktur proyek MBKM.") — the full course-by-course transcription this analysis recommended has not been done. Still ✅ **fillable from 2020** whenever that transcription work happens. |
| 2025 row / narrative (`\todoitem`) | ⛔ Still NOT fillable from 2020 (unchanged) | By construction — needs the actual 2025 curriculum-committee decision record/minutes, which postdates the 2020 document. The `\todoitem` text is unchanged: "Tambahkan narasi rekonstruksi terbaru berdasarkan dokumen keputusan atau notulensi pengembangan kurikulum 2025." |
| **New gap found 2026-07-16:** IABEE accreditation alignment | ⛔ NOT fillable from 2020 | Not present in the original pass. A `\reviewfrompdf` now states: "Penyelarasan dengan standar IABEE pada kurikulum 2025 belum didokumentasikan secara formal dalam berita acara atau keputusan rapat kurikulum yang terpisah dari dokumen ini." A companion `\todoitem` asks to confirm IABEE submission/accreditation status with the prodi before the document is final. 2020 predates IABEE alignment work entirely, so this needs fresh 2025 institutional input, same category as the row above. |

### Lampiran 1 — Buku Pedoman Akademik
**Book:** `book/src/appendices/01-pedoman-akademik.tex` · **2020 source:** pages 75–147

| Item | Status | Evidence |
|---|---|---|
| Full Visi/Misi (duplicate of BAB I, standalone document) | ✅ Fillable from 2020 | community 15 — near-identical text already exists in 2020's Lampiran 1, `semantically_similar_to` the book's own §1.2. |
| **Short Silabus / per-course descriptions** (CPL, Pokok Bahasan, Referensi) — the bulk of this Lampiran | ✅ **Resolved 2026-07-16 — but via 2025 RPS, not 2020 transcription** | *Original finding:* the 2020 PDF's Lampiran 1 contains a full per-course catalog entry (CPL + pokok bahasan + pustaka) for every 2021-curriculum course, and this was flagged as "the single biggest concrete gap," recommending those ~59 entries be transcribed and reconciled against renamed/new courses. *Current state:* `book/src/appendices/01-pedoman-akademik.tex` now has these descriptions filled in for all courses — but sourced directly from the 2025 RPS (Lampiran II), not transcribed from the 2020 document. Its own `\reviewfrompdf` explains why: "RPS 2025 adalah sumber yang lebih akurat dan terkini untuk setiap mata kuliah saat ini" — i.e. the 2020 text would have been stale/wrong for renamed or restructured courses anyway, so going straight to the current RPS was the more correct call. Net effect: the gap is closed, just not by the originally-recommended method. |

### Lampiran 2 — RPS
**Book:** `book/src/appendices/02-rps/index.tex` · **2020 source:** pages 148–697 (skipped, per plan — already embedded)

Fully populated (59 `\RPSInput` calls). No gap — out of scope for this analysis.

### Lampiran 3 — Rencana Penilaian Mata Kuliah
**Book:** `book/src/appendices/03-penilaian/index.tex` · **2020 source:** pages 698–1101 (sampled 698–720)

| Item | Status | Evidence |
|---|---|---|
| Per-course assessment plan (rubric structure: Bentuk/Metode Penilaian, Indikator/Kriteria/Bobot, Jadwal Pelaksanaan) | ✅ **Resolved 2026-07-08** | Query `"rencana penilaian rubrik indikator kriteria bobot"` confirmed the 2020 PDF has this fully fleshed out per course (e.g. `Pengujian Perangkat Lunak`, `Proyek 1`, `Kecerdasan Buatan`, each with 17-week rubric detail). At the time of this analysis, the 2025 book's Lampiran 3 was a 3-sentence redirect saying this content lived only inside the RPS (Lampiran 2). Following a subsequent restructuring request, each course's RPS+Rubric content was split into separate `- RPS.tex`/`- Rubrik.tex`/`- Tanda Tangan.tex` files (see `docs/book-todo-checklist.md`); Lampiran 3 now `\RubrikInput`s the real rubric content (RTM header + `\assessmentblock` tables) for all 59 courses in portrait, no longer a redirect stub. The standalone `make rps` build still combines RPS+Rubric+signature per course in landscape, unchanged from before. |

### Daftar Pustaka
**Book:** inline in `book/main.tex` · **2020 source:** ❓ not confirmed in this pass

| Item | Status | Evidence |
|---|---|---|
| 5 general references (Anderson & Krathwohl 2001, Bloom 1984, Permendikbud 3/2020, Perpres 8/2012, UU 12/2012) | Already populated | — |
| `\reviewfrompdf`: "Referensi umum dari dokumen template 2020 perlu ditinjau" | ❓ **Unverified — needs a follow-up pass** | The 2020 TOC lists a "DAFTAR PUSTAKA" entry, but its actual page location is ambiguous (the TOC prints "339," which doesn't match the BAB VII @ p54–74 range and likely refers to an internally-restarted page count inside a lampiran). My corpus split only covered BAB I–VII (pages 6–74) plus a 23-page sample of Lampiran 3 — the real bibliography section was not captured. **Action:** locate and extract the 2020 doc's actual Daftar Pustaka before concluding whether it's portable. |

---

## Approval page (`book/src/frontmatter/approval.tex`) — not in the 2020 doc at all

| Item | Status | Evidence |
|---|---|---|
| Nama Penyusun 1/2/3, Tanggal Pengesahan, Nama+NIP Ka. Prodi | ✅ **Resolved** (confirmed still in place 2026-07-16) | *Original finding:* the 2020 document has no equivalent signatory block (per-cycle administrative artifact); the Ka. Prodi name/NIP was already known from `subjects/*.tex` but not yet propagated to `approval.tex`. *Current state:* `book/src/frontmatter/approval.tex` is fully filled in — an 11-person Tim Penyusun list, "Diimplementasikan pada: Tahun Ajaran \CurriculumYear," a signed date ("Malang, 1 Agustus 2025"), and both signatories with name+NIP (Ketua Jurusan Mungki Astiningrum and Ketua Program Studi Dr. Ely Setyo Astuti). No remaining gap here. |

---

## Priority checklist — what to fill first

**Status as of 2026-07-16** — 3 of the original 8 items are now fully resolved and a 4th
(tracer study) is substantially resolved:

1. ~~**Approval page Ka. Prodi name/NIP**~~ — ✅ done (`approval.tex` fully filled in).
2. ~~**Lampiran 1 short-silabus course descriptions**~~ — ✅ done, sourced from 2025 RPS rather than transcribed from 2020.
3. ~~**BAB V pohon/peta kurikulum diagrams**~~ — ✅ done (jejaring kurikulum concept map + 10 CPL peta jalan diagrams + Matrik Organisasi Mata Kuliah), though still flagged for curriculum-team validation.
4. **BAB VII 2018/2019/2020 detailed change tables** — still just one-line summaries; 2020 still has the full detail ready to transcribe (see BAB VII row above). Not started.
5. **Daftar Pustaka** — still unverified; locate the actual 2020 bibliography section before deciding what's portable. Not started.
6. **BAB VII 2025 row + IABEE alignment confirmation + BAB IV profil lulusan validation + BAB III post-2020 legal check** — all genuinely need fresh 2025 institutional input; 2020 cannot help further. (IABEE alignment is a newly-found gap, added to this bucket.)
7. ~~**BAB II tracer study**~~ — 🟡 **substantially resolved**: a real 2022–2024 tracer study (344 respondents) now exists, replacing the old 2017–2020 dataset as primary data. Remaining sub-gap: the new survey doesn't cover hard-skill/soft-skill competency assessment — that piece still needs a fresh instrument, not a documentation fix.
8. **BAB I SK/akreditasi/gelar verification** — an institutional fact-check (contact the relevant office), not a document-editing task. Not started.

**New item found this pass:** **BAB VI SKS mismatch for 5 courses** (RTI253005, RTI255008,
RTI256205, RTI256206, RTI256207) between their RPS and the semester distribution table —
needs curriculum-team confirmation of which number is correct (see BAB VI row above).

## Supporting graph artifacts
- `graphify-out/GRAPH_REPORT.md` — full report (god nodes, all 19 communities, ambiguous edges, suggested questions).
- `graphify-out/graph.json` — raw graph (GraphRAG-ready), queryable via `graphify query "<question>"` after pointing `--graph` at this repo's `graphify-out/graph.json`.
- `analysis/corpus/` — the split source files used for extraction (2020-ref/ + book-2025/), kept for reproducibility; gitignored.
