"""
Automatic File Organizer
------------------------
See docs/pre-project.md for the problem statement and full scope.

Status: can actually move files, with --dry-run mode
for safe simulation before execution.
"""

import sys
import shutil
from pathlib import Path

# Extension mapping -> category folder name.
# Separated into a dictionary (instead of long if/elif) so it's easy
# to add without changing the logic in get_category().
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
    Determine the category folder from the file extension.
    Unknown extensions go to "Others" (default fallback),
    according to risk mitigation #3 in pre-project.md.
    """
    extension = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def resolve_collision(destination: Path) -> Path:
    """
    If a file with the same name already exists in the destination folder, do not overwrite the old file.
    Add a number behind the file name: photo.jpg -> photo_1.jpg

    See docs/decision-log.md for the reason why this approach was chosen
    instead of skip or overwrite.
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
    Main function: scan folder, then move each file to a subfolder
    according to its category.

    dry_run=True means only SIMULATION (print what WILL happen,
    without actually moving the files). This is important for safe testing
    before running on the real folder — according to risk mitigation #1
    in pre-project.md.
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return

    if not folder.is_dir():
        print(f"❌ This path is not a folder: {folder}")
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

    print(f"\nDone. {moved_count} files processed.")
    if dry_run:
        print("(This is only a simulation — run without --dry-run for real execution)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python organizer.py <folder_path> [--dry-run]")
        sys.exit(1)

    target_path = sys.argv[1]
    is_dry_run = "--dry-run" in sys.argv

    organize_folder(target_path, dry_run=is_dry_run)
