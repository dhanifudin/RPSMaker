# Sub-CPMK Wording Review (for IABEE Accreditation)

**Scope:** wording quality of Sub-CPMK (kemampuan akhir tiap tahapan belajar) statements in
`docs/cpl-cpmk-subcpmk.xlsx`, and whether each Sub-CPMK actually relates to the course's own
Materi Pembelajaran / Bahan Kajian — the constructive-alignment link IABEE assessors check
directly. This was originally a recommendations-only review; the code-level defects in §1
(duplicate codes, fixable orphan codes) have since been **applied** to the workbook by
`scripts/fix_subcpmk_metode_codes.py` — see the status note at the top of §1. The wording
rewrites in §2/§5 remain recommendations only; no prose text was changed.

**Sheets read:** `MK-CPMK-SubCPMK-Metode` (the only sheet where Sub-CPMK prose actually lives),
`MK-CPMK-SubCPMK` (the intended canonical sheet), `CPL-CPMK` (master CPMK list), `Audit Findings`
(prior code-validity audit — cited, not re-derived). Cross-checked against the published RPS
convention in `subjects/RTI251006-dasar-pemrograman/… - RPS.tex` and
`subjects/RTI252006-basis-data/… - RPS.tex`.

---

## Headline numbers

| Metric | Count |
|---|---|
| Rows in canonical `MK-CPMK-SubCPMK` sheet | 1,047 |
| …of which Sub-CPMK code + text is **empty** | 1,039 (99.2%) |
| Rows in draft `MK-CPMK-SubCPMK-Metode` sheet | 1,150 |
| …of which Sub-CPMK text is filled | 198 |
| Filled Sub-CPMK that are **auto-generated boilerplate** (see §1) | 86 (43%) |
| …of those, rows missing a `Kode SubCPMK` altogether | 30 |
| Hand-written rows also missing a `Kode SubCPMK` (separate defect, see §1) | 6 |
| Remaining "hand-written" Sub-CPMK (198 − 86) | 112 |
| …starting "Mahasiswa mampu …" vs "Mampu …" | 0 vs 198 (resolved, see §0d) |
| Rows with an unmeasurable verb (memahami/mengetahui/mengerti/mengenal) | 6+ |
| Rows with a tautological doubled verb ("X dan X") | 4 |
| Courses whose RPS uses inline Bloom brackets `[Cx, Ax, Px]` | ~4 of 59 |

**Bottom line:** the wording problem is not primarily "a few awkward sentences" — it's that
**43% of the only Sub-CPMK text that exists in this workbook was mechanically generated** by
truncating the parent CPMK description and appending a template tail, rather than being authored
as a distinct, assessable Sub-CPMK. Fix the generation defect first; the remaining hand-written
rows need a smaller, more conventional wording clean-up.

---

## 0. Code-level fixes applied

Two passes were run against the workbook. The first pass (`scripts/fix_subcpmk_metode_codes.py`)
fixed 3 apparent collisions and filled 26 orphan rows, but used the wrong rule to pick each new
code's trailing serial (it picked "next free serial for this specific CPMK", usually `01`). The
**real, documented convention** (`docs/rti-mk-crosswalk.md`: `SCPMK<cpmk>-<MKnum3digit><seq2digit>`)
is that the serial is **one running counter per course across all of that course's CPMKs** — not
per-CPMK. Checking the first pass against every affected course's actual published
`subjects/*/…-RPS.tex` found that **every one of the 26 orphan fills, plus 2 of the 3 collision
fixes, collided with a real, already-published Sub-CPMK code** — worse than the original empty
cell, since the sheet then visibly contradicted the published curriculum. A second pass
(`scripts/fix_subcpmk_metode_codes_v2.py`) corrected all of it, anchored to each course's real
published maximum serial. Final, verified state:

- **1 duplicate-code cell was a genuine collision needing correction twice**: `SCPMK0706-03101`
  (Kecerdasan Artifisial) was reused for 3 different statements. The untouched 4th row in that
  course's block already legitimately owns serial `02` (`SCPMK1005-03102`, matching the real
  published RPS) — so rows 105/106 are now `SCPMK0706-03103`/`…-03104`, continuing past it,
  not `…-03102`/`…-03103` as the first pass had it.
- **1 duplicate-code cell needed a full re-derivation, not just a renumber**: `SCPMK0102-00101`
  was shared by Pancasila (row 2, correct) and a mislabeled Komunikasi Dan Etika Profesi row
  (row 156). The first pass's `…-00102` collided with Pancasila's own real, published 2nd
  Sub-CPMK. Root cause: Komunikasi Dan Etika Profesi's whole draft block (rows 155–158) used
  Pancasila's course-prefix (`001`) instead of its own (`045`). Cross-checked all 4 rows against
  the master `CPL-CPMK` sheet: row 155 (CPMK0101) is published for this course → corrected to
  the real code `SCPMK0101-04501`; row 156 (CPMK0102) is validly assigned to this course but
  unused in the final RPS → given a provisional code continuing the real sequence,
  `SCPMK0102-04504`; rows 157/158 (CPMK0313/CPMK0314) don't exist anywhere in the master list —
  left untouched (still carry the wrong `001` prefix), flagged for a curriculum-owner decision
  alongside the 10 rows below, not mechanically fixed.
- `SCPMK0502-01303`, used 3x for Sistem Operasi, was correctly left alone both passes — confirmed
  against the published RPS as one Sub-CPMK legitimately spanning three weekly sessions, not a
  collision. (Rows 41/42 do have byte-identical Sub-CPMK *text* though, which looks like an
  unrelated copy-paste content issue — flagged, not fixed here.)
- **26 orphan (missing-code) rows**, all re-verified against their course's published RPS and
  corrected to continue past that course's real maximum serial (e.g. Manajemen Proyek's real
  Sub-CPMK run `01`–`04`, so its new draft-only Sub-CPMK became `05`, not `01`). Full per-row
  before/after table is in `scripts/fix_subcpmk_metode_codes_v2.py`'s `CORRECTIONS` dict.
- **10 rows deliberately left empty**: their Kode CPMK doesn't exist anywhere in the master
  `CPL-CPMK` list (Bahasa Indonesia CPMK0307/0308, Kewirausahaan Berbasis Teknologi
  CPMK0311/0312, Proyek Teknologi Terintegrasi CPMK0317/0318, Magang CPMK0319/0320, Skripsi
  CPMK0321/0322). Assigning a Sub-CPMK code to these would embed a fabricated CPMK reference —
  this needs a curriculum-owner decision on which real CPMK each should remap to before a code
  can be assigned (see the `metode-sheet-cpmk-column-findings` note on the CPL03 cluster).

**Verified**: zip integrity intact; zero exact-duplicate codes remain in the draft sheet except
the confirmed-legitimate `SCPMK0502-01303`; zero collisions between any draft code and any real
published code across all 13 affected courses; 188 non-empty / 10 empty `Kode SubCPMK` cells,
matching the corrected plan exactly.

## 0b. Full-sheet code-format normalization (`fix_subcpmk_metode_codes_v3.py`)

A follow-up pass verified **every** non-empty `Kode SubCPMK` cell (188 total) against the
documented format `SCPMK<cpmk>-<MKnum3digit><seq2digit>` (`docs/rti-mk-crosswalk.md`). This
found 54 more non-conforming codes beyond what the prior passes had touched:

- **14 malformed-length codes**, not matching the pattern at all: `MK003` (2 rows) and `MK029`
  (6 rows) had a 3-digit serial instead of 2-digit (e.g. `SCPMK0208-029001`); `MK051` (6 rows)
  was missing the 3-digit course-number segment entirely (e.g. `SCPMK0905-01`).
- **30 well-formed-but-wrong-prefix codes**: `MK009`, `MK014` (10 rows), `MK023` (2 rows),
  `MK024` (2 rows), `MK035`, `MK036` (11 rows), `MK045` (rows 157/158), `MK047` embedded a
  *different* course's number than their own (confirmed against each row's own `Kode MK`/
  `Nama MK` columns, which match `docs/rti-mk-crosswalk.md` in every case). Notably, `MK014`'s
  wrong `050`-prefixed rows had been **byte-for-byte colliding, right now, with `MK050` Big
  Data's own real published codes** — this pass resolved that collision as a side effect.
- **10 of those 40 needed no fix**: the Magang/Skripsi rows mislabeled `MK053`/`MK054` (see §0
  above) already correctly embed `057`/`058` — confirmed, not re-touched.
- **MK045 rows 157/158** (`CPMK0313`/`CPMK0314`, previously left untouched entirely): this pass
  corrects *only* the course-number segment (`001`→`045`); the underlying CPMK0313/0314
  validity question (neither exists in the master `CPL-CPMK` list) remains open, same as the 10
  already-flagged rows — confirmed in-scope for the prefix fix specifically before applying.

All 44 corrections reprefix to the row's own correct course number and assign a serial
strictly past that course's real published maximum — never reusing a real serial, even for a
CPMK that might plausibly match a specific published position (content alignment can't be
assumed; see §3a's Fisika example). One self-caught issue during verification: the first
attempt at `MK035` row 114 landed on `SCPMK0902-03503`, which turned out to equal `MK024`
Metode Numerik's own real *published* code (see the new finding below) — corrected to
`SCPMK0902-03505` to clear it.

**New finding: `MK024`'s own published RPS has a pre-existing numbering bug**, independent of
this workbook — `subjects/RTI253006-metode-numerik/…-RPS.tex` uses course-number segment `035`
(Statistik Komputasi's number) instead of its own `024` for all 4 of its codes. Two of those
four are consequently byte-for-byte identical to `MK035`'s own real codes. Out of scope for the
xlsx fix (can't edit published `.tex` here), but worth a dedicated follow-up alongside the
already-known `MK044` published-RPS numbering bug below.

**Verified**: zip integrity intact after every edit; full-sheet re-scan shows **zero** malformed
codes and **zero** unexplained prefix mismatches remaining (188/188 conform, aside from the
documented Magang/Skripsi label exception and the 10 still-empty flagged rows); zero
unintended collisions against real published codes for every one of the newly-touched courses.

Also observed but **not** touched (out of scope for this pass):
- `MK044`'s own **published** RPS (`subjects/RTI255008-…/…-RPS.tex`) has a pre-existing numbering
  bug independent of this workbook: three codes (`SCPMK0501-04401`, `…0502-04401`, `…0505-04401`)
  all claim serial `01` before `…0505-04402` continues correctly. Worth a separate follow-up.
- `MK024`'s published RPS numbering bug (see above) — same class of issue, also worth a
  follow-up, ideally addressed together with the `MK044` one.
- **`MK023` Basis Data Lanjut's published RPS has this same bug too** — a full-corpus recheck
  (below) found all 4 of its published codes use course-number `016` (Praktikum Basis Data's
  number) instead of its own `023`, colliding with Praktikum Basis Data's real codes. This means
  the draft sheet's row 78 (`SCPMK0203-02301`, left untouched by the v3 pass as "already
  correct") uses the *structurally correct* number but does **not** literally match what's
  actually published — consistent with how `MK024` was handled (workbook uses the correct
  number; the published `.tex` bug is a separate, unaddressed problem). Three courses now show
  this exact bug class: `MK023`, `MK024`, `MK044`.
- `MK053`/`MK054` rows in the draft sheet are mislabeled (they're actually Magang/`MK057` and
  Skripsi/`MK058` per `docs/rti-mk-crosswalk.md`) — confirmed harmless since the *codes* already
  used the correct `057`/`058` prefix and neither collides with the real MK053 (Proyek Inovasi)
  or MK054 (Workshop Teknologi Terapan) courses' own published codes. Only the "Kode MK" label
  text is stale; not fixed in this pass.

## 0c. Full-corpus consistency recheck

Re-verified everything above independently, at full scale, rather than trusting the
per-course spot checks from earlier passes:
- Collected every `SCPMK\d{4}-\d{5}` token from all 59 courses' published `subjects/*/…-RPS.tex`
  files (200 distinct codes) and checked which are claimed by more than one course folder — found
  exactly the 3 already-documented published-RPS bugs (`MK023`↔`MK016`, `MK024`↔`MK035`) plus
  confirmed no others exist anywhere in the corpus.
- Cross-checked all 188 draft-sheet codes against all 200 published codes: 88 draft codes happen
  to equal some real published code; of those, **85 correctly belong to that same course, and the
  remaining 3 are the already-documented Magang/Skripsi label exceptions — zero genuine
  cross-course mismatches** across the entire sheet, not just the rows touched by prior passes.
- Re-ran the internal-duplicate and format/prefix scans on the current state: 188 non-empty
  codes, 0 malformed, 0 unexplained prefix mismatches, 1 confirmed-legitimate internal duplicate
  (`SCPMK0502-01303`, the multi-week Sistem Operasi code).

## 0d. Wording fix: dropped "Mahasiswa" as the leading word (`fix_subcpmk_metode_wording_mahasiswa.py`)

The first-round §2A finding tentatively recommended standardizing on "Mahasiswa mampu" (the
majority stem at the time, 63 vs 49 among hand-written rows). The curriculum owner made the
**opposite, explicit call**: no Sub-CPMK statement should start with "Mahasiswa" at all.

A pre-fix scan of the (by-then code-normalized) sheet found **149 of 198** filled Sub-CPMK text
cells started with "Mahasiswa" — 147 as `"Mahasiswa mampu …"` (→ `"Mampu …"`) and 2 as
`"Mahasiswa mengetahui/mengerti …"` (→ `"Mengetahui/Mengerti …"` — the already-flagged weak-verb
rows in §2B; this pass only removed the leading subject, it didn't upgrade those verbs). Applied
via a single generic regex substitution (rather than 149 hand-transcribed before/after pairs,
which would be verbose and error-prone for a purely mechanical, uniform transform) across
**every** filled row, including the 86 rows already flagged in §1 as needing a full content
rewrite — removing the wrong leading subject is correct and additive regardless of what else is
still wrong with those cells.

**Not touched:** 4 mid-sentence (non-leading) "Mahasiswa" occurrences (rows 24, 76, 162, 174) —
a second "Mahasiswa mampu…" clause appearing after a period or bullet inside one cell. These
need splitting into separate Sub-CPMK, not a prefix strip — folded into the existing §2C
bundled-multi-competency finding, still open.

**Verified**: zip integrity intact; re-scan shows 0 cells still start with "Mahasiswa" (down from
149) while the 4 mid-sentence occurrences remain exactly as before; total filled-cell count
unchanged at 198 (text-only edit, no rows added/removed); spot-checked several cells including
both weak-verb rows via the scratchpad reader.

**House style is now settled**: `Mampu <verb>…`, no explicit subject — see the updated §4.

---

## 1. Auto-generated / truncated Sub-CPMK (the dominant defect)

86 of the 198 filled Sub-CPMK cells follow one template:

> `Mahasiswa mampu [VERB1] [ …CPMK description, cut wherever it ran out… ], sesuai konteks {Course Name} dan capaian {CPMK code}.`

The tail `sesuai konteks … dan capaian CPMKxxxx` is boilerplate, not a real qualifying
clause — the sentence before it is frequently cut mid-phrase, leaving dangling commas and
incomplete clauses:

- `SCPMK0206-01302` (Sistem Operasi): *"…lalu merancang strategi manajemen sumber daya sistem
  (seperti memori, proses, sesuai konteks Sistem Operasi dan capaian CPMK0206."* — cut off
  before finishing the parenthetical list.
- `SCPMK0203` row (Sistem Informasi Manajemen): *"…menerapkan konsep perancangan perangkat lunak
  menggunakan UML secara tepat berdasarkan prosedur baku, dan sesuai konteks…"* — trailing "dan"
  with nothing after it.
- Two rows even paste a doubled, tautological verb from the generator prepending a verb onto an
  already-verb-led CPMK description: `SCPMK0706-04001` *"Mahasiswa mampu **mengevaluasi
  memahami** konsep dasar pembelajaran mesin…"*, and a Manajemen Proyek row *"Mahasiswa mampu
  **mengimplementasikan memahami** fase pelaksanaan proyek…"*.
- `SCPMK0901-01301` / `SCPMK0901-03202` repeat the identical verb: *"Mahasiswa mampu
  **menganalisis dan menganalisis** cara kerja sistem komputer…"* — nonsensical duplication.
  Two further rows do the same with "mengimplementasikan dan mengimplementasikan".
- `SCPMK0706-03101` (Kecerdasan Artifisial) is truncated to a single stray letter: *"Mahasiswa
  mampu menganalisis **q** sesuai konteks Kecerdasan Artifisial dan capaian CPMK0706."* This is
  also a **duplicate-code** case: `SCPMK0706-03101` is reused for two *other*, properly-written
  Sub-CPMK in the same course ("Mampu menjelaskan konsep dasar kecerdasan artifisial serta
  menganalisis persoalan…" and "Mampu merancang representasi pengetahuan dan model agen
  cerdas…") — three different statements sharing one code is a data-integrity bug on top of the
  wording defect; each Sub-CPMK needs its own unique code before the text can even be fixed.
- 30 of these 86 boilerplate rows don't carry a `Kode SubCPMK` at all — orphan text with no code
  to reference from a weekly RPS table. A further 6 rows elsewhere in the sheet are hand-written,
  non-boilerplate Sub-CPMK that are *also* missing a code (e.g. "Menerapkan konsep inheritance
  dalam pemodelan kelas…", "Mampu membangun infrastruktur jaringan aman melalui desain
  arsitektur…") — well-written text that simply can't be cited from a weekly table until a code
  is assigned.

**Recommendation:** treat all 86 rows as **not yet authored**, not as "needing wording polish."
Each must be rewritten from scratch as a standalone, complete Sub-CPMK sentence per the standard
in §3 — using the parent CPMK's full (untruncated) statement as the source of the competency,
not the truncated fragment. Do not keep the "sesuai konteks … dan capaian CPMKxxxx" tail in any
rewritten version — the code already links the row to its CPMK; restating it in prose is
redundant and is what produced the truncation bug in the first place.

## 2. Wording defects in the hand-written rows (112 rows)

- **A — Inconsistent stem. RESOLVED (see §0d).** Was 63 "Mahasiswa mampu …" vs 49 "Mampu …" (no
  explicit subject) among the hand-written rows (149 vs 49 across all 198 filled rows). This
  mirrored an inconsistency already present at course level in the published RPS: Dasar
  Pemrograman uses "Mahasiswa mampu…" (`RTI251006 … - RPS.tex` lines 19–22); Basis Data uses
  "Mampu…" (`RTI252006 … - RPS.tex` lines 19–20) — that inconsistency in the *published* RPS
  files themselves is unchanged, out of scope for the xlsx fix. The curriculum owner has settled
  on dropping "Mahasiswa" for the workbook; `scripts/fix_subcpmk_metode_wording_mahasiswa.py`
  applied this to all 149 affected cells.
- **B — Unmeasurable verbs.** `SCPMK0101-00802`: *"Mahasiswa **mengetahui** perundang-undangan
  yang menjadi dasar semua kebijakan…"*; `SCPMK0101-00803`: *"Mahasiswa **mengerti** lingkup
  kesehatan, lingkungan, keselamatan…"*. Neither verb names an observable action an assessor can
  score.
- **C — Bundled multi-competency.** `SCPMK0902-00601` (Fisika) states two separate abilities in
  one Sub-CPMK: *"…dalam sistem informasi. **Mahasiswa mampu** mengidentifikasi, menganalisis
  fakta dan opini…"* — should be split into two Sub-CPMK, each with its own code and assessment.
- **D — Bloom bracket used inconsistently.** Only Dasar Pemrograman-style RPS append `[C2, A3]` /
  `[C4, A3, P2]` after the Sub-CPMK sentence; ASD and Basis Data RPS carry no bracket at all. Pick
  all-or-none program-wide (see §3).

## 3. Sub-CPMK ↔ Materi Pembelajaran mismatch (constructive-alignment gap)

This is the check IABEE cares about most directly: does the Sub-CPMK a student is assessed
against actually correspond to what was taught that week? Two confirmed cases:

### 3a. Fisika (MK009) — cross-course copy-paste

`SCPMK0902-00601`'s Sub-CPMK text is entirely about **discrete math / logic / sets**:

> *"Mahasiswa mampu menerapkan konsep diskrit, logika, himpunan, dan fungsi matematika dasar
> dalam sistem informasi…"*

but its Materi Pembelajaran is entirely **classical physics**:

> *"1. Hakikat dan Ruang Lingkup Fisika … 4. Kinematika Gerak Lurus dan 2 Dimensi … 6. Usaha dan
> Energi … 8. Medan listrik dan gaya Coulomb …"*

Cause: CPMK0902 ("prinsip matematis dan struktur diskrit…") is shared by Fisika, Matematika
Dasar, and Aljabar Linier. The Sub-CPMK text was written once for the math courses and copied
into Fisika's row without being reworded to match Fisika's own materials — Aljabar Linier's
`SCPMK0902-011xx` rows, by contrast, do correctly describe matrix/vector content matching their
own Materi.

### 3b. Proyek Sistem Informasi (MK036) — systemic, not one-off

Every Sub-CPMK in this course is generic software-engineering competency prose, while every
Materi cell is a single PMBOK knowledge-area label — and the two don't correspond row-by-row:

| Kode SubCPMK | Sub-CPMK topic | Materi (same row) |
|---|---|---|
| `SCPMK0602-00102` | merancang arsitektur & komponen perangkat lunak (design patterns) | *Resource Management & Procurement Management* |
| `SCPMK0802-00102` | merancang & mengevaluasi UI/UX, SQA | *Cost Management, Quality Management* |
| `SCPMK0803-00101` | menggunakan tools manajemen proyek | *Communications Management & Risk Management* |
| `SCPMK1008-00101` | mengintegrasikan hasil analisis & desain sistem | *Project Closure* |

Software-architecture and UI/UX outcomes are paired against project-management knowledge areas
that share no topic overlap. Either the Sub-CPMK column or the Materi column for this course was
populated from a different template than the other and the two were never reconciled — this
needs a course-owner decision on which column is correct, then the other rewritten to match.

**Recommendation:** run this same manual cross-check (Sub-CPMK topic vs. same-row Materi topic)
for every course before submission — automated keyword-overlap scoring was tried and produces
too many false positives (RPS style intentionally uses abstract competency prose against a
concrete topic-keyword Materi list, e.g. "struktur data non-linear" ↔ "Tree, BST" is a *correct*
pairing despite zero shared words), so this check needs a human reader, not a script.

---

## 4. Recommended house-style standard

1. **Stem:** `Mampu ` + one operational verb — **no leading "Mahasiswa"** — applied to every
   Sub-CPMK program-wide (updated from this doc's original draft recommendation of "Mahasiswa
   mampu"; the curriculum owner made the opposite call — see §0d. Already applied to all 149
   affected cells in the workbook).
2. **One competency per Sub-CPMK**, phrased ABCD (Audience–Behavior–Condition–Degree). Split any
   sentence joined by ". Mahasiswa" or a mid-sentence second clause into two coded Sub-CPMK (4
   such mid-sentence occurrences remain — rows 24, 76, 162, 174 — left untouched by the stem fix
   since they need splitting, not just prefix removal).
3. **Verb bank:** use Bloom's revised taxonomy (Anderson & Krathwohl 2001 — already cited as a
   reference in `docs/gap-analysis-2020-vs-2025.md`). Replace banned non-measurable verbs:

   | Banned (unmeasurable) | Use instead |
   |---|---|
   | memahami | menjelaskan, menguraikan, menerapkan |
   | mengetahui | menyebutkan, mengidentifikasi |
   | mengerti | menguraikan, menjelaskan |
   | mengenal | menjelaskan, mengidentifikasi |

4. **No boilerplate tail.** Never restate "sesuai konteks {MK} dan capaian {CPMK}" in the
   sentence — the row's Kode CPMK / Kode MK columns already carry that link.
5. **Cognitive level of a Sub-CPMK ≤ its parent CPMK.** A sub-step cannot claim a higher Bloom
   level than the outcome it supports.
6. **Constructive alignment check:** before publishing, every Sub-CPMK must trace to (a) actual
   rows in that course's own Materi Pembelajaran, and (b) an Indikator/Bentuk Penilaian that can
   observe the verb used. Do this as a manual read, not a keyword script (see §3b note).
7. **Bloom bracket `[Cx, Ax, Px]`:** apply to every Sub-CPMK across all 59 courses, or drop it
   everywhere — the current ~4-course partial use looks inconsistent to an assessor.
8. **Code format:** keep the existing `SCPMK<CPMK 4-digit>-<sequence 5-digit>` convention already
   used in the published RPS weekly tables — it doesn't need to change.

---

## 5. Before / After examples

*Note: these examples predate the §0d stem decision and illustrate other defects (truncation,
tautology, weak verbs, bundling) — their "Before" text reflects the pre-§0d state (still has
"Mahasiswa"), and their "After" text should additionally drop any leading "Mahasiswa" per the
now-settled house style, if these particular cells are ever content-rewritten.*

**Truncated boilerplate (Sistem Operasi, `SCPMK0206-01302`)**
- Before: *"Mahasiswa mampu merancang karakteristik dan kebutuhan sumber daya dari aplikasi
  multi-platform, lalu merancang strategi manajemen sumber daya sistem (seperti memori, proses,
  sesuai konteks Sistem Operasi dan capaian CPMK0206."*
- After: *"Mahasiswa mampu merancang strategi manajemen sumber daya sistem (memori, proses, dan
  penjadwalan) untuk aplikasi multi-platform."*

**Doubled/tautological verb (`SCPMK0901-01301`)**
- Before: *"Mahasiswa mampu menganalisis dan menganalisis cara kerja sistem komputer beserta
  komponen utamanya sesuai konteks Sistem Operasi dan capaian CPMK0901."*
- After: *"Mahasiswa mampu menganalisis cara kerja sistem komputer beserta komponen utamanya."*

**Corrupted stray-letter fragment (Kecerdasan Artifisial, code collision on `SCPMK0706-03101`)**
- Before: *"Mahasiswa mampu menganalisis q sesuai konteks Kecerdasan Artifisial dan capaian
  CPMK0706."*
- After: assign a new, unused code (e.g. `SCPMK0706-03103`, since `…-03101` and presumably
  `…-03102` are already taken by the other two Sub-CPMK under this CPMK) and rewrite as a
  distinct third competency, not a duplicate of its siblings — e.g. *"Mahasiswa mampu
  mengevaluasi kinerja model kecerdasan artifisial sederhana menggunakan metrik yang sesuai
  dengan domain permasalahan."*

**Unmeasurable verb (`SCPMK0101-00802`)**
- Before: *"Mahasiswa mengetahui perundang-undangan yang menjadi dasar semua kebijakan yang
  berhubungan dengan keselamatan dan kesehatan kerja."*
- After: *"Mahasiswa mampu mengidentifikasi perundang-undangan yang menjadi dasar kebijakan
  keselamatan dan kesehatan kerja."*

**Bundled two-in-one (Fisika, `SCPMK0902-00601`) — also fixes the Materi mismatch from §3a**
- Before: *"Mahasiswa mampu menerapkan konsep diskrit, logika, himpunan, dan fungsi matematika
  dasar dalam sistem informasi. Mahasiswa mampu mengidentifikasi, menganalisis fakta dan opini,
  serta menyusun solusi sistematis terhadap masalah teknis."*
- After (split, reworded to match Fisika's own Materi — kinematics/energy/electricity):
  *"Mahasiswa mampu menganalisis besaran kinematika dan dinamika partikel (gerak lurus, gaya,
  usaha, dan energi) untuk menjelaskan fenomena fisis dalam sistem komputer."* (as its own
  Sub-CPMK; the discrete-math/logic clause stays with Matematika Dasar / Aljabar Linier where it
  belongs.)

---

## Appendix: method

- Parsed `docs/cpl-cpmk-subcpmk.xlsx` with a pure-stdlib xlsx reader (openpyxl/pandas/libreoffice
  are not installed on this machine); every sheet was listed and the two Sub-CPMK sheets
  (`MK-CPMK-SubCPMK`, `MK-CPMK-SubCPMK-Metode`) were dumped to TSV for `awk`/`python3` analysis.
- Counts in the headline table are reproducible: filter `MK-CPMK-SubCPMK-Metode` column
  `SubCPMK` (col I) for non-empty; the boilerplate subset matches regex
  `sesuai konteks .* dan capaian CPMK`; the stem split and weak-verb/tautology counts are direct
  substring/regex counts on the non-boilerplate remainder.
- Automated Sub-CPMK↔Materi keyword-overlap scoring was tried (Jaccard-style over Indonesian
  content words) to find mismatches beyond Fisika/Proyek Sistem Informasi, but produced mostly
  false positives — abstract competency prose vs. concrete topic-keyword Materi legitimately
  share few words even when correctly aligned. §3's two cases were confirmed by manual reading
  and are the ones with high confidence; a full-catalog alignment check still needs a human pass
  per course before submission (see recommendation in §3b).
- House-style baseline (Sub-CPMK code format, RPS table columns, "Mahasiswa mampu" convention,
  Bloom-bracket usage) was derived from the published `subjects/*/* - RPS.tex` files, primarily
  Dasar Pemrograman and Basis Data, plus the `book/src/appendices/02-rps/` and `03-penilaian/`
  chapter includes.
- Related, out-of-scope-for-wording findings already on record and not re-derived here: CPMK code
  validity issues and dead codes are tracked in the workbook's own `Audit Findings` sheet.
