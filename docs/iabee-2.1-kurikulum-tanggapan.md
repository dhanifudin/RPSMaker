# Ringkasan Temuan Evaluator IABEE — Kriteria 2.1 KURIKULUM

Ringkasan `docs/tanggapan.xlsx` (siklus General Accreditation – Interim Evaluation With
On-Site Visit, 2026-2027, kategori Eng. Technology) untuk Kriteria 2.1, difokuskan pada
temuan evaluator di sheet "Tanggapan Pertama Prodi" dan status penanganannya.

**Status per 2026-09-16**: kolom *Answer* untuk seluruh 7 item review Kriteria 2.1 — dan
sebenarnya seluruh 48 item review di sheet ini — masih **kosong**, meski tahap "Tanggapan
Pertama Prodi" berstatus *Ongoing* dengan tenggat **19 September 2026** (≈3 hari dari
tanggal ringkasan ini dibuat).

## Temuan evaluator per sub-kriteria dan solusi yang direkomendasikan

| Sub-kriteria | Isu dari Evaluator | Solusi yang Direkomendasikan |
|---|---|---|
| **2.1.1** — Cakupan bidang kajian (matematika/sains dasar, muatan sub-disiplin, TIK, pendidikan umum) | Proporsi SKS (≥65% sub-disiplin+TIK, ≤25% pendidikan umum) sudah terpenuhi menurut Tabel Suplemen B1 revisi, **namun** belum ada kebijakan transisi/ekuivalensi bagi mahasiswa yang menempuh kurikulum *sebelum* MK Fisika berdiri sendiri (Feb 2025) — sehingga pemenuhan sains dasar untuk seluruh mahasiswa dalam siklus akreditasi belum terverifikasi. | Susun kebijakan transisi/ekuivalensi kurikulum (mis. MK penyetaraan atau pengakuan capaian dari MK lama yang memuat materi sains dasar) beserta bukti implementasinya (SK, daftar mahasiswa terdampak, skema konversi nilai). |
| **2.1.2** — Pengembangan kurikulum melibatkan pemangku kepentingan | (a) Mekanisme kaji ulang (SOP, Advisory Board, FGD) sudah ada, tapi belum ada analisis/justifikasi bahwa *hasil* kaji ulang benar memenuhi kebutuhan masyarakat/industri/profesi dan selaras misi institusi. (b) Belum ada justifikasi bahwa pemangku kepentingan yang dilibatkan (baru 3 perusahaan: PT. Infonika, PT. Pos Indonesia, PT. SAI) representatif — evaluator eksplisit menyebut cakupan seharusnya juga mencakup alumni, pengguna lulusan, mahasiswa, dosen, asosiasi profesi, pemerintah (bila relevan). | (a) Lampirkan dokumen analisis hasil kaji ulang + matriks keterkaitan masukan↔perubahan kurikulum. (b) Perluas/ dokumentasikan keterwakilan stakeholder di luar 3 industri yang ada — tambahkan bukti pelibatan alumni & pengguna lulusan (tracer study, forum alumni) sebagai pemangku kepentingan formal dalam kaji ulang kurikulum. |
| **2.1.3** — Hubungan struktural kurikulum↔CPP, silabus lengkap (5 item review, sub-kriteria dengan temuan terbanyak) | Rekonstruksi OBE Feb 2025 sudah memperbaiki pemetaan CPP (1 MK bisa >1 CPP), tapi: **(1)** transkrip nilai 2 lulusan/angkatan (4 tahun terakhir) yang diminta *belum dilampirkan*; **(2)** belum ada penjelasan bagaimana struktur kurikulum membangun penguasaan CPP secara *bertahap*; **(3)** belum ada pemetaan eksplisit topik Kriteria Disiplin (computing essentials, requirements analysis, software V&V, security, dll.) ke MK+SKS+kedalaman materi; **(4)** belum ada mekanisme formal yang memastikan seluruh RPS direview/divalidasi/disahkan secara konsisten; **(5)** portofolio MK perlu menunjukkan keterlusuran CPMK→instrumen→rubrik→hasil→analisis→tindak lanjut, bukan sekadar kumpulan dokumen. **Kelima item ini SEMUA menyebut dokumen pendukung tidak dapat diakses/folder kosong.** | (1) Lampirkan scan transkrip sesuai permintaan. (2) Tambahkan narasi progresi CPP per semester (mis. diagram/tabel bertahap). (3) Buat matriks topik Kriteria Disiplin → MK → SKS → kedalaman (bisa berbasis matriks kurikulum yang sudah ada di `book/`). (4) Dokumentasikan SOP review/validasi/pengesahan RPS oleh KBK sebagai siklus formal, bukan hanya hasil akhirnya. (5) Revisi format portofolio MK agar eksplisit menunjukkan rantai keterlusuran tsb. **Untuk semua 5 item: perbaiki dulu akses tautan (lihat bagian Audit Tautan di bawah) sebelum menilai apakah kontennya sendiri sudah cukup.** |
| **2.1.4** — Pengalaman praktik rekayasa & proyek desain utama (capstone) | Substansi (TA/Skripsi 8 SKS sebagai capstone, kerja tim, rubrik Standar Keteknikan/Batasan Realistis, Magang Industri/MBKM) **sudah dinilai sesuai kebutuhan kriteria oleh evaluator** — catatan tersisa hanya (a) sejumlah dokumen pendukung tidak dapat diakses, dan (b) perlu penjelasan keterlusuran MK pendukung → capstone. | Ini sub-kriteria dengan risiko terendah — perbaiki akses tautan, tambahkan 1-2 paragraf yang secara eksplisit menyusun daftar MK pendukung dan bagaimana masing-masing berkontribusi ke capstone. |

## Audit tautan `poline.ma` yang dirujuk di 2.1.3 dan 2.1.4

Seluruh 17 tautan (10 unik di 2.1.3, 7 unik di 2.1.4) memakai layanan pemendek tautan
internal "Polinema SnapLink" — halaman *splash* dengan hitung-mundur 5 detik yang baru
mengeksekusi `window.location.replace(...)` ke tujuan asli via JavaScript. **Fetch statis
(termasuk kemungkinan alat yang dipakai evaluator) tidak pernah menunggu redirect ini**,
sehingga bisa jadi sumber utama keluhan "dokumen tidak dapat diakses" di 2.1.3/2.1.4 —
bukan berarti dokumennya benar-benar rusak.

Setelah menelusuri redirect ke tujuan asli satu per satu:

| Status | Jumlah | Detail |
|---|---|---|
| ✅ **Publik, terverifikasi bisa diakses** | 1 | `JqdS` (Pedoman Akademik) → PDF asli 20 halaman di `devel-jti.polinema.ac.id`, berhasil diunduh langsung tanpa login. **Catatan**: ini subdomain *development/staging* (`devel-`), bukan lokasi permanen — sebaiknya dipindah ke domain tetap. |
| ❌ **Rusak/terkunci, terkonfirmasi** | 2 | `x6a2j` (2.1.3, Suplemen Tabel B2) → Google Sheets link `edit`, **HTTP 401** (tidak dibagikan publik). `2LjYH` (2.1.3, sosialisasi kurikulum dosen) → folder Drive, mengarah ke halaman **"Google Drive: Sign-in"** sungguhan (satu-satunya dari 16 tautan Drive yang judul halamannya tidak ter-resolve ke nama file/folder asli). |
| ⚠️ **Kemungkinan besar publik, belum terverifikasi 100%** | 14 | Sisanya (`ibqVf`, `5Vmas`, `V67u`, `uVxk`, `MLxAH`, `brvt6`, `nWwYB`, `N9CH`, `p4Wg`, `KF2`, `5CE`, `XiU`, `vBW`, `3QeEK`) — judul halaman setelah redirect menampilkan nama file/folder asli (mis. "Pedoman Pelaksanaan Skripsi Capstone - D4 TI 2026.pdf – Google Drive"), yang biasanya hanya terjadi jika berkas dapat diakses tautan; tidak bisa dipastikan 100% tanpa sesi browser + akun Google nyata (tidak tersedia di lingkungan analisis ini). |

### Tindakan yang direkomendasikan (urutan prioritas)

1. **Perbaiki 2 tautan yang terkonfirmasi rusak** — ubah setelan berbagi Google Sheets
   `x6a2j` dan folder Drive `2LjYH` menjadi "Siapa saja yang memiliki tautan → Pelihat".
   Ini fix satu klik per tautan.
2. **Pindahkan PDF Pedoman Akademik (`JqdS`) keluar dari subdomain `devel-jti`** ke lokasi
   permanen (mis. Drive resmi atau domain utama `jti.polinema.ac.id`), agar tidak hilang
   sewaktu-waktu tanpa peringatan.
3. **Verifikasi manual seluruh 14 tautan "kemungkinan publik"** dengan membuka masing-masing
   di jendela penyamaran (incognito, tanpa login akun Polinema) untuk memastikan benar-benar
   dapat diakses pihak eksternal (evaluator IABEE), bukan hanya oleh akun institusi.
4. **Pertimbangkan mengganti seluruh tautan `poline.ma` dengan tautan Google Drive langsung**
   di dokumen tanggapan — menghindari ketergantungan pada hitung-mundur JavaScript 5 detik
   yang berisiko tidak selesai dieksekusi oleh alat/metode akses evaluator.

## Prioritas tindak lanjut keseluruhan

1. **Segera**: isi kolom *Answer* di sheet "Tanggapan Pertama Prodi" untuk 7 item Kriteria
   2.1 — saat ini kosong, tenggat 19 September 2026.
2. **Cepat/murah**: perbaikan 2 tautan rusak (`x6a2j`, `2LjYH`) dan migrasi `JqdS` keluar dari
   subdomain dev — dampak besar (berpotensi menyelesaikan mayoritas keluhan akses di
   2.1.3/2.1.4) dengan usaha minimal.
3. **Butuh konten baru**: kebijakan transisi kurikulum (2.1.1), perluasan/dokumentasi
   keterwakilan stakeholder (2.1.2), matriks topik Kriteria Disiplin→MK dan mekanisme
   formal validasi RPS (2.1.3).

**Catatan**: temuan ini murni dari pembacaan `docs/tanggapan.xlsx` dan penelusuran tautan
`poline.ma` yang dirujuk di dalamnya (dijalankan 2026-09-16, tanpa sesi browser
terautentikasi) — bukan snapshot langsung dari portal IABEE, sehingga status yang berubah
di portal setelah tanggal ini tidak akan tercermin di sini.

## Draf Jawaban (kolom "Answer") — 2.1.1

Belum ditemukan kebijakan transisi/ekuivalensi kurikulum di repo ini (bukan hanya belum
didigitalisasi — bagian "Rekonstruksi 2025" di `book/src/chapters/07-rekonstruksi.tex`
masih berupa `\todoitem` kosong, dan analisis di atas juga sudah menandai butir ini sebagai
"Butuh konten baru"). Draf di bawah karena itu disusun sebagai **usulan kebijakan**, dengan
placeholder `[___]` eksplisit untuk data institusional yang belum diketahui — bukan jawaban
final yang siap disalin apa adanya ke sheet.

**Isu dari Evaluator**

> Namun, paparan belum menjelaskan mekanisme transisi kurikulum bagi mahasiswa yang telah
> menempuh kurikulum sebelum mata kuliah Fisika diberlakukan, sehingga pemenuhan
> kompetensi sains dasar bagi seluruh mahasiswa dalam siklus akreditasi belum dapat
> diverifikasi. Program Studi perlu melengkapi kebijakan transisi atau ekuivalensi
> kurikulum beserta bukti implementasinya untuk menunjukkan bahwa seluruh mahasiswa tetap
> memperoleh kompetensi sains dasar yang dipersyaratkan.

**Solusi yang Diusulkan (draf jawaban)**

> Menindaklanjuti masukan evaluator, Program Studi mengonfirmasi bahwa proporsi beban SKS
> pada Tabel Suplemen B1 revisi (muatan spesifik sub-disiplin dan TIK >65%, pendidikan
> umum ≤25%) berlaku untuk kurikulum hasil rekonstruksi Februari 2025. Untuk menjamin
> bahwa mahasiswa yang telah menempuh kurikulum sebelum penetapan mata kuliah Fisika
> secara mandiri tetap memperoleh kompetensi sains dasar yang dipersyaratkan, Program
> Studi menetapkan kebijakan transisi kurikulum sebagai berikut:
>
> **1. Cakupan Mahasiswa Terdampak**
> Kebijakan ini berlaku bagi mahasiswa angkatan **[___] sampai dengan [___]** (mahasiswa
> yang telah menempuh mata kuliah semester 1 sebelum Februari 2025), sejumlah **[___]**
> mahasiswa aktif pada saat kebijakan ditetapkan.
>
> **2. Skema Ekuivalensi/Konversi** — pilih/sesuaikan salah satu mekanisme berikut sesuai
> keputusan Prodi/KBK:
> - *Opsi A — Pengakuan capaian melalui pemetaan ulang:* Program Studi memetakan capaian
>   kompetensi sains dasar yang telah diperoleh mahasiswa terdampak melalui mata kuliah
>   yang relevan pada kurikulum sebelumnya (mis. Matematika Dasar/Matematika 1–3),
>   didukung analisis kesetaraan CPMK, sehingga tidak diwajibkan mengulang.
> - *Opsi B — Kewajiban menempuh MK Fisika sebagai mata kuliah tambahan/pilihan:*
>   Mahasiswa terdampak yang belum lulus diwajibkan menempuh MK Fisika pada semester
>   berjalan sebagai mata kuliah tambahan di luar paket semester tetapnya.
>
> **3. Dasar Kebijakan**
> Ditetapkan melalui **SK [nomor/tanggal — TBD]** tentang Kebijakan Transisi Kurikulum
> 2025 Program Studi D4 Teknik Informatika.
>
> **4. Bukti Implementasi**
> Daftar dokumen pendukung yang perlu dilampirkan: SK penetapan, daftar mahasiswa
> terdampak per angkatan, skema konversi/pengakuan nilai, bukti sosialisasi kebijakan
> kepada mahasiswa terdampak.

**Hal yang masih perlu diverifikasi oleh Prodi sebelum draf ini disalin ke sheet:**

- Seluruh `[___]` perlu diisi data nyata — rentang angkatan, jumlah mahasiswa, mekanisme
  yang benar-benar dipilih, nomor/tanggal SK.
- Draf sengaja menyajikan dua opsi mekanisme (pengakuan capaian vs. kewajiban MK tambahan)
  alih-alih memutuskan salah satu — itu keputusan kebijakan kurikulum riil milik
  Prodi/KBK, bukan sesuatu yang seharusnya saya tentukan.
- Narasi "materi Fisika sebelumnya terintegrasi ke MK Internet of Things" (dari Laporan
  Evaluasi Diri) tidak didukung oleh data kurikulum 2020 yang terdigitalisasi di repo ini
  (semester 1 kurikulum 2020 tidak memiliki MK fisika — sains dasar saat itu ditempuh
  lewat Matematika 1–3; IoT sendiri sudah berdiri sendiri sejak kurikulum 2020). Ini tidak
  serta-merta berarti klaim LED salah — bisa jadi ringkasan yang terdigitalisasi memang
  tidak mencakup detail sampai tingkat sub-topik — tapi sebaiknya dicek ulang terhadap SK
  kurikulum 2020 asli (non-digital) sebelum draf ini difinalisasi, terlepas dari status
  kebijakan transisi di atas.
