"""
File Organizer Otomatis
------------------------
Lihat docs/pre-project.md untuk problem statement dan scope lengkap.

Status: sudah bisa mengkategorikan file berdasarkan ekstensi.
Belum memindahkan file secara nyata (masih tahap kategorisasi saja).
"""

import sys
from pathlib import Path

# Mapping ekstensi -> nama folder kategori.
# Dipisah jadi dictionary (bukan if/elif panjang) supaya gampang
# ditambah tanpa mengubah logic di get_category().
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv"],
}


def get_category(extension: str) -> str:
    """
    Tentukan kategori folder dari ekstensi file.
    Ekstensi yang tidak dikenal masuk ke "Others" (fallback default),
    sesuai mitigasi risiko #3 di pre-project.md.
    """
    extension = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def organize_folder(folder_path: str, dry_run: bool = False) -> None:
    """
    Fungsi utama. Saat ini sudah bisa mengkategorikan tiap file,
    tapi BELUM benar-benar memindahkannya (lihat print di bawah).
    Pemindahan nyata + dry-run mode akan ditambahkan di commit berikutnya.
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"❌ Folder tidak ditemukan: {folder}")
        return

    if not folder.is_dir():
        print(f"❌ Path ini bukan folder: {folder}")
        return

    for item in folder.iterdir():
        if item.is_dir():
            continue
        category = get_category(item.suffix)
        print(f"{item.name} -> akan masuk kategori: {category}")
    # TODO: pemindahan file nyata + dry-run mode (commit berikutnya)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cara pakai: python organizer.py <folder_path> [--dry-run]")
        sys.exit(1)

    target_path = sys.argv[1]
    is_dry_run = "--dry-run" in sys.argv

    organize_folder(target_path, dry_run=is_dry_run)
