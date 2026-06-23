# Decision Log — File Organizer

---

## [2026-06-22] Implementing file logging with the --log flag

**Context:**
After the MVP was complete, a file logging feature was added so that
activity history could be traced — as noted in "What I'd Do Differently"
in the README. A decision was needed on how to implement it without
breaking existing behavior.

**Options considered:**

1. **Replace all `print()` calls with `logging` and always write to a file**
   - Pro: a single, consistent output mechanism
   - Con: changes the default behavior (terminal output format may differ),
     and affects users who don't need logging at all

2. **Add `--log` as an optional flag with two separate handlers**
   - Pro: non-breaking — without the flag, behavior is identical to before.
     With the flag, terminal output stays the same (plain format), plus
     a file handler with per-line timestamps for history
   - Con: slightly more complex due to the two-handler setup

3. **Always write a log file automatically on every run**
   - Pro: history is always available without remembering to use a flag
   - Con: creates a `logs/` folder everywhere without the user asking for it;
     violates the "least surprise" principle for a CLI script

**Decision:** Option 2 — optional `--log` flag with two separate handlers

**Rationale:**
The top priority was not breaking existing behavior. Users who don't pass
`--log` experience no change whatsoever. Two handlers (StreamHandler for
the terminal, FileHandler for the file) allow different formats for
different needs: the terminal stays clean and concise, while the log file
is rich with per-line timestamps.

**Technical details:**
- Uses Python's built-in `logging` module — no new dependencies
- Log files are saved to `logs/organizer_YYYY-MM-DD_HH-MM-SS.log`
- The `logs/` directory is created automatically if it doesn't exist, and is excluded from git (`.gitignore`)
- Error messages (`❌`) are sent to `logger.error()`, info messages to `logger.info()`

**Trade-off accepted:**
If the user forgets to pass `--log`, no history is saved. This is considered
acceptable because it is better than creating unexpected side-effects.

---

## [2026-06-21] Handling files with name collisions

**Context:**
When moving files to a category folder, there is a chance that a file
with the same name already exists in the destination (e.g., two `report.pdf`
files moved at different times). This is risk #2 documented in pre-project.md.

**Options considered:**

1. **Overwrite (replace the existing file)**
   - Pro: simplest approach, no extra logic needed
   - Con: risks deleting data without the user's knowledge — directly
     contradicts the success metric "no files are lost"

2. **Skip (leave the file in place, don't move it)**
   - Pro: safe, no risk of data loss
   - Con: the file is left behind in the source folder and must be moved
     manually — undermines the automation goal of this project

3. **Auto-rename with a numeric suffix** (photo.jpg → photo_1.jpg)
   - Pro: safe (no overwriting) and still fully automatic (no files left behind)
   - Con: can produce many numbered files if the script is run repeatedly
     on the same folder

**Decision:** Option 3 — auto-rename with a numeric suffix

**Rationale:**
The top priority of this project is data safety (see the success metric),
while still preserving the automated nature that is the reason the project
exists. Skip (option 2) betrays the "automation" goal, while overwrite
(option 1) is too risky for the user's files.

**Trade-off accepted:**
If the script is run multiple times on the same folder without clearing
previous results, many numbered files (`_1`, `_2`, etc.) will accumulate.
This is considered acceptable because it is safer than losing data, and
the user can still clean them up manually.

---

## [2026-06-21] No external libraries for the MVP version

**Context:**
Python has many third-party libraries for file management (e.g., `send2trash`
for recycle bin support, or `watchdog` for folder monitoring). A decision
was needed on whether to use any of them in the first version.

**Options considered:**

1. **Use external libraries from the start**
   - Pro: richer features (e.g., undo via recycle bin)
   - Con: adds dependencies, and this project is also a practice exercise
     in Python fundamentals (see the tech stack in pre-project.md)

2. **Built-in only (`os`, `shutil`, `pathlib`)**
   - Pro: no `pip install` needed, easier for anyone to run, and keeps
     the focus on core logic first
   - Con: no automatic undo to the recycle bin

**Decision:** Option 2 — built-in only for the MVP version

**Rationale:**
In line with the scope defined in pre-project.md, the focus of the first
version is correct logic, not a full feature set. Using only built-in
libraries also makes this project zero-configuration for anyone who clones
the repo.

**Trade-off accepted:**
No "undo to recycle bin" feature — if the user runs the script by mistake,
files must be moved back manually. This has been noted as a Known Limitation
in the README.
