# Peta CPL–CPMK–Sub-CPMK–MK–Materi–Penilaian

Referensi silang seluruh 59 mata kuliah program D4 Teknik Informatika Polinema:
untuk setiap mata kuliah (MK), dokumen ini memetakan Capaian Pembelajaran
Lulusan (CPL-Prodi) yang didukung, Capaian Pembelajaran Mata Kuliah (CPMK)
yang diturunkan darinya, Sub-CPMK (kemampuan akhir tiap tahapan belajar),
Bahan Kajian/Materi Pembelajaran, dan metode penilaian (bentuk asesmen +
bobot) yang digunakan untuk mengukur setiap Sub-CPMK.

**Sumber data:** diekstrak langsung dari file `<Nama MK> - RPS.tex` tiap mata
kuliah di `subjects/<KODE-MK>-<slug>/`, khususnya bagian blok Capaian
Pembelajaran (CP) dan matriks bobot CPMK × Bentuk Penilaian.

**Cara membaca kolom:**

| Kolom | Isi |
|---|---|
| **Sub-CPMK** | Kode `SCPMKxxxx-yyyyy` (xxxx = kode CPMK induk, yyyyy = kode MK + urutan) beserta deskripsi ringkas kemampuan akhir mingguan. |
| **CPMK Induk** | Kode `CPMKxxxx` beserta deskripsi capaian pembelajaran mata kuliah yang menaungi Sub-CPMK tersebut. |
| **CPL** | Kode CPL-Prodi (CPL01–CPL10) yang didukung oleh CPMK tersebut. |
| **Bentuk Penilaian & Bobot** | Daftar bentuk asesmen (Tugas, Kuis, UTS, PBL, UAS, atau bentuk khusus proyek/skripsi seperti Sprint/Dok.Perencanaan/Reviu Proposal/Sidang) beserta persentase bobotnya untuk Sub-CPMK tersebut, dan totalnya. |

**Catatan:**
- Bobot per Sub-CPMK dijumlahkan dari matriks "CPMK × Bentuk Penilaian" pada
  RPS masing-masing MK; totalnya di seluruh Sub-CPMK dalam satu MK berjumlah
  100%. Beberapa baris (mis. sebagian Sub-CPMK di RTI255008 dan RTI253007)
  tidak memiliki bobot terpisah karena terintegrasi penuh ke penilaian
  Sub-CPMK lain pada minggu yang sama — ditandai sebagai catatan pada baris
  tersebut.
- Dokumen ini adalah snapshot per 2026-07-16 hasil ekstraksi otomatis dari
  RPS yang berlaku saat itu. RPS dapat berubah (revisi kurikulum, perbaikan
  CPL/CPMK, dll.) — dokumen ini **tidak otomatis tersinkron** dan perlu
  digenerate ulang setelah perubahan signifikan pada RPS.
- Legenda kode CPL01–CPL10 mengacu pada `book/src/chapters/04-cpl.tex`.

---

## RTI251001 — Pancasila (Semester 1)

**CPL-Prodi:** CPL01

**Bahan Kajian / Materi Pembelajaran:**
- Pendidikan Pancasila dalam tinjauan historis, kultural, yuridis, dan filosofis
- Pancasila dalam konteks sejarah perjuangan bangsa Indonesia
- Pancasila sebagai sistem filsafat
- UUD RI 1945 dan amandemen UUD RI 1945
- Trias Politika dan kelembagaan negara menurut UUD RI 1945
- Pancasila sebagai ideologi nasional dan ideologi lain yang berkembang di dunia
- Pancasila dan HAM serta pelaksanaan HAM dalam UUD RI 1945
- Tindak pidana korupsi
- Pancasila sebagai paradigma pembangunan

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0102-00101: Menjelaskan Pendidikan Pancasila secara historis, kultural, yuridis, filosofis, sejarah bangsa, dan sistem filsafat | CPMK0102: Menginternalisasi nilai ketakwaan, Pancasila, kewarganegaraan, dan semangat belajar sepanjang hayat | CPL01 | Tugas: 5%, Kuis: 5%, UTS: 10% (Total: 20%) |
| SCPMK0102-00102: Menjelaskan UUD RI 1945, amandemen, Trias Politika, dan kelembagaan negara | CPMK0102 | CPL01 | Tugas: 10%, UTS: 10% (Total: 20%) |
| SCPMK0102-00103: Menjelaskan Pancasila sebagai ideologi nasional dan membandingkan dengan ideologi dunia | CPMK0102 | CPL01 | Tugas: 2.5%, Kuis: 5%, UAS: 15% (Total: 22.5%) |
| SCPMK0102-00104: Menginternalisasi nilai Pancasila dalam isu HAM, antikorupsi, dan paradigma pembangunan | CPMK0102 | CPL01 | Tugas: 2.5%, Case Method: 15%, UAS: 20% (Total: 37.5%) |

## RTI251002 — Konsep Teknologi Informasi (Semester 1)

**CPL-Prodi:** CPL02, CPL05, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Konsep teknologi dan inovasi teknologi
- Perkembangan IPTEK dan etika rekayasa
- Perkembangan ICT
- Sistem komputer dan konsep sistem komputer
- Representasi data, aljabar Boolean, dan flowchart
- Jaringan komputer dan internet
- Aplikasi TI di berbagai bidang dan sertifikasi bidang TI

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0901-00201: Menjelaskan konsep TI, inovasi teknologi, perkembangan IPTEK/ICT, dan etika rekayasa | CPMK0901: Menjelaskan cara kerja sistem komputer dan komponen utamanya | CPL09 | Tugas: 10%, Kuis 1: 12%, UTS: 7% (Total: 29%) |
| SCPMK0901-00202: Menjelaskan cara kerja sistem komputer beserta struktur, arsitektur, dan komponen utamanya | CPMK0901 | CPL09 | Tugas: 4%, UTS: 8% (Total: 12%) |
| SCPMK0901-00203: Menerapkan representasi data, aljabar Boolean, dan flowchart untuk masalah komputasi sederhana | CPMK0901 | CPL09 | Tugas: 6%, Kuis 2: 12%, UAS: 15% (Total: 33%) |
| SCPMK0208-00204: Memilih jaringan komputer, aplikasi TI, dan sertifikasi sesuai kebutuhan pengguna/organisasi | CPMK0208: Memilih arsitektur computing system sesuai kebutuhan aplikasi multi-platform | CPL02 | Tugas: 6%, UAS: 17% (Total: 23%) |
| SCPMK0502-00205: Mengidentifikasi aspek keamanan dasar pada sistem operasi, jaringan komputer, dan cloud | CPMK0502: Mengidentifikasi dan menangani isu keamanan pada OS, jaringan, dan cloud | CPL05 | UAS: 3% (Total: 3%) |

## RTI251003 — Critical Thinking dan Problem Solving (Semester 1)

**CPL-Prodi:** CPL04

**Bahan Kajian / Materi Pembelajaran:**
- Berpikir dan Menalar
- Pondasi Berpikir Kritis
- Kemampuan Dasar Pemecahan Masalah
- Applied Critical Thinking
- Kemampuan Pemecahan Masalah Tingkat Lanjut
- Teknik-teknik Lanjutan untuk Pemecahan Masalah
- Penalaran Kritis

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0401-00301: Mengidentifikasi, menganalisis, dan mengevaluasi argumen, membedakan fakta/opini, mengenali bias dan kesalahan logika | CPMK0401: Menganalisis permasalahan kompleks dan merumuskan solusi rasional berbasis data | CPL04 | Tugas: 10%, Kuis: 15%, UTS: 5% (Total: 30%) |
| SCPMK0401-00302: Menerapkan teknik dan alat pemecahan masalah (pemikiran lateral, brainstorming, root cause) | CPMK0401 | CPL04 | Tugas: 8%, UTS: 5% (Total: 13%) |
| SCPMK0401-00303: Mengembangkan solusi logis berbasis bukti dan membelanya melalui argumentasi ilmiah | CPMK0401 | CPL04 | Tugas: 2%, PBL: 20%, UAS: 35% (Total: 57%) |

## RTI251004 — Matematika Dasar (Semester 1)

**CPL-Prodi:** CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Proposisi dan logika
- Teori himpunan
- Relasi dan fungsi
- Teori bilangan dan sistem bilangan
- Induksi dan rekursi
- Aljabar Boolean
- Kombinatorial
- Teori graf dan pohon

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0902-00401: Menerapkan logika proposisi dan operasi himpunan untuk memodelkan relasi dan solusi komputasional | CPMK0902: Menerapkan prinsip matematis dan struktur diskrit untuk analisis komputasional | CPL09 | Tugas: 5%, Kuis 1: 7.5%, UTS: 15% (Total: 27.5%) |
| SCPMK0902-00402: Melakukan perhitungan pada relasi, fungsi, dan konversi antarsistem bilangan | CPMK0902 | CPL09 | Tugas: 4.5%, UTS: 15% (Total: 19.5%) |
| SCPMK0902-00403: Menerapkan induksi matematika, aljabar Boolean, dan kombinatorial | CPMK0902 | CPL09 | Tugas: 6%, Kuis 2: 7.5%, UAS: 17.5% (Total: 31%) |
| SCPMK0902-00404: Menerapkan konsep graf dan pohon untuk representasi dan penyelesaian persoalan komputasi | CPMK0902 | CPL09 | Tugas: 4.5%, UAS: 17.5% (Total: 22%) |

## RTI251005 — Bahasa Inggris 1 (Semester 1)

**CPL-Prodi:** CPL03

**Bahan Kajian / Materi Pembelajaran:**
- Computer Applications: kinds of applications, Simple Present Tense, imperatives, sequencers, software installation process
- Computer Architecture: types of computers, hardware and its functions, computer ads, adjectives, comparatives, superlatives
- Multimedia: multimedia hardware, toolbox of a graphic program, passive sentences, time clauses
- Computer Network: network hardware, network topology, if-clause
- Websites: features, types, analytics, data visualization, characteristics of a good website
- Careers in IT: IT jobs and responsibilities, modals for skills and qualifications
- IT Support Staff: computer problems and solutions, service report, help desk ticket, email
- Workstation Health and Safety: problems, expressions for giving advice and declaring prohibition

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0303-00501: Memahami dan menggunakan vocabulary serta grammatical functions bahasa Inggris dalam konteks TI | CPMK0303: Mengembangkan diri, berkomunikasi profesional, mempresentasikan diri, mengelola karir | CPL03 | Kuis: 10%, UTS: 5%, UAS: 5% (Total: 20%) |
| SCPMK0303-00502: Memahami teks lisan dan tulisan berbahasa Inggris topik TI dan menjelaskan kembali isinya | CPMK0303 | CPL03 | Praktik Lisan: 5%, UTS: 5%, UAS: 5% (Total: 15%) |
| SCPMK0303-00503: Menulis teks fungsional bahasa Inggris (instruksi, perbandingan, deskripsi, review, deskripsi pekerjaan) | CPMK0303 | CPL03 | Tugas: 5%, Praktik Lisan: 10%, UTS: 5%, UAS: 5% (Total: 25%) |
| SCPMK0303-00504: Mempresentasikan gagasan dan hasil kerja secara lisan dalam bahasa Inggris secara mandiri dan profesional | CPMK0303 | CPL03 | Praktik Lisan: 40% (Total: 40%) |

## RTI251006 — Dasar Pemrograman (Semester 1)

**CPL-Prodi:** CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Konsep algoritma, analisis permasalahan, version control, dan Kanban
- Tipe data, variabel, konstanta, nilai, ekspresi, input-output, sequence, dan operator
- Analisa kasus: pemilihan dan perulangan (sederhana dan bersarang)
- Array 1 dan 2 dimensi, fungsi iteratif dan rekursif

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0903-00601: Menjelaskan konsep algoritma, version control, Kanban, dan menganalisis permasalahan sederhana ke bentuk algoritma | CPMK0903: Menjelaskan prinsip logika komputasi serta menerapkan teknik dasar pemrograman dan algoritma | CPL09 | Tugas: 4%, Kuis 1: 5%, UTS: 6% (Total: 15%) |
| SCPMK0903-00602: Menjelaskan tipe data, variabel, input-output, sequence, dan operator serta menerapkannya | CPMK0903 | CPL09 | Tugas: 2%, Kuis 1: 5%, UTS: 8% (Total: 15%) |
| SCPMK0704-00603: Menuliskan algoritma pemilihan dan perulangan (sederhana/bersarang) menggunakan flowchart | CPMK0704: Menerapkan berbagai bahasa dan paradigma pemrograman untuk menyelesaikan masalah komputasi | CPL07 | Tugas: 8%, UTS: 16%, Kuis 2: 5%, UAS: 10% (Total: 39%) |
| SCPMK0704-00604: Menyelesaikan studi kasus dengan array 1/2 dimensi serta fungsi iteratif dan rekursif | CPMK0704 | CPL07 | Tugas: 6%, Kuis 2: 5%, UAS: 20% (Total: 31%) |

## RTI251007 — Praktikum Dasar Pemrograman (Semester 1)

**CPL-Prodi:** CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Konsep algoritma, representasi algoritma, translator, dan bahasa pemrograman
- Tipe data, variabel, konstanta, nilai, ekspresi, dan input-output
- Sequence, analisa kasus, pencabangan, dan perulangan
- Array dan fungsi/prosedur

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0903-00701: Menjelaskan konsep program, bahasa pemrograman, compiler, debugging, instalasi Java, dan memodelkan permasalahan sederhana ke algoritma | CPMK0903: Menjelaskan prinsip logika komputasi serta menerapkan teknik dasar pemrograman dan algoritma | CPL09 | Tugas Praktikum: 4%, Kuis 1: 4% (Total: 8%) |
| SCPMK0704-00702: Menerapkan tipe data, variabel, operator, IO, sequence, dan struktur pemilihan ke program Java | CPMK0704: Menerapkan berbagai bahasa dan paradigma pemrograman untuk menyelesaikan masalah komputasi | CPL07 | Tugas Praktikum: 6%, Kuis 1: 6%, UTS Praktik: 10% (Total: 22%) |
| SCPMK0704-00703: Menerapkan struktur perulangan serta array 1/2 dimensi untuk studi kasus dalam program Java | CPMK0704 | CPL07 | Tugas Praktikum: 8%, UTS Praktik: 10%, Kuis 2: 10% (Total: 28%) |
| SCPMK0704-00704: Menerapkan fungsi, parameter, return, dan fungsi rekursif, membangun program Java utuh dan mendemonstrasikannya | CPMK0704 | CPL07 | Tugas Praktikum: 4%, PBL: 8%, UAS: 30% (Total: 42%) |

## RTI251008 — Keselamatan dan Kesehatan Kerja (Semester 1)

**CPL-Prodi:** CPL01

**Bahan Kajian / Materi Pembelajaran:**
- Konsep K3: sejarah, pengertian, dan tujuan K3
- Undang-undang K3: undang-undang yang melandasi K3 dan peraturan pemerintah
- Kesehatan masyarakat: dasar peraturan, pemeriksaan kesehatan sebelum dan setelah kerja
- Lingkungan kerja fisik dan non fisik
- Keselamatan kerja: faktor yang berpengaruh, sumber bahaya, pencegahan kecelakaan kerja
- Alat-alat keselamatan kerja
- Organisasi K3: maksud dan tujuan organisasi K3
- Asuransi: prinsip dasar, jenis-jenis, dan klaim asuransi
- Penerapan protokol kesehatan di pendidikan dan industri era new normal
- Implementasi K3 untuk menciptakan inovasi revolusi industri 4.0

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0101-00801: Menjelaskan sejarah, pengertian, tujuan, lambang K3 serta perundang-undangan dan landasan hukum K3 | CPMK0101: Menunjukkan profesionalisme, etika profesi TI, dan disiplin kerja melalui penerapan K3 | CPL01 | Tugas: 4%, Kuis 1: 8%, UTS: 8% (Total: 20%) |
| SCPMK0101-00802: Menguraikan sistem manajemen K3 serta hubungan faktor penyebab kecelakaan dan sumber bahaya | CPMK0101 | CPL01 | Tugas: 8%, UTS: 12% (Total: 20%) |
| SCPMK0101-00803: Menerapkan manajemen risiko, APD, protokol kesehatan new normal, dan metode statistik K3 | CPMK0101 | CPL01 | Tugas: 6%, Kuis 2: 4%, UAS: 14% (Total: 24%) |
| SCPMK0101-00804: Merancang program kerja, organisasi, komunikasi, audit, dan perbaikan SMK3 termasuk era industri 4.0 | CPMK0101 | CPL01 | Tugas: 6%, Kuis 2: 4%, Case Method: 10%, UAS: 16% (Total: 36%) |

## RTI251009 — Fisika (Semester 1)

**CPL-Prodi:** CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Hakikat dan ruang lingkup fisika
- Pengantar ilmu sains dan metode ilmiah
- Pengukuran dan satuan
- Kinematika gerak lurus dan dua dimensi
- Dinamika partikel
- Usaha dan energi
- Impuls dan momentum
- Medan listrik dan gaya Coulomb
- Potensial listrik
- Kapasitansi dan energi dalam medan listrik
- Arus listrik dan analisis rangkaian listrik DC

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0902-00901: Menjelaskan hakikat fisika, peran fisika dalam TI, metode ilmiah, pengukuran, konversi satuan, ketidakpastian | CPMK0902: Menerapkan prinsip matematis dan struktur diskrit sebagai dasar analisis komputasional | CPL09 | Tugas: 5%, Kuis: 10%, UTS: 10% (Total: 25%) |
| SCPMK0902-00902: Menganalisis kinematika gerak lurus dan dua dimensi serta hukum Newton untuk dinamika partikel | CPMK0902 | CPL09 | Tugas: 6%, UTS: 20% (Total: 26%) |
| SCPMK0902-00903: Menganalisis hubungan usaha-energi serta impuls, momentum, dan hukum kekekalan momentum pada tumbukan | CPMK0902 | CPL09 | Tugas: 3%, Kuis: 10%, UAS: 8% (Total: 21%) |
| SCPMK0902-00904: Menganalisis gaya Coulomb, medan/potensial listrik, kapasitansi, dan rangkaian listrik DC | CPMK0902 | CPL09 | Tugas: 6%, UAS: 22% (Total: 28%) |

## RTI252001 — Agama (Semester 2)

**CPL-Prodi:** CPL01

**Bahan Kajian / Materi Pembelajaran:**
- Pendahuluan: visi pendidikan agama, deskripsi mata kuliah, pendekatan kuliah, tata tertib, dan sistem penilaian
- Manusia dan Agama: konsep agama dan Islam, agama kebutuhan manusia, dimensi ajaran Islam, metode memahami Islam, misi agama Islam, masa depan agama
- Konsep Tauhid: tauhid kebutuhan manusia, problem syirik, dampak tauhid
- Konsep Manusia: manusia dalam pandangan Islam, fungsi dan tugas hidup manusia, hakikat kehidupan dunia dan akhirat
- Wawasan Ekologi dalam Islam: hakikat alam semesta, arti dan sifat sunnatullah, manfaat alam semesta, Islam dan wawasan lingkungan
- Aktualisasi Akhlak: makna perjuangan Rasul, aktualisasi misi Rasul, aplikasi sifat-sifat Rasul dalam ilmu teknologi, ibadah dan pembentukan akhlak
- IPTEKS: hakikat ilmu dalam Islam, paradigma iptek, sumber ilmu pengetahuan, aplikasi pola dzikir dan pikir
- Etos Kerja: etos kerja dalam Islam, motivasi kerja dalam Islam, aktualisasi jihad dalam pembangunan
- Ekonomi: pengertian, prinsip, dan etika ekonomi syariah, pemberdayaan umat, manajemen zakat, wakaf, infak, dan sedekah
- Masyarakat Islam: fungsi keluarga dalam Islam, pembentukan keluarga sakinah, masjid sebagai pusat peradaban

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0102-01001: Menghargai perbedaan keyakinan dan agama dalam interaksi akademik dan sosial | CPMK0102: Menginternalisasi nilai ketakwaan, Pancasila, kewarganegaraan, dan pembelajaran sepanjang hayat | CPL01 | Case Method: 15% (Total: 15%) |
| SCPMK0102-01002: Bertindak jujur dalam pengerjaan tugas, ujian, dan interaksi akademik | CPMK0102 | CPL01 | Tugas: 10%, Kuis 1: 5%, UTS: 10%, Case Method: 15% (Total: 40%) |
| SCPMK0102-01003: Menunjukkan kedisiplinan dan tanggung jawab dalam menyelesaikan kewajiban akademik tepat waktu | CPMK0102 | CPL01 | Kuis 2: 5% (Total: 5%) |
| SCPMK0102-01004: Merefleksikan nilai-nilai keagamaan dalam pengambilan keputusan etis di lingkungan kampus | CPMK0102 | CPL01 | Case Method: 25%, UAS: 15% (Total: 40%) |

## RTI252002 — Aljabar Linier (Semester 2)

**CPL-Prodi:** CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Permodelan Sistem Persamaan Linier (SPL)
- Notasi matriks SPL dan dasar operasi baris elementer
- Metode Gauss dan Gauss-Jordan
- Operasi matriks
- Inversi matriks
- Determinan
- Aturan Cramer
- Vektor
- Eigenvector dan eigenvalue
- Proyeksi ortogonal

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0902-01101: Mampu menyelesaikan SPL menggunakan metode eliminasi dan representasi matriks, serta memvalidasi hasil | CPMK0902: Mahasiswa mampu menguasai prinsip matematis dan struktur diskrit serta pendekatan komputasional | CPL09 | Tugas: 5%, Kuis 1: 10%, UTS: 12.5%, UAS: 10% (Total: 37.5%) |
| SCPMK0902-01102: Mampu menerapkan operasi matriks (invers, transpose, determinan) untuk menyelesaikan permasalahan | CPMK0902 | CPL09 | Tugas: 9%, UTS: 12.5%, Kuis 2: 5%, UAS: 12.5% (Total: 39%) |
| SCPMK0902-01103: Mampu menerapkan konsep vektor dan ruang vektor untuk interpretasi geometri dan komputasi dasar | CPMK0902 | CPL09 | Tugas: 6%, Kuis 2: 5%, UAS: 12.5% (Total: 23.5%) |

## RTI252003 — Desain Antarmuka (Semester 2)

**CPL-Prodi:** CPL02, CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Pengenalan UI/UX dan design thinking
- Persona, journey map, dan kebutuhan pengguna
- Figma, wireframe, visual design, dan design system
- UX writing, prototyping, UX motion, dan usability testing

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0202-01201: Mampu menjelaskan prinsip UI/UX, design thinking, user persona, dan journey map | CPMK0202: Mahasiswa mampu menerapkan prinsip dan metode UX Design untuk merancang prototipe interaktif | CPL02 | Tugas: 8.40%, Kuis 1: 5%, UTS: 12.85% (Total: 26.25%) |
| SCPMK0202-01202: Mampu merancang wireframe, visual design, design system, dan UX writing | CPMK0202 | CPL02 | Tugas: 14.00%, UTS: 7.15%, PBL: 5.70% (Total: 26.85%) |
| SCPMK0601-01203: Mampu menghasilkan prototipe interaktif dan mengevaluasi usability berdasarkan skenario pengujian | CPMK0601: Mahasiswa mampu merancang dan mengevaluasi kualitas pengalaman pengguna melalui prototipe | CPL06 | Tugas: 11.20%, Kuis 2: 5%, UAS: 12.55% (Total: 28.75%) |
| SCPMK0802-01204: Mampu mengelola artefak proyek UI/UX, mempresentasikan rationale desain, dan menyusun rekomendasi perbaikan | CPMK0802: Mahasiswa mampu mengelola proses rekayasa perangkat lunak dan UI/UX dalam siklus hidup proyek | CPL08 | Tugas: 2.80%, PBL: 5.70%, UAS: 9.65% (Total: 18.15%) |

## RTI252004 — Sistem Operasi (Semester 2)

**CPL-Prodi:** CPL02, CPL05, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Konsep sistem operasi dan instalasi Linux
- Terminal, I/O, proses, Bash, memori, dan system call
- Permission, ACL, user/group, layanan, aplikasi, backup, recovery
- Remastering sistem operasi berbasis Linux

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0901-01301: Mampu menjelaskan konsep dasar sistem operasi, kernel, distribusi Linux, instalasi, partisi, sistem file | CPMK0901: Mahasiswa mampu menjelaskan cara kerja sistem komputer dan komponen utamanya | CPL09 | Tugas: 4.50%, Kuis 1: 5%, UTS: 5% (Total: 14.50%) |
| SCPMK0206-01302: Mampu menerapkan perintah terminal, I/O, proses, Bash, memori, dan system call | CPMK0206: Mahasiswa mampu merancang strategi manajemen sumber daya sistem aplikasi multi-platform | CPL02 | Tugas: 7.50%, UTS: 20% (Total: 27.50%) |
| SCPMK0502-01303: Mampu menganalisis permission, ACL, user/group, sudo, dan risiko keamanan administrasi sistem operasi | CPMK0502: Mahasiswa mampu menganalisis isu keamanan sistem operasi, jaringan, dan cloud | CPL05 | Tugas: 10.50%, Kuis 2: 5%, UAS: 10% (Total: 25.50%) |
| SCPMK0208-01304: Mampu mengonfigurasi layanan, aplikasi, backup, recovery, dan remastering Linux sesuai kebutuhan sistem | CPMK0208: Mahasiswa mampu memilih arsitektur computing system sesuai kebutuhan aplikasi multi-platform | CPL02 | Tugas: 20%, PBL: 5%, UAS: 7.50% (Total: 32.50%) |

## RTI252005 — Rekayasa Perangkat Lunak (Semester 2)

**CPL-Prodi:** CPL02, CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar RPL dan Software Development Life Cycle (SDLC)
- Waterfall, Prototype, Spiral, dan RUP
- Agile, Scrum, dan Kanban
- Pseudocode dan Flowchart
- Data Flow Diagram dan Context Diagram
- UML: Use Case, Use Case Specification, Activity Diagram, dan Sequence Diagram
- Kebutuhan Perangkat Lunak
- Desain Perangkat Lunak
- Implementasi
- Testing
- Evolusi Perangkat Lunak

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0205-01405: Mampu merealisasikan blueprint menjadi komponen aplikasi yang modular, maintainable, dan sesuai standar kode | CPMK0205: Mampu menerapkan prinsip dan pola desain perangkat lunak untuk membuat blueprint arsitektural | CPL02 | Case Method: 20% (Total: 20%) |
| SCPMK0211-01403: Mampu mentransformasi kebutuhan menjadi desain teknis menggunakan pemodelan sistem (UML/Diagram) | CPMK0211: Mampu menerapkan metodologi analisis dan desain sistem terstruktur untuk spesifikasi teknis | CPL02 | Tugas: 5%, Kuis: 5% (Total: 10%) |
| SCPMK0602-01404: Mampu merancang arsitektur sistem dan memilih pola desain (Design Patterns) yang sistematis | CPMK0602: Mampu merancang arsitektur dan komponen perangkat lunak menggunakan pola desain yang sesuai | CPL06 | PBL: 10%, UAS: 10% (Total: 20%) |
| SCPMK0607-01402: Mampu menganalisis kebutuhan organisasi dan melakukan elisitasi untuk menghasilkan spesifikasi kebutuhan (SRS) | CPMK0607: Mampu menganalisis kebutuhan organisasi untuk merancang solusi sistem informasi terintegrasi | CPL06 | Tugas: 10% (Total: 10%) |
| SCPMK0802-01401: Mampu menjelaskan prinsip manajemen proses RPL, SDLC, metodologi preskriptif, Agile, SQA, dan pemeliharaan | CPMK0802: Mampu mengelola proses rekayasa perangkat lunak dan desain antarmuka dalam siklus hidup proyek | CPL08 | Tugas: 5%, Kuis: 2.5%, UTS: 2.5%, Case Method: 5%, PBL: 15%, UAS: 10% (Total: 40%) |

## RTI252006 — Basis Data (Semester 2)

**CPL-Prodi:** CPL02, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar Basis Data
- Entity Relationship Diagram
- Contextual Data Model
- Physical Data Model dan Relational Model
- Normalisasi Basis Data
- Pengantar MySQL dan DDL
- DML MySQL
- Query SELECT
- SELECT Multi Table
- Studi Kasus (identifikasi kebutuhan, ERD, pemetaan, dan implementasi basis data)

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0203-01501: Mampu memahami konsep data, basis data relasional, serta merancang model dan skema basis data | CPMK0203: Mampu merancang skema dan arsitektur manajemen data yang efektif dan terstruktur | CPL02 | Tugas: 10%, Kuis: 10%, UTS: 30% (Total: 50%) |
| SCPMK1001-01501: Mampu mengimplementasikan skema basis data dan menyusun query SQL sesuai studi kasus | CPMK1001: Mampu menganalisis permasalahan pengelolaan data untuk merancang solusi berbasis basis data | CPL10 | Tugas: 10%, Kuis: 10% (Total: 20%) |
| SCPMK1001-01502: Mampu menganalisis kebutuhan data, merancang skema, dan menyusun query SQL secara efisien | CPMK1001 | CPL10 | Case Method: 10%, UAS: 20% (Total: 30%) |

## RTI252007 — Praktikum Basis Data (Semester 2)

**CPL-Prodi:** CPL02, CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar Basis Data (Konsep Data, Informasi, Basis Data Relasional)
- Pemodelan Data dan ER Diagram
- Perancangan Basis Data Menggunakan ER Diagram
- Pemetaan ERD ke Model Relasional
- Normalisasi Basis Data
- Implementasi Basis Data dengan MySQL (DDL)
- Pengelolaan Data dengan SQL (DML)
- Query Data (SQL-DQL dan Multi Table)
- Studi Kasus Terpadu: Perancangan dan Implementasi Basis Data

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0203-01601: Mampu mengimplementasikan perancangan model dan skema basis data konseptual dan logikal melalui praktikum | CPMK0203: Mampu merancang skema dan arsitektur manajemen data yang efektif dan terstruktur | CPL02 | Laporan Praktikum: 12.5%, Kuis: 7.5%, Case Method: 15% (Total: 35%) |
| SCPMK0701-01601: Mampu mengimplementasikan skema basis data dan mengeksekusi query SQL sesuai studi kasus | CPMK0701: Mampu merancang, mengimplementasikan, dan mengevaluasi sistem manajemen data yang handal | CPL07 | Laporan Praktikum: 12.5%, Kuis: 7.5%, Case Method: 15% (Total: 35%) |
| SCPMK1001-01601: Mampu mengimplementasikan perancangan skema basis data dan implementasinya melalui query SQL | CPMK1001: Mampu menganalisis permasalahan pengelolaan data untuk merancang solusi berbasis basis data | CPL10 | Case Method: 30% (Total: 30%) |

## RTI252008 — Algoritma dan Struktur Data (Semester 2)

**CPL-Prodi:** CPL02, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Searching
- Sorting
- Queue
- Stack
- Linked List
- Tree
- Graph
- Brute Force
- Divide-Conquer
- Depth First Search
- Breadth First Search

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0207-01701: Mampu menjelaskan karakteristik struktur data serta alur pengelolaan data untuk penyelesaian masalah komputasi | CPMK0207: Mampu menganalisis kompleksitas permasalahan komputasi serta merancang struktur data dan algoritma optimal | CPL02 | Tugas: 10%, Kuis 2 (Tes tulis 3/Asessment 1): 20%, UAS (Tes tulis 4/Asessment 2): 20% (Total: 50%) |
| SCPMK0903-01701: Mampu menganalisis permasalahan komputasi pada struktur data array of object dan membandingkan pendekatan algoritmik | CPMK0903: Mahasiswa mampu menjelaskan prinsip logika komputasi serta teknik dasar pemrograman dan algoritma | CPL09 | Tugas: 10%, Kuis 1 (Tes tulis 1/Asessment 1): 20%, UTS (Tes tulis 2/Asessment 2): 20% (Total: 50%) |

## RTI252009 — Praktikum Algoritma dan Struktur Data (Semester 2)

**CPL-Prodi:** CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Searching
- Sorting
- Queue
- Stack
- Linked List
- Tree
- Graph
- Brute Force
- Divide-Conquer
- Depth First Search
- Breadth First Search

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0903-01801: Mampu menerapkan teknik dasar pemrograman dan algoritma untuk menyelesaikan masalah komputasi menggunakan array of object | CPMK0903: Mahasiswa mampu menjelaskan prinsip logika komputasi serta teknik dasar pemrograman dan algoritma | CPL09 | Tugas: 5%, Tes Praktik 1 (Asessment 1): 20%, Tes Case Method 1 (Asessment 2): 25.5% (Total: 50.5%) |
| SCPMK0708-01801: Mampu mengimplementasikan struktur data linear dan mengintegrasikannya ke dalam algoritma untuk penyelesaian masalah | CPMK0708: Mampu menerapkan konsep struktur data dalam perancangan dan implementasi algoritma efisien | CPL07 | Tugas: 2%, Tes Case Method 2 (Asessment 1): 25.5% (Total: 27.5%) |
| SCPMK0703-01801: Mampu memilih dan mengimplementasikan struktur data non-linear serta koleksi data untuk solusi efisien | CPMK0703: Mampu memilih dan mengimplementasikan struktur data serta algoritma yang efisien | CPL07 | Tugas: 2%, Tes Praktik 2 (Asessment 1): 20% (Total: 22%) |

## RTI253001 — Manajemen Proyek (Semester 3)

**CPL-Prodi:** CPL03, CPL04, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Konsep proyek, fase, dan 10 knowledge area manajemen proyek
- Manajemen integrasi, ruang lingkup, waktu, dan biaya proyek
- Manajemen kualitas, SDM, dan pengadaan proyek
- Manajemen komunikasi, risiko, dan pemangku kepentingan proyek
- Agile (Scrum, Kanban, XP), penutupan proyek, dan simulasi proyek perangkat lunak

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0801-01901: Mampu menjelaskan konsep proyek, fase, 10 knowledge area PMBOK, dan menyusun perencanaan proyek | CPMK0801: Mahasiswa mampu menyusun rencana proyek TI mencakup estimasi, penjadwalan, alokasi sumber daya, risiko | CPL08 | Tugas Proyek: 10%, Kuis 1: 7%, UTS: 15%, UAS: 8% (Total: 40%) |
| SCPMK0803-01902: Mampu menerapkan manajemen sumber daya, pengadaan, kualitas, risiko, dan prinsip Agile | CPMK0803: Mahasiswa mampu melaksanakan eksekusi, monitoring, dan controlling proyek serta mengelola dinamika tim | CPL08 | Tugas Proyek: 8%, UTS: 5%, Kuis 2: 7%, UAS: 8% (Total: 28%) |
| SCPMK0302-01903: Mampu mengelola pemangku kepentingan, komunikasi, dan kerja sama tim proyek | CPMK0302: Mahasiswa mampu mengelola tim dan proyek melalui perencanaan, koordinasi, komunikasi, presentasi hasil | CPL03 | Tugas Proyek: 2%, Kuis 1: 3%, UTS: 5%, Kuis 2: 3%, UAS: 5% (Total: 18%) |
| SCPMK0402-01904: Mampu menyusun dokumentasi dan evaluasi proyek perangkat lunak secara sistematis | CPMK0402: Mahasiswa mampu mendokumentasikan proyek TI secara sistematis dalam bentuk laporan teknis | CPL04 | Tugas Proyek: 6%, UAS: 8% (Total: 14%) |

## RTI253002 — Sistem Informasi Manajemen (Semester 3)

**CPL-Prodi:** CPL02, CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Konsep dasar sistem dan informasi
- Struktur dan komponen SIM
- Organisasi dan pengambilan keputusan
- SI strategis dan antar organisasi
- Database, TIK, dan pengembangan SIM

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0211-02001: Mampu menganalisis konsep dasar sistem, informasi, dan struktur SIM untuk kebutuhan organisasi | CPMK0211: Mahasiswa mampu menerapkan metodologi analisis dan desain sistem terstruktur untuk spesifikasi teknis | CPL02 | Tugas: 10%, Kuis 1: 5% (Total: 15%) |
| SCPMK0211-02002: Mampu merancang model konseptual SIM berdasarkan analisis proses bisnis dan alur keputusan | CPMK0211 | CPL02 | Tugas: 5%, CM: 5% (Total: 10%) |
| SCPMK0607-02003: Mampu menerapkan konsep SI strategis dan pendukung untuk pengelolaan informasi organisasi kompleks | CPMK0607: Mahasiswa mampu mengembangkan solusi sistem informasi manajemen terintegrasi yang kompleks | CPL06 | Tugas: 5%, CM: 30%, Kuis 2: 5% (Total: 40%) |
| SCPMK0802-02004: Mampu menyusun rencana pengembangan SIM menggunakan pendekatan SDLC yang tepat | CPMK0802: Mahasiswa mampu menerapkan rekayasa perangkat lunak dan prinsip SDLC dalam siklus hidup proyek | CPL08 | CM: 20%, UAS: 15% (Total: 35%) |

## RTI253003 — Kewarganegaraan (Semester 3)

**CPL-Prodi:** CPL01

**Bahan Kajian / Materi Pembelajaran:**
- Identitas Nasional
- Negara dan Konstitusi
- Hubungan Negara dan Warga Negara
- Negara Hukum
- Demokrasi
- Hak Asasi Manusia
- Wawasan Nusantara
- Ketahanan Nasional
- Integrasi Nasional

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0102-02101: Menjelaskan konsep identitas nasional, negara, konstitusi, dan hubungan negara-warga negara | CPMK0102: Menginternalisasi nilai ketakwaan, Pancasila, kewarganegaraan, dan tanggung jawab sosial | CPL01 | Tugas: 8%, Kuis: 4%, UTS: 10%, UAS: 10% (Total: 32%) |
| SCPMK0102-02102: Menganalisis sistem demokrasi dan negara hukum dalam kehidupan berbangsa dan bernegara di Indonesia | CPMK0102 | CPL01 | Tugas: 6%, Kuis: 3%, UTS: 8%, PBL: 5%, UAS: 10% (Total: 32%) |
| SCPMK0102-02103: Menjelaskan konsep HAM, prinsip-prinsipnya, dan mekanisme penegakannya | CPMK0102 | CPL01 | Tugas: 3%, Kuis: 2%, UTS: 1%, PBL: 5%, UAS: 8% (Total: 19%) |
| SCPMK0102-02104: Menguraikan wawasan nusantara, ketahanan nasional, dan integrasi nasional | CPMK0102 | CPL01 | Tugas: 3%, Kuis: 1%, UTS: 1%, PBL: 5%, UAS: 7% (Total: 17%) |

## RTI253004 — Desain dan Pemrograman Web (Semester 3)

**CPL-Prodi:** CPL02, CPL06, CPL07

**Bahan Kajian / Materi Pembelajaran:**
- HTML, CSS, JavaScript dasar, dan konsep client-server
- PHP, form processing, upload, cookie, dan session
- MySQL dan pemrograman database dengan PHP
- Hosting dan proyek aplikasi web sederhana

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0704-02201: Menerapkan HTML, CSS, JavaScript dasar, dan PHP untuk membangun halaman web | CPMK0704: Menerapkan berbagai bahasa dan paradigma pemrograman untuk menyelesaikan masalah komputasi | CPL07 | Tugas: 9%, Kuis 1: 5%, UTS: 10% (Total: 24.00%) |
| SCPMK0209-02202: Memilih mekanisme client-server, form, session, cookie, dan database sesuai kebutuhan | CPMK0209: Memilih dan menerapkan teknologi pengembangan berbasis platform | CPL02 | Tugas: 9%, UTS: 10% (Total: 19.00%) |
| SCPMK0603-02203: Mengimplementasikan aplikasi web dinamis dengan PHP dan MySQL serta debugging | CPMK0603: Mengimplementasikan dan melakukan deployment aplikasi web/mobile/framework | CPL06 | Tugas: 8%, Kuis 2: 5%, UAS: 12.50% (Total: 25.50%) |
| SCPMK0603-02204: Menghasilkan aplikasi web sederhana yang dapat dipresentasikan dan diunggah ke hosting | CPMK0603 | CPL06 | Tugas: 8%, PBL: 11%, UAS: 12.50% (Total: 31.50%) |

## RTI253005 — Basis Data Lanjut (Semester 3)

**CPL-Prodi:** CPL02, CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengenalan PostgreSQL dan query dasar
- Query lanjutan: sub-query, JOIN, grouping, dan CTE
- Indeks dan optimasi query
- Function, view, materialized view, dan stored procedure
- Transaksi, concurrency, full-text search, dan JSONB
- Backup-restore dan migrasi basis data
- Integrasi basis data dengan aplikasi dan studi kasus

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0203-02301: Mengoperasikan PostgreSQL, query dasar (DDL, DML) serta lanjutan (sub-query, JOIN, grouping, CTE) | CPMK0203: Merancang skema dan arsitektur manajemen data yang efektif dan terstruktur | CPL02 | Tugas: 10%, Kuis 1: 10%, UTS: 5% (Total: 25%) |
| SCPMK0203-02302: Mengimplementasikan optimasi query dengan indeks serta membangun objek basis data | CPMK0203 | CPL02 | Tugas: 5%, UTS: 8% (Total: 13%) |
| SCPMK0701-02303: Menerapkan transaksi, concurrency, full-text search, JSONB, backup-restore, migrasi | CPMK0701: Membangun sistem manajemen data yang handal untuk penyimpanan dan pengelolaan informasi | CPL07 | Tugas: 5%, UTS: 7% (Total: 12%) |
| SCPMK1001-02304: Mengintegrasikan PostgreSQL dengan aplikasi dan studi kasus kompleks | CPMK1001: Menganalisis permasalahan pengelolaan data kompleks dengan wawasan multidisiplin | CPL10 | Tugas: 5%, PBL: 20%, UAS: 25% (Total: 50%) |

## RTI253006 — Metode Numerik (Semester 3)

**CPL-Prodi:** CPL09, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar metode numerik dan galat
- Sistem persamaan linear: Gauss, Gauss-Jordan, Gauss-Seidel
- Persamaan nonlinear: metode tertutup dan terbuka
- Diferensiasi numerik
- Integrasi numerik: Riemann, trapezoidal, Simpson
- Interpolasi dan regresi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0902-02401: Menjelaskan konsep metode numerik, galat, dan menyelesaikan SPL dengan Gauss, Gauss-Jordan, Gauss-Seidel | CPMK0902: Menerapkan prinsip matematis dan pendekatan komputasi untuk persoalan komputasional | CPL09 | Tugas: 8%, Kuis 1: 10%, UTS: 10% (Total: 28%) |
| SCPMK0902-02402: Menyelesaikan persamaan nonlinear dengan metode tertutup dan terbuka | CPMK0902 | CPL09 | Tugas: 4%, UTS: 15% (Total: 19%) |
| SCPMK0902-02403: Menyelesaikan diferensiasi dan integrasi numerik (Riemann, trapezoidal, Simpson) | CPMK0902 | CPL09 | Tugas: 5%, Kuis 2: 10%, UAS: 15% (Total: 30%) |
| SCPMK1007-02404: Menerapkan interpolasi dan regresi numerik untuk aproksimasi fungsi dan analisis data | CPMK1007: Mengembangkan solusi numerik berbasis pendekatan komputasi diskrit | CPL10 | Tugas: 3%, UAS: 20% (Total: 23%) |

## RTI253007 — Pemrograman Berbasis Objek (Semester 3)

**CPL-Prodi:** CPL02, CPL06, CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Konsep dasar OOP: kelas, objek, enkapsulasi
- Relasi kelas, inheritance, dan overriding
- Interface, kelas abstrak, dan polymorfisme
- GUI dan Java API
- Java GUI dengan database

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0210-02501: Menjelaskan prinsip OOP (enkapsulasi, inheritance, polymorfisme) dan menerapkannya dalam rancangan kelas | CPMK0210: Memahami dan menerapkan prinsip fundamental RPL dan OOP untuk spesifikasi teknis terstruktur | CPL02 | Tugas: 5%, Kuis 1: 5%, UTS: 10%, CM: 10% (Total: 30%) |
| SCPMK0704-02502: Mengimplementasikan konsep OOP menggunakan Java dalam berbagai paradigma pemrograman | CPMK0704: Menggunakan berbagai bahasa dan paradigma pemrograman berorientasi objek | CPL07 | Tugas: 5%, CM: 30%, Kuis 2: 5% (Total: 40%) |
| SCPMK0903-02503: Membangun aplikasi Java berbasis GUI dan database menggunakan prinsip OOP secara menyeluruh | CPMK0903: Menerapkan logika komputasi, PBO, dan algoritma untuk membangun aplikasi perangkat lunak | CPL09 | Tugas: 5%, CM: 15%, UAS: 10% (Total: 30%) |
| SCPMK0211-02504: Menerapkan konsep inheritance dalam pemodelan kelas untuk desain modular, reusable, scalable | CPMK0211: Menerapkan metodologi analisis dan desain sistem terstruktur untuk spesifikasi teknis komprehensif | CPL02 | terintegrasi dengan penilaian Minggu 6–7 (tidak ada bobot terpisah) |
| SCPMK0606-02505: Merancang dan mengimplementasikan struktur kelas dengan enkapsulasi dan interface yang jelas | CPMK0606: Mengelola proses deployment dan rencana pemeliharaan perangkat lunak sesuai SDLC | CPL06 | terintegrasi dengan penilaian Minggu 3, 11 (tidak ada bobot terpisah) |
| SCPMK0607-02506: Mengimplementasikan integrasi antar subsistem melalui interface dan API, GUI dan persistensi data | CPMK0607: Menganalisis kebutuhan organisasi untuk solusi sistem informasi terintegrasi yang kompleks | CPL06 | terintegrasi dengan penilaian Minggu 15–16 (tidak ada bobot terpisah) |

## RTI253008 — Praktikum Pemrograman Berbasis Objek (Semester 3)

**CPL-Prodi:** CPL02, CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Kelas, objek, enkapsulasi, konstruktor, dan relasi kelas
- Inheritance, overriding, overloading, kelas abstrak, dan interface
- Polymorfisme, exception handling, collections, dan generics
- GUI Swing: komponen dasar dan event handling
- Koneksi database JDBC dan aplikasi terintegrasi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0210-02601: Mengimplementasikan kelas, enkapsulasi, relasi kelas, dan inheritance dalam kode Java yang berfungsi | CPMK0210: Menerapkan prinsip fundamental OOP dalam implementasi kode Java yang terstruktur | CPL02 | Tugas: 12%, Kuis 1: 5%, UTS: 8% (Total: 25%) |
| SCPMK0704-02602: Mengimplementasikan overriding, overloading, interface, kelas abstrak, dan polymorfisme pada kasus nyata | CPMK0704: Menggunakan bahasa Java dengan berbagai paradigma OOP untuk masalah komputasi berbasis kasus | CPL07 | Tugas: 10%, UTS: 7%, Kuis 2: 5%, PBL: 10% (Total: 32%) |
| SCPMK0903-02603: Membangun aplikasi Java berbasis GUI (Swing/JavaFX) dengan koneksi database JDBC | CPMK0903: Membangun aplikasi Java lengkap berbasis GUI dan koneksi database menggunakan OOP | CPL09 | Tugas: 8%, PBL: 12%, UAS: 23% (Total: 43%) |

## RTI253009 — Bahasa Inggris 2 (Semester 3)

**CPL-Prodi:** CPL01, CPL03

**Bahan Kajian / Materi Pembelajaran:**
- Reading: kosakata teknis IT, pemahaman teks teknis, dan membaca literatur
- Writing: paragraf akademik, laporan teknis, dan CV serta email profesional
- Listening: ceramah dan presentasi teknis
- Speaking: diskusi, presentasi teknis, dan wawancara simulasi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0102-02701: Membaca dan memahami teks teknis bahasa Inggris bidang TI serta mengekspresikan ide akademik secara tertulis | CPMK0102: Menunjukkan sikap profesional, pembelajaran sepanjang hayat, dan tanggung jawab akademik internasional | CPL01 | Tugas: 15%, Kuis 1: 5%, UTS: 10%, UAS: 10% (Total: 40%) |
| SCPMK0303-02702: Berkomunikasi lisan dalam bahasa Inggris pada diskusi teknis, presentasi, dan wawancara simulasi | CPMK0303: Mengembangkan kemampuan komunikasi profesional dalam bahasa Inggris untuk keperluan akademik dan teknis | CPL03 | Tugas: 15%, UTS: 5%, Kuis 2: 5%, PBL: 22%, UAS: 13% (Total: 60%) |

## RTI254001 — Sistem Pendukung Keputusan (Semester 4)

**CPL-Prodi:** CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Konsep SPK, teori keputusan, dan MCDM dasar (WSM, WPM)
- Pembobotan subjektif: AHP (benefit dan cost)
- Metode perankingan lanjutan: ROC, EDAS, MARCOS, MEREC
- GDSS dan metode fuzzy untuk ketidakpastian
- Perancangan, implementasi, dan evaluasi sistem DSS

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0706-02801: Menjelaskan konsep dan evolusi SPK, teori pengambilan keputusan, menerapkan metode baseline WSM/WPM | CPMK0706: Mengimplementasikan berbagai metode MCDM dan SPK untuk pengambilan keputusan multi-kriteria | CPL07 | Tugas: 5.6%, Kuis 1: 5%, UTS: 5% (Total: 15.6%) |
| SCPMK0706-02802: Menerapkan metode AHP untuk pembobotan kriteria benefit maupun cost | CPMK0706 | CPL07 | Tugas: 8.4%, UTS: 8% (Total: 16.4%) |
| SCPMK0706-02803: Menerapkan metode ROC, EDAS, MARCOS, MEREC untuk perankingan dan pembobotan objektif | CPMK0706 | CPL07 | Tugas: 11.2%, UTS: 7%, Kuis 2: 5% (Total: 23.2%) |
| SCPMK0706-02804: Mengimplementasikan GDSS dan metode fuzzy untuk ketidakpastian dan penilaian linguistik | CPMK0706 | CPL07 | Tugas: 5.6%, PBL: 5.7% (Total: 11.3%) |
| SCPMK1005-02805: Merancang, mengimplementasikan, dan mengevaluasi sistem DSS lengkap dengan analisis metrik kinerja | CPMK1005: Mengevaluasi dan membandingkan kinerja metode-metode SPK berdasarkan akurasi, konsistensi, interpretabilitas | CPL10 | Tugas: 2.8%, PBL: 5.7%, UAS: 25% (Total: 33.5%) |

## RTI254002 — Analisis dan Desain Berorientasi Objek (Semester 4)

**CPL-Prodi:** CPL02, CPL06, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Paradigma OO dan pemodelan kebutuhan: domain model, use case, use case description
- Robustness analysis dan activity diagram
- Pemutakhiran domain model, sequence diagram, dan class diagram
- Advanced class diagram, state machine diagram, dan deployment diagram
- Penyusunan dan review Spesifikasi Kebutuhan Perangkat Lunak (SKPL)

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0211-02901: Menganalisis kebutuhan sistem dan memodelkan domain dengan UML (use case, class, sequence, activity) | CPMK0211: Menerapkan metodologi analisis dan desain berorientasi objek untuk spesifikasi teknis komprehensif | CPL02 | Tugas: 12%, Kuis 1: 5%, UTS: 8% (Total: 25%) |
| SCPMK0602-02902: Merancang struktur komponen dan arsitektur perangkat lunak OO dengan UML lanjutan | CPMK0602: Merancang komponen perangkat lunak menggunakan software design pattern yang tepat | CPL06 | Tugas: 10%, UTS: 5%, Kuis 2: 5%, PBL: 10% (Total: 30%) |
| SCPMK1008-02903: Mengintegrasikan artefak ADBO (SRS, model domain, diagram arsitektur) menjadi spesifikasi teknis | CPMK1008: Mengintegrasikan hasil analisis dan desain sistem OO ke dalam spesifikasi pengembangan yang implementable | CPL10 | Tugas: 8%, PBL: 12%, UAS: 25% (Total: 45%) |

## RTI254003 — Bahasa Indonesia (Semester 4)

**CPL-Prodi:** CPL03, CPL04

**Bahan Kajian / Materi Pembelajaran:**
- Ragam bahasa, ejaan, diksi, dan kalimat efektif
- Paragraf, laporan teknis, proposal, dan presentasi ilmiah
- Karya tulis ilmiah: struktur, rumusan masalah, metodologi
- Sitasi, daftar pustaka, abstrak, dan artikel ilmiah

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0301-03001: Menulis laporan teknis, makalah, dan proposal dalam bahasa Indonesia yang baku, sistematis, efektif | CPMK0301: Mengelola diri secara profesional, berkomunikasi efektif lisan dan tulisan dalam bahasa Indonesia baku | CPL03 | Tugas: 15%, Kuis 1: 5%, UTS: 8%, UAS: 10% (Total: 38%) |
| SCPMK0401-03002: Menyusun karya tulis ilmiah sederhana dengan rumusan masalah, metodologi, pembahasan, kesimpulan valid | CPMK0401: Menganalisis masalah dan menulis karya ilmiah berbasis data menggunakan kaidah bahasa Indonesia | CPL04 | Tugas: 15%, UTS: 7%, Kuis 2: 5%, PBL: 22%, UAS: 13% (Total: 62%) |

## RTI254004 — Kecerdasan Artifisial (Semester 4)

**CPL-Prodi:** CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar AI, agen cerdas, dan algoritma pencarian
- Representasi pengetahuan, logika, dan sistem inferensi
- Sistem pakar, Jaringan Bayes, dan probabilistic reasoning
- Machine learning, NLP dasar, dan Computer Vision dasar

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0706-03101: Mampu mengimplementasikan algoritma pencarian, representasi pengetahuan, dan sistem inferensi berbasis aturan | CPMK0706: Mahasiswa mampu mengembangkan sistem cerdas berbasis AI, ML, dan analisis data untuk keputusan bermakna | CPL07 | Tugas: 18%, Kuis 1: 5%, UTS: 10%, PBL: 12%, UAS: 10% (Total: 55%) |
| SCPMK1005-03102: Mampu mengevaluasi dan membandingkan kinerja berbagai algoritma AI berdasarkan metrik evaluasi yang sesuai | CPMK1005: Mahasiswa mampu mengevaluasi solusi sistem cerdas berdasarkan kinerja, keandalan, dan interpretabilitas | CPL10 | Tugas: 12%, UTS: 5%, Kuis 2: 5%, PBL: 10%, UAS: 13% (Total: 45%) |

## RTI254005 — Jaringan Komputer (Semester 4)

**CPL-Prodi:** CPL05, CPL09, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar jaringan, model OSI, TCP/IP, dan media transmisi
- Protokol application, transport, dan network layer
- Wireless networking dan data link layer
- Keamanan jaringan: ancaman, firewall, VPN, dan monitoring

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0504-03201: Mampu menganalisis arsitektur jaringan (OSI, TCP/IP) dan mengkonfigurasi protokol pada setiap lapisan | CPMK0504: Mahasiswa mampu merancang arsitektur, memilih protokol, dan mengkonfigurasi infrastruktur jaringan komputer | CPL05 | Tugas: 12%, UTS: 5%, PBL: 12%, UAS: 12% (Total: 41%) |
| SCPMK0901-03202: Mampu menjelaskan komponen jaringan (router, switch, media transmisi) dan cara kerja protokol komunikasi | CPMK0901: Mahasiswa mampu menjelaskan cara kerja sistem komputer dan komponen utama infrastruktur jaringan | CPL09 | Tugas: 10%, Kuis 1: 5%, UTS: 8% (Total: 23%) |
| SCPMK1002-03203: Mampu menganalisis ancaman keamanan jaringan dan merekomendasikan mekanisme perlindungan yang sesuai | CPMK1002: Mahasiswa mampu menganalisis mekanisme keamanan jaringan untuk melindungi data dan layanan digital | CPL10 | Tugas: 8%, Kuis 2: 5%, PBL: 10%, UAS: 13% (Total: 36%) |

## RTI254006 — Praktikum Jaringan Komputer (Semester 4)

**CPL-Prodi:** CPL05, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Media dan konfigurasi perangkat jaringan
- Protokol lapisan aplikasi dan transport
- IPv4, subnetting, dan routing
- Packet Tracer dan analisis traffic

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0504-03301: Mampu mengkonfigurasi perangkat jaringan (NIC, router, switch) dan melakukan pengujian konektivitas | CPMK0504: Mahasiswa mampu memilih arsitektur, protokol, dan mengkonfigurasi infrastruktur jaringan komputer secara praktis | CPL05 | Tugas: 7%, PBL: 18% (Total: 25%) |
| SCPMK0504-03302: Mampu melakukan subnetting IPv4 dan konfigurasi routing dasar menggunakan Packet Tracer | CPMK0504 | CPL05 | Tugas: 7%, Kuis 1: 5%, PBL: 19% (Total: 31%) |
| SCPMK0901-03303: Mampu menganalisis traffic jaringan menggunakan tools (ping, traceroute, ARP) dan mendokumentasikan hasilnya | CPMK0901: Mahasiswa mampu menerapkan cara kerja sistem jaringan komputer melalui praktikum konfigurasi dan troubleshooting | CPL09 | Tugas: 6%, Kuis 2: 5%, PBL: 18%, UAS: 15% (Total: 44%) |

## RTI254007 — Pemrograman Web Lanjut (Semester 4)

**CPL-Prodi:** CPL02, CPL06, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Laravel, MVC, routing, controller, view, dan Git
- Migration, Eloquent ORM, Blade, layout, dan validasi
- Authentication, authorization, import/export, API, testing, dan proyek Laravel

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0209-03401: Mampu menerapkan konsep framework web, MVC, routing, controller, view, dan version control | CPMK0209: Mahasiswa mampu memilih dan menerapkan teknologi pengembangan berbasis platform untuk membangun aplikasi | CPL02 | Tugas: 10%, UTS: 10%, PBL: 3.33% (Total: 23.33%) |
| SCPMK0603-03402: Mampu mengimplementasikan migration, ORM, Blade, layout, validasi, auth, import/export, dan API pada Laravel | CPMK0603: Mahasiswa mampu mengimplementasikan dan melakukan deployment aplikasi web, mobile, atau framework | CPL06 | Tugas: 35%, UTS: 10%, PBL: 5.34% (Total: 50.34%) |
| SCPMK1006-03403: Mampu mengevaluasi kualitas aplikasi Laravel berdasarkan fungsi, keamanan, API, dan kebutuhan pengguna | CPMK1006: Mahasiswa mampu mengevaluasi dan mengembangkan aplikasi web/mobile berdasarkan kebutuhan, kualitas, dan UX | CPL10 | Tugas: 8%, Kuis: 5%, PBL: 5%, UAS: 8.33% (Total: 26.33%) |

## RTI254008 — Statistik Komputasi (Semester 4)

**CPL-Prodi:** CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Statistika deskriptif dan probabilitas
- Distribusi dan inferensi statistik
- Regresi, ANOVA, dan uji non-parametrik
- Simulasi Monte Carlo dan analisis data eksploratori
- Visualisasi data dan time series dasar

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0707-03501: Mampu mengimplementasikan metode statistika deskriptif dan inferensial menggunakan perangkat komputasi (Python/R) | CPMK0707: Mahasiswa mampu melakukan pemodelan dan simulasi statistika komputasi untuk analisis dan pengambilan keputusan berbasis data | CPL07 | Tugas: 18%, UTS: 7%, Kuis 2: 5%, PBL: 22%, UAS: 13% (Total: 65%) |
| SCPMK0902-03502: Mampu menerapkan metode probabilitas, distribusi, dan pengujian hipotesis dalam analisis data TI | CPMK0902: Mahasiswa mampu menerapkan prinsip matematis dan statistik untuk analisis komputasional masalah TI | CPL09 | Tugas: 12%, Kuis 1: 5%, UTS: 8%, UAS: 10% (Total: 35%) |

## RTI254009 — Proyek Sistem Informasi (Semester 4)

**CPL-Prodi:** CPL03, CPL06, CPL08, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Perencanaan proyek: WBS, jadwal, anggaran, risiko
- Metodologi SDLC dan Scrum/Agile
- Implementasi SI berbasis web: back-end, front-end, dan database
- Sprint execution, review, dan retrospective
- Deployment, UAT, laporan akhir, dan demo proyek

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0801-03601: Mampu menyusun rencana proyek SI meliputi WBS, jadwal, anggaran, dan risk register | CPMK0801: Mahasiswa mampu merencanakan proyek sistem informasi dengan estimasi sumber daya, jadwal, dan manajemen risiko | CPL08 | Dok.Perencanaan: 15% (Total: 15%) |
| SCPMK0802-03602: Mampu mengimplementasikan SI berbasis web menggunakan metodologi SDLC dengan dokumentasi lengkap | CPMK0802: Mahasiswa mampu mengimplementasikan siklus hidup rekayasa perangkat lunak secara menyeluruh dalam pengembangan SI | CPL06 | Sprint 1-2: 7%, Sprint 3: 10% (Total: 17%) |
| SCPMK1008-03605: Mampu mengintegrasikan hasil analisis kebutuhan dan arsitektur SI ke dalam tech stack dan rencana pengembangan yang koheren | CPMK1008: Mampu mengintegrasikan hasil analisis dan desain sistem ke dalam proses pengembangan perangkat lunak secara koheren | CPL10 | Sprint 1-2: 3% (Total: 3%) |
| SCPMK0803-03603: Mampu melaksanakan sprint review, monitoring kemajuan, dan mengelola dinamika tim proyek SI | CPMK0803: Mahasiswa mampu mengeksekusi, memonitor, dan mengendalikan proyek serta mengelola tim secara profesional | CPL08 | UTS Milestone: 15%, Laporan: 4%, UAS Demo: 8% (Total: 27%) |
| SCPMK0302-03606: Mampu mengelola dinamika tim proyek dan menyampaikan hasil kerja tim kepada pemangku kepentingan secara profesional | CPMK0302: Mampu mengelola tim dan proyek secara terencana, dari perencanaan hingga penyampaian hasil ke pemangku kepentingan | CPL03 | Laporan: 1%, UAS Demo: 2% (Total: 3%) |
| SCPMK0607-03604: Mampu mengintegrasikan front-end, back-end, dan database dalam sistem informasi yang deployable | CPMK0607: Mahasiswa mampu menghasilkan solusi sistem informasi terintegrasi yang menjawab kebutuhan pengguna nyata | CPL06 | Sprint 1-2: 10%, Sprint 3: 10%, Laporan: 5%, UAS Demo: 10% (Total: 35%) |

## RTI255001 — Kewirausahaan Berbasis Teknologi (Semester 5)

**CPL-Prodi:** CPL01, CPL03

**Bahan Kajian / Materi Pembelajaran:**
- Konsep kewirausahaan, karakteristik wirausaha, dan intensi kewirausahaan
- Analisis pasar, aspek teknis bisnis, dan manajemen keuangan dasar
- Business Model Canvas, sumber pendanaan, dan aspek legal bisnis
- Manajemen SDM dan pengembangan produk baru
- Penyusunan dan presentasi rencana bisnis teknologi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0101-03701: Mampu menjelaskan konsep kewirausahaan, karakteristik wirausaha, intensi kewirausahaan, serta membangkitkan/memilih ide produk teknologi | CPMK0101: Mahasiswa mampu menerapkan etika profesi, jiwa kewirausahaan berbasis teknologi, dan tanggung jawab sosial | CPL01 | CM: 13%, Tugas: 5%, Kuis: 5%, UTS: 5% (Total: 28%) |
| SCPMK0101-03702: Mampu menganalisis permintaan pasar, menyusun rencana pemasaran, aspek teknis bisnis, serta laporan keuangan dasar dan penetapan harga | CPMK0101 | CPL01 | Tugas: 23%, Kuis: 5%, UTS: 5% (Total: 33%) |
| SCPMK0301-03703: Mampu merancang Business Model Canvas, menganalisis sumber pendanaan, aspek hukum, tanggung jawab sosial, SDM, dan strategi produk baru | CPMK0301: Mahasiswa mampu mengelola diri secara profesional, berkomunikasi efektif, dan mempresentasikan rencana bisnis teknologi | CPL03 | CM: 12%, Tugas: 7% (Total: 19%) |
| SCPMK0301-03704: Mampu menyusun dan mempresentasikan rencana bisnis teknologi secara profesional dengan argumentasi berbasis data | CPMK0301 | CPL03 | UAS: 20% (Total: 20%) |

## RTI255002 — Metodologi Penelitian (Semester 5)

**CPL-Prodi:** CPL04, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Jenis penelitian dan etika ilmiah
- Studi literatur dan identifikasi masalah
- Metode penelitian dan pengumpulan data
- Analisis data dan pemodelan sistem
- Penulisan proposal penelitian

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0403-03801: Mampu menjelaskan jenis-jenis penelitian TI, etika penelitian, dan melakukan studi literatur yang sistematis | CPMK0403: Mahasiswa mampu merumuskan masalah penelitian, metodologi, dan menyusun proposal penelitian TI secara ilmiah | CPL04 | Tugas: 4.50%, Kuis 1: 5%, PBL: 5% (Total: 14.50%) |
| SCPMK0403-03802: Mampu merumuskan masalah, tujuan, manfaat, dan kerangka konseptual penelitian TI | CPMK0403 | CPL04 | Tugas: 3%, PBL: 15% (Total: 18%) |
| SCPMK0403-03803: Mampu menyusun metode penelitian (pengumpulan data, instrumen, validitas) dan penulisan proposal skripsi/LA | CPMK0403 | CPL04 | Tugas: 5.50%, PBL: 25%, UAS: 8% (Total: 38.50%) |
| SCPMK0401-03804: Mampu menganalisis data penelitian secara kuantitatif/kualitatif dan mempresentasikan hasil secara saintifik | CPMK0401: Mahasiswa mampu menganalisis masalah kompleks dan menghasilkan solusi rasional berbasis data yang dideskripsikan secara saintifik | CPL04 | Tugas: 2%, Kuis 2: 5%, PBL: 10%, UAS: 9% (Total: 26%) |
| SCPMK1009-03805: Mampu mengidentifikasi tahapan penyelesaian ilmiah yang tepat untuk menyelesaikan persoalan kompleks di bidang informatika | CPMK1009: Mampu mengidentifikasi tahapan penyelesaian ilmiah yang tepat untuk persoalan kompleks di bidang informatika | CPL10 | UAS: 3% (Total: 3%) |

## RTI255003 — Pemrograman Mobile (Semester 5)

**CPL-Prodi:** CPL02, CPL06, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Dasar Dart dan Flutter
- Widget, layout, navigasi, plugin, dan kamera
- State management, asynchronous programming, stream, persistence, dan RESTful API
- Proyek aplikasi mobile berbasis Flutter

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0209-03901: Mampu menerapkan Dart, Flutter, widget, layout, navigation, dan plugin untuk aplikasi mobile | CPMK0209: Mahasiswa mampu memilih dan menerapkan teknologi pengembangan berbasis platform untuk membangun aplikasi | CPL02 | Tugas: 13% (Total: 13.00%) |
| SCPMK0603-03902: Mampu mengimplementasikan state management, asynchronous programming, stream, persistence, dan RESTful API | CPMK0603: Mahasiswa mampu mengimplementasikan dan melakukan deployment aplikasi web, mobile, atau framework | CPL06 | Tugas: 17% (Total: 17.00%) |
| SCPMK1006-03903: Mampu menganalisis kebutuhan UI/UX mobile dan mengevaluasi kualitas aplikasi berdasarkan fungsi, integrasi, dan UX | CPMK1006: Mahasiswa mampu mengevaluasi dan mengembangkan aplikasi web/mobile berdasarkan kebutuhan, kualitas, dan UX | CPL10 | UTS: 15% (Total: 15.00%) |
| SCPMK0603-03904: Mampu menghasilkan aplikasi mobile berbasis Flutter sebagai proyek PBL | CPMK0603 | CPL06 | PBL: 30%, UAS: 25% (Total: 55.00%) |

## RTI255004 — Pembelajaran Mesin (Semester 5)

**CPL-Prodi:** CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Supervised learning: regresi, decision tree, random forest, SVM, k-NN
- Model evaluation: cross-validation, confusion matrix, metrik, regularisasi
- Unsupervised learning: k-Means, DBSCAN, dan dimensionality reduction (PCA)
- Ensemble methods, deep learning dasar, dan interpretabilitas model
- End-to-end ML project: pipeline, optimasi, dan presentasi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0706-04001: Mampu mengimplementasikan algoritma ML supervised dan unsupervised untuk masalah klasifikasi, regresi, dan clustering | CPMK0706: Mahasiswa mampu mengembangkan sistem ML dan melakukan analisis data berbasis AI untuk keputusan bermakna | CPL07 | Tugas: 16%, Kuis 1: 5%, UTS: 10%, PBL: 12%, UAS: 10% (Total: 53%) |
| SCPMK1005-04002: Mampu mengevaluasi kinerja model ML menggunakan metrik yang tepat dan menerapkan teknik optimasi model | CPMK1005: Mahasiswa mampu mengevaluasi solusi sistem cerdas berdasarkan kinerja, keandalan, dan interpretabilitas model | CPL10 | Tugas: 12%, UTS: 5%, Kuis 2: 5%, PBL: 13%, UAS: 12% (Total: 47%) |

## RTI255005 — Business Intelligence (Semester 5)

**CPL-Prodi:** CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar BI, data warehouse, dan proses ETL
- Analisis OLAP dan operasi multidimensional
- Visualisasi data, tools BI, dan desain dashboard
- Data mining, predictive analytics, dan real-time BI
- Implementasi proyek dashboard BI dan evaluasi insight

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0705-04101: Mahasiswa mampu merancang dan mengimplementasikan data warehouse dengan skema bintang/snowflake dan proses ETL | CPMK0705: Mahasiswa mampu melakukan pengolahan data dan visualisasi untuk menghasilkan insight bermakna bagi keputusan bisnis | CPL07 | Tugas: 12%, Kuis 1: 5%, UTS: 7% (Total: 24%) |
| SCPMK0706-04102: Mahasiswa mampu membangun dashboard BI interaktif yang mengintegrasikan analisis OLAP dan visualisasi data | CPMK0706: Mahasiswa mampu mengembangkan sistem BI berbasis AI/ML untuk analisis data dan pendukung keputusan | CPL07 | Tugas: 10%, UTS: 6%, PBL: 10%, UAS: 12% (Total: 38%) |
| SCPMK1004-04103: Mahasiswa mampu mengevaluasi kualitas visualisasi data dan menyajikan insight bisnis akurat kepada pemangku kepentingan | CPMK1004: Mahasiswa mampu merancang dan menginterpretasikan visualisasi grafis data untuk analisis dan keputusan strategis | CPL10 | Tugas: 8%, Kuis 2: 5%, PBL: 12%, UAS: 13% (Total: 38%) |

## RTI255006 — Penjaminan Mutu Perangkat Lunak (Semester 5)

**CPL-Prodi:** CPL05, CPL06

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar SQA dan standar ISO
- Pendekatan, tipe, dan level pengujian
- Test planning, test scenario, test case, dan traceability
- Test monitoring, test control, test completion, dan test reporting
- Functional testing
- Non-functional testing
- Strategi QA komprehensif

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0608-04201: Mahasiswa mampu menganalisis prinsip SQA, standar mutu, tipe dan level pengujian, serta konteks pengujian dalam SDLC | CPMK0608: Mahasiswa mampu merancang strategi pengujian, verifikasi dan validasi, serta mengevaluasi jaminan mutu perangkat lunak | CPL06 | Tugas: 4%, Kuis: 7%, UTS: 5% (Total: 16%) |
| SCPMK0608-04202: Mahasiswa mampu merancang dokumen test plan, test scenario, test case, test monitoring, test control, dan test report | CPMK0608 | CPL06 | Tugas: 7%, Kuis: 3%, UTS: 10%, PBL: 5% (Total: 25%) |
| SCPMK0608-04203: Mahasiswa mampu menerapkan dan mengevaluasi functional testing menggunakan tools sesuai untuk memverifikasi kesesuaian perangkat lunak | CPMK0608 | CPL06 | Tugas: 15%, PBL: 10%, UAS: 5% (Total: 30%) |
| SCPMK0608-04204: Mahasiswa mampu merancang, menerapkan, dan mengevaluasi non-functional testing serta menyusun rekomendasi peningkatan kualitas perangkat lunak | CPMK0608 | CPL06 | Tugas: 3%, PBL: 7%, UAS: 10% (Total: 20%) |
| SCPMK0605-04206: Mahasiswa mampu mengembangkan dan memelihara kualitas kode perangkat lunak melalui unit dan integration testing serta code review | CPMK0605: Mampu mengembangkan dan memelihara kualitas kode perangkat lunak sesuai standar yang berlaku | CPL06 | Tugas: 3% (Total: 3%) |
| SCPMK0606-04207: Mahasiswa mampu menyusun proses deployment dan rencana pemeliharaan perangkat lunak berbasis SDLC sebagai strategi jaminan mutu komprehensif | CPMK0606: Mampu menyusun proses deployment dan rencana pemeliharaan perangkat lunak berbasis SDLC | CPL06 | PBL: 3% (Total: 3%) |
| SCPMK0508-04205: Mahasiswa mampu menerapkan prinsip information assurance dan software security dalam pengujian non-functional dan jaminan mutu | CPMK0508: Mampu menerapkan prinsip information assurance dan software security dalam pengembangan sistem | CPL05 | Tugas: 3% (Total: 3%) |

## RTI255007 — Pengolahan Citra dan Visi Komputer (Semester 5)

**CPL-Prodi:** CPL07, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengolahan citra digital: representasi, operasi pixel, histogram, dan color space
- Filtering spasial, deteksi tepi, dan segmentasi citra
- Transformasi morfologi dan evaluasi kualitas citra
- CNN: arsitektur, klasifikasi, deteksi objek, dan segmentasi gambar
- Transfer learning, augmentasi data, dan evaluasi model visi komputer

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0705-04301: Mahasiswa mampu mengimplementasikan teknik pengolahan citra (filtering, segmentasi, transformasi) menggunakan OpenCV | CPMK0705: Mahasiswa mampu melakukan pengolahan citra digital dan visualisasi untuk menghasilkan representasi bermakna | CPL07 | Tugas: 12%, Kuis 1: 5%, UTS: 8% (Total: 25%) |
| SCPMK0706-04302: Mahasiswa mampu membangun sistem visi komputer berbasis CNN untuk klasifikasi, deteksi objek, dan segmentasi | CPMK0706: Mahasiswa mampu mengembangkan sistem visi komputer berbasis deep learning untuk deteksi, segmentasi, dan pengenalan objek | CPL07 | Tugas: 8%, PBL: 13%, UAS: 11% (Total: 32%) |
| SCPMK1004-04303: Mahasiswa mampu mengevaluasi kualitas citra dan hasil pemrosesan visual menggunakan metrik kuantitatif | CPMK1004: Mahasiswa mampu mengevaluasi kualitas hasil pengolahan citra dan representasi visual untuk aplikasi nyata | CPL10 | Tugas: 8%, UTS: 7% (Total: 15%) |
| SCPMK1005-04304: Mahasiswa mampu mengevaluasi kinerja model visi komputer menggunakan metrik mAP, IoU, dan accuracy | CPMK1005: Mahasiswa mampu mengevaluasi kinerja sistem visi komputer berdasarkan metrik kualitas yang sesuai konteks | CPL10 | Kuis 2: 5%, PBL: 12%, UAS: 11% (Total: 28%) |

## RTI255008 — Administrasi dan Keamanan Jaringan (Semester 5)

**CPL-Prodi:** CPL05, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Pengenalan infrastruktur & keamanan jaringan, CIA Triad, dan penilaian risiko
- Identifikasi ancaman siber dan kerentanan sistem jaringan
- Desain topologi jaringan aman: segmentasi, VLAN, DMZ
- Simulasi desain keamanan jaringan
- Konsep dan pemilihan gateway internet
- Instalasi dan konfigurasi dasar gateway internet
- Konfigurasi NAT dan firewall pada gateway
- Administrasi sistem jaringan: AAA, RADIUS/TACACS+
- Manajemen pengguna, RBAC, dan kontrol akses
- Monitoring jaringan dan dasar logging/SIEM
- Simulasi administrasi dan troubleshooting jaringan
- Identifikasi bottleneck dan optimasi kinerja jaringan
- Benchmarking, QoS, dan traffic shaping
- Simulasi optimasi kinerja dan integrasi SIEM

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0501-04401: Mahasiswa mampu menganalisis dan merancang kebijakan keamanan infrastruktur jaringan termasuk desain topologi aman dan pemilihan gateway | CPMK0501: Mahasiswa mampu merancang dan menerapkan kebijakan serta prosedur keamanan infrastruktur jaringan dan cloud | CPL05 | Tugas: 6%, Kuis: 4%, UTS: 10% (Total: 20%) |
| SCPMK0502-04401: Mahasiswa mampu mengidentifikasi dan menganalisis ancaman, kerentanan, serta dampak keamanan pada sistem dan jaringan komputer | CPMK0502: Mahasiswa mampu menganalisis isu keamanan pada sistem operasi, jaringan, dan cloud untuk menentukan strategi mitigasi | CPL05 | Tugas: 4%, UTS: 10%, PBL: 13% (Total: 27%) |
| SCPMK0505-04401: Mahasiswa mampu mengkonfigurasi dan menguji mekanisme keamanan jaringan meliputi NAT, firewall, administrasi akses, dan monitoring SIEM | CPMK0505: Mahasiswa mampu mengkonfigurasi, mengelola, dan mengoptimalkan mekanisme keamanan jaringan sesuai standar dan best practice | CPL05 | Tugas: 6%, Kuis: 6%, PBL: 13% (Total: 25%) |
| SCPMK0505-04402: Mahasiswa mampu melakukan optimasi kinerja jaringan, troubleshooting, benchmarking, dan mengintegrasikan SIEM untuk perencanaan kapasitas | CPMK0505 | CPL05 | Tugas: 8%, UAS: 20% (Total: 28%) |
| SCPMK0504-04403: Mampu membangun infrastruktur jaringan aman melalui desain arsitektur, segmentasi, dan konfigurasi gateway | CPMK0504: Mampu membangun dan mengelola infrastruktur jaringan komputer dengan arsitektur, protokol, dan konfigurasi sesuai kebutuhan | CPL05 | terintegrasi dengan penilaian Minggu 3, 6 (tidak ada bobot terpisah) |
| SCPMK1002-04404: Mampu merancang dan mengevaluasi mekanisme perlindungan data serta sumber daya menggunakan monitoring dan logging | CPMK1002: Mampu merancang, menerapkan, dan mengevaluasi mekanisme keamanan jaringan untuk melindungi data, layanan, dan sumber daya jaringan | CPL10 | terintegrasi dengan penilaian Minggu 11 (tidak ada bobot terpisah) |
| SCPMK1003-04405: Mampu menganalisis permasalahan kompleks dan mengelola solusi optimasi jaringan yang aman dan scalable | CPMK1003: Mampu menganalisis permasalahan kompleks pada infrastruktur dan layanan jaringan untuk merancang solusi jaringan on-premise/cloud | CPL10 | terintegrasi dengan penilaian Minggu 14–15 (tidak ada bobot terpisah) |

## RTI256001 — Komunikasi dan Etika Profesi (Semester 6)

**CPL-Prodi:** CPL01, CPL03

**Bahan Kajian / Materi Pembelajaran:**
- Etika profesi TI, kode etik ACM/IEEE, hukum ITE, dan K3
- Komunikasi profesional: presentasi teknis dan penulisan laporan
- Dinamika tim, kolaborasi lintas fungsi, dan isu sosial teknologi
- Personal branding, portofolio digital, dan perencanaan karir
- Strategi pencarian kerja, CV, wawancara, dan etika penelitian

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0101-04501: Mahasiswa mampu menganalisis kasus pelanggaran etika profesi, hukum ITE, dan K3 untuk merekomendasikan tindakan tepat | CPMK0101: Mahasiswa mampu menerapkan etika profesi TI, kesadaran hukum, K3, dan nilai profesionalisme di lingkungan kerja digital | CPL01 | Tugas: 14%, Kuis 1: 5%, UTS: 7% (Total: 26%) |
| SCPMK0301-04502: Mahasiswa mampu menyajikan presentasi teknis, menulis laporan profesional, dan berkolaborasi dalam tim lintas fungsi | CPMK0301: Mahasiswa mampu berkomunikasi dan mempresentasikan gagasan teknis secara efektif dalam konteks kerja profesional | CPL03 | Tugas: 10%, UTS: 6%, PBL: 10% (Total: 26%) |
| SCPMK0303-04503: Mahasiswa mampu menyusun portofolio profesional dan rencana pengembangan karir berbasis kompetensi TI | CPMK0303: Mahasiswa mampu menyusun rencana pengembangan karir dan portofolio profesional di bidang TI | CPL03 | Tugas: 6%, Kuis 2: 5%, PBL: 12%, UAS: 25% (Total: 48%) |

## RTI256002 — Pengembangan Karir (Semester 6)

**CPL-Prodi:** CPL01, CPL03

**Bahan Kajian / Materi Pembelajaran:**
- Pengantar pengembangan karir: konsep, tahapan, dan faktor karir
- Pemetaan minat, bakat, dan potensi diri (self-assessment)
- Karir mandiri dan fleksibel di era digital (gig economy, freelance, startup)
- Profesi bidang informatika: klasifikasi, kompetensi, dan jalur karir
- Karir organisasi vs freelance: perbandingan dan strategi
- Karir era Industri 4.0: otomasi, AI, IoT, dan lifelong learning
- Personal branding: identitas digital, LinkedIn, dan reputasi profesional
- Public speaking profesional: komunikasi verbal/nonverbal dan presentasi karir
- Manajemen karir jangka panjang dan networking profesional
- Perencanaan karir: SMART goals, roadmap, dan strategi pencapaian
- Penilaian kinerja: KPI, feedback, dan pengaruh terhadap karir
- Internasionalisasi karir: peluang kerja global dan persyaratan internasional
- Budaya manajerial global dan kolaborasi lintas budaya
- Pembuatan CV profesional yang relevan dan ATS-friendly

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0102-04601: Mahasiswa mampu menerapkan nilai etika profesional dan sikap integritas dalam pengambilan keputusan karir sehari-hari | CPMK0102: Mahasiswa mampu menerapkan nilai ketakwaan, integritas, dan etika profesional sebagai dasar keputusan karir dan perilaku profesional | CPL01 | Tugas: 6%, UTS: 8% (Total: 14%) |
| SCPMK0303-04602: Mahasiswa mampu mengidentifikasi dan menganalisis minat, bakat, potensi diri, serta peluang karir sesuai kompetensi dan tren industri | CPMK0303: Mahasiswa mampu mengembangkan diri berkelanjutan, berkomunikasi profesional, dan mengelola karir sistematis untuk tujuan karir jangka panjang | CPL03 | Tugas: 8%, UTS: 9%, UAS: 4% (Total: 21%) |
| SCPMK0303-04603: Mahasiswa mampu merancang strategi personal branding dan komunikasi profesional efektif untuk pengembangan karir di era digital | CPMK0303 | CPL03 | Tugas: 6%, UTS: 8%, UAS: 3% (Total: 17%) |
| SCPMK0303-04604: Mahasiswa mampu menyusun Career Development Plan (CDP) sistematis mencakup tujuan SMART, gap kompetensi, dan timeline | CPMK0303 | CPL03 | Tugas: 8%, PBL: 40% (Total: 48%) |

## RTI256003 — Pemrograman Berbasis Framework (Semester 6)

**CPL-Prodi:** CPL02, CPL06

**Bahan Kajian / Materi Pembelajaran:**
- Setup, routing, styling, custom document
- API routes, CSR, SSR, SSG, ISR, middleware, route protection
- Authentication, multi-role, optimasi, unit testing, dan proyek PBL

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0209-04701: Mahasiswa mampu menerapkan setup, routing, styling, custom document, API routes, CSR, SSR, SSG, ISR, middleware, route protection | CPMK0209: Mahasiswa mampu memilih dan menerapkan teknologi pengembangan berbasis platform untuk membangun aplikasi sesuai kebutuhan | CPL02 | Tugas: 10%, UTS: 10% (Total: 20.00%) |
| SCPMK0603-04702: Mahasiswa mampu mengimplementasikan authentication, multi-role system, optimasi, dan unit testing pada aplikasi framework modern | CPMK0603: Mahasiswa mampu mengimplementasikan dan melakukan deployment aplikasi web, mobile, atau framework sesuai kebutuhan pengguna | CPL06 | Tugas: 10% (Total: 10.00%) |
| SCPMK0603-04703: Mahasiswa mampu menghasilkan aplikasi berbasis framework melalui PBL berdasarkan kebutuhan stakeholder | CPMK0603 | CPL06 | PBL: 70% (Total: 70.00%) |

## RTI256104 — Proyek Teknologi Terintegrasi (Semester 6)

**CPL-Prodi:** CPL02, CPL03, CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Manajemen proyek TI: perencanaan, WBS, jadwal, anggaran, dan risiko
- Rekayasa perangkat lunak agile: Scrum, sprint planning, backlog, dan velocity
- Pengembangan aplikasi multi-platform: integrasi front-end, back-end, dan basis data
- Monitoring proyek, kontrol kualitas, deployment, dan defense produk akhir

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0801-04801: Mahasiswa mampu menyusun dokumen perencanaan proyek TI terintegrasi mencakup WBS, jadwal, anggaran, dan risk register | CPMK0801: Mahasiswa mampu merencanakan proyek TI terintegrasi dengan estimasi biaya, jadwal, alokasi sumber daya, dan manajemen risiko | CPL08 | Dok.Perencanaan: 15% (Total: 15%) |
| SCPMK0802-04802: Mahasiswa mampu mengimplementasikan aplikasi multi-platform menggunakan metodologi agile dengan sprint yang terdokumentasi | CPMK0802: Mahasiswa mampu mengimplementasikan siklus hidup rekayasa perangkat lunak menyeluruh dalam proyek nyata multi-platform | CPL08 | Sprint 1-2: 7%, Sprint 3-4: 10% (Total: 17%) |
| SCPMK0803-04803: Mahasiswa mampu melaksanakan monitoring sprint, mengelola backlog, dan menyajikan laporan kemajuan proyek | CPMK0803: Mahasiswa mampu mengeksekusi, memonitor, dan mengendalikan proyek serta mengelola dinamika tim secara profesional | CPL08 | UTS Milestone: 15%, UAS Defense: 10% (Total: 25%) |
| SCPMK0804-04804: Mahasiswa mampu mendemonstrasikan produk akhir proyek TI terintegrasi dengan defense teknis komprehensif | CPMK0804: Mahasiswa mampu mendemonstrasikan pengelolaan proyek TI utuh dari perencanaan hingga deliverable akhir | CPL08 | Laporan: 9%, UAS Defense: 8% (Total: 17%) |
| SCPMK0607-04805: Mahasiswa mampu mengintegrasikan solusi front-end, back-end, dan basis data dalam satu produk yang deployable | CPMK0607: Mahasiswa mampu menghasilkan solusi sistem informasi terintegrasi yang menjawab kebutuhan nyata pengguna | CPL06 | Sprint 1-2: 10%, Sprint 3-4: 10% (Total: 20%) |
| SCPMK0205-04806: Mahasiswa mampu merancang blueprint arsitektural dan komponen solusi modular, maintainable, dan scalable untuk aplikasi multi-platform | CPMK0205: Mampu menerapkan prinsip dan pola desain perangkat lunak untuk blueprint arsitektural dan komponen solusi aplikasi multi-platform | CPL02 | Sprint 1-2: 3% (Total: 3%) |
| SCPMK0302-04807: Mahasiswa mampu mengelola dinamika tim proyek dan menyampaikan hasil kerja tim kepada pemangku kepentingan profesional | CPMK0302: Mampu mengelola tim dan proyek terencana, dari perencanaan, koordinasi, komunikasi, hingga penyampaian hasil kepada stakeholder | CPL03 | Laporan: 1%, UAS Defense: 2% (Total: 3%) |

## RTI256105 — Internet of Things (Semester 6)

**CPL-Prodi:** CPL02, CPL05, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Arsitektur IoT: konsep, komponen, sensor, aktuator, gateway, dan layer edge-fog-cloud
- Mikrokontroler dan SBC: Arduino, Raspberry Pi, dan antarmuka sensor
- Protokol komunikasi IoT: MQTT, HTTP, CoAP, WebSocket, dan pemrosesan data sensor
- Platform IoT: Node-RED, AWS IoT, keamanan, integrasi cloud, dan visualisasi data real-time

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0204-04901: Mahasiswa mampu merancang arsitektur sistem IoT end-to-end meliputi sensor, gateway, dan cloud platform | CPMK0204: Mahasiswa mampu menganalisis kebutuhan komputasi dan merancang arsitektur solusi IoT terdistribusi | CPL02 | Tugas: 14%, Kuis 1: 5%, UTS: 8% (Total: 27%) |
| SCPMK0503-04902: Mahasiswa mampu mengimplementasikan protokol komunikasi IoT (MQTT, HTTP, CoAP) dan pemrosesan data sensor terdistribusi | CPMK0503: Mahasiswa mampu mengimplementasikan solusi komputasi paralel-terdistribusi untuk sistem IoT | CPL05 | Tugas: 14%, UTS: 7%, Kuis 2: 5%, PBL: 12% (Total: 38%) |
| SCPMK0904-04903: Mahasiswa mampu mengkonfigurasi platform IoT (Node-RED, AWS IoT, atau setara) dan mengintegrasikan layanan cloud untuk monitoring | CPMK0904: Mahasiswa mampu menguraikan prinsip kerja sistem paralel-terdistribusi untuk pemrosesan data skala besar | CPL09 | PBL: 13%, UAS: 22% (Total: 35%) |

## RTI256106 — Big Data (Semester 6)

**CPL-Prodi:** CPL05, CPL07, CPL09

**Bahan Kajian / Materi Pembelajaran:**
- Konsep Big Data: 4V (Volume, Velocity, Variety, Veracity), arsitektur Lambda, Kappa, dan HDFS
- Pemrosesan terdistribusi: MapReduce, Hadoop ekosistem (YARN, Hive, Pig), dan Apache Spark (RDD, DataFrame, SQL)
- Stream processing: Spark Streaming, Apache Kafka, dan pemrosesan event real-time
- Data lakehouse: Delta Lake, Apache Iceberg, NoSQL (Cassandra, MongoDB), dan visualisasi Big Data

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0702-05001: Mahasiswa mampu merancang dan mengimplementasikan pipeline pemrosesan Big Data menggunakan ekosistem Hadoop/Spark | CPMK0702: Mahasiswa mampu memproses data skala besar menggunakan arsitektur paralel dan terdistribusi | CPL07 | Tugas: 18%, UTS: 7%, Kuis 2: 5%, PBL: 17%, UAS: 15% (Total: 62%) |
| SCPMK0904-05002: Mahasiswa mampu menjelaskan arsitektur dan prinsip kerja sistem terdistribusi untuk batch processing dan stream processing | CPMK0904: Mahasiswa mampu menjelaskan prinsip kerja sistem paralel-terdistribusi pada pemrosesan data skala besar | CPL09 | Tugas: 12%, Kuis 1: 5%, UTS: 8%, UAS: 8% (Total: 33%) |
| SCPMK0503-05003: Mahasiswa mampu merancang dan menerapkan solusi komputasi paralel dan terdistribusi untuk kebutuhan Big Data dan cloud computing | CPMK0503: Mampu merancang dan menerapkan solusi komputasi paralel dan terdistribusi untuk kebutuhan IoT, Big Data, dan cloud | CPL05 | PBL: 5% (Total: 5%) |

## RTI256107 — Cloud Computing (Semester 6)

**CPL-Prodi:** CPL05, CPL09, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Virtualisasi, containerisasi, dan model layanan cloud (IaaS/PaaS/SaaS)
- Docker dan Kubernetes: containerisasi dan orkestrasi
- Arsitektur cloud: microservices, VPC, keamanan, dan jaringan
- Optimasi biaya, governance, dan strategi multi-cloud/hybrid

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0509-05101: Mahasiswa mampu merancang arsitektur cloud yang scalable menggunakan IaaS, PaaS, dan SaaS pada platform cloud utama | CPMK0509: Mahasiswa mampu merancang dan mengimplementasikan layanan komputasi virtual yang efisien, scalable, dan berkelanjutan | CPL05 | Tugas: 14%, UTS: 6%, PBL: 11%, UAS: 12% (Total: 43%) |
| SCPMK0905-05102: Mahasiswa mampu menjelaskan model virtualisasi, containerisasi (Docker, Kubernetes), dan arsitektur microservices | CPMK0905: Mahasiswa mampu menjelaskan konsep virtualisasi dan prinsip cloud computing serta model layanan cloud | CPL09 | Tugas: 10%, Kuis 1: 5%, UTS: 7% (Total: 22%) |
| SCPMK1003-05103: Mahasiswa mampu mengevaluasi dan memilih solusi cloud berdasarkan keandalan, keamanan, skalabilitas, dan biaya | CPMK1003: Mahasiswa mampu menganalisis dan merancang solusi jaringan on-premise/cloud yang andal, aman, dan scalable | CPL10 | Tugas: 6%, Kuis 2: 5%, PBL: 11%, UAS: 13% (Total: 35%) |

## RTI256108 — Komputasi Hijau (Semester 6)

**CPL-Prodi:** CPL01, CPL05

**Bahan Kajian / Materi Pembelajaran:**
- Konsep komputasi hijau, carbon footprint, dan regulasi keberlanjutan TI
- Efisiensi energi perangkat keras, PUE, dan data center hijau
- Virtualisasi, green software, cloud computing, dan renewable energy
- E-waste, green IT governance, dan studi kasus sustainabilitas

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0101-05201: Mahasiswa mampu menganalisis dampak lingkungan dari infrastruktur TI dan merekomendasikan strategi komputasi hijau berbasis etika profesi | CPMK0101: Mahasiswa mampu menerapkan etika profesi TI dan tanggung jawab sosial termasuk aspek keberlanjutan lingkungan | CPL01 | Tugas: 15%, Kuis 1: 5%, UTS: 8%, PBL: 8% (Total: 36%) |
| SCPMK0509-05202: Mahasiswa mampu merancang dan mengevaluasi solusi infrastruktur TI hemat energi menggunakan virtualisasi, optimasi server, dan renewable energy | CPMK0509: Mahasiswa mampu merancang dan mengimplementasikan layanan komputasi virtual yang efisien dan berkelanjutan dari perspektif lingkungan | CPL05 | Tugas: 15%, UTS: 7%, Kuis 2: 5%, PBL: 14%, UAS: 23% (Total: 64%) |

## RTI256204 — Proyek Inovasi (Semester 6)

**CPL-Prodi:** CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Problem framing, opportunity analysis, dan technology landscape
- Proposal inovasi: WBS, jadwal, anggaran, dan manajemen risiko
- Metodologi agile/scrum: sprint planning, review, dan retrospective
- Implementasi MVP, UAT, deployment, dan dokumentasi proyek

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0801-05301: Mahasiswa mampu menyusun proposal proyek inovasi TI dengan analisis masalah, solusi teknologi, WBS, dan rencana risiko | CPMK0801: Mahasiswa mampu merencanakan proyek inovasi TI berbasis konteks industri nyata | CPL08 | Proposal: 15% (Total: 15%) |
| SCPMK0803-05302: Mahasiswa mampu mengeksekusi proyek inovasi berbasis sprint, melaporkan kemajuan, dan mengelola perubahan tim | CPMK0803: Mahasiswa mampu mengeksekusi, memonitor, dan mengendalikan proyek inovasi serta memimpin tim | CPL08 | Sprint 1-2: 10%, UTS Milestone: 15% (Total: 25%) |
| SCPMK0804-05303: Mahasiswa mampu mempresentasikan hasil proyek inovasi dengan defense teknis dan bisnis yang komprehensif | CPMK0804: Mahasiswa mampu mendemonstrasikan penyelesaian proyek inovasi TI secara utuh | CPL06 | Sprint 3-4: 10%, Laporan: 10%, UAS Defense: 10% (Total: 30%) |
| SCPMK0607-05304: Mahasiswa mampu mengintegrasikan teknologi mutakhir menjadi solusi inovatif yang scalable dan deployable | CPMK0607: Mahasiswa mampu menghasilkan solusi sistem informasi inovatif yang menjawab permasalahan nyata industri | CPL06 | Sprint 1-2: 10%, Sprint 3-4: 10%, UAS Defense: 10% (Total: 30%) |

## RTI256205 — Workshop Teknologi Terapan (Semester 6)

**CPL-Prodi:** CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Rekayasa perangkat lunak dalam konteks industri: sprint planning dan backlog management
- Pengembangan produk iteratif: implementasi fitur, integrasi, dan validasi
- Quality assurance: unit testing, integration testing, dan UAT
- Manajemen proyek workshop: stakeholder communication, demo, dan retrospective

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0603-05401: Mahasiswa mampu merancang dan mengeksekusi rencana pengujian komprehensif termasuk unit testing, integration testing, dan UAT | CPMK0603: Mahasiswa mampu menerapkan teknik pengujian perangkat lunak dan quality assurance dalam konteks industri nyata | CPL06 | Sprint 1-2: 8%, Sprint 3-4: 10%, Laporan QA: 10% (Total: 28%) |
| SCPMK0802-05402: Mahasiswa mampu mengembangkan produk teknologi terapan melalui iterasi sprint berbasis kebutuhan industri nyata | CPMK0802: Mahasiswa mampu mengimplementasikan siklus hidup rekayasa perangkat lunak secara menyeluruh dalam workshop industri | CPL06 | Rencana: 7%, Sprint 1-2: 12%, Sprint 3-4: 10%, UAS Demo: 10% (Total: 39%) |
| SCPMK0803-05403: Mahasiswa mampu memimpin tim dalam workshop, mengelola backlog, dan melaporkan kemajuan kepada stakeholder industri | CPMK0803: Mahasiswa mampu mengeksekusi dan mengelola proyek workshop teknologi secara profesional dalam tim lintas fungsi | CPL08 | Rencana: 8%, UTS: 15%, UAS Demo: 10% (Total: 33%) |

## RTI256206 — Rekayasa Sistem (Semester 6)

**CPL-Prodi:** CPL02, CPL06

**Bahan Kajian / Materi Pembelajaran:**
- Requirement elicitation: teknik wawancara, use case, user story, dan spesifikasi kebutuhan
- Arsitektur sistem enterprise: pola arsitektur, komponen, antarmuka, dan dokumentasi ADR
- Pipeline CI/CD: automated testing, integrasi, dan strategi deployment (blue-green, canary)
- Monitoring, observability, dan pemeliharaan sistem produksi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0211-05501: Mahasiswa mampu merancang arsitektur sistem enterprise meliputi komponen, antarmuka, aliran data, dan ketergantungan antar modul | CPMK0211: Mahasiswa mampu merancang arsitektur sistem skala enterprise yang memenuhi kebutuhan fungsional dan non-fungsional | CPL02 | Dok Arsitektur: 8%, Sprint 1-2: 10%, Sprint 3-4: 8%, UAS Defense: 8% (Total: 34%) |
| SCPMK0602-05502: Mahasiswa mampu melakukan elicitation, analisis, spesifikasi, dan validasi kebutuhan sistem yang kompleks | CPMK0602: Mahasiswa mampu melakukan rekayasa kebutuhan (requirement engineering) yang komprehensif untuk sistem kompleks | CPL06 | Dok Arsitektur: 7%, UTS: 15%, Laporan SRS: 10% (Total: 32%) |
| SCPMK0609-05503: Mahasiswa mampu merancang dan mengimplementasikan pipeline CI/CD serta strategi deployment blue-green/canary untuk sistem produksi | CPMK0609: Mahasiswa mampu merancang dan mengimplementasikan strategi deployment dan operasi sistem yang handal | CPL06 | Sprint 1-2: 10%, Sprint 3-4: 12%, UAS Defense: 12% (Total: 34%) |

## RTI256207 — Teknologi Terapan (Semester 6)

**CPL-Prodi:** CPL02, CPL05, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Needs assessment, technology mapping, dan feasibility study untuk solusi teknologi industri
- Perencanaan implementasi teknologi: roadmap, manajemen risiko, dan stakeholder management
- Implementasi solusi iteratif: prototipe, pengembangan, integrasi, dan optimasi
- Deployment produksi, transfer knowledge, dan evaluasi dampak teknologi

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0204-05601: Mahasiswa mampu melakukan analisis kebutuhan teknologi industri dan merancang solusi teknologi terapan yang tepat guna | CPMK0204: Mahasiswa mampu menganalisis kebutuhan dan merancang arsitektur solusi teknologi terapan berbasis kebutuhan nyata | CPL02 | Analisis: 8%, Sprint 1-2: 8%, Sprint 3-4: 8%, Laporan: 5% (Total: 29%) |
| SCPMK0503-05602: Mahasiswa mampu mengimplementasikan solusi teknologi terapan mulai dari prototipe hingga deployment produksi | CPMK0503: Mahasiswa mampu mengimplementasikan solusi teknologi terapan yang efisien dan memenuhi kebutuhan operasional | CPL05 | Sprint 1-2: 12%, Sprint 3-4: 12%, Laporan: 5%, UAS Presentasi: 10% (Total: 39%) |
| SCPMK0801-05603: Mahasiswa mampu menyusun rencana implementasi teknologi, mengelola risiko, dan melaporkan kemajuan kepada stakeholder | CPMK0801: Mahasiswa mampu merencanakan dan mengelola implementasi teknologi terapan di lingkungan industri | CPL08 | Analisis: 7%, UTS: 15%, UAS Presentasi: 10% (Total: 32%) |

## RTI257001 — Magang (Semester 7)

**CPL-Prodi:** CPL03, CPL06, CPL08

**Bahan Kajian / Materi Pembelajaran:**
- Pembekalan magang, etika profesi, dan orientasi industri
- Praktik kerja industri dan logbook kegiatan
- Aplikasi kompetensi rekayasa perangkat lunak di industri
- Penulisan laporan magang dan komunikasi profesional
- Presentasi dan sidang magang

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0301-05701: Mahasiswa mampu berkomunikasi profesional secara lisan dan tulisan selama kegiatan magang di industri TI | CPMK0301: Mahasiswa mampu berkomunikasi secara profesional lisan dan tulisan dalam lingkungan kerja industri TI | CPL03 | Logbook: 10%, Laporan: 8% (Total: 18%) |
| SCPMK0303-05702: Mahasiswa mampu menyusun dan mempresentasikan laporan magang yang komprehensif kepada pembimbing akademik dan penguji | CPMK0303: Mahasiswa mampu mempresentasikan hasil kerja dan laporan magang secara efektif kepada pembimbing dan penguji | CPL03 | Laporan: 12%, Sidang: 15% (Total: 27%) |
| SCPMK0804-05703: Mahasiswa mampu menyelesaikan target pekerjaan industri yang diberikan pembimbing lapangan secara mandiri dan tepat waktu | CPMK0804: Mahasiswa mampu menyelesaikan proyek atau tugas industri secara mandiri dan profesional selama magang | CPL08 | Logbook: 10%, Nilai Lapangan: 15% (Total: 25%) |
| SCPMK0607-05704: Mahasiswa mampu mengaplikasikan minimal satu kompetensi rekayasa perangkat lunak dalam proyek atau tugas industri nyata | CPMK0607: Mahasiswa mampu mengaplikasikan kompetensi rekayasa perangkat lunak dalam konteks industri nyata | CPL06 | Nilai Lapangan: 15%, Sidang: 15% (Total: 30%) |

## RTI258001 — Skripsi (Semester 8)

**CPL-Prodi:** CPL01, CPL03, CPL04, CPL08, CPL10

**Bahan Kajian / Materi Pembelajaran:**
- Reviu proposal yang telah disetujui dan penyusunan kontrak bimbingan
- Analisis dan perancangan sistem (BAB IV)
- Implementasi sistem sesuai rancangan (BAB V)
- Pengujian dan pembahasan hasil (BAB VI)
- Penyusunan kesimpulan dan saran (BAB VII)
- Penulisan naskah skripsi lengkap sesuai standar ilmiah
- Seminar kemajuan, sidang, dan diseminasi hasil

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0802-05803: Mahasiswa mampu menyusun proposal penelitian, membuat jadwal, dan mengelola progress skripsi secara mandiri | CPMK0802: Mahasiswa mampu merencanakan dan mengelola jalannya penelitian/pengembangan skripsi secara profesional | CPL08 | Reviu Proposal: 3% (Total: 3%) |
| SCPMK0101-05806: Mahasiswa mampu menunjukkan profesionalisme dan disiplin akademik melalui kepatuhan pada etika penelitian dan kontrak bimbingan skripsi | CPMK0101: Mampu menunjukkan profesionalisme melalui penerapan etika profesi TI dan disiplin dalam penelitian | CPL01 | Reviu Proposal: 2% (Total: 2%) |
| SCPMK0403-05801: Mahasiswa mampu melaksanakan penelitian atau pengembangan sistem TIK secara sistematis sesuai metodologi yang dipilih | CPMK0403: Mahasiswa mampu melaksanakan penelitian/pengembangan TIK secara sistematis dan mandiri berdasarkan metodologi ilmiah | CPL04 | Seminar Kemajuan (Pembimbing): 5%, Naskah Skripsi: 7% (Total: 12%) |
| SCPMK1009-05805: Mahasiswa mampu menganalisis permasalahan TIK secara sistematis dan menghasilkan solusi yang tervalidasi secara ilmiah | CPMK1009: Mahasiswa mampu menganalisis permasalahan TIK secara komprehensif dan menghasilkan solusi yang tervalidasi | CPL10 | Seminar Kemajuan (Pembimbing): 7%, Naskah Skripsi: 8%, Sidang Skripsi (Penguji): 10% (Total: 25%) |
| SCPMK0301-05807: Mahasiswa mampu mengelola diri secara profesional dan mempresentasikan kemajuan penelitian secara lisan dan tertulis secara efektif | CPMK0301: Mampu mengelola diri secara profesional, berkomunikasi lisan/tertulis, dan presentasi efektif dalam konteks kerja | CPL03 | Seminar Kemajuan (Pembimbing): 3% (Total: 3%) |
| SCPMK0404-05802: Mahasiswa mampu menyusun naskah skripsi yang memenuhi standar penulisan ilmiah Polinema | CPMK0404: Mahasiswa mampu menyusun laporan/artikel ilmiah skripsi yang memenuhi standar publikasi | CPL04 | Naskah Skripsi: 15%, Sidang Skripsi (Penguji): 10% (Total: 25%) |
| SCPMK0804-05804: Mahasiswa mampu mempresentasikan dan mempertahankan skripsi di hadapan tim penguji | CPMK0804: Mahasiswa mampu mempertahankan hasil penelitian/pengembangan di hadapan tim penguji | CPL08 | Sidang Skripsi (Penguji): 27% (Total: 27%) |
| SCPMK1008-05808: Mahasiswa mampu mengintegrasikan hasil analisis dan desain sistem ke dalam pengembangan BAB IV–VI secara koheren dan mempertahankannya di sidang | CPMK1008: Mahasiswa mampu mengintegrasikan hasil analisis dan desain sistem ke dalam proses pengembangan perangkat lunak secara koheren | CPL10 | Sidang Skripsi (Penguji): 3% (Total: 3%) |

## RTI258002 — Bahasa Inggris Persiapan Kerja (Semester 8)

**CPL-Prodi:** CPL01, CPL03

**Bahan Kajian / Materi Pembelajaran:**
- Professional CV, LinkedIn profile, cover letter, dan email profesional
- Technical writing dan dokumentasi proyek TI
- Presentasi teknis dan komunikasi tim multikultural
- Job interview: STAR method, behavioral dan technical interview
- Business English, IT portfolio, dan mock interview

| Sub-CPMK | CPMK Induk | CPL | Bentuk Penilaian & Bobot |
|---|---|---|---|
| SCPMK0303-05901: Mahasiswa mampu menyusun dokumen profesional dalam Bahasa Inggris meliputi CV, cover letter, portofolio, dan email profesional | CPMK0303: Mahasiswa mampu mengomunikasikan dan mempresentasikan hasil kerja TI secara efektif dalam Bahasa Inggris | CPL03 | Tugas Dokumen: 18%, Kuis 1: 5%, UTS: 8%, PBL Mock: 10%, UAS: 10% (Total: 51%) |
| SCPMK0102-05902: Mahasiswa mampu melakukan simulasi wawancara kerja, presentasi teknis, dan komunikasi dalam tim multikultural secara efektif dalam Bahasa Inggris | CPMK0102: Mahasiswa mampu menerapkan etika profesi, profesionalisme, dan komunikasi lintas budaya dalam lingkungan kerja TI global | CPL01 | Tugas Dokumen: 12%, UTS: 7%, Kuis 2: 5%, PBL Mock: 12%, UAS: 13% (Total: 49%) |
