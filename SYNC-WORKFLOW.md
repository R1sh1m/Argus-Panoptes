# Team Sync Workflow (4 laptops, all on `main`)

One script, same on Windows + Mac. Run it before and after every work session
so everyone stays on the same page.

## 1. One-time setup (each teammate, on their own laptop)

```bash
# Mac
git clone https://github.com/R1sh1m/Argus-Panoptes.git
cd Argus-Panoptes
python3 tools/sync.py install-hooks

# Windows (PowerShell)
git clone https://github.com/R1sh1m/Argus-Panoptes.git
cd Argus-Panoptes
python tools/sync.py install-hooks
```

`install-hooks` copies `tools/githooks/pre-commit` + `pre-push` into your
local `.git/hooks/` (that folder is per-clone, never pushed — hence the
installer). Re-run it after any hook update.

Optional but recommended (makes `git pull` fast-forward-only on `main`):

```bash
git config pull.ff only
```

## 2. Daily use (everyone, every session)

```bash
# BEFORE working — pulls latest, autostashes dirty files, restores them after
python tools/sync.py start        # Mac: python3 tools/sync.py start

# ... work, then commit often ...
git add -A
git commit -m "what you changed"

# AFTER working — pushes your commits (refuses if you're behind)
python tools/sync.py end

# Anytime — check if you're in sync
python tools/sync.py status
```

What each command does:

| Command | Does |
|---|---|
| `start` | `fetch --prune` → autostash dirty files (incl. untracked) → `pull --ff-only origin main` → pop stash. Fails loudly if `main` diverged, with recovery steps. Works offline (prints last-fetch time, exits 0). |
| `end` | `fetch` → warns about uncommitted files → blocks push if behind → asks confirmation → `push origin main`. |
| `status` | Branch, ahead/behind vs `origin/main`, dirty files, last 5 local + remote commits. |
| `install-hooks` | Installs guards into `.git/hooks/`. |

Flags: `start --no-stash` (fail if dirty instead of autostashing),
`end --yes` (skip push confirmation).

## 3. Rules for all-on-`main` (please follow)

1. `start` before you touch files. `end` (or at least push) before you close the laptop.
2. Small, frequent commits + pushes beat one giant push — fewer conflicts.
3. Never `git push --force` on `main`. If `start` reports "diverged", merge — don't reset.
4. Commit messages: short verb, e.g. `fix flood filter threshold`, `docs add coupon log`.

## 4. Guards (automatic)

- `pre-commit`: blocks `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.DS_Store`, `*.log`, `report.json`. Large files (>10MB) only warn — research PDFs are legitimately big.
- `pre-push`: blocks pushing while behind `origin/main` ("run `start` first").
- `.gitignore` intentionally unchanged per team choice.

## 5. If something goes wrong

- **Diverged main** (`start` fails on `pull --ff-only`): `git log --graph --oneline HEAD...origin/main`, then `git merge origin/main`, resolve, test, `end`.
- **Stash pop conflicted** (autostash kept): `git status`, fix files, `git stash list` → verify → `git stash drop` only when files look right.
- **Push rejected**: someone pushed first — `start`, then `end` again.
- **Offline / Mac on hotspot**: script prints last-fetch time and continues; push later with `end`.
- **Forgot hooks on a new clone**: just run `install-hooks` — no re-clone needed.
