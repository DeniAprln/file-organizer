# Pre-Project — File Organizer

## Problem Statement

**Who has this problem:**
Anyone who regularly downloads files — students, workers, or myself.
The `Downloads` folder becomes a dumping ground: assignment PDFs, screenshots,
installers, and zip files all mixed together.

**The problem they face:**
Hard to find old files because everything is mixed without any category.
To find one PDF you have to scroll past dozens of other irrelevant files.

**How often they face it:**
Almost every week — every time something new is downloaded, the folder gets
messier, and it never actually gets organized because it feels too tedious.

**Why existing solutions aren't enough:**
Manual organization (dragging files one by one into folders) is possible
but time-consuming and never done consistently. There's no habit for it.

**Definition of success (measurable):**
The script can move at least 5 different file types (PDF, images, spreadsheets,
installers, archives) to the appropriate folder, with no files lost or
overwritten, and can be run by someone else in under 2 minutes after cloning
the repo.

---

## Specific Target User

Not "everyone" — focused on: **individual students or workers who have
one personal Downloads folder and want to organize it themselves**, not
system admins managing many computers or servers.

---

## Success Metric

- ✅ Successfully categorizes at least 7 common file extension types
- ✅ No files are overwritten (collisions are handled)
- ✅ A simulation mode (dry-run) is available before real execution
- ✅ Can be run without installing any additional dependencies

---

## Scope

### ✅ IN SCOPE (built)
- [x] Scan a single folder (non-recursive)
- [x] Categorize files by extension
- [x] Dry-run mode (simulation without execution)
- [x] File name collision handling
- [x] Customizable categories via external `config.json` — originally out of scope,
      added in v2 so new file types can be added without editing the code

### ❌ OUT OF SCOPE (and why)

| Feature                        | Reason not built (this version)                                     |
|--------------------------------|----------------------------------------------------------------------|
| GUI                            | Focus on correct logic first; a GUI adds complexity                  |
| Recursive scan into subfolders | Risk of disrupting folder structures that are already organized      |
| Auto-run in the background     | Requires a separate scheduler; not the core problem to solve first   |
| Sort by date                   | Solve one problem (file type) before adding another dimension        |
| ~~Hardcoded categories~~       | ~~Was a known limitation in v1~~ → resolved in v2 via `config.json` |

---

## Tech Stack + Rationale

**Python 3 — built-in libraries only (`sys`, `json`, `shutil`, `pathlib`, `logging`)**

Rationale: this is a first project to practice Python fundamentals without
external dependencies. No need for high speed or concurrency, so no
additional libraries are required. `pathlib` was chosen over `os.path`
because its API is more modern and easier to read. `json` was added in v2
to support reading the external `config.json` category mapping.

---

## 3 Main Risks

1. **Accidentally moving or deleting an important file**
   → Mitigation: test on a dummy folder first, not the real one. Provide
   a `--dry-run` mode so the result can be previewed before real execution.

2. **A file being overwritten by another with the same name during the move**
   → Mitigation: check for collisions before moving; add a numeric suffix
   if the name is already taken in the destination folder.

3. **Unrecognized file types (unusual or unlisted extensions)**
   → Mitigation: provide a default "Others" folder as a fallback, so no
   file fails to be processed or causes an error.
