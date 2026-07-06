---
course_code: RTI256107
course_name: Cloud Computing
sub_cpmk: SCPMK509-05101, SCPMK10.3-05103
assessment_form: Project Based Learning
---

# PBL Deployment Aplikasi Cloud

**Bentuk Tugas/Evaluasi:** Project Based Learning

**Sub-CPMK:** SCPMK509-05101, SCPMK10.3-05103

## Deskripsi
Mahasiswa men-deploy aplikasi nyata ke platform cloud menggunakan container, mengkonfigurasi keamanan dan jaringan, serta mengoptimalkan biaya operasional secara berkelompok.

## Metode Pengerjaan
Merancang arsitektur deployment, mengimplementasikan containerisasi dengan Docker/Kubernetes, mengkonfigurasi VPC dan IAM, menguji fungsionalitas end-to-end, dan mendokumentasikan seluruh proses.

## Bentuk Format Luaran
Aplikasi yang berjalan di platform cloud, konfigurasi infrastruktur (Infrastructure as Code jika memungkinkan), laporan teknis deployment, dan bukti pengujian.

## Rubrik Penilaian

| Indikator Penilaian | Bobot (%) | Kriteria 3 (Baik) | Kriteria 2 (Cukup) | Kriteria 1 (Kurang) |
| --- | ---: | --- | --- | --- |
| Keberhasilan deployment dan konfigurasi infrastruktur | 9 | Aplikasi berhasil di-deploy ke platform cloud dengan containerisasi yang benar, networking (VPC/Load Balancer) terkonfigurasi, dan endpoint dapat diakses dari internet. | Deployment berhasil tetapi konfigurasi networking atau containerisasi masih memiliki kekurangan teknis minor. | Deployment gagal atau aplikasi tidak dapat diakses dari luar environment cloud. |
| Implementasi keamanan dan IAM | 7 | IAM dikonfigurasi dengan prinsip least privilege, enkripsi data-at-rest dan in-transit diterapkan, dan kepatuhan terhadap best practice keamanan terdokumentasi. | Konfigurasi IAM dan enkripsi ada tetapi prinsip least privilege atau dokumentasi keamanan belum lengkap. | IAM tidak dikonfigurasi dengan benar atau keamanan dasar tidak diterapkan. |
| Optimasi biaya dan dokumentasi | 6 | Strategi optimasi biaya diterapkan (right-sizing, auto-scaling), estimasi biaya bulanan realistis, dan dokumentasi infrastruktur lengkap serta reproducible. | Optimasi biaya dipertimbangkan tetapi strategi atau dokumentasi belum komprehensif. | Tidak ada pertimbangan optimasi biaya atau dokumentasi infrastruktur tidak memadai. |
