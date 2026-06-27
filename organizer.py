"""
Automatic File Organizer
------------------------
See docs/pre-project.md for the problem statement and full scope.

Status: can actually move files, with --dry-run mode
for safe simulation before execution.
Logging: supports --log flag to write a timestamped log file to logs/.
Config: file categories are loaded from config.json (next to this script),
so new file types can be added without editing the code.
Undo: every live run saves a record to undo_log.json; pass --undo to
reverse the most recent session without touching any other files.
"""

import sys
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path

# Path to the config file (sits next to this script).
CONFIG_PATH = Path(__file__).parent / "config.json"

# Undo log: records every move made so the last session can be reversed.
# Each entry is { "from": "<original path>", "to": "<destination path>" }.
UNDO_LOG_PATH = Path(__file__).parent / "undo_log.json"


def load_categories() -> dict:
    """
    Load the extension-to-category mapping from config.json.

    The file must live next to organizer.py and follow this structure:
        { "categories": { "CategoryName": [".ext1", ".ext2"] } }

    Raises FileNotFoundError if config.json is missing, and
    KeyError/ValueError if the JSON structure is invalid — both
    with a clear message so the user knows exactly what to fix.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"❌ Config file not found: {CONFIG_PATH}\n"
            "   Please create config.json next to organizer.py.\n"
            "   See README.md for the expected format."
        )

    with CONFIG_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    if "categories" not in data or not isinstance(data["categories"], dict):
        raise ValueError(
            f"❌ Invalid config.json: expected a top-level 'categories' object.\n"
            f"   Example: {{ \"categories\": {{ \"Images\": [\".jpg\", \".png\"] }} }}"
        )

    return data["categories"]


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


def get_category(extension: str, categories: dict) -> str:
    """
    Determine the category folder from the file extension.

    categories is the dict loaded from config.json.
    Unknown extensions go to "Others" (default fallback),
    according to risk mitigation #3 in pre-project.md.
    """
    extension = extension.lower()
    for category, extensions in categories.items():
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


def save_undo_log(moves: list) -> None:
    """
    Persist the list of moves from the current session to undo_log.json,
    replacing any previous session's data.

    Each item in `moves` is a dict with keys "from" and "to" (absolute
    string paths), so the undo step can reverse the move exactly.

    Overwriting the previous log on every live run is intentional: only
    the most recent session can be undone, which keeps the logic simple
    and prevents the log from growing unbounded.
    See docs/decision-log.md for the full rationale.
    """
    data = {
        "session_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "moves": moves,
    }
    with UNDO_LOG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def undo_last_session(logger: logging.Logger) -> None:
    """
    Reverse the moves recorded in undo_log.json.

    Each file is moved back from its destination to its original path.
    If the original location already has a file with the same name
    (an edge case where the user put a new file there manually),
    resolve_collision() is used so nothing is overwritten.

    After a successful undo the log file is deleted — running --undo
    twice in a row would have nothing to reverse.
    """
    if not UNDO_LOG_PATH.exists():
        logger.error(
            "❌ No undo log found. Run the organizer at least once (without --dry-run) first."
        )
        return

    with UNDO_LOG_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    moves = data.get("moves", [])
    session_time = data.get("session_time", "unknown")

    if not moves:
        logger.info("ℹ️  Undo log is empty — nothing to reverse.")
        UNDO_LOG_PATH.unlink()
        return

    logger.info(f"↩️  Undoing session from {session_time} ({len(moves)} moves)...")

    restored_count = 0
    failed_count = 0

    for move in reversed(moves):
        src = Path(move["to"])
        dst = Path(move["from"])

        if not src.exists():
            logger.warning(f"⚠️  Skipped (file not found at destination): {src}")
            failed_count += 1
            continue

        # Ensure the original folder still exists (it should, but be safe).
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst = resolve_collision(dst)

        shutil.move(str(src), str(dst))
        logger.info(f"↩️  {src.name} -> {dst}")
        restored_count += 1

    logger.info(f"\nUndo complete. {restored_count} restored, {failed_count} skipped.")

    # Remove the log so a second --undo doesn't try to reverse nothing.
    UNDO_LOG_PATH.unlink()
    logger.info("🗑️  Undo log cleared.")


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

    Categories are loaded from config.json at the start of each run,
    so changes to the config take effect immediately without restarting.

    Every live run writes a move record to undo_log.json so the session
    can be reversed with --undo.
    """
    # Fallback to a basic logger if called without one (e.g. in tests/imports)
    if logger is None:
        logger = logging.getLogger("organizer")
        if not logger.handlers:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    # Load categories from config.json — fail early with a clear message.
    try:
        categories = load_categories()
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        logger.error(str(exc))
        return

    logger.info(f"📋 Loaded {len(categories)} categories from {CONFIG_PATH.name}")

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
    # Accumulate move records for undo_log.json (live mode only).
    move_records = []

    for item in folder.iterdir():
        if item.is_dir():
            continue

        category = get_category(item.suffix, categories)
        target_folder = folder / category
        destination = target_folder / item.name
        destination = resolve_collision(destination)

        if dry_run:
            logger.info(f"[DRY RUN] {item.name} -> {category}/{destination.name}")
        else:
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            logger.info(f"✅ {item.name} -> {category}/{destination.name}")
            # Record the exact paths so the move can be reversed.
            move_records.append({"from": str(item), "to": str(destination)})

        moved_count += 1

    logger.info(f"\nDone. {moved_count} files processed.")
    if dry_run:
        logger.info("(This is only a simulation — run without --dry-run for real execution)")
    else:
        # Persist the undo log only after a successful live run.
        save_undo_log(move_records)
        logger.info(f"💾 Undo log saved to {UNDO_LOG_PATH.name} (run with --undo to reverse)")

    logger.info(f"--- Session end ---")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python organizer.py <folder_path> [--dry-run] [--log]")
        print("       python organizer.py --undo [--log]")
        sys.exit(1)

    is_undo = "--undo" in sys.argv
    is_logging = "--log" in sys.argv

    app_logger = setup_logging(log_to_file=is_logging)

    if is_undo:
        # --undo mode: reverse last session; no folder path required.
        undo_last_session(logger=app_logger)
    else:
        target_path = sys.argv[1]
        is_dry_run = "--dry-run" in sys.argv
        organize_folder(target_path, dry_run=is_dry_run, logger=app_logger)
