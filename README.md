# File Organizer

> Script Python sederhana yang otomatis merapikan folder berantakan (misalnya Downloads) dengan memindahkan setiap file ke subfolder sesuai tipenya.

Proses berpikir lengkap project ini (problem statement, scope, keputusan teknis) didokumentasikan di folder [`docs/`](./docs) dan bisa ditelusuri lewat git history — bukan cuma kode jadi.

## The Problem

Folder seperti `Downloads` sering jadi tempat sampah digital — PDF, gambar, installer, dan dokumen semua tercampur jadi satu. Merapikannya secara manual itu membosankan dan biasanya tidak pernah benar-benar dilakukan secara rutin.

## How It Works

Jalankan script, tunjuk ke folder yang mau dirapikan, dan setiap file akan otomatis dipindahkan ke subfolder berdasarkan tipenya.

**Sebelum:**
```
Downloads/
├── laporan.pdf
├── foto.jpg
├── musik.mp3
├── data.xlsx
├── installer.exe
└── arsip.zip
```

**Sesudah:**
```
Downloads/
├── Documents/laporan.pdf
├── Images/foto.jpg
├── Audio/musik.mp3
├── Spreadsheets/data.xlsx
├── Installers/installer.exe
└── Archives/arsip.zip
```

## Architecture

```
organizer.py
├── FILE_CATEGORIES      # mapping ekstensi -> nama folder kategori
├── get_category()       # tentukan kategori dari ekstensi file
├── resolve_collision()  # cegah file tertimpa jika nama sudah ada
└── organize_folder()    # fungsi utama: scan folder lalu pindahkan file
```

**Key decisions** (detail lengkap di [`docs/decision-log.md`](./docs/decision-log.md)):
- **Collision ditangani dengan rename otomatis**, bukan overwrite atau skip — menyeimbangkan keamanan data dengan sifat otomatis yang jadi tujuan project ini
- **Tidak ada dependency eksternal** — sengaja dibuat hanya dengan built-in Python untuk fokus ke logic dasar dan kemudahan setup

## Getting Started

```bash
git clone https://github.com/[username]/file-organizer
cd file-organizer

# Simulasi dulu (tidak memindahkan file apa pun)
python organizer.py /path/ke/folder --dry-run

# Eksekusi beneran
python organizer.py /path/ke/folder
```

Tidak ada dependency eksternal — cukup Python 3.6+.

## Project Documentation

- [`docs/pre-project.md`](./docs/pre-project.md) — problem statement, target user, scope, dan risiko yang diidentifikasi sebelum coding dimulai
- [`docs/decision-log.md`](./docs/decision-log.md) — keputusan teknis non-trivial selama development, lengkap dengan opsi yang dipertimbangkan

## Known Limitations

Ini trade-off yang disadari, bukan kelalaian:

- **Tidak rekursif ke subfolder** — hanya memproses file di level folder yang ditunjuk. Sengaja dibatasi supaya tidak mengacak-acak struktur folder yang sudah rapi.
- **Tidak ada undo otomatis** — kalau salah jalankan, harus dipindahkan manual kembali. Lihat decision log soal alasan tidak memakai library recycle bin di versi ini.
- **Kategori ekstensi hardcoded** — menambah tipe file baru harus edit kode langsung, belum ada file config terpisah.

## What I'd Do Differently

Jika mulai ulang:
1. Tambahkan file `config.json` untuk kategori — supaya bisa dikustomisasi tanpa edit kode
2. Tambahkan logging ke file (bukan cuma print ke terminal) — supaya ada riwayat yang bisa ditelusuri atau di-undo

## Lessons Learned

- **Teknis:** `pathlib` jauh lebih nyaman dibanding `os.path` untuk operasi path — lebih sedikit kode, lebih mudah dibaca
- **Proses:** menulis dry-run mode sebelum logic pemindahan nyata membuat testing jauh lebih aman, karena bisa lihat hasil tanpa risiko merusak data. Membangun fitur secara bertahap (skeleton → kategorisasi → pemindahan → collision handling) juga membuat tiap bug lebih mudah dilacak ke commit penyebabnya.
