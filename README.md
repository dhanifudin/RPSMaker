# Buku Kurikulum D4 Teknik Informatika

Repositori ini memuat sumber RPS per mata kuliah dan buku kurikulum LaTeX untuk Kurikulum 2025 Program Studi D4 Teknik Informatika.

## Struktur Utama

- `subjects/`: sumber LaTeX RPS, RTM, dan rubrik per mata kuliah.
- `RPS/`: hasil PDF RPS yang dibangkitkan dari `subjects/` dan digunakan sebagai lampiran buku.
- `data/`: ekspor JSON per mata kuliah (`rps_<kode>_<slug>.json`), dibangkitkan dari `scripts/export_rps_json.py`.
- `docs/`: ringkasan sumber kurikulum 2025, termasuk distribusi MK serta CPL/CPMK.
- `book/`: sumber buku kurikulum LaTeX yang diadopsi dari proyek accreditation.
- `book/main.tex`: berkas utama buku kurikulum.

## Build

Bangun semua RPS dan buku kurikulum:

```bash
make all
```

Bangun hanya RPS:

```bash
make rps
```

Bangun hanya buku kurikulum dari RPS yang sudah ada:

```bash
make book
```

Hasil buku kurikulum dibuat sebagai `book/main.pdf`.

## Ekspor JSON

Ekspor RPS semua 59 mata kuliah ke `data/` (satu file JSON per MK):

```bash
make json
```

Validasi kelengkapan dan konsistensi hasil ekspor:

```bash
make validate-json
```

Atau gunakan skrip langsung untuk satu mata kuliah:

```bash
python3 scripts/export_rps_json.py --subject RTI251006 --print
```

## Catatan Sumber Data

Gunakan `docs/kurikulum-2025-distribusi-mk.md` dan `docs/kurikulum-2025-cpl-cpmk.md` sebagai acuan ringkas kurikulum 2025. Berkas tersebut lebih baru daripada draft accreditation awal dan mencatat perubahan terakhir terkait penghapusan `CPMK506` dan `CPMK507`.
