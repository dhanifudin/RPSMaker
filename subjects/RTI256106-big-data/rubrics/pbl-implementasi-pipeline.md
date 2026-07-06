---
course_code: RTI256106
course_name: Big Data
sub_cpmk: SCPMK702-05001
assessment_form: Project Based Learning
---

# PBL Implementasi Pipeline Big Data

**Bentuk Tugas/Evaluasi:** Project Based Learning

**Sub-CPMK:** SCPMK702-05001

## Deskripsi
Mahasiswa mengimplementasikan pipeline pemrosesan Big Data lengkap menggunakan ekosistem Hadoop/Spark yang mencakup batch processing, stream processing, dan penyimpanan data dalam data lakehouse.

## Metode Pengerjaan
Membangun pipeline end-to-end, mengimplementasikan Spark job untuk batch dan streaming, mengintegrasikan Kafka, menyimpan ke Delta Lake/Iceberg, dan memvisualisasikan hasil.

## Bentuk Format Luaran
Pipeline berjalan di cluster/Docker, kode sumber, data catalog, laporan implementasi, dan visualisasi output data.

## Rubrik Penilaian

| Indikator Penilaian | Bobot (%) | Kriteria 3 (Baik) | Kriteria 2 (Cukup) | Kriteria 1 (Kurang) |
| --- | ---: | --- | --- | --- |
| Kelengkapan dan fungsionalitas pipeline | 9 | Pipeline mencakup ingestion, batch processing, stream processing, storage, dan serving; semua komponen berjalan end-to-end tanpa error kritis. | Pipeline mencakup sebagian besar komponen tetapi beberapa stage (terutama streaming atau storage) belum berjalan optimal. | Pipeline tidak dapat berjalan end-to-end atau lebih dari setengah komponen tidak berfungsi. |
| Kualitas implementasi Spark dan Kafka | 8 | Spark job teroptimasi (partitioning, caching, serialization), Kafka consumer/producer terkonfigurasi dengan benar, dan throughput memenuhi target. | Spark job dan Kafka berjalan tetapi optimasi atau konfigurasi masih dapat ditingkatkan secara signifikan. | Spark job atau Kafka tidak berjalan dengan benar atau throughput sangat jauh di bawah target. |
| Dokumentasi dan visualisasi output | 5 | Kode terdokumentasi, arsitektur pipeline divisualisasikan, output data divisualisasikan secara bermakna, dan laporan implementasi lengkap. | Dokumentasi dan visualisasi tersedia tetapi beberapa komponen masih kurang rinci atau tidak informatif. | Dokumentasi tidak mencukupi untuk mereproduksi pipeline atau output data tidak divisualisasikan. |
