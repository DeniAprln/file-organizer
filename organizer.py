"""
File Organizer Otomatis
------------------------
Lihat docs/pre-project.md untuk problem statement dan scope lengkap.

Status: bisa memindahkan file secara nyata, dengan mode --dry-run
untuk simulasi aman sebelum eksekusi.
"""

import sys
import shutil
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


def resolve_collision(destination: Path) -> Path:
    """
    Kalau nama file sudah ada di folder tujuan, jangan menimpa file lama.
    Tambahkan angka di belakang nama file: foto.jpg -> foto_1.jpg

    Lihat docs/decision-log.md untuk alasan kenapa pendekatan ini dipilih
    dibanding skip atau overwrite.
    """
    if not destination.exists():
        return destination

    counter = 1
    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent

    new_destination = parent / f"{stem}_{counter}{suffix}"
    while new_destination.exists():
        counter += 1
        new_destination = parent / f"{stem}_{counter}{suffix}"

    return new_destination


def organize_folder(folder_path: str, dry_run: bool = False) -> None:
    """
    Fungsi utama: scan folder, lalu pindahkan tiap file ke subfolder
    sesuai kategorinya.

    dry_run=True artinya cuma SIMULASI (print apa yang AKAN terjadi,
    tanpa benar-benar memindahkan file). Ini penting untuk testing aman
    sebelum dijalankan ke folder asli — sesuai mitigasi risiko #1
    di pre-project.md.
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"❌ Folder tidak ditemukan: {folder}")
        return

    if not folder.is_dir():
        print(f"❌ Path ini bukan folder: {folder}")
        return

    moved_count = 0

    for item in folder.iterdir():
        if item.is_dir():
            continue

        category = get_category(item.suffix)
        target_folder = folder / category
        destination = target_folder / item.name
        destination = resolve_collision(destination)

        if dry_run:
            print(f"[DRY RUN] {item.name} -> {category}/{destination.name}")
        else:
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            print(f"✅ {item.name} -> {category}/{destination.name}")

        moved_count += 1

    print(f"\nSelesai. {moved_count} file diproses.")
    if dry_run:
        print("(Ini cuma simulasi — jalankan tanpa --dry-run untuk eksekusi nyata)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cara pakai: python organizer.py <folder_path> [--dry-run]")
        sys.exit(1)

    target_path = sys.argv[1]
    is_dry_run = "--dry-run" in sys.argv

    organize_folder(target_path, dry_run=is_dry_run)
