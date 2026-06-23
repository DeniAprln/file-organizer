# File Organizer

> A simple Python script that automatically organizes messy folders (e.g., Downloads) by moving each file into a subfolder according to its type.

The complete thought process of this project (problem statement, scope, technical decisions) is documented in the [`docs/`](./docs) folder and can be traced through the git history — not just the finished code.

## The Problem

Folders like `Downloads` often become digital dumping grounds — PDFs, images, installers, and documents all mixed together. Organizing them manually is tedious and usually never actually done on a regular basis.

## How It Works

Run the script, point it to the folder you want to organize, and every file will automatically be moved to a subfolder based on its type.

**Before:**
```
Downloads/
├── report.pdf
├── photo.jpg
├── music.mp3
├── data.xlsx
├── installer.exe
└── archive.zip
```

**After:**
```
Downloads/
├── Documents/report.pdf
├── Images/photo.jpg
├── Audio/music.mp3
├── Spreadsheets/data.xlsx
├── Installers/installer.exe
└── Archives/archive.zip
```

## Architecture

```
organizer.py
├── FILE_CATEGORIES      # extension mapping -> category folder name
├── setup_logging()      # configure terminal + optional file logger
├── get_category()       # determine category from file extension
├── resolve_collision()  # prevent file overwriting if name already exists
└── organize_folder()    # main function: scan folder then move files
```

**Key decisions** (full details in [`docs/decision-log.md`](./docs/decision-log.md)):
- **Collisions are handled with auto-rename**, not overwrite or skip — balancing data safety with the automated nature that is the goal of this project
- **No external dependencies** — intentionally built using only built-in Python to focus on basic logic and ease of setup

## Getting Started

```bash
git clone https://github.com/[username]/file-organizer
cd file-organizer

# Simulate first (does not move any files)
python organizer.py /path/to/folder --dry-run

# Real execution
python organizer.py /path/to/folder

# Real execution with file logging (saves a timestamped log to logs/)
python organizer.py /path/to/folder --log

# Combine dry-run + log (safest for first-time use)
python organizer.py /path/to/folder --dry-run --log
```

No external dependencies — Python 3.6+ is sufficient.

Log files are saved to `logs/organizer_YYYY-MM-DD_HH-MM-SS.log` in the same directory as the script.

## Project Documentation

- [`docs/pre-project.md`](./docs/pre-project.md) — problem statement, target user, scope, and risks identified before coding began
- [`docs/decision-log.md`](./docs/decision-log.md) — non-trivial technical decisions during development, complete with options considered

## Known Limitations

These are conscious trade-offs, not oversights:

- **Not recursive to subfolders** — only processes files at the designated folder level. Intentionally limited so as not to mess up already organized folder structures.
- **No automatic undo** — if run by mistake, must be moved back manually. See the decision log for reasons not to use a recycle bin library in this version.
- **Hardcoded extension categories** — adding new file types requires editing the code directly, there is no separate config file yet.

## What I'd Do Differently

If starting over:
1. Add a `config.json` file for categories — so it can be customized without editing the code

## Lessons Learned

- **Technical:** `pathlib` is much more convenient than `os.path` for path operations — less code, easier to read
- **Process:** writing a dry-run mode before actual moving logic makes testing much safer, because you can see the results without the risk of destroying data. Building features gradually (skeleton → categorization → moving → collision handling) also makes each bug easier to trace to the commit that caused it.
