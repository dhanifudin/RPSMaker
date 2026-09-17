# Checklist TODO Buku Kurikulum 2025 (vs. Dokumen 2020)

Status per 2026-09-17 (pass kedua, sore hari) — **0** `\todoitem` dan **0** `\reviewfrompdf`
tersisa di `book/src/`. Seluruh 21 marker (2 `\todoitem` + 19 `\reviewfrompdf` yang tersisa
setelah pass pagi hari) diselesaikan pada pass ini, sebagian dengan riset sumber primer dan
sebagian dengan keputusan institusional langsung dari anggota Tim Penyusun (lihat "Keputusan
Tim Penyusun 2026-09-17" di bawah). Konten yang genuinely masih perlu tindak lanjut institusional
di masa depan (bukan sekadar penelusuran dokumen) dipertahankan sebagai catatan naratif biasa
(bukan kotak highlight), bukan dihapus begitu saja — lihat baris terkait di bawah.

## Keputusan Tim Penyusun 2026-09-17

Empat keputusan berikut diberikan langsung oleh anggota Tim Penyusun (lihat
`book/src/frontmatter/approval.tex:12-22`) dalam sesi ini, menjadi dasar penyelesaian marker
yang sebelumnya menunggu validasi institusional:

1. **RTI253005 Basis Data Lanjut = 3 SKS** (nilai distribusi dipertahankan; RPS diperbaiki).
2. **RTI255008 Administrasi dan Keamanan Jaringan = 2 SKS** (nilai distribusi dipertahankan; RPS diperbaiki).
3. **Validasi/sign-off diberikan** untuk: diagram jejaring kurikulum + peta jalan CPL (termasuk keterkaitan garis bertitik berbasis kesamaan topik), pemetaan Profil Lulusan 2020 ke CPL 2025, pemetaan Proyek 1 (2020) → Proyek Sistem Informasi (2025), dan tata letak matriks organisasi mata kuliah.
4. **Dasar formal Rekonstruksi 2025** = Nota Dinas Wakil Direktur I No. 19/WADIR.I/KM/2025 (6 Februari 2025); dicatat sebagai dasar transisi OBE, bukan lagi ditandai sebagai kekurangan dokumentasi.

## Ringkasan penyelesaian per bab

- **`book/main.tex`** — Daftar Pustaka lengkap 9 referensi (3 Permendikbud 2013/2014/2020 ditranskripsi dari PDF 2020 halaman 1101 pada pass pagi; Permendiktisaintek No. 39/2025 ditambahkan pada pass ini menyusul riset landasan yuridis).
- **`01-identitas.tex`** — Nilai Akreditasi "Unggul" / SK 127/SK/LAM-INFOKOM/Ak/STr/VIII/2023 (berlaku s.d. 2028), diverifikasi via halaman akreditasi resmi Polinema; catatan audit-trail dihapus, datanya cukup berdiri sendiri di tabel identitas.
- **`02-evaluasi.tex`** — catatan historis kompetensi lulusan (survei 2020, 199 partisipan) diubah dari kotak highlight menjadi paragraf pembuka biasa; substansi caveat (bukan data final, perlu instrumen survei kompetensi baru) dipertahankan karena ini genuinely belum ada datanya, bukan sekadar butuh riset dokumen.
- **`03-landasan.tex`** — item 9 baru di Landasan Yuridis: Permendiktisaintek No. 39/2025 tentang Penjaminan Mutu Pendidikan Tinggi (pengganti aktif Permendikbud No. 3/2020, via Permendikbudristek No. 53/2023); paragraf penutup menjelaskan rantai regulasi tsb menggantikan kotak review.
- **`04-cpl.tex`** — Profil Lulusan 2020 (4 profil) dan pemetaannya ke CPL 2025 dinyatakan telah ditetapkan dan divalidasi tim kurikulum (Keputusan #3).
- **`05-matriks.tex`** — jejaring kurikulum, 10 diagram peta jalan CPL, dan matriks organisasi mata kuliah dinyatakan telah divalidasi tim kurikulum (Keputusan #3); catatan metodologi (data source, representasi peta konsep vs. prasyarat, makna garis bertitik) dipertahankan sebagai teks biasa karena tetap berguna bagi pembaca.
- **`06-rancangan-kurikulum.tex`** & **`01-pedoman-akademik.tex`** — SKS RTI253005 (→3) dan RTI255008 (→2) diperbaiki di RPS/Rubrik/deskripsi Lampiran I/tabel distribusi seluruhnya konsisten (Keputusan #1-2); catatan SKS-mismatch yang sebelumnya menandai 5 MK (2 di antaranya sudah tidak berlaku sejak pass pagi) dihapus sepenuhnya.
- **`07-rekonstruksi.tex`** — tabel Rekonstruksi 2025 diperbarui: Proyek 1 (RTI204002) dipindah dari "Matakuliah Baru" ke "Matakuliah Berubah Nama" sebagai Proyek 1 → Proyek Sistem Informasi (Keputusan #3, sebelumnya ditandai `$^{*}$` sebagai interpretasi belum terkonfirmasi); kotak review chapter-level dan baris ringkasan tahun 2018-2025 diubah menjadi teks/tabel biasa; catatan ketiadaan SK/berita-acara terpisah diganti dengan kutipan Nota Dinas Wadir I sebagai dasar formal (Keputusan #4).
- **`book/src/frontmatter/toc.tex`** — `\legendboxes` (legenda kotak highlight kuning/merah) dihapus karena tidak ada lagi kotak yang perlu dijelaskan.

## Verifikasi

- `grep -rc 'todoitem{'` dan `'reviewfrompdf{'` atas `book/src/` → keduanya 0.
- Tidak ada referensi path internal repo (`docs/*.xlsx`, dll.) yang tersisa di prosa buku; hanya URL dokumentasi eksternal legitimate (PostgreSQL, Laravel) yang tersisa.
- Quicktest `xelatex` gabungan (01-identitas, 02-evaluasi, 03-landasan, 04-cpl, 07-rekonstruksi, Lampiran I) — bersih, 0 error, 93 halaman; spot-check visual seluruh bagian yang diedit.
- Dua RPS standalone (`RTI253005 Basis Data Lanjut.tex`, `RTI255008 Administrasi dan Keamanan Jaringan.tex`) dikompilasi individual — bersih, header menampilkan 3 SKS/6 jam dan 2 SKS/4 jam sesuai keputusan.
- `make book` (build penuh) dijalankan ulang setelah seluruh edit pass ini — lihat commit/log build untuk hasil akhir.

**Catatan**:
- Lihat `docs/gap-analysis-2020-vs-2025.md` untuk audit trail lengkap dari pass-pass sebelumnya.
- Checklist ini sekarang mencerminkan keadaan akhir `book/src/` — tidak ada lagi marker terbuka. Jika muncul kebutuhan konten baru di masa depan (mis. revisi kurikulum berikutnya), mulai checklist baru daripada menambah ke file ini.
