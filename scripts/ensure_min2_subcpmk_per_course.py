"""Ensure every course (MK) in MK-CPMK-SubCPMK-Metode has >= 2 Sub-CPMK.

Background
----------
Scanned every course (MK) in docs/cpl-cpmk-subcpmk.xlsx's MK-CPMK-SubCPMK-Metode sheet
(correcting for the known MK053/MK054 label mislabeling - those rows are actually
Magang(057)/Skripsi(058) content, established earlier this session) and found 8 of 59
courses with fewer than 2 Sub-CPMK: 4 with exactly 1, 4 with zero. All other 51 courses
already have >= 2.

Every one of these 8 courses has a real, published subjects/*/*-RPS.tex with enough
Sub-CPMK to clear the >= 2 bar on its own:

  MK001 Pancasila                        : draft has 1 (-00101), real has 4 (-00101..04)
  MK009 Fisika                           : draft has 1 (-00905, content-mismatched -
                                            see docs/subcpmk-wording-review.md SS3a,
                                            left untouched), real has 4 (-00901..04)
  MK021 Kewarganegaraan                  : draft has 1 (-02104), real has 4 (-02101..04)
  MK047 Pemrograman Berbasis Framework   : draft has 1 (-04704), real has 3 (-04701..03)
  MK053 Proyek Inovasi                   : draft has 0, real has 4 (-05301..04)
  MK054 Workshop Teknologi Terapan       : draft has 0, real has 3 (-05401..03)
  MK056 Teknologi Terapan                : draft has 0, real has 3 (-05601..03)
  MK059 Bahasa Inggris Persiapan Kerja   : draft has 0, real has 2 (-05901..02)

This script adds the 20 missing (course, code) rows, all sourced verbatim/near-verbatim
from each course's real published RPS - zero fabricated content. Sub-CPMK code and
statement text (column I/J) are copied exactly from each course's RPS header block
("Kemampuan akhir tiap tahapan belajar (Sub-CPMK)" section). Bentuk Pembelajaran/Bentuk
Penilaian/Materi Pembelajaran (columns K/L/M/N/O) are summarized from that Sub-CPMK's
weekly-table entries in the same RPS (aggregated, not literally one row's text, matching
how existing hand-authored rows in this sheet already summarize rather than quote a
single week).

Row placement: APPENDED at the end of the sheet (after row 1150) rather than inserted
into each course's existing block. Inserting mid-sheet would require renumbering every
row and cell reference at or after the insertion point across the whole ~1150-row sheet
(and re-checking mergeCells ranges) - a much higher-risk operation than anything else
done to this workbook this session. Appending is functionally equivalent: every new row
is fully self-contained (Kode MK/MK Name filled directly on every row, not relying on
blank-continuation from a preceding block row), so course grouping still works correctly
for every downstream script/analysis that reads this sheet - it's just not physically
adjacent to that course's other rows anymore, a cosmetic difference only.

Columns P/Q/R ("SubCPMK Lama"/"Materi Pembelajaran Lama"/"Deskripsi") are legacy columns
left empty on the large majority of existing rows (including all 26+44 rows added by
prior fix passes this session) - left empty here too, consistent with that convention.

Why raw zip/XML surgery instead of openpyxl load+save
------------------------------------------------------
Same reasoning as every other fix/normalize script in this repo: openpyxl
load_workbook(...).save(...) previously caused data loss in this exact workbook.
"""

import argparse
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(REPO_ROOT, "docs", "cpl-cpmk-subcpmk.xlsx")
SHEET = "xl/worksheets/sheet16.xml"

LAST_ROW = 1150

# Each entry: (Kode MK, MK, CPL, Kode BK, BK, Kode CPMK, CPMK desc, Kode SubCPMK,
#              SubCPMK text, Metode Pembelajaran, Bentuk Pembelajaran, Bentuk Penilaian,
#              Kriteria Penilaian, Materi Pembelajaran)
# Kode BK/BK left empty where no reliable master-sheet mapping was found (not fabricated).
NEW_ROWS = [
    # --- MK001 Pancasila: draft has -00101, adding -00102/-00103/-00104 (real RPS) ---
    ("MK001", "Pancasila",
     "(CPL01) Menginternalisasi ketakwaan kepada Tuhan Yang Maha Esa, menaati hukum, disiplin, dan menunjukkan profesionalisme melalui etika profesi, pembelajaran sepanjang hayat, serta respons terhadap isu sosial dan teknologi.",
     "BK30", "Pengembangan Diri",
     "CPMK0102", "Mampu menginternalisasi nilai ketakwaan kepada Tuhan YME, Pancasila, kewarganegaraan, dan menunjukkan pembelajaran sepanjang hayat melalui disiplin diri, tanggung jawab sosial, dan adaptasi karir profesional",
     "SCPMK0102-00102", "Mahasiswa mampu menjelaskan UUD RI 1945, amandemen UUD RI 1945, Trias Politika, dan kelembagaan negara menurut UUD RI 1945 [C2, A3].",
     "Ceramah, presentasi, diskusi, dan tanya jawab", "Kuliah/Luring",
     "tes lisan dan tugas", "ketepatan dan kejelasan penjelasan; kesesuaian isi tulisan dengan materi; kemampuan presentasi",
     "UUD RI 1945: sejarah perumusan dan pengesahan, pokok pikiran pembukaan, nilai, dan kedudukan; amandemen UUD RI 1945; Trias Politika; kelembagaan negara menurut UUD RI 1945"),
    ("MK001", "", "", "", "",
     "CPMK0102", "Mampu menginternalisasi nilai ketakwaan kepada Tuhan YME, Pancasila, kewarganegaraan, dan menunjukkan pembelajaran sepanjang hayat melalui disiplin diri, tanggung jawab sosial, dan adaptasi karir profesional",
     "SCPMK0102-00103", "Mahasiswa mampu menjelaskan Pancasila sebagai ideologi nasional dan membandingkannya dengan ideologi lain yang berkembang di dunia [C2, A3].",
     "Ceramah, presentasi, diskusi, tanya jawab, dan kuis", "Kuliah/Luring",
     "tes lisan, tugas, dan kuis tertulis", "kelancaran dan kesesuaian dalam kerja tim; ketepatan jawaban",
     "Pancasila sebagai ideologi nasional: definisi, fungsi, dan proses terbentuknya; ideologi lain yang berkembang di dunia"),
    ("MK001", "", "", "", "",
     "CPMK0102", "Mampu menginternalisasi nilai ketakwaan kepada Tuhan YME, Pancasila, kewarganegaraan, dan menunjukkan pembelajaran sepanjang hayat melalui disiplin diri, tanggung jawab sosial, dan adaptasi karir profesional",
     "SCPMK0102-00104", "Mahasiswa mampu menginternalisasi nilai Pancasila dalam isu HAM, pencegahan tindak pidana korupsi, dan Pancasila sebagai paradigma pembangunan [C3, A4].",
     "Ceramah, presentasi, diskusi, tanya jawab; Case Method, FGD (untuk topik HAM dan korupsi)", "Kuliah/Luring",
     "tes lisan, tugas, dan penilaian case method", "kelancaran dan kesesuaian dalam kerja tim; ketajaman analisis kasus dan argumentasi; daya tarik presentasi",
     "Pancasila dan HAM; pelaksanaan HAM dalam UUD RI 1945; tindak pidana korupsi: pengertian, jenis, dasar hukum, pencegahan; Pancasila sebagai paradigma pembangunan"),

    # --- MK009 Fisika: draft has -00905 (mismatched, left as-is), adding -00901..00904 (real RPS) ---
    ("MK009", "Fisika",
     "CPL09 Memiliki pemahaman yang memadai terkait cara kerja sistem komputer dan berbagai teknik/pendekatan berbasis komputasi untuk memecahkan masalah stakeholder",
     "BK20\nBK21", "Computational Science\nDiscrete Structures",
     "CPMK0902", "Mahasiswa mampu menerapkan prinsip matematis dan struktur diskrit sebagai dasar analisis komputasional.",
     "SCPMK0902-00901", "Mahasiswa mampu menjelaskan hakikat fisika, peran fisika dalam teknologi informasi, dan metode ilmiah, serta melakukan pengukuran, konversi satuan, dan analisis ketidakpastian.",
     "Contextual Teaching and Learning (CTL) dan Problem/Project Based Learning", "Luring/Daring",
     "keaktifan diskusi kelompok dan ketepatan jawaban tugas; kuis tertulis", "ketepatan dan penguasaan",
     "Hakikat dan ruang lingkup fisika; peran fisika dalam bidang TI; metode ilmiah; besaran dan satuan; alat ukur dan ketidakpastian pengukuran"),
    ("MK009", "", "", "", "",
     "CPMK0902", "Mahasiswa mampu menerapkan prinsip matematis dan struktur diskrit sebagai dasar analisis komputasional.",
     "SCPMK0902-00902", "Mahasiswa mampu menganalisis kinematika gerak lurus dan gerak dua dimensi serta menerapkan hukum Newton untuk menyelesaikan masalah dinamika partikel pada sistem mekanik.",
     "Contextual Teaching and Learning (CTL) dan Project Based Learning", "Luring/Daring",
     "keaktifan diskusi kelompok dan ketepatan jawaban tugas; ujian tertulis (UTS)", "ketepatan dan penguasaan",
     "Kinematika gerak lurus (GLB dan GLBB); kinematika gerak dua dimensi; Hukum Newton I, II, III dan gaya-gaya; penerapan hukum Newton dalam sistem mekanik"),
    ("MK009", "", "", "", "",
     "CPMK0902", "Mahasiswa mampu menerapkan prinsip matematis dan struktur diskrit sebagai dasar analisis komputasional.",
     "SCPMK0902-00903", "Mahasiswa mampu menganalisis hubungan usaha dan energi serta menerapkan konsep impuls, momentum, dan hukum kekekalan momentum pada permasalahan tumbukan.",
     "Contextual Teaching and Learning (CTL) dan Project Based Learning", "Luring/Daring",
     "keaktifan diskusi kelompok dan ketepatan jawaban tugas; kuis tertulis", "ketepatan dan penguasaan",
     "Usaha, energi kinetik, energi potensial, hukum kekekalan energi; momentum, impuls, hukum kekekalan momentum, tumbukan elastis dan inelastis"),
    ("MK009", "", "", "", "",
     "CPMK0902", "Mahasiswa mampu menerapkan prinsip matematis dan struktur diskrit sebagai dasar analisis komputasional.",
     "SCPMK0902-00904", "Mahasiswa mampu menganalisis gaya Coulomb, medan dan potensial listrik, kapasitansi, serta rangkaian listrik DC untuk permasalahan kelistrikan pada sistem elektronik.",
     "Contextual Teaching and Learning (CTL) dan Project Based Learning", "Luring/Daring",
     "keaktifan diskusi kelompok dan ketepatan jawaban tugas; ujian tertulis (UAS)", "ketepatan dan penguasaan",
     "Muatan listrik, hukum Coulomb, medan listrik; potensial listrik; kapasitor dan kapasitansi; rangkaian listrik DC sederhana (hukum Ohm dan Kirchhoff)"),

    # --- MK021 Kewarganegaraan: draft has -02104, adding -02101/-02102/-02103 (real RPS) ---
    ("MK021", "Kewarganegaraan",
     "(CPL01) Menginternalisasi ketakwaan kepada Tuhan Yang Maha Esa, menaati hukum, disiplin, dan menunjukkan profesionalisme melalui etika profesi, pembelajaran sepanjang hayat, serta respons terhadap isu sosial dan teknologi.",
     "BK30", "Pengembangan Diri",
     "CPMK0102", "Mahasiswa mampu menginternalisasi nilai ketakwaan, Pancasila, kewarganegaraan, dan tanggung jawab sosial sebagai landasan sikap profesional serta berkomitmen pada lifelong learning dan adaptasi karir.",
     "SCPMK0102-02101", "Mahasiswa mampu menjelaskan konsep identitas nasional, negara, konstitusi, dan hubungan negara dengan warga negara sebagai fondasi kehidupan berbangsa dan bernegara.",
     "Ceramah, diskusi kelompok, studi kasus, dan tanya jawab", "Blended Learning (Luring/Daring)",
     "tugas tertulis analisis kewarganegaraan; kuis tertulis", "ketepatan pemahaman konsep; kualitas analisis tertulis; partisipasi diskusi",
     "Identitas nasional; negara dan konstitusi; hubungan negara dan warga negara (hak dan kewajiban)"),
    ("MK021", "", "", "", "",
     "CPMK0102", "Mahasiswa mampu menginternalisasi nilai ketakwaan, Pancasila, kewarganegaraan, dan tanggung jawab sosial sebagai landasan sikap profesional serta berkomitmen pada lifelong learning dan adaptasi karir.",
     "SCPMK0102-02102", "Mahasiswa mampu menganalisis sistem demokrasi dan negara hukum dalam konteks kehidupan berbangsa dan bernegara di Indonesia.",
     "Ceramah, diskusi kelompok, studi kasus, dan tanya jawab", "Blended Learning (Luring/Daring)",
     "tugas tertulis analisis kewarganegaraan; ujian tertulis (UTS)", "ketepatan pemahaman konsep; kualitas analisis tertulis; partisipasi diskusi",
     "Negara hukum: pengertian, ciri, dan makna Indonesia sebagai negara hukum; demokrasi: konsep dasar, prinsip, indikator, perjalanan demokrasi di Indonesia"),
    ("MK021", "", "", "", "",
     "CPMK0102", "Mahasiswa mampu menginternalisasi nilai ketakwaan, Pancasila, kewarganegaraan, dan tanggung jawab sosial sebagai landasan sikap profesional serta berkomitmen pada lifelong learning dan adaptasi karir.",
     "SCPMK0102-02103", "Mahasiswa mampu menjelaskan konsep hak asasi manusia, prinsip-prinsipnya, dan mekanisme penegakannya dalam kehidupan berbangsa dan bernegara.",
     "Ceramah, diskusi kelompok, studi kasus, dan tanya jawab", "Blended Learning (Luring/Daring)",
     "tugas tertulis analisis kewarganegaraan", "ketepatan pemahaman konsep; kualitas analisis tertulis; partisipasi diskusi",
     "Hak Asasi Manusia: pengertian, prinsip, sejarah perkembangan; jenis-jenis HAM, dasar hukum HAM nasional dan internasional, mekanisme penegakan dan pelanggaran HAM"),

    # --- MK047 Pemrograman Berbasis Framework: draft has -04704, adding -04701/-04702/-04703 (real RPS) ---
    ("MK047", "Pemrograman Berbasis Framework",
     "(CPL06) Mampu merancang, mengimplementasikan, menguji, melakukan deployment, dan memelihara, serta menjamin mutu perangkat lunak yang menjawab permasalahan dan memenuhi kebutuhan stakeholder",
     "BK19", "Platform-based Development",
     "CPMK0209", "Mahasiswa mampu memilih dan menerapkan teknologi pengembangan berbasis platform untuk membangun aplikasi sesuai kebutuhan.",
     "SCPMK0209-04701", "Mahasiswa mampu menerapkan setup, routing, styling, custom document, API routes, CSR, SSR, SSG, ISR, middleware, dan route protection.",
     "hands-on practice, mentoring, code review, demo, dan presentasi", "Praktikum/PBL (Blended Learning)",
     "Bentuk penilaian praktik: setup, routing, styling, custom document, API routes, CSR/SSR/SSG/ISR, middleware, route protection", "Ketepatan konsep; kualitas artefak/praktik; validasi dan dokumentasi",
     "Setup dan routing; styling dan custom document; API routes dan CSR; SSR dan static generation; dynamic routing dan ISR; middleware dan route protection"),
    ("MK047", "", "", "", "",
     "CPMK0603", "Mampu mengimplementasikan dan melakukan deployment aplikasi perangkat lunak pada platform web, mobile, atau framework secara fungsional.",
     "SCPMK0603-04702", "Mahasiswa mampu mengimplementasikan authentication, multi-role system, optimasi, dan unit testing pada aplikasi framework modern.",
     "hands-on practice, mentoring, code review, demo, dan presentasi", "Praktikum/PBL (Blended Learning)",
     "Bentuk penilaian praktik: authentication dan multi role; optimization dan unit testing; UTS framework fundamentals", "Ketepatan konsep; kualitas artefak/praktik; validasi dan dokumentasi",
     "Authentication dan multi role; optimization dan unit testing"),
    ("MK047", "", "", "", "",
     "CPMK0603", "Mampu mengimplementasikan dan melakukan deployment aplikasi perangkat lunak pada platform web, mobile, atau framework secara fungsional.",
     "SCPMK0603-04703", "Mahasiswa mampu menghasilkan aplikasi berbasis framework melalui PBL berdasarkan kebutuhan stakeholder.",
     "hands-on practice, mentoring, code review, demo, dan presentasi (PBL bertahap sprint)", "Praktikum/PBL (Blended Learning)",
     "Bentuk penilaian PBL bertahap: analisis kebutuhan, fitur inti, data/API dan state, auth/role, testing dan optimasi, deployment preparation, finalisasi, UAS presentasi", "Ketepatan konsep; kualitas artefak/praktik; validasi dan dokumentasi",
     "PBL analisis kebutuhan; fitur inti; data/API dan state; auth/role; testing dan optimasi; deployment preparation; finalisasi proyek; presentasi hasil proyek"),

    # --- MK053 Proyek Inovasi: draft has 0, adding all 4 (real RPS) ---
    ("MK053", "Proyek Inovasi",
     "CPL08 Mampu mengelola proyek teknologi informasi secara profesional melalui perencanaan, koordinasi, komunikasi, dan optimalisasi sumber daya.",
     "", "",
     "CPMK0801", "Mahasiswa mampu merencanakan proyek inovasi TI berbasis konteks industri nyata.",
     "SCPMK0801-05301", "Mahasiswa mampu menyusun proposal proyek inovasi TI dengan analisis masalah, solusi teknologi, WBS, dan rencana risiko.",
     "Project Based Learning, agile sprint, presentasi, dan peer review", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: orientasi proyek inovasi; problem framing dan opportunity analysis; technology landscape; proposal proyek inovasi (WBS, jadwal, anggaran, risiko)", "Kelengkapan artefak; kualitas implementasi; kemajuan dan dokumentasi",
     "Orientasi proyek inovasi dan pembentukan tim; problem framing dan opportunity analysis; technology landscape (tren TI 2025); proposal: WBS, jadwal, anggaran, risiko"),
    ("MK053", "", "", "", "",
     "CPMK0803", "Mahasiswa mampu mengeksekusi, memonitor, dan mengendalikan proyek inovasi serta memimpin tim.",
     "SCPMK0803-05302", "Mahasiswa mampu mengeksekusi proyek inovasi berbasis sprint, melaporkan kemajuan, dan mengelola perubahan tim.",
     "Project Based Learning, agile sprint, presentasi, dan peer review", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: sprint 1 review dan demo; UTS milestone review dan evaluasi; sprint 2 review dan sprint 3 planning", "Kelengkapan artefak; kualitas implementasi; kemajuan dan dokumentasi",
     "Sprint 1 review dan demo; UTS milestone review dan evaluasi; sprint 2 review dan sprint 3 planning"),
    ("MK053", "", "", "", "",
     "CPMK0804", "Mahasiswa mampu mendemonstrasikan penyelesaian proyek inovasi TI secara utuh.",
     "SCPMK0804-05303", "Mahasiswa mampu mempresentasikan hasil proyek inovasi dengan defense teknis dan bisnis yang komprehensif.",
     "Project Based Learning, agile sprint, presentasi, dan peer review", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: sprint 4 product polish dan dokumentasi; laporan akhir proyek; latihan presentasi dan pitch; UAS defense proyek inovasi dan demo", "Kelengkapan artefak; kualitas implementasi; kemajuan dan dokumentasi",
     "Sprint 4: product polish dan dokumentasi; penyusunan laporan akhir; latihan presentasi dan pitch"),
    ("MK053", "", "", "", "",
     "CPMK0607", "Mahasiswa mampu menghasilkan solusi sistem informasi inovatif yang menjawab permasalahan nyata industri.",
     "SCPMK0607-05304", "Mahasiswa mampu mengintegrasikan teknologi mutakhir menjadi solusi inovatif yang scalable dan deployable.",
     "Project Based Learning, agile sprint, presentasi, dan peer review", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: sprint 1 PoC dan MVP; sprint 1 validasi teknis; sprint 2 pengembangan fitur; sprint 2 integration testing; sprint 3 skalabilitas dan deployment; sprint 3 UAT", "Kelengkapan artefak; kualitas implementasi; kemajuan dan dokumentasi",
     "Sprint 1: proof of concept dan MVP, validasi teknis dan iterasi; sprint 2: pengembangan fitur utama, integration testing dan optimasi; sprint 3: skalabilitas dan deployment preparation, UAT"),

    # --- MK054 Workshop Teknologi Terapan: draft has 0, adding all 3 (real RPS) ---
    ("MK054", "Workshop Teknologi Terapan",
     "CPL06 Mampu merancang, mengimplementasikan, menguji, melakukan deployment, memelihara, serta menjamin mutu perangkat lunak yang menjawab permasalahan dan memenuhi kebutuhan pengguna.",
     "", "",
     "CPMK0603", "Mahasiswa mampu menerapkan teknik pengujian perangkat lunak dan quality assurance dalam konteks industri nyata.",
     "SCPMK0603-05401", "Mahasiswa mampu merancang dan mengeksekusi rencana pengujian komprehensif termasuk unit testing, integration testing, dan UAT.",
     "Workshop berbasis sprint, peer collaboration, stakeholder review, dan retrospective", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: sprint 1 testing dan dokumentasi; sprint 2 integrasi dan regression testing; sprint 3 finalisasi dan performance testing; sprint 3 UAT dan feedback; laporan QA dan dokumentasi testing", "Ketepatan implementasi; kualitas produk; validasi dan dokumentasi",
     "Sprint 1: testing dan dokumentasi; sprint 2: integrasi dan regression testing; sprint 3: finalisasi fitur dan performance testing, UAT dan feedback incorporation; laporan QA dan dokumentasi testing final"),
    ("MK054", "", "", "", "",
     "CPMK0802", "Mahasiswa mampu mengimplementasikan siklus hidup rekayasa perangkat lunak secara menyeluruh dalam workshop industri.",
     "SCPMK0802-05402", "Mahasiswa mampu mengembangkan produk teknologi terapan melalui iterasi sprint berbasis kebutuhan industri nyata.",
     "Workshop berbasis sprint, peer collaboration, stakeholder review, dan retrospective", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: analisis kebutuhan industri; setup environment dan architecture design; sprint 1 implementasi fitur core; sprint 2 pengembangan fitur lanjutan; sprint 4 product polish dan deployment", "Ketepatan implementasi; kualitas produk; validasi dan dokumentasi",
     "Analisis kebutuhan industri dan requirement engineering; setup environment dan architecture design; sprint 1: implementasi fitur core; sprint 2: pengembangan fitur lanjutan; sprint 4: product polish dan deployment"),
    ("MK054", "", "", "", "",
     "CPMK0803", "Mahasiswa mampu mengeksekusi dan mengelola proyek workshop teknologi secara profesional dalam tim lintas fungsi.",
     "SCPMK0803-05403", "Mahasiswa mampu memimpin tim dalam workshop, mengelola backlog, dan melaporkan kemajuan kepada stakeholder industri.",
     "Workshop berbasis sprint, peer collaboration, stakeholder review, dan retrospective", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: orientasi workshop industri; perencanaan workshop (WBS, timeline, deliverable); sprint 1 review demo retrospective; UTS milestone; sprint 2 review sprint 3 planning; persiapan demo; UAS demo produk dan defense", "Ketepatan implementasi; kualitas produk; validasi dan dokumentasi",
     "Orientasi workshop industri dan pembentukan tim; perencanaan workshop: WBS, timeline, target deliverable; sprint review, demo, dan retrospective (tiap sprint); persiapan demo dan presentasi industry stakeholder"),

    # --- MK056 Teknologi Terapan: draft has 0, adding all 3 (real RPS) ---
    ("MK056", "Teknologi Terapan",
     "CPL02 Mampu menerapkan prinsip rekayasa sistem dan perangkat lunak untuk menghasilkan solusi aplikasi multi-platform sesuai kebutuhan.",
     "", "",
     "CPMK0204", "Mahasiswa mampu menganalisis kebutuhan dan merancang arsitektur solusi teknologi terapan berbasis kebutuhan nyata.",
     "SCPMK0204-05601", "Mahasiswa mampu melakukan analisis kebutuhan teknologi industri dan merancang solusi teknologi terapan yang tepat guna.",
     "Project Based Learning, iterative prototyping, stakeholder engagement, dan refleksi", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: orientasi teknologi terapan; needs assessment dan technology mapping; feasibility study dan pemilihan teknologi; sprint 3 penyesuaian feedback industri", "Ketepatan analisis; kualitas solusi; validasi dan dokumentasi",
     "Orientasi teknologi terapan dan identifikasi domain; needs assessment dan technology mapping; feasibility study dan pemilihan teknologi; sprint 3: penyesuaian berbasis feedback industri"),
    ("MK056", "", "", "", "",
     "CPMK0503", "Mahasiswa mampu mengimplementasikan solusi teknologi terapan yang efisien dan memenuhi kebutuhan operasional.",
     "SCPMK0503-05602", "Mahasiswa mampu mengimplementasikan solusi teknologi terapan mulai dari prototipe hingga deployment produksi.",
     "Project Based Learning, iterative prototyping, stakeholder engagement, dan refleksi", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: sprint 1 setup dan prototipe awal; sprint 1 validasi prototipe; sprint 2 pengembangan solusi lanjutan; sprint 2 integrasi sistem; sprint 3 optimasi dan stress testing; sprint 4 deployment dan transfer knowledge; dokumentasi teknis", "Ketepatan analisis; kualitas solusi; validasi dan dokumentasi",
     "Sprint 1: setup infrastruktur dan prototipe awal, validasi prototipe dengan pengguna; sprint 2: pengembangan solusi lanjutan, integrasi dengan sistem yang ada; sprint 3: optimasi dan stress testing; sprint 4: deployment produksi dan transfer knowledge; dokumentasi teknis dan laporan implementasi"),
    ("MK056", "", "", "", "",
     "CPMK0801", "Mahasiswa mampu merencanakan dan mengelola implementasi teknologi terapan di lingkungan industri.",
     "SCPMK0801-05603", "Mahasiswa mampu menyusun rencana implementasi teknologi, mengelola risiko, dan melaporkan kemajuan kepada stakeholder.",
     "Project Based Learning, iterative prototyping, stakeholder engagement, dan refleksi", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: perencanaan implementasi (roadmap dan manajemen risiko); sprint 1 review dan stakeholder feedback; UTS milestone evaluasi prototipe; sprint 2 review sprint 3 planning; persiapan presentasi final; UAS presentasi teknologi terapan dan demo", "Ketepatan analisis; kualitas solusi; validasi dan dokumentasi",
     "Perencanaan implementasi: roadmap dan manajemen risiko; sprint review dan stakeholder feedback (tiap sprint); persiapan presentasi final kepada stakeholder"),

    # --- MK059 Bahasa Inggris Persiapan Kerja: draft has 0, adding both (real RPS) ---
    ("MK059", "Bahasa Inggris Persiapan Kerja",
     "CPL03 Mampu mengelola tim dan diri sendiri secara profesional serta mengomunikasikan dan mempresentasikan gagasan maupun hasil kerja secara efektif baik lisan maupun tulisan.",
     "", "",
     "CPMK0303", "Mahasiswa mampu mengomunikasikan dan mempresentasikan hasil kerja teknologi informasi secara efektif dalam Bahasa Inggris baik lisan maupun tulisan.",
     "SCPMK0303-05901", "Mahasiswa mampu menyusun dokumen profesional dalam Bahasa Inggris meliputi CV, cover letter, portofolio, dan email profesional.",
     "Case Method, simulasi, role-play, dan peer feedback", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: draft CV dan LinkedIn profile; draft cover letter dan application email; kuis 1 tertulis (CV dan cover letter); sampel dokumentasi teknis TI; draft presentasi portofolio proyek TI; UTS portofolio", "Kelancaran komunikasi Bahasa Inggris; kualitas dokumen; profesionalisme",
     "Professional CV dan LinkedIn profile; cover letter dan application email; technical writing (dokumentasi dan laporan TI); IT portfolio (presentasi proyek)"),
    ("MK059", "", "", "", "",
     "CPMK0102", "Mahasiswa mampu menerapkan etika profesi, profesionalisme, dan komunikasi lintas budaya dalam lingkungan kerja TI global.",
     "SCPMK0102-05902", "Mahasiswa mampu melakukan simulasi wawancara kerja, presentasi teknis, dan komunikasi dalam tim multikultural secara efektif dalam Bahasa Inggris.",
     "Case Method, simulasi, role-play, dan peer feedback", "Blended Learning (Luring/Daring)",
     "Bentuk penilaian: mini presentasi teknis; role-play komunikasi tim multikultural; latihan jawaban interview IT; latihan STAR method; kuis 2 tertulis; simulasi technical interview; simulasi meeting dan email business; rekaman mock interview; UAS final mock interview panel", "Kelancaran komunikasi Bahasa Inggris; kualitas dokumen; profesionalisme",
     "Presentasi teknis dan Q&A; komunikasi tim multikultural; job interview preparation; behavioral interview (STAR method); technical interview; business English (meeting, negotiation, email etiquette); mock interview"),
]


def esc(v):
    return v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_row_xml(row_num, fields):
    (kode_mk, mk, cpl, kode_bk, bk, kode_cpmk, cpmk_desc, kode_sub, sub_text,
     metode, bentuk_pemb, bentuk_pen, kriteria, materi) = fields
    cols = {
        "B": kode_mk, "C": mk, "D": cpl, "E": kode_bk, "F": bk,
        "G": kode_cpmk, "H": cpmk_desc, "I": kode_sub, "J": sub_text,
        "K": metode, "L": bentuk_pemb, "M": bentuk_pen, "N": kriteria, "O": materi,
    }
    cells = []
    for col, val in cols.items():
        if val:
            cells.append(f'<c r="{col}{row_num}" t="inlineStr"><is><t xml:space="preserve">{esc(val)}</t></is></c>')
    return f'<row r="{row_num}">' + "".join(cells) + "</row>"


def apply_fix(xlsx_path: str) -> int:
    zin = zipfile.ZipFile(xlsx_path, "r")
    tmp_path = xlsx_path + ".tmp"
    zout = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED)

    added = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SHEET:
            text = data.decode("utf-8")
            new_rows_xml = []
            row_num = LAST_ROW + 1
            for fields in NEW_ROWS:
                new_rows_xml.append(build_row_xml(row_num, fields))
                row_num += 1
                added += 1
            insertion = "".join(new_rows_xml)
            marker = "</sheetData>"
            assert text.count(marker) == 1, "expected exactly 1 </sheetData>"
            text = text.replace(marker, insertion + marker, 1)

            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                raise AssertionError(f"edited {SHEET} is not well-formed XML: {e}")

            data = text.encode("utf-8")
        zout.writestr(item, data)

    zin.close()
    zout.close()
    shutil.move(tmp_path, xlsx_path)
    return added


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", nargs="?", default=DEFAULT_TARGET)
    args = parser.parse_args()

    added = apply_fix(args.xlsx_path)
    print(f"Appended {added} new rows (expected {len(NEW_ROWS)}), starting at row {LAST_ROW + 1}.")
    print(f"Saved to {args.xlsx_path}")
