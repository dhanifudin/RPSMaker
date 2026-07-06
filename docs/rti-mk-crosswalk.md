# RTI25 → MK → CPL/CPMK Crosswalk

Dibangun berdasarkan analisis `kurikulum-2025-cpl-cpmk.md`, `kurikulum-2025-distribusi-mk.md`,
dan reverse-engineering dari kode Sub-CPMK pada 23 mata kuliah yang sudah di-author.

MK numbering: sequential per kurikulum order (Sem 1 = MK001–009, Sem 2 = MK010–018, dst.).
Sem 6 reguler = MK048–052; Sem 6 magang = MK053–056; Sem 7 = MK057; Sem 8 = MK058–059.

## Tabel Crosswalk

| RTI25 code | Nama MK | SKS | Sem | MK# | CPL | CPMK utama |
|---|---|---|---|---|---|---|
| RTI251001 | Pancasila | 2 | 1 | MK001 | CPL01 | CPMK102 |
| RTI251002 | Konsep TI | 2 | 1 | MK002 | CPL09 | CPMK208, CPMK901 |
| RTI251003 | Critical Thinking | 2 | 1 | MK003 | CPL04 | CPMK401 |
| RTI251004 | Matematika Dasar | 2 | 1 | MK004 | CPL09 | CPMK902 |
| RTI251005 | Bahasa Inggris 1 | 2 | 1 | MK005 | CPL03 | CPMK303 |
| RTI251006 | Dasar Pemrograman | 2 | 1 | MK006 | CPL09 | CPMK903 |
| RTI251007 | Prak Dasar Pemrograman | 3 | 1 | MK007 | CPL09 | CPMK903 |
| RTI251008 | K3 | 2 | 1 | MK008 | CPL01 | CPMK101 |
| RTI251009 | Fisika | 2 | 1 | MK009 | CPL09 | CPMK902 |
| RTI252001 | Agama | 2 | 2 | MK010 | CPL01 | CPMK102 |
| RTI252002 | Aljabar Linier | 2 | 2 | MK011 | CPL09 | CPMK902 |
| RTI252003 | Desain Antarmuka | 2 | 2 | MK012 | CPL02, CPL06, CPL08 | CPMK202, CPMK601, CPMK802 |
| RTI252004 | Sistem Operasi | 2 | 2 | MK013 | CPL09, CPL05 | CPMK206, CPMK208 |
| RTI252005 | RPL | 2 | 2 | MK014 | CPL02, CPL06 | CPMK210, CPMK602 |
| RTI252006 | Basis Data | 2 | 2 | MK015 | CPL02, CPL10 | CPMK203, CPMK10.1 |
| RTI252007 | Prak Basis Data | 2 | 2 | MK016 | CPL02, CPL07 | CPMK203, CPMK701 |
| RTI252008 | Algoritma dan Struktur Data | 2 | 2 | MK017 | CPL09, CPL07 | CPMK903, CPMK703 |
| RTI252009 | Prak ASD | 3 | 2 | MK018 | CPL09, CPL07 | CPMK903, CPMK703 |
| RTI253001 | Manajemen Proyek | 2 | 3 | MK019 | CPL08, CPL03 | CPMK801, CPMK803 |
| **RTI253002** | **Sistem Informasi Manajemen** | **2** | **3** | **MK020** | **CPL02, CPL06, CPL08** | **CPMK211, CPMK607, CPMK802** |
| RTI253003 | Kewarganegaraan | 2 | 3 | MK021 | CPL01 | CPMK102 |
| RTI253004 | Desain dan Pemrograman Web | 3 | 3 | MK022 | CPL02, CPL06 | CPMK603, CPMK704 |
| RTI253005 | Basis Data Lanjut | 3 | 3 | MK023 | CPL02, CPL07, CPL10 | CPMK203, CPMK701, CPMK10.1 |
| RTI253006 | Metode Numerik | 2 | 3 | MK024 | CPL09, CPL10 | CPMK902, CPMK10.7 |
| **RTI253007** | **Pemrograman Berbasis Objek** | **2** | **3** | **MK025** | **CPL02, CPL07, CPL09** | **CPMK210, CPMK704, CPMK903** |
| **RTI253008** | **Prak PBO** | **2** | **3** | **MK026** | **CPL02, CPL07, CPL09** | **CPMK210, CPMK704, CPMK903** |
| **RTI253009** | **Bahasa Inggris 2** | **2** | **3** | **MK027** | **CPL01, CPL03** | **CPMK102, CPMK303** |
| RTI254001 | Sistem Pendukung Keputusan | 2 | 4 | MK028 | CPL07, CPL10 | CPMK706, CPMK10.5 |
| **RTI254002** | **Analisis dan Desain Berorientasi Objek** | **2** | **4** | **MK029** | **CPL02, CPL06, CPL10** | **CPMK211, CPMK602, CPMK10.8** |
| **RTI254003** | **Bahasa Indonesia** | **2** | **4** | **MK030** | **CPL03, CPL04** | **CPMK301, CPMK401** |
| **RTI254004** | **Kecerdasan Artifisial** | **2** | **4** | **MK031** | **CPL07, CPL09, CPL10** | **CPMK706, CPMK10.5** |
| **RTI254005** | **Jaringan Komputer** | **2** | **4** | **MK032** | **CPL05, CPL09, CPL10** | **CPMK504, CPMK901, CPMK10.2** |
| **RTI254006** | **Prak Jaringan Komputer** | **2** | **4** | **MK033** | **CPL05, CPL09** | **CPMK504, CPMK901** |
| RTI254007 | Pemrograman Web Lanjut | 3 | 4 | MK034 | CPL02, CPL06, CPL10 | CPMK603, CPMK10.6 |
| **RTI254008** | **Statistik Komputasi** | **2** | **4** | **MK035** | **CPL07, CPL09, CPL10** | **CPMK707, CPMK902** |
| **RTI254009** | **Proyek Sistem Informasi** | **3** | **4** | **MK036** | **CPL02, CPL06, CPL08** | **CPMK801, CPMK802, CPMK803, CPMK607** |
| RTI255001 | Kewirausahaan Berbasis Teknologi | 2 | 5 | MK037 | CPL01, CPL08 | CPMK101, CPMK801 |
| **RTI255002** | **Metodologi Penelitian** | **2** | **5** | **MK038** | **CPL04, CPL03** | **CPMK403, CPMK401** |
| RTI255003 | Pemrograman Mobile | 3 | 5 | MK039 | CPL02, CPL06, CPL10 | CPMK603, CPMK10.6 |
| **RTI255004** | **Pembelajaran Mesin** | **3** | **5** | **MK040** | **CPL07, CPL10** | **CPMK706, CPMK10.5** |
| **RTI255005** | **Business Intelligence** | **2** | **5** | **MK041** | **CPL07, CPL10** | **CPMK705, CPMK706, CPMK10.4** |
| RTI255006 | Penjaminan Mutu PL | 2 | 5 | MK042 | CPL06 | CPMK608, CPMK606 |
| **RTI255007** | **Pengolahan Citra dan Visi Komputer** | **3** | **5** | **MK043** | **CPL07, CPL10** | **CPMK705, CPMK706, CPMK10.4, CPMK10.5** |
| RTI255008 | Administrasi dan Keamanan Jaringan | 2 | 5 | MK044 | CPL05, CPL10 | CPMK501, CPMK505 |
| **RTI256001** | **Komunikasi dan Etika Profesi** | **2** | **6** | **MK045** | **CPL01, CPL03** | **CPMK101, CPMK301, CPMK303** |
| RTI256002 | Pengembangan Karir | 2 | 6 | MK046 | CPL01, CPL03 | CPMK102, CPMK303 |
| RTI256003 | Pemrograman Berbasis Framework | 2 | 6 | MK047 | CPL02, CPL06, CPL10 | CPMK603, CPMK10.6 |
| **RTI256104** | **Proyek Teknologi Terintegrasi** | **6** | **6** | **MK048** | **CPL02, CPL06, CPL08, CPL10** | **CPMK801, CPMK802, CPMK803, CPMK804, CPMK607** |
| **RTI256105** | **Internet of Things** | **3** | **6** | **MK049** | **CPL05, CPL02, CPL09** | **CPMK204, CPMK503, CPMK904** |
| **RTI256106** | **Big Data** | **2** | **6** | **MK050** | **CPL07, CPL05, CPL09** | **CPMK702, CPMK904** |
| **RTI256107** | **Cloud Computing** | **2** | **6** | **MK051** | **CPL05, CPL09, CPL10** | **CPMK509, CPMK905, CPMK10.3** |
| **RTI256108** | **Komputasi Hijau** | **2** | **6** | **MK052** | **CPL01, CPL05** | **CPMK101, CPMK509** |
| **RTI256204** | **Proyek Inovasi** | **6** | **6** | **MK053** | **CPL08, CPL02, CPL06** | **CPMK801, CPMK803, CPMK804, CPMK607** |
| **RTI256205** | **Workshop Teknologi Terapan** | **3** | **6** | **MK054** | **CPL02, CPL06, CPL08** | **CPMK603, CPMK802, CPMK803** |
| **RTI256206** | **Rekayasa Sistem** | **3** | **6** | **MK055** | **CPL02, CPL06, CPL10** | **CPMK211, CPMK602, CPMK609** |
| **RTI256207** | **Teknologi Terapan** | **2** | **6** | **MK056** | **CPL02, CPL05, CPL08** | **CPMK204, CPMK503, CPMK801** |
| **RTI257001** | **Magang** | **20** | **7** | **MK057** | **CPL03, CPL06, CPL08** | **CPMK301, CPMK303, CPMK804, CPMK607** |
| **RTI258001** | **Skripsi** | **8** | **8** | **MK058** | **CPL04, CPL06, CPL08, CPL10** | **CPMK403, CPMK404, CPMK802, CPMK804, CPMK10.9** |
| **RTI258002** | **Bahasa Inggris Persiapan Kerja** | **2** | **8** | **MK059** | **CPL01, CPL03** | **CPMK303, CPMK102** |

Bold = 28 mata kuliah yang belum ada RPS (target fase ini).

## Sub-CPMK Numbering Convention

Format: `SCPMK<cpmk>-<MKnum3digit><seq2digit>`

Contoh: SCPMK211-02001 = Sub-CPMK dari CPMK211, MK020 (RTI253002 SIM), indikator 01.

Per course, sequencing is: 01, 02, 03, ... regardless of which CPMK each sub-CPMK belongs to.

## Catatan Sumber

Lihat `legacy-report.json` di scratchpad. Banyak file SIAKAD 2020 memiliki konten mismatch (kode ≠ nama):
- RTI214002 "Proyek 1" → isi ADBO/UML topics → pakai untuk RTI254002 ADBO
- RTI214004 "Machine Learning" → isi Software Project topics → pakai untuk RTI254009 Proyek SI  
- RTI215002 "Proyek 2" → isi Bahasa Indonesia → pakai untuk RTI254003
- RTI215004 "Business Intelligence" → isi Pembelajaran Mesin → pakai untuk RTI255004
- RTI215006 "Bahasa Indonesia" → isi Pengolahan Citra → pakai untuk RTI255007
- RTI215008 "Komputasi Awan" → isi SPK topics → tidak dipakai (SPK sudah ada)
- RTI216005, RTI216006, RTI217008 → kosong
