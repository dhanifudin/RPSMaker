# Checklist TODO Buku Kurikulum 2025 (vs. Dokumen 2020)

Status per 2026-07-08 — 9 `\todoitem` terbuka di `book/src/` (9/14 checklist gap-analysis selesai + 5 item tambahan di luar cakupan awal selesai, satu item BAB I dipecah jadi 3 baris terpisah untuk pelacakan lebih rinci), hasil audit
`docs/gap-analysis-2020-vs-2025.md` (dibangun dengan graphify, membandingkan
`docs/Dokumen Kurikulum D4 TI 2020 OBE - compressed.pdf` terhadap `book/`).
Setiap butir ditandai kemudahan pengisiannya:

- ✅ **Fillable from 2020** — datanya ada di PDF 2020, tinggal transkripsi/penyesuaian.
- 🎨 **Needs re-creation** — datanya sudah tersedia (di buku atau di 2020), tapi bentuknya (diagram) perlu dibuat ulang.
- ⛔ **Needs fresh 2025 input** — dokumen 2020 tidak bisa membantu; perlu data/keputusan baru.
- ❓ **Unverified** — belum dicek di pass analisis ini.

## Quick win (data sudah diketahui dari repo ini)

- [x] Nama + NIP Ka. Prodi di halaman pengesahan — `book/src/frontmatter/approval.tex:25-26` — ✅ *(diisi 2026-07-08: Dr. Ely Setyo Astuti, S.T., M.T. / NIP. 19760515 200912 2 001, konsisten dengan seluruh `subjects/*.tex`)*

## Fillable from 2020 (kerja transkripsi)

- [x] Deskripsi mata kuliah lengkap (Lampiran I — CPL/Pokok Bahasan/Referensi per MK) — `book/src/appendices/01-pedoman-akademik.tex` §"Deskripsi Mata Kuliah" — ✅ *(diisi 2026-07-08: 59 blok deskripsi mata kuliah, diekstrak langsung dari RPS 2025 di `subjects/*.tex` — bukan ditranskripsi dari PDF 2020 — karena RPS 2025 lebih akurat & terkini untuk kurikulum saat ini; rebuild `make book` bersih — exit 0, 526 halaman (+70), tidak ada overfull baru)*
- [x] Tabel rinci perubahan MK 2018/2019/2020 (dihapus/berubah nama/baru) — `book/src/chapters/07-rekonstruksi.tex` §2 — ✅ *(diisi 2026-07-08: 3 subsection dengan tabel lengkap per tahun, ditranskripsi dari `docs/Dokumen Kurikulum D4 TI 2020 OBE - compressed.pdf`; rebuild `make book` bersih — exit 0, 456 halaman (+3), tidak ada overfull baru)*

## Selesai di luar cakupan awal (permintaan lanjutan 2026-07-08)

- [x] Format tabel RPS: baris label CPL-Prodi/CPL-MK/Sub-CPMK dibuat bold/abu-abu, sel "Kode CPMK"/"Kode SCPMK" yang berulang di-merge (row-span) — `subjects/*.tex` (semua 59 file) — ✅ *(diverifikasi: 59/59 file kompilasi bersih standalone)*
- [x] Placeholder OTORISASI "Dosen Pengembang RPS" ("Tim Pengajar Program Studi D4 TI") diganti nama Koordinator KBK per mata kuliah — 27 file `subjects/*.tex` — ✅ *(diverifikasi: 0 file masih memakai placeholder di baris tsb; 27/27 kompilasi bersih)*
- [x] Tujuan Program Studi ditambahkan ke Lampiran I (sebelumnya hanya Visi/Misi) — `book/src/appendices/01-pedoman-akademik.tex` — ✅
- [x] Ringkasan Struktur Kurikulum dibangun ulang sebagai 8 tabel per-semester bergaya tabularray (No/Kode MK/Mata Kuliah/Kelompok/Teori/Praktik/SKS), retitle dari "2021" ke "2025" — `book/src/appendices/01-pedoman-akademik.tex` §"Ringkasan Struktur Kurikulum 2025" — ✅
- [x] **RPS dan Rubrik dipisah menjadi file berbeda** per mata kuliah (`<kode> <nama> - RPS.tex`, `- Rubrik.tex`, `- Tanda Tangan.tex`, plus wrapper standalone tak berubah nama) untuk seluruh 59 mata kuliah — Lampiran II (RPS) dan Lampiran III (Rubrik) di buku kini **portrait**, OTORISASI tetap tampil, tanda tangan dikecualikan dari buku; build standalone (`make rps`) tetap **landscape** dan menggabungkan RPS+Rubrik+tanda tangan seperti semula — ✅ *(menyelesaikan temuan gap-analysis "Lampiran III thin redirect": kini berisi konten rubrik nyata untuk semua 59 mata kuliah, bukan lagi redirect 3-kalimat)*. Diverifikasi: `make book` exit 0 (536 halaman, tanpa overfull baru yang parah), `make rps` exit 0 (59/59 PDF landscape multi-halaman berisi RPS+Rubrik+tanda tangan), spot-check visual beberapa halaman di kedua Lampiran.

## Needs re-creation (datanya ada, diagramnya belum)

- [ ] Diagram Peta Kurikulum & Pohon Kurikulum — `book/src/chapters/05-matriks.tex:44` — 🎨 *(halaman 2020 untuk §5.3/§5.4 berupa gambar, bukan teks; datanya sudah ada di matriks BK & distribusi semester buku sendiri)*

## Needs verification

- [ ] Lokasi & isi Daftar Pustaka asli di PDF 2020 — `book/main.tex` (Daftar Pustaka, ~baris 36) — ❓ *(nomor halaman TOC 2020 untuk "DAFTAR PUSTAKA" tidak cocok dengan rentang BAB I-VII yang sudah di-split; perlu pencarian lanjutan sebelum disimpulkan portable atau tidak)*

## Needs fresh 2025 input (2020 tidak bisa membantu lebih jauh)

- [ ] Nama Penyusun 1/2/3 — `book/src/frontmatter/approval.tex:12-14` — ⛔
- [ ] Tanggal Pengesahan — `book/src/frontmatter/approval.tex:22` — ⛔
- [ ] Narasi rekonstruksi 2025 — `book/src/chapters/07-rekonstruksi.tex:14` — ⛔ *(perlu dokumen keputusan/notulensi kurikulum 2025)*
- [ ] Verifikasi Profil Lulusan dengan FGD industri/alumni terbaru — `book/src/chapters/04-cpl.tex:180` — ⛔ *(2020 sudah dipakai sebagai draft awal; 2020 punya usulan profil tambahan dari kuesioner dosen — QA/Tester, Technical Writer, DevOps Engineer, dll — yang belum dipertimbangkan, tapi validasi akhir tetap perlu FGD baru)*
- [ ] Cek peraturan pasca Permendikbud No. 3/2020 untuk landasan yuridis — `book/src/chapters/03-landasan.tex:21` — ⛔
- [ ] Data tracer study terbaru + visualisasi resmi — `book/src/chapters/02-evaluasi.tex:191` — ⛔ *(paling kritis: data saat ini adalah salinan persis dataset 2020 — 199 partisipan, tahun 2017/2018-2019/2020 — dan secara eksplisit ditandai tidak boleh jadi data final)*
- [ ] Verifikasi Nilai Akreditasi masih berlaku — `book/src/chapters/01-identitas.tex:12` — ⛔ *(bukan tugas dokumen — perlu konfirmasi ke pihak prodi/jurusan apakah nilai 2020 masih berlaku di 2025)*
- [ ] Verifikasi No. SK BAN-PT masih berlaku — `book/src/chapters/01-identitas.tex:13` — ⛔ *(sama seperti di atas)*
- [x] Gelar Lulusan — `book/src/chapters/01-identitas.tex:19` — ⛔→✅ *(diisi 2026-07-08: S.Tr.Kom. (Sarjana Terapan Komputer), menggantikan S.ST dari kurikulum 2020)*

---

**Ringkasan**: 1/1 quick win selesai ✅, 2/2 fillable dari 2020 selesai ✅ (BAB VII, Lampiran I), 5/5 item tambahan di luar cakupan awal selesai ✅ (format tabel RPS, OTORISASI, Tujuan Prodi, Ringkasan Kurikulum, split RPS/Rubrik), 1 perlu pembuatan diagram, 1 perlu verifikasi lokasi sumber, 1/3 sub-item BAB I selesai (Gelar Lulusan), 6 perlu input 2025 yang baru.

**Catatan**:
- Lihat `docs/gap-analysis-2020-vs-2025.md` untuk bukti lengkap (hasil query graphify) di balik setiap klasifikasi di atas.
- Mencentang butir di sini berarti `\todoitem`/`\reviewfrompdf` yang bersangkutan di `book/src/` juga harus diselesaikan (dihapus atau diganti kontennya).
- Jumlah `\todoitem` di `book/src/` saat ini: 9 (`grep -rn "todoitem{" book/src/ | wc -l`) — turun dari 12: Ka. Prodi (2026-07-08) dan BAB VII rekonstruksi tables (2026-07-08, `make book` exit 0, 456 halaman, tidak ada overfull baru).
- Gelar Lulusan (`\reviewfrompdf`, bukan `\todoitem`) diisi 2026-07-08 dengan S.Tr.Kom. — Nilai Akreditasi dan No. SK BAN-PT pada baris yang sama masih menunggu verifikasi institusional.
