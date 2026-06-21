"""
File Organizer Otomatis
------------------------
Lihat docs/pre-project.md untuk problem statement dan scope lengkap.

Status: skeleton awal — baru menerima argumen folder, belum ada
logic kategorisasi.
"""

import sys
from pathlib import Path


def organize_folder(folder_path: str, dry_run: bool = False) -> None:
    """
    Fungsi utama. Saat ini baru validasi folder, logic pemindahan
    file akan ditambahkan di commit berikutnya.
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"❌ Folder tidak ditemukan: {folder}")
        return

    if not folder.is_dir():
        print(f"❌ Path ini bukan folder: {folder}")
        return

    print(f"Folder valid: {folder}")
    # TODO: scan isi folder dan kategorikan file (commit berikutnya)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cara pakai: python organizer.py <folder_path> [--dry-run]")
        sys.exit(1)

    target_path = sys.argv[1]
    is_dry_run = "--dry-run" in sys.argv

    organize_folder(target_path, dry_run=is_dry_run)
