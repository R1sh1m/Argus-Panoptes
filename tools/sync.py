#!/usr/bin/env python3
"""Argus-Panoptes team sync — one script for Windows + Mac.

Everyone clones the same repo (separate laptops) and works on `main`.
Run before/after each work session so all 4 stay on the same page.

Usage (Windows PowerShell AND Mac Terminal — same commands):
    python tools/sync.py start          # before working: fetch + autostash + pull --ff-only
    python tools/sync.py end            # after working: remind to commit + push (blocked if behind)
    python tools/sync.py status         # show ahead/behind, dirty files, last commits
    python tools/sync.py install-hooks  # one-time per clone: installs pre-commit / pre-push guards

Flags:
    --no-stash   with `start`: do NOT autostash; fail if the tree is dirty instead.
    --yes        with `end`: push without the confirmation prompt (for quick use).

Design notes:
- stdlib only, Python 3.8+ (works with Mac system python3 and Windows Python).
- Autostash is ON by default for `start` (per team choice): dirty work is
  stashed (including untracked, -u), pull runs on a clean tree, then the
  stash is popped. If the pop conflicts, the stash is KEPT and we exit 1.
- Offline-safe: if `git fetch` fails, we print the last FETCH_HEAD time and
  continue without pulling/pushing instead of erroring out.
- Never auto-resolves diverged `main`: `pull --ff-only` fails loudly with
  recovery instructions so nobody silently rewrites a teammate's work.
"""
from __future__ import annotations

import argparse
import datetime
import getpass
import os
import shutil
import subprocess
import sys

MAIN_BRANCH = "main"
REMOTE = "origin"


def run(*args: str, check: bool = False, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(args), capture_output=True, text=True, timeout=timeout,
    )


def run_live(*args: str) -> int:
    """Run letting output stream (for push/pull so users see progress)."""
    return subprocess.run(list(args)).returncode


def repo_root() -> str:
    p = run("git", "rev-parse", "--show-toplevel")
    if p.returncode != 0:
        sys.exit("ERROR: not inside a git repo. Run from your Argus-Panoptes clone.")
    return p.stdout.strip()


def current_branch() -> str:
    p = run("git", "rev-parse", "--abbrev-ref", "HEAD")
    return p.stdout.strip() if p.returncode == 0 else "?"


def dirty_files() -> list[str]:
    p = run("git", "status", "--porcelain=v1", "-uall")
    if p.returncode != 0:
        return []
    return [ln for ln in p.stdout.splitlines() if ln.strip()]


def ahead_behind(branch: str = MAIN_BRANCH) -> tuple[int | None, int | None]:
    """(ahead, behind) of HEAD vs origin/main. None if remote ref unknown."""
    p = run("git", "rev-list", "--left-right", "--count", f"HEAD...{REMOTE}/{branch}")
    if p.returncode != 0:
        return None, None
    try:
        a, b = p.stdout.strip().split()
        return int(a), int(b)
    except ValueError:
        return None, None


def last_fetch_age() -> str:
    root = repo_root()
    fh = os.path.join(root, ".git", "FETCH_HEAD")
    if not os.path.exists(fh):
        return "never fetched"
    mtime = os.path.getmtime(fh)
    dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return f"last fetch: {dt}"


def do_fetch() -> bool:
    """Returns True if fetch worked, False if offline/failed."""
    print(f"$ git fetch {REMOTE} --prune")
    p = run("git", "fetch", REMOTE, "--prune", timeout=60)
    if p.returncode != 0:
        print("OFFLINE or fetch failed — continuing with local state.")
        print(f"  ({last_fetch_age()})")
        if p.stderr.strip():
            print("  " + p.stderr.strip().splitlines()[-1])
        return False
    print("Fetched latest from origin.")
    return True


def show_status() -> None:
    branch = current_branch()
    print(f"Branch : {branch}")
    print(f"Root   : {repo_root()}")
    print(f"({last_fetch_age()})")
    a, b = ahead_behind()
    if a is None:
        print("Upstream: origin/main not found locally (fetch first).")
    else:
        print(f"Sync   : ahead {a} | behind {b}  (vs origin/main)")
        if b and b > 0:
            print("  -> you are BEHIND. Run: python tools/sync.py start")
        elif a and a > 0:
            print("  -> you are AHEAD. Run: python tools/sync.py end  (to push)")
        else:
            print("  -> in sync with origin/main.")
    dirty = dirty_files()
    if dirty:
        print(f"Dirty  : {len(dirty)} uncommitted file(s):")
        for ln in dirty[:20]:
            print(f"    {ln}")
        if len(dirty) > 20:
            print(f"    ... and {len(dirty) - 20} more")
    else:
        print("Dirty  : clean.")
    print("--- recent local commits ---")
    p = run("git", "log", "--oneline", "-5")
    print(p.stdout.strip() or "  (no commits?)")
    print("--- recent origin/main commits ---")
    p = run("git", "log", "--oneline", "-5", f"{REMOTE}/{MAIN_BRANCH}")
    print(p.stdout.strip() or "  (unknown — fetch first)")


def cmd_start(use_stash: bool = True) -> int:
    os.chdir(repo_root())
    branch = current_branch()
    if branch != MAIN_BRANCH:
        print(f"WARNING: you are on '{branch}', not '{MAIN_BRANCH}'.")
        print(f"  Team rule is all-on-main. Switch with: git switch {MAIN_BRANCH}")
    if not do_fetch():
        show_status()
        return 0  # offline: stay usable, don't fail

    a, b = ahead_behind()
    if a is None:
        print("ERROR: origin/main not found. Check remote: git remote -v")
        return 1
    print(f"Sync: ahead {a} | behind {b}")

    stashed = False
    dirty = dirty_files()
    if dirty:
        if not use_stash:
            print(f"Dirty tree ({len(dirty)} file(s)) and --no-stash given. Commit or stash first:")
            for ln in dirty[:15]:
                print(f"    {ln}")
            return 1
        user = getpass.getuser()
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        msg = f"sync-start-autostash {stamp} {user}"
        print(f"Autostashing {len(dirty)} dirty file(s) as '{msg}' ...")
        p = run("git", "stash", "push", "-u", "-m", msg)
        if p.returncode != 0:
            print("ERROR: stash failed:\n" + p.stderr)
            return 1
        stashed = True

    print(f"$ git pull --ff-only {REMOTE} {MAIN_BRANCH}")
    p = run("git", "pull", "--ff-only", REMOTE, MAIN_BRANCH, timeout=120)
    if p.returncode != 0:
        print("PULL FAILED — your main has diverged from origin/main.")
        print((p.stderr or p.stdout).strip())
        print("--- what differs ---")
        d = run("git", "log", "--graph", "--oneline", "-8", f"HEAD...{REMOTE}/{MAIN_BRANCH}")
        print(d.stdout.strip())
        if stashed:
            print("Your uncommitted work is SAFE in the stash. Recover with:")
            print("  git stash list")
            print(f"  git merge {REMOTE}/{MAIN_BRANCH}   # then: git stash pop")
        else:
            print("Recover with:")
            print(f"  git merge {REMOTE}/{MAIN_BRANCH}   # review, then push")
        return 1

    print("Pull OK — you are on the latest origin/main.")
    if stashed:
        print("Restoring your autostash ...")
        p = run("git", "stash", "pop")
        if p.returncode != 0:
            print("STASH POP CONFLICTED — stash KEPT. Resolve then run:")
            print("  git status")
            print("  git stash list   # your work is the top entry")
            print("  git stash drop   # only after files look right")
            return 1
        print("Autostash restored.")
    new = run("git", "log", "--oneline", "-5")
    print("--- now on ---")
    print(new.stdout.strip())
    if dirty_files():
        print("Note: you still have uncommitted files (see above) — normal, keep working.")
    return 0


def cmd_end(auto_yes: bool = False) -> int:
    os.chdir(repo_root())
    if not do_fetch():
        print("Offline: cannot push. Your commits are safe locally.")
        return 0
    a, b = ahead_behind()
    if a is None:
        print("ERROR: origin/main not found.")
        return 1
    dirty = dirty_files()
    if dirty:
        print(f"Reminder: {len(dirty)} uncommitted file(s) — commit them so teammates see your work:")
        for ln in dirty[:15]:
            print(f"    {ln}")
        print('  git add -A && git commit -m "describe your change"')
    if b and b > 0:
        print(f"BLOCKED: you are BEHIND by {b}. Run first: python tools/sync.py start")
        return 1
    if not a or a == 0:
        print("Nothing to push — origin/main already has your commits.")
        return 0
    print(f"You are AHEAD by {a} commit(s). Pushing ...")
    if not auto_yes:
        try:
            ans = input(f"Push {a} commit(s) to {REMOTE}/{MAIN_BRANCH}? [Y/n] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return 1
        if ans not in ("", "y", "yes"):
            print("Cancelled — push later with: python tools/sync.py end")
            return 1
    rc = run_live("git", "push", REMOTE, MAIN_BRANCH)
    if rc != 0:
        print("PUSH REJECTED — someone pushed first. Run:")
        print("  python tools/sync.py start   # pulls their work")
        print("  python tools/sync.py end     # push again")
        return 1
    print("Pushed. Teammates will get it on their next `start`.")
    return 0


def cmd_install_hooks() -> int:
    os.chdir(repo_root())
    src_dir = os.path.join(repo_root(), "tools", "githooks")
    dst_dir = os.path.join(repo_root(), ".git", "hooks")
    if not os.path.isdir(src_dir):
        print(f"ERROR: {src_dir} not found. Pull latest main first.")
        return 1
    os.makedirs(dst_dir, exist_ok=True)
    installed = []
    for name in ("pre-commit", "pre-push"):
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        if not os.path.exists(src):
            print(f"SKIP: {name} not found in tools/githooks/")
            continue
        shutil.copyfile(src, dst)
        try:
            os.chmod(dst, 0o755)  # needed on Mac; harmless on Windows
        except OSError:
            pass
        installed.append(name)
    if not installed:
        return 1
    print(f"Installed hooks into .git/hooks/: {', '.join(installed)}")
    print("Each teammate runs this ONCE per laptop after cloning.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Argus-Panoptes team sync (Windows + Mac).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start", help="sync to repo before working (fetch + autostash + pull --ff-only)")
    s.add_argument("--no-stash", action="store_true", help="fail if dirty instead of autostashing")
    e = sub.add_parser("end", help="push check after working (fetch + push, blocked if behind)")
    e.add_argument("--yes", action="store_true", help="push without confirmation")
    sub.add_parser("status", help="show ahead/behind, dirty files, recent commits")
    sub.add_parser("install-hooks", help="one-time per clone: install pre-commit/pre-push guards")
    args = ap.parse_args()
    if shutil.which("git") is None:
        sys.exit("ERROR: git not found. Install git first (https://git-scm.com).")
    if args.cmd == "start":
        return cmd_start(use_stash=not args.no_stash)
    if args.cmd == "end":
        return cmd_end(auto_yes=args.yes)
    if args.cmd == "status":
        os.chdir(repo_root())
        do_fetch_silent = run("git", "fetch", REMOTE, "--prune", timeout=60)
        if do_fetch_silent.returncode != 0:
            print("(offline — showing local state)")
        show_status()
        return 0
    if args.cmd == "install-hooks":
        return cmd_install_hooks()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
