# Pre-Project — File Organizer

## Problem Statement

**Siapa yang punya masalah ini:**
Siapa pun yang sering download file — mahasiswa, pekerja, atau saya sendiri.
Folder `Downloads` jadi tempat campur aduk: PDF tugas, screenshot, installer,
file zip semua jadi satu.

**Masalah yang mereka hadapi:**
Susah cari file lama karena semua bercampur tanpa kategori. Mau cari 1 PDF
harus scroll lewat puluhan file lain yang tidak relevan.

**Seberapa sering mereka menghadapinya:**
Hampir tiap minggu — setiap kali download sesuatu baru, folder makin
berantakan, dan tidak pernah benar-benar dirapikan karena terasa membosankan.

**Kenapa solusi yang ada tidak cukup:**
Merapikan manual (drag satu-satu ke folder) memungkinkan tapi memakan waktu
dan tidak pernah dilakukan secara rutin. Tidak ada habit untuk itu.

**Definisi sukses (measurable):**
Script bisa memindahkan minimal 5 tipe file berbeda (PDF, gambar, spreadsheet,
installer, arsip) ke folder yang sesuai, tanpa ada file yang hilang atau
tertimpa, dan bisa dijalankan oleh orang lain dalam kurang dari 2 menit
setelah clone repo.

---

## Target User Spesifik

Bukan "semua orang" — fokus ke: **mahasiswa/pekerja individu yang punya
satu folder Downloads pribadi dan ingin merapikannya sendiri**, bukan
admin sistem yang mengelola banyak komputer/server.

---

## Success Metric

- ✅ Berhasil mengkategorikan minimal 7 tipe ekstensi umum
- ✅ Tidak ada file yang tertimpa (collision ditangani)
- ✅ Ada mode simulasi (dry-run) sebelum eksekusi nyata
- ✅ Bisa dijalankan tanpa install dependency tambahan

---

## Scope

### ✅ IN SCOPE (akan dibangun)
- [ ] Scan satu folder (non-rekursif)
- [ ] Kategorikan file berdasarkan ekstensi
- [ ] Mode dry-run (simulasi tanpa eksekusi)
- [ ] Penanganan collision nama file

### ❌ OUT OF SCOPE (dan kenapa)

| Fitur                          | Alasan tidak dibangun (versi ini)                        |
|---------------------------------|-----------------------------------------------------------|
| GUI                             | Fokus dulu ke logic yang benar; GUI nambah kompleksitas   |
| Scan rekursif ke subfolder      | Risiko mengacak-acak struktur folder yang sudah rapi      |
| Jalan otomatis di background    | Butuh scheduler terpisah; bukan masalah inti yang ingin diselesaikan dulu |
| Sortir berdasarkan tanggal      | Satu masalah dulu (tipe file) sebelum nambah dimensi lain |

---

## Tech Stack + Alasan

**Python 3 — hanya built-in library (`os`, `shutil`, `pathlib`)**

Alasan: ini project pertama untuk belajar fundamental Python tanpa
ketergantungan eksternal. Tidak butuh kecepatan tinggi atau concurrency,
jadi tidak perlu library tambahan. `pathlib` dipilih dibanding `os.path`
karena API-nya lebih modern dan mudah dibaca.

---

## 3 Risiko Utama

1. **Salah pindah/hapus file penting**
   → Mitigasi: testing di folder dummy dulu, bukan folder asli. Sediakan
   mode `--dry-run` supaya bisa preview sebelum eksekusi nyata.

2. **File dengan nama sama tertimpa saat dipindah**
   → Mitigasi: cek collision sebelum memindahkan, tambahkan suffix angka
   kalau nama sudah dipakai di folder tujuan.

3. **Tipe file yang tidak dikenali (ekstensi aneh/tidak ada di daftar)**
   → Mitigasi: sediakan folder default "Others" sebagai fallback, supaya
   tidak ada file yang gagal diproses atau menyebabkan error.
