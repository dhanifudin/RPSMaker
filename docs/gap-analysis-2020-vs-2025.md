# Gap Analysis: 2020 Curriculum Document vs. 2025 Curriculum Book

**Method:** built with [graphify](https://github.com/sponsors/safishamsi) — the 2020 reference
PDF (`docs/Dokumen Kurikulum D4 TI 2020 OBE - compressed.pdf`, 1101 pages) was split by
chapter/lampiran and the 2025 book's narrative sources (`book/src/chapters/*.tex`,
`book/src/appendices/{01-pedoman-akademik,02-rps/index,03-penilaian/index}.tex`,
`book/main.tex`) were extracted into one knowledge graph (456 nodes, 632 edges, 19
communities). Every gap below was confirmed by a `graphify query` traversal, not
just inferred from headings — see the query evidence cited per row. Raw outputs:
`graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`.

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
| **Tracer Study Alumni** (participant counts, employment stats, charts) | ⛔ **NOT fillable from 2020 — this is the core gap** | Query `"tracer study alumni terbaru visualisasi"` shows the book's tracer-study node is the *exact same* 199-participant, 2017/2018–2019/2020 dataset as the 2020 PDF (`Ringkasan Hasil Tracer Study (Data 2017/2018-2019/2020)` in the book ↔ `2.2 Tracer Study Alumni D4 Teknik Informatika (199 partisipan, lulusan 2017-2019)` in 2020 — same numbers, same years). The book's own `\todoitem` says this outright: "data referensi dari kurikulum 2020 dan tidak boleh digunakan sebagai data final." 2020 **is** the stale source, not a fix for it. |
| Tracer study **visualizations/charts** (2020 PDF has `Gambar 1`–`Gambar 13` per the Daftar Gambar) | ⛔ NOT fillable from 2020 | Same reasoning — the 2020 charts describe 2017–2020 alumni, not usable as 2025 visuals. |

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
| **Peta Kurikulum** (§5.3) diagram | 🎨 Fillable, but needs re-creation | Query `"pohon kurikulum peta kurikulum diagram"` confirms the 2020 PDF pages for §5.3/§5.4 extract to almost no text (just the section titles) — they are **images**, not portable text. The underlying data to redraw them (current BK codes, semester distribution) already exists in the book's own §5 and §6. This is a "build a diagram from data we already have" task, not "copy text from 2020." |
| **Pohon Kurikulum** (§5.4) diagram | 🎨 Fillable, but needs re-creation | Same as above. |

### BAB VI — Rancangan Kurikulum Implementasi
**Book:** `book/src/chapters/06-rancangan-kurikulum.tex` · **2020 source:** pages 46–53

Fully populated with real 2025 content (semester 1–8 tables, SKS recap); no `\todoitem`/`\reviewfrompdf`. No gap.

### BAB VII — Rekonstruksi Kurikulum
**Book:** `book/src/chapters/07-rekonstruksi.tex` · **2020 source:** pages 54–74

| Item | Status | Evidence |
|---|---|---|
| Ringkasan struktur 2018/2019/2020 rows | ✅ **Fillable from 2020** | Query `"rekonstruksi perubahan mata kuliah narasi 2025"` surfaces full itemized 2020 detail: `7.1 Struktur Kurikulum MBKM 2018`, `7.2 ... 2019`, `7.3 ... 2020`, each with complete "a. Matakuliah yang Dihapus / b. Berubah Nama / c. Matakuliah Baru" course-by-course lists (e.g. `Kapita Selekta`, `Proposal Skripsi`, `Sistem Terdistribusi` removed; `Magang Industri 1/2/3`, `Pengembangan Karir`, `QMS` added). The book currently only has a one-line `\reviewfrompdf` summary per year — the full detail sits unused in the 2020 PDF and can be transcribed directly. |
| 2025 row / narrative (`\todoitem` ×2) | ⛔ NOT fillable from 2020 | By construction — needs the actual 2025 curriculum-committee decision record/minutes, which postdates the 2020 document. |

### Lampiran 1 — Buku Pedoman Akademik
**Book:** `book/src/appendices/01-pedoman-akademik.tex` · **2020 source:** pages 75–147

| Item | Status | Evidence |
|---|---|---|
| Full Visi/Misi (duplicate of BAB I, standalone document) | ✅ Fillable from 2020 | community 15 — near-identical text already exists in 2020's Lampiran 1, `semantically_similar_to` the book's own §1.2. |
| **Short Silabus / per-course descriptions** (CPL, Pokok Bahasan, Referensi) — the bulk of this Lampiran | ✅ **Fillable from 2020, this is the single biggest concrete gap** | Query `"buku pedoman akademik silabus deskripsi mata kuliah"` shows the 2020 PDF's Lampiran 1 contains a full per-course catalog entry (CPL mapping + pokok bahasan + pustaka) for every 2021-curriculum course — 30+ nodes extracted (`Pancasila`, `Matematika 1`, `Big Data`, `Komputasi Awan`, `Magang Industri 1/2/3`, etc.), each already `conceptually_related_to` its 2025-book counterpart course. The book currently only ships a thin "Ringkasan Struktur Kurikulum 2021 sebagai Acuan Review" table and explicitly flags the rest as not carried over. Filling this means porting ~59 course descriptions and updating renamed/new courses (see BAB VII rename list) against the current course list. |

### Lampiran 2 — RPS
**Book:** `book/src/appendices/02-rps/index.tex` · **2020 source:** pages 148–697 (skipped, per plan — already embedded)

Fully populated (59 `\RPSInput` calls). No gap — out of scope for this analysis.

### Lampiran 3 — Rencana Penilaian Mata Kuliah
**Book:** `book/src/appendices/03-penilaian/index.tex` · **2020 source:** pages 698–1101 (sampled 698–720)

| Item | Status | Evidence |
|---|---|---|
| Per-course assessment plan (rubric structure: Bentuk/Metode Penilaian, Indikator/Kriteria/Bobot, Jadwal Pelaksanaan) | 🎨 Structure available, but book made a different (valid) design choice | Query `"rencana penilaian rubrik indikator kriteria bobot"` confirms the 2020 PDF has this fully fleshed out per course (e.g. `Pengujian Perangkat Lunak`, `Proyek 1`, `Kecerdasan Buatan`, each with 17-week rubric detail). The 2025 book's Lampiran 3 is currently a **3-sentence redirect** stating this content is embedded per-course inside the RPS (Lampiran 2) instead — which is architecturally consistent with `\assessmentblock` already appearing in every RPS file. This isn't a missing-data gap so much as an intentional restructuring; if a standalone assessment appendix (matching the 2020 layout) is still wanted, the 2020 rubric format is directly reusable as a template. |

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
| Nama Penyusun 1/2/3, Tanggal Pengesahan, Nama+NIP Ka. Prodi | ⛔ Not from 2020 (it's not a 2020 concept) — **but a quick win from repo data already on hand** | The 2020 document has no equivalent "Halaman Pengesahan" signatory block for a specific committee — this is a per-cycle administrative artifact. However, the Ka. Prodi name/NIP (Dr. Ely Setyo Astuti, S.T., M.T. / NIP. 19760515 200912 2 001) is **already known and used throughout `subjects/*.tex`** from earlier work this session — it just hasn't been propagated to `approval.tex` yet. Penyusun names and the pengesahan date still need fresh input (whoever compiled this book, and when). |

---

## Priority checklist — what to fill first

Ranked by (a) confirmed fillable-from-2020 or already-available, and (b) effort:

1. **Approval page Ka. Prodi name/NIP** — already known, zero new research needed (independent of 2020 vs 2025 question).
2. **Lampiran 1 short-silabus course descriptions** — the single largest concrete, portable gap; 2020 has full per-course CPL/pokok-bahasan/pustaka text for ~59 courses, ready to transcribe and reconcile against 2025's renamed/new courses.
3. **BAB VII 2018/2019/2020 detailed change tables** — fully present in 2020, just needs transcription from the summarized `\reviewfrompdf` stub into real tables.
4. **BAB V pohon/peta kurikulum diagrams** — data already exists in the book's own BK matrix and semester tables; needs diagram creation (TikZ or image), not new research.
5. **Daftar Pustaka** — locate the actual 2020 bibliography section (unverified in this pass) before deciding what's portable.
6. **BAB VII 2025 row + BAB IV profil lulusan validation + BAB III post-2020 legal check** — all genuinely need fresh 2025 input; 2020 cannot help further.
7. **BAB II tracer study** — the hardest and most explicitly-flagged gap; needs an actual new tracer study, not a documentation fix.
8. **BAB I SK/akreditasi/gelar verification** — an institutional fact-check (contact the relevant office), not a document-editing task.

## Supporting graph artifacts
- `graphify-out/GRAPH_REPORT.md` — full report (god nodes, all 19 communities, ambiguous edges, suggested questions).
- `graphify-out/graph.json` — raw graph (GraphRAG-ready), queryable via `graphify query "<question>"` after pointing `--graph` at this repo's `graphify-out/graph.json`.
- `analysis/corpus/` — the split source files used for extraction (2020-ref/ + book-2025/), kept for reproducibility; gitignored.
