# Mapping CPMK: Kurikulum 2020 (Lama) → Kurikulum 2025 (Baru)

Sumber: Google Sheet `1BZcVR1zdJXAFmSrEKKNzog7tb5KtJdLVunXvoz3Ty_8`, tab
"MK-CPMK-SubCPMK-Metode" (gid `753390927`), diekspor 2026-07-06.

## Metodologi

Pemetaan ini berada pada level **Sub-CPMK**, dikunci pada Sub-CPMK **baru**
(kurikulum 2025). Sheet acuan menyertakan dua kolom referensi kurikulum lama
yang diisi langsung oleh penyusun kurikulum: `SubCPMK Lama` dan
`Materi Pembelajaran Lama`. Sisi lama masih memakai penomoran asli RPS 2020
masing-masing mata kuliah (mis. `2.2.1.1`, `7.1.1.1`, `Sub CPMK - 03.1.1`,
`Sub-CPMK 6.2.1.1`) — tidak dinormalisasi ke format `CPMKxxx` di sini, sesuai
apa adanya di sumber.

Dari 113 baris Sub-CPMK aktif pada sheet (32 dari 55 mata kuliah kurikulum
2025 sudah memiliki baris Sub-CPMK), **26 baris pada 25 mata kuliah**
memiliki data kurikulum lama. Tabel di bawah hanya memuat baris-baris
tersebut — murni ekstraksi dari sheet, tidak ada tautan lama↔baru yang
ditambahkan/diinferensikan.

`RTI25` diresolusi dari `Kode MK` (`MKxxx`) via `MK#` pada
[`rti-mk-crosswalk.md`](rti-mk-crosswalk.md). `Kode Lama` adalah identifier
dotted terdepan yang diparsing dari `SubCPMK Lama` (mis. `2.2.1.1`); "—"
bila kolom tersebut hanya berisi teks deskriptif tanpa penomoran, atau
kosong.

## Tabel Mapping

<!-- markdownlint-disable MD013 -->

| RTI25 | MK | Nama MK | CPMK Baru | Sub-CPMK Baru | Kode Lama | Sub-CPMK Lama (2020) | Materi Lama |
|---|---|---|---|---|---|---|---|
| RTI251001 | MK001 | Pancasila | CPMK102 | Mahasiswa mampu menganalisis nilai-nilai Pancasila, sejarah perjuangan bangsa, dan sistem ketatanegaraan Indonesia untuk menerapkannya sebagai dasar sikap dan tindakan sebagai warga negara yang bertakwa dan berintegritas… | — | Mahasiswa mampu menerapkan prinsip etika, nilai-nilai Pancasila, serta aspek keselamatan dan kesehatan kerja dalam pengembangan dan pemeliharaan sistem informasi. | 1. Pendidikan pancasila dalam tinjauan historis, cultural, yuridis dan filosofis 2. Pancasila dalam konteks sejarah perjuangan bangsa Indonesia 3. Pancasila sebagai sistem filsafat 4. UUD RI 1945 5. Amandemen UUD RI 1945 6. Trias Politika dalam Negara RI 7. Ke… |
| RTI251002 | MK002 | Konsep TI | CPMK208 | Mahasiswa mampu menganalisis kebutuhan komputasi suatu solusi teknologi informasi dengan mempertimbangkan konsep sistem komputer, interaksi hardware, sistem operasi, dan aplikasi, serta jaringan komputer dan internet unt… | — | Mahasiswa mampu menggunakan konsep teknologi informasi untuk menyelesaikan masalah | Konsep Teknologi 1. Inovasi Teknologi 2. Perkembangan Iptek 3. Etika Rekayasa 4. Perkembangan ICT 5. Sistem Komputer 6. Konsep Sistem Komputer 7. Representasi Data 8. Aljabar Boolean 9. Flowchart 10. Jaringan Komputer dan Internet 11. Aplikasi TI di Berbagai B… |
| RTI251003 | MK003 | Critical Thinking | CPMK401 | Mahasiswa mampu menganalisis argumen dan permasalahan secara kritis melalui identifikasi fakta, klaim, bias, kesalahan penalaran, serta penerapan berbagai bentuk penalaran logis dan statistik. | 2.2.1.1 | 2.2.1.1 SUBCPMK1 Mahasiswa mampu mengidentifikasi, menganalisis, dan mengevaluasi argumen dalam berbagai konteks diskusi atau materi tertulis, dengan membedakan antara fakta dan opini serta mengenali bias dan kesalahan logika yang umum. 2.2.1.2 SUBCPMK2 Mahasi… | 1. Berpikir dan Menalar 2. Pondasi Berpikir Kritis 3. Kemampuan Dasar Pemecahan Masalah 4. Applied Critical Thinking 5. Kemampuan Pemecahan Masalah Tingkat Lanjut 6. Teknik-teknik Lanjutan untuk Pemecahan Masalah 7. Penalaran Kritis |
| RTI251004 | MK004 | Matematika Dasar | CPMK902 | - Mampu menjelaskan dan memodelkan konsep dasar matematika diskrit (logika, himpunan, graf) untuk representasi data. | — | — | Proposisi dan Logika, Teori Bilangan, Teori Himpunan, Relasi dan Fungsi, Induksi dan Rekursi, Aljabar Boolean, Teori Graf dan Pohon. |
| RTI251005 | MK005 | Bahasa Inggris 1 | CPMK303 | Mampu menyampaikan opini, argumentasi, pertanyaan, dan jawaban menggunakan bahasa Inggris dalam kegiatan diskusi atau presentasi akademik. | 3.2.1.1 | 3.2.1.1 SUBCPMK1 Mahasiswa mampu menerapkan pengetahuan tentang teknik berkomunikasi lisan dan tulisan menggunakan bahasa Inggris dalam konteks Teknik Informatika. 3.2.1.2 SUBCPMK2 Mahasiswa mampu berkomunikasi dengan menggunakan bahasa Inggris secara lisan da… | 1. Topic 1: Computer Applications 1.1. Kinds of Computer Applications and Their Uses 1.2. Grammatical Functions: Present Simple, Imperatives, and Sequencers 1.3. Software Installation Process 2. Topic 2: Computer Architecture 2.1. Types of Computers 2.2. Compu… |
| RTI251006 | MK006 | Dasar Pemrograman | CPMK903 | - Mahasiswa mampu menjelaskan konsep algoritma, variabel, konstanta, tipe data, serta mengevaluasi ekspresi logika/aritmatika dalam memecahkan masalah sederhana. | — | SUB-CPMK 1 Mahasiswa mengenal konsep dasar algoritma serta mampu menganalisis permasalahan sederhana ke dalam bentuk algoritma [C2, A3] SUB-CPMK 2 Mahasiswa memahami tentang pentingnya version dan cara version control bekerja. Mahasiswa memahami prinsip-prinsi… | Konsep Algoritma, Bahasa Pemrograman, Tipe Data, Variabel, Konstanta, Nilai, Ekspresi, Input-Output, Sequence, Analisa Kasus, Pemilihan, Perulangan, Array, Fungsi |
| RTI251008 | MK008 | K3 | CPMK101 | Mahasiswa mampu mengimplementasikan teori, konsep, dan prinsip ilmu keselamatan dan kesehatan kerja dalam rangka menerapkan derajat kesehatan pada para pekerja. | — | — | Keselamatan kerja. Mahasiswa mengerti lingkup kesehatan; lingkungan kerja; keselamatan kerja; asuransi kerja dan organisasi kerja yang menjadi bagian dari sebuah sistem tenaga kerja. 1. Konsep K3; Sejarah kesehatan dan keselamatan kerja, Pengertian K3, Tujaun … |
| RTI251009 | MK009 | Fisika | CPMK902 | Mahasiswa mampu menerapkan konsep diskrit, logika, himpunan, dan fungsi matematika dasar dalam sistem informasi. Mahasiswa mampu mengidentifikasi, menganalisis fakta dan opini, serta menyusun solusi sistematis terhadap m… | 2.1.1.1 | 2.1.1.1 SUBCPMK1 Mahasiswa mampu menerapkan konsep diskrit, logika, himpunan, dan fungsi matematika dasar dalam sistem informasi. 2.2.1.1 SUBCPMK1 Mahasiswa mampu mengidentifikasi, menganalisis fakta dan opini, serta menyusun solusi sistematis terhadap masalah… | 1. Hakikat dan Ruang Lingkup Fisika 2. Pengantar Ilmu Sains & Metode Ilmiah 3. Pengukuran dan Satuan 4. Kinematika Gerak Lurus dan 2 Dimensi 5. Dinamika Partikel 6. Usaha dan Energi 7. Impuls dan momentum 8. Medan listrik dan gaya Coulomb 9. Potensial listrik … |
| RTI252001 | MK010 | Agama | CPMK102 | Mahasiswa mampu menganalisis hakikat penciptaan manusia melalui pemahaman konsep agama dan Tauhid untuk membentuk karakter yang jujur, disiplin, dan bertakwa dalam interaksi akademik maupun sosial | — | — | 1. PENDAHULUAN: • Visi Pendidikan Agama • Deskripsi Mata Kuliah • Pendekatan Kuliah • Tata Tertib Perkuliahan • Sistem Penilaian 2. MANUSIA DAN AGAMA •Konsep Agama dan Islam •Agama Kebutuhan Manusia •Dimensi Ajaran Islam •Metode Memahami Islam •Misi Agama Isla… |
| RTI252002 | MK011 | Aljabar Linier | CPMK902 | Mahasiswa mampu menyelesaikan sistem persamaan linier menggunakan metode eliminasi dan representasi matriks, serta memvalidasi hasil secara komputasional | — | Mahasiswa mampu menerapkan Konsep Himpunan, Relasi, Fungsi, Matriks dan Penyelesaian Sistem Persamaan (Linier dan Non-Linier) | - Menyelesaikan sistem persamaan linier dengan menggunakan metode Gauss dan Gauss Jordan - Memahami operasi perhitungan pada matriks - Menghitung invers dan transpos matriks - Menghitung determinan matriks dengan menggunakan metode Expansi Kofaktor (Expansi La… |
| RTI252002 | MK011 | Aljabar Linier | CPMK902 | Mahasiswa mampu menerapkan operasi matriks (invers, transpose, determinan) untuk menyelesaikan permasalahan | — | Mahasiswa mampu menyelesaikan persoalan matematis secara mandiri dengan tanggung jawab serta memperhatikan nilai, norma, dan etika akademik | — |
| RTI252003 | MK012 | Desain Antarmuka | CPMK202 | Mahasiswa mampu membuat wireframe dan prototipe antarmuka menggunakan tools desain UI secara sistematis dan konsisten. | — | — | • Pengantar UI UX • User Persona • User Journey Mapping • User Flow • Wireframing • Low Fidelity • High Fidelity • Color Theory • F Pattern • Z Pattern • Porximity • Common Region • User Profiling • Hick’s Law • Fitts’s Law • A/B Testing • Prototyping • UI UX … |
| RTI252005 | MK014 | RPL | CPMK205 | Mampu merealisasikan blueprint menjadi komponen aplikasi yang modular, maintainable, dan sesuai standar kode. | 7.1.1.1 | 7.1.1.1 SUBCPMK1 Mahasiswa mampu menguasai konsep rekayasa perangkat lunak, software development life cycle (SDLC), UML dan dasar pengujian (testing) pada pengembangan perangkat lunak (produk TIK) 7.1.1.2 SUBCPMK2 Mahasiswa mampu mengoperasikan piranti penduku… | 1. Pengantar RPL 2. Model Pengembangan Perangkat Lunak (Waterfall) 3. Model Pengembangan Perangkat Lunak (Spiral) 4. Model Pengembangan Perangkat Lunak (RUP) 5. Pengantar Model Pengembangan Perangkat Lunak Agile 6. Model Pengembangan Perangkat Lunak Agile (Scr… |
| RTI252006 | MK015 | Basis Data | CPMK203 | Mampu memahami konsep data, basis data, dan basis data relasional, serta merancang model dan skema basis data secara konseptual dan logikal dengan memperhatikan integritas data dan konsep normalisasi. | — | - Mahasiswa mampu menguasai konsep dan metode pengembangan basis data sebagai bagian dari pengembangan produk TIK - Mahasiswa mampu merancang basis data relasional dengan benar - Mahasiswa mampu menggunakan bahasa SQL untuk mengimplementasikan dan mengelola ba… | 1. Pengantar (Konsep Data, Informasi) 2. Konsep Basis Data Relasional 3. ERD 1 4. ERD 2 5. Pemetaan ERD ke Model Relational 6. Pemetaan ERD ke Model Relational (2) 7. Normalisasi Basis Data 8. Pengantar MySQL dan DDL 9. DML MySQL 10. Query Select 11. Select Mu… |
| RTI252007 | MK016 | Prak Basis Data | CPMK203 | Mampu mengimplementasikan perancangan model dan skema basis data konseptual dan logikal melalui kegiatan praktikum dengan memperhatikan integritas data dan prinsip normalisasi. | — | - Mampu merumuskan masalah, menganalisa kebutuhan sistem, merancang, dan membangun sistem berdasarkan hasil perancangan, menguji coba, serta mengintegrasikan sistem sesuai dengan tahapan dalam membangun sistem dibidang pengolahan data dan informasi, multimedia… | 1. Pengantar (Konsep Data, Informasi) 2. Konsep Basis Data Relasional 3. ERD 1 4. ERD 2 5. Pemetaan ERD ke Model Relational 6. Pemetaan ERD ke Model Relational (2) 7. Normalisasi Basis Data 8. Pengantar MySQL dan DDL 9. DML MySQL 10. Query Select 11. Select Mu… |
| RTI252008 | MK017 | Algoritma dan Struktur Data | CPMK207 | Mahasiswa mampu menjelaskan karakteristik berbagai struktur data serta alur pengelolaan data dalam mendukung penyelesaian permasalahan komputasi. | — | — | 1. Searching 2. Sorting 3. Queue 4. Stack 5. Linked List 6. Tree 7. Graf 8. Bruteforce 9. Divide-Conquer 10. Depth First Search 11. Breadth First Search |
| RTI253005 | MK023 | Basis Data Lanjut | CPMK203 | Mahasiswa mampu menggunakan dan merancang arsitektur Database Management System (DBMS) tingkat enterprise untuk mendukung integritas data, efisiensi query, dan skalabilitas sistem multi-platform. | 03.1.1 | Sub CPMK - 03.1.1 Mahasiswa mampu menggunakan dan mengelola Database Management System (DBMS) pada tingkat enterprise Sub CPMK - 03.1.2 Mahasiswa mampu merancang, membangun, dan memanipulasi basis data menggunakan perintah SQL dasar dan lanjutan, seperti DDL, … | 1. Pengenalan PostgreSQL dan Instalasi 2. Query Dasar (DDL dan DML) 3. Query Lanjutan (SELECT, JOIN, AGREGASI, TABLE EXPRESSION) 4. INDEX dan Optimasi Query 5. Fungsi, View, dan Stored Procedure 6. Transaction dan Concurrency 7. Full-Text SEARCh dan JSONB 8. B… |
| RTI253009 | MK027 | Bahasa Inggris 2 | CPMK303 | Mahasiswa mampu berkomunikasi dengan menggunakan bahasa Inggris secara lisan dan tulisan dalam konteks Teknik Informatika. | 3.2.1.1 | 3.2.1.1 SUBCPMK1 Mahasiswa mampu menerapkan pengetahuan tentang teknik berkomunikasi lisan dan tulisan menggunakan bahasa Inggris dalam konteks Teknik Informatika. 3.2.1.2 SUBCPMK2 Mahasiswa mampu berkomunikasi dengan menggunakan bahasa Inggris secara lisan da… | Topic 1: Programming 1.1 Stages in Programming 1.2 Flowcharting 1.3 Programming Language 1.4 Grammatical Functions: Reporting Screen Message Topic 2: Database 2.1. Database Basics 2.2. Grammatical Functions: If-Clause 2.3. Data Processing 2.4. Data Storage Dev… |
| RTI254001 | MK028 | Sistem Pendukung Keputusan | CPMK706 | Mahasiswa mampu merancang, mengimplementasikan dan menganalisa penerapan metode sistem pendukung keputusan pada kasus yang ada | 8.2.1.1 | 8.2.1.1 SUPCPMK 1 Mahasiswa mampu memahami konsep dan aplikasi dari Pengantar SPK, Karakteristik dan Komponen SPK, Weighted Product, Analytic Hierarchy Process, Profil Matching, TOPSIS, ELECTRE, Pengantar Fuzzy, Fuzzy Inference System, Group Decision Support S… | Pengantar SPK, Model Sistem, Metode SAW, Metode AHP, Metode MOORA, Metode Electre, Metode TOPSIS, GDSS, dan Fuzzy. |
| RTI254002 | MK029 | Analisis dan Desain Berorientasi Objek | CPMK208 | Mahasiswa mampu merancang struktur dan komponen perangkat lunak berorientasi objek menggunakan class diagram dan advanced class diagram UML sebagai blueprint desain yang modular, maintainable, dan scalable. | 7.1.1.1 | Sub-CPMK 7.1.1.1 Mahasiswa mampu menerapkan berbagai model diagram UML yang digunakan pada proses pengembangan produk TIK secara mandiri Sub-CPMK 7.1.1.2 Mahasiswa mampu menganalisis sebuah permasalahan dan membuat desain perancangan perangkat lunak pada domai… | 1. Introduction 2. Modeling Requirements: Domain Model 3. Modeling Requirements: Use Cases 4. Modeling Requirements: Use Cases Description 5. Robustness Analysis 6. Modeling System Workflows: Activity Diagrams 7. Modeling Requirements: Domain Model Updated 8. … |
| RTI254008 | MK035 | Statistik Komputasi | CPMK902 | Mahasiswa mampu menerapkan konsep statistika deskriptif dan inferensial (pemusatan data, persebaran data, probabilitas, dan pengujian hipotesis) untuk menganalisis data dalam pendekatan komputasional. | — | — | • Pengenalakan statistika • Pengumpulan data • Penyajian data • Pemusatan data • Persebaran data • Probabilitas • Distribusi data • Statistik inferensial • Populasi, sampel dan proporsi • Hipotesis • Uji normalitas • Uji homogenitas • Analisis korelasi • Anali… |
| RTI254009 | MK036 | Proyek Sistem Informasi | CPMK602 | Mampu menganalisis kebutuhan stakeholder sebagai dasar perancangan arsitektur perangkat lunak. | — | — | 1. Pengenalan proyek sistem informasi 2. Analisa kebutuhan proyek sistem informasi 3. Perancangan proyek sistem informasi 4. Implementasi proyek sistem informasi 5. Pengujian proyek sistem informasi 6. Deployment proyek sistem informasi |
| RTI255002 | MK038 | Metodologi Penelitian | CPMK403 | Mahasiswa mampu menggali permasalahan penelitian secara kritis dan inovatif serta menyusun proposal penelitian dengan memperhatikan kesahihan dan orisinalitas. | 7.5.3.1 | 7.5.3.1 SUBCPMK1 Mahasiswa mampu menggali permasalahan di masyarakat dan lingkungan, menggali kebutuhan, berfikir kritis dan inovatif dalam mencari solusi dan ide skripsi dengan memperhatikan kesahihan dan orisinalitas 7.5.3.2 SUBCPMK2 Mahasiswa mampu menulisk… | 1 Konsep Dasar Penelitian 2 Tahapan Penelitian Computing 3 Studi Pustaka dan Artikel Ilmiah 1 4 Studi Pustaka dan Artikel Ilmiah 2 5 Kuis 1 6 Identifikasi Masalah 7 Metode, Teknik, dan Instrumen Penelitian 8 CM dan UTS 9 Pemodelan Sistem 10 Analisis Kuantitati… |
| RTI255007 | MK043 | Pengolahan Citra dan Visi Komputer | CPMK705 | Mahasiswa mampu mengidentifikasi karakteristik citra digital serta memanfaatkan perangkat lunak dan pustaka pemrograman untuk melakukan akuisisi dan visualisasi citra | 8.2.2.1 | 8.2.2.1 SUBCPMK1 Mahasiswa mampu mengidentifikasi karakteristik citra digital serta memanfaatkan perangkat lunak dan pustaka pemrograman untuk melakukan akuisisi dan visualisasi citra 8.2.2.2 SUBCPMK2 Mahasiswa mampu mengolah citra digital melalui penerapan be… | 1. Pengantar Citra Digital dan Visi Komputer - Konsep dasar citra digital dan visi komputer - Pengenalan tools pendukung (GitHub, Google - Colaboratory, OpenCV, NumPy) - Membaca, menampilkan, dan visualisasi citra 2.Representasi dan Karakteristik Citra Digital… |
| RTI256003 | MK047 | Pemrograman Berbasis Framework | CPMK603 | - Mahasiswa mampu melakukan konfigurasi environment pengembangan (IDE, SDK, dan Framework) serta memilih arsitektur yang sesuai dengan platform target (Web atau Mobile). - Mahasiswa mampu merancang skema basis data dan -… | — | Menguasai konsep matematika terapan, pengetahuan dasar TIK (Algoritma, Pemrograman, Basis Data, Jaringan Komputer, dll), sains rekayasa, dan prinsip rekayasa dalam bidang TIK | Mata Kuliah Pemrograman Berbasis Framework adalah sebuah mata kuliah yang diharapkan dapat memberikan pengetahuan dan keterampilan pembuatan aplikasi web menggunakan framework ReactJS, firebase, dan backend Laravel. |
| RTI256107 | MK051 | Cloud Computing | CPMK905 | Mampu menjelaskan konsep virtualisasi dan karakteristik layanan cloud (IaaS, PaaS, SaaS) serta melakukan teknik dasar penyediaan (provisioning) instance. | 6.2.1.1 | Sub-CPMK 6.2.1.1 Mahasiswa mampu menguasai konsep komputasi awan beserta layanan-layanannya secara mendalam dengan memperhatikan perkembangan teknologi dan isu terkini Sub-CPMK 6.2.1.2 Mahasiswa mampu menggunakan perangkat berupa sejumlah virtual mesin sebagai… | 1. Cloud Environments 2. Layanan Cloud 3. IaaS 4. Virtual Cloud Network 5. PaaS 6. SaaS 7. Cloud Storage 8. Container 9. CI/CD 10. Serverless Computing 11. High Availability |

<!-- markdownlint-enable MD013 -->

## Tanpa Padanan Kurikulum Lama di Sheet

30 dari 55 mata kuliah kurikulum 2025 tidak memiliki data `SubCPMK Lama` /
`Materi Pembelajaran Lama` di sheet acuan — bukan berarti tidak ada
predecessor 2020, hanya belum diisi pada sheet ini.

**23 MK belum punya baris Sub-CPMK aktif sama sekali** di tab ini (baris MK
hanya berisi deklarasi CPL/CPMK, belum dipecah ke Sub-CPMK):
MK013 Sistem Operasi, MK019 Manajemen Proyek, MK020 Sistem Informasi
Manajemen, MK021 Kewarganegaraan, MK022 Desain & Pemrograman Web,
MK024 Metode Numerik, MK025 Pemrograman Berbasis Objek, MK026 Praktikum
Pemrograman Berbasis Objek, MK030 Bahasa Indonesia, MK032 Jaringan
Komputer, MK033 Praktikum Jaringan Komputer, MK034 Pemrograman Web Lanjut,
MK037 Kewirausahaan Berbasis Teknologi, MK039 Pemrograman Mobile,
MK040 Pembelajaran Mesin, MK041 Business Intelligence, MK042 Penjaminan
Mutu Perangkat Lunak, MK044 Administrasi dan Keamanan Jaringan,
MK048 Proyek Teknologi Terintegrasi, MK049 Internet of Things,
MK052 Komputasi Hijau, MK053 Magang, MK054 Skripsi.

**7 MK punya baris Sub-CPMK aktif, tapi tanpa data kurikulum lama**:
MK007 Praktikum Dasar Pemrograman, MK018 Praktikum Algoritma dan Struktur
Data, MK031 Kecerdasan Artifisial, MK045 Komunikasi dan Etika Profesi,
MK046 Pengembangan Karir, MK050 Big Data, MK055 Bahasa Inggris Persiapan
Kerja.

## Catatan

- **MK009 Fisika**: teks `SubCPMK Lama` pada baris pertama tampak tercampur
  dengan materi matematika diskrit ("konsep diskrit, logika, himpunan, dan
  fungsi matematika dasar") — kemungkinan salin-tempel dari mata kuliah lain
  saat penyusunan sheet. Direproduksi apa adanya, tidak diperbaiki di sini.
- **MK011 Aljabar Linier** memiliki 2 baris Sub-CPMK aktif dengan
  `Kode CPMK` yang sama (CPMK902) — keduanya tercantum sebagai baris
  terpisah pada tabel di atas.
- Penomoran Sub-CPMK lama tidak konsisten antar-MK (`2.2.1.1` vs `7.1.1.1`
  vs `Sub CPMK - 03.1.1` vs `SUPCPMK 1` tanpa desimal) karena RPS 2020
  disusun independen per mata kuliah/dosen pengampu.
- Lihat juga [`cpl-cpmk-subcpmk-yellow3-validation.txt`](../generated/cpl-cpmk-subcpmk-yellow3-validation.txt)
  untuk status pengisian sel yellow-3 (kolom Sub-CPMK/Metode/Bentuk/Kriteria/
  Materi baru) pada sheet yang sama.
