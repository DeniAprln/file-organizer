# Decision Log — File Organizer

---

## [2026-06-21] Penanganan file dengan nama collision

**Konteks:**
Saat memindahkan file ke folder kategori, ada kemungkinan nama file
sudah ada di folder tujuan (misalnya dua file `laporan.pdf` yang
dipindahkan di waktu berbeda). Ini risiko #2 yang sudah dicatat di
pre-project.md.

**Opsi yang dipertimbangkan:**

1. **Overwrite (timpa file lama)**
   - Pro: paling sederhana, tidak perlu logic tambahan
   - Con: berisiko menghapus data tanpa sepengetahuan user — bertentangan
     langsung dengan success metric "tidak ada file yang hilang"

2. **Skip (lewati, jangan pindahkan)**
   - Pro: aman, tidak ada risiko kehilangan data
   - Con: file jadi tertinggal di folder asal, user harus pindahkan manual
     — mengurangi nilai otomasi yang jadi tujuan project ini

3. **Rename otomatis dengan suffix angka** (foto.jpg -> foto_1.jpg)
   - Pro: aman (tidak menimpa), dan tetap otomatis (tidak ada file
     tertinggal)
   - Con: bisa menghasilkan banyak file bernomor kalau dijalankan
     berkali-kali di folder yang sama

**Keputusan:** Opsi 3 — rename otomatis dengan suffix angka

**Alasan:**
Prioritas utama project ini adalah keamanan data (lihat success metric),
tapi tetap mempertahankan sifat otomatis yang jadi alasan project ini
dibuat. Skip (opsi 2) mengkhianati tujuan "otomatisasi", sedangkan
overwrite (opsi 1) terlalu berisiko untuk file pengguna.

**Trade-off yang diterima:**
Kalau script dijalankan berulang kali di folder yang sama tanpa membersihkan
hasil sebelumnya, akan muncul banyak file bernomor (`_1`, `_2`, dst).
Ini dianggap acceptable karena lebih aman daripada kehilangan data,
dan masih bisa diberesi oleh user.

---

## [2026-06-21] Tidak menggunakan library eksternal untuk versi MVP

**Konteks:**
Python punya banyak library pihak ketiga untuk file management (misalnya
`send2trash` untuk recycle bin, atau `watchdog` untuk monitoring folder).
Perlu diputuskan apakah memakai itu di versi pertama atau tidak.

**Opsi yang dipertimbangkan:**

1. **Pakai library eksternal sejak awal**
   - Pro: fitur lebih kaya (misalnya bisa undo via recycle bin)
   - Con: menambah dependency, dan project ini juga untuk latihan
     fundamental Python (lihat tech stack di pre-project.md)

2. **Built-in only (`os`, `shutil`, `pathlib`)**
   - Pro: tidak perlu `pip install`, lebih mudah dijalankan siapa pun,
     fokus ke logic dasar dulu
   - Con: tidak ada fitur undo otomatis ke recycle bin

**Keputusan:** Opsi 2 — built-in only untuk versi MVP

**Alasan:**
Sesuai scope yang sudah ditentukan di pre-project.md, fokus versi pertama
adalah logic yang benar, bukan fitur lengkap. Built-in library juga
membuat setup project ini nol-konfigurasi bagi siapa pun yang clone repo.

**Trade-off yang diterima:**
Tidak ada fitur "undo ke recycle bin" — kalau user salah jalankan,
harus pindahkan manual kembali. Ini sudah dicatat sebagai Known
Limitation di README.
