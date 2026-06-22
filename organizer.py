"""
Automatic File Organizer
------------------------
See docs/pre-project.md for the problem statement and full scope.

Status: can actually move files, with --dry-run mode
for safe simulation before execution.
Logging: supports --log flag to write a timestamped log file to logs/.
"""

import sys
import shutil
import logging
from datetime import datetime
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


def setup_logging(log_to_file: bool) -> logging.Logger:
    """
    Configure and return the application logger.

    Always attaches a StreamHandler so terminal output looks exactly
    like the old print() calls (plain message, no level prefix).
    When log_to_file=True, also attaches a FileHandler that writes to
    logs/organizer_<timestamp>.log with full timestamp + level info,
    creating the logs/ directory if it does not yet exist.
    """
    logger = logging.getLogger("organizer")
    logger.setLevel(logging.DEBUG)

    # --- Terminal handler: plain message only, same feel as print() ---
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stream_handler)

    # --- File handler: only when --log flag is passed ---
    if log_to_file:
        logs_dir = Path(__file__).parent / "logs"
        logs_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = logs_dir / f"organizer_{timestamp}.log"

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

        # Let the user know where the log is being written
        logger.info(f"Logging to: {log_path}")

    return logger


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


def organize_folder(
    folder_path: str, dry_run: bool = False, logger: logging.Logger = None
) -> None:
    """
    Main function: scan folder, then move each file to a subfolder
    according to its category.

    dry_run=True means only SIMULATION (print what WILL happen,
    without actually moving the files). This is important for safe testing
    before running on the real folder — according to risk mitigation #1
    in pre-project.md.

    logger is the configured Logger instance from setup_logging(). When
    file logging is enabled it will also write every message to the log file.
    """
    # Fallback to a basic logger if called without one (e.g. in tests/imports)
    if logger is None:
        logger = logging.getLogger("organizer")
        if not logger.handlers:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    folder = Path(folder_path)

    if not folder.exists():
        logger.error(f"❌ Folder not found: {folder}")
        return

    if not folder.is_dir():
        logger.error(f"❌ This path is not a folder: {folder}")
        return

    mode_label = "DRY RUN" if dry_run else "LIVE"
    logger.info(f"--- Session start | folder: {folder} | mode: {mode_label} ---")

    moved_count = 0

    for item in folder.iterdir():
        if item.is_dir():
            continue

        category = get_category(item.suffix)
        target_folder = folder / category
        destination = target_folder / item.name
        destination = resolve_collision(destination)

        if dry_run:
            logger.info(f"[DRY RUN] {item.name} -> {category}/{destination.name}")
        else:
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            logger.info(f"✅ {item.name} -> {category}/{destination.name}")

        moved_count += 1

    logger.info(f"\nDone. {moved_count} files processed.")
    if dry_run:
        logger.info("(This is only a simulation — run without --dry-run for real execution)")

    logger.info(f"--- Session end ---")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python organizer.py <folder_path> [--dry-run] [--log]")
        sys.exit(1)

    target_path = sys.argv[1]
    is_dry_run = "--dry-run" in sys.argv
    is_logging = "--log" in sys.argv

    app_logger = setup_logging(log_to_file=is_logging)
    organize_folder(target_path, dry_run=is_dry_run, logger=app_logger)
