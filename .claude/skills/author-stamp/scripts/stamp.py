#!/usr/bin/env python3
"""Stamp the sections of docs/ Markdown files that an AI session changed.

Each changed section gets one hidden comment right below its heading:

    <!-- author-stamp: session=<id> | author=<name <email>> | at=<ISO 8601> -->

Stamps of untouched sections are kept, and a section only ever holds its latest
stamp. Usage: `begin FILE...` before editing (snapshots the files), then
`end FILE...` after editing (diffs against the snapshot, or against HEAD when
there is none, and stamps the sections that differ). Standard library only.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

DOCS_DIR = "docs/"
# Templates are copied verbatim into new documents; stamps there would be
# inherited by every copy and attribute the new document to the wrong session.
EXCLUDED_DIRS = ("docs/_templates/",)

STAMP = re.compile(r"^<!-- author-stamp: .* -->$")
HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


@dataclass(frozen=True)
class Section:
    key: tuple[str, int]  # (heading text, occurrence) so duplicate headings stay distinct
    heading: int | None  # line index of the heading; None when the file has no heading
    start: int
    end: int  # exclusive


def split_sections(lines: list[str]) -> list[Section]:
    """Sections run from one ATX heading to the next. Front matter and anything
    before the first heading belong to the first section."""
    headings: list[int] = []
    i = 0
    if lines and lines[0].strip() == "---":
        closing = next((j for j in range(1, len(lines)) if lines[j].strip() == "---"), None)
        i = closing + 1 if closing is not None else 0
    fence: str | None = None
    for index in range(i, len(lines)):
        line = lines[index]
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None and HEADING.match(line):
            headings.append(index)

    if not headings:
        return [Section(("", 0), None, 0, len(lines))]

    seen: dict[str, int] = {}
    sections = []
    for n, heading in enumerate(headings):
        text = lines[heading].strip()
        seen[text] = seen.get(text, 0) + 1
        start = 0 if n == 0 else heading
        end = headings[n + 1] if n + 1 < len(headings) else len(lines)
        sections.append(Section((text, seen[text]), heading, start, end))
    return sections


def content(lines: list[str], section: Section) -> list[str]:
    return [line for line in lines[section.start:section.end] if not STAMP.match(line)]


def changed_sections(old: list[str] | None, new: list[str]) -> list[Section]:
    sections = split_sections(new)
    if old is None:
        return sections
    before = {s.key: content(old, s) for s in split_sections(old)}
    return [s for s in sections if before.get(s.key) != content(new, s)]


def stamp_of(lines: list[str], section: Section) -> str | None:
    stamps = [line for line in lines[section.start:section.end] if STAMP.match(line)]
    return stamps[-1] if stamps else None


def previous_stamps(old: list[str] | None) -> dict[tuple[str, int], str]:
    if old is None:
        return {}
    found = {s.key: stamp_of(old, s) for s in split_sections(old)}
    return {key: stamp for key, stamp in found.items() if stamp}


def apply_stamps(lines: list[str], stamps: dict[Section, str]) -> list[str]:
    lines = list(lines)
    for section in sorted(stamps, key=lambda s: s.start, reverse=True):
        stamp = stamps[section]
        if section.heading is None:
            while lines and (STAMP.match(lines[-1]) or lines[-1] == ""):
                lines.pop()
            lines += ["", stamp, ""]
            continue
        below = section.heading + 1
        while below < len(lines) and STAMP.match(lines[below]):
            del lines[below]
        lines.insert(below, stamp)
    return lines


def clean(value: str) -> str:
    value = value.replace("\n", " ").replace("|", "/")
    while "--" in value:
        value = value.replace("--", "-")
    return value.strip()


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def repo_root(path: Path) -> Path:
    result = git(path.parent if path.parent.exists() else Path.cwd(), "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        sys.exit(f"author-stamp: {path} is not inside a Git repository")
    return Path(result.stdout.strip())


def snapshot_path(root: Path, session: str, rel: str) -> Path:
    git_dir = Path(git(root, "rev-parse", "--absolute-git-dir").stdout.strip())
    return git_dir / "author-stamp" / clean(session) / f"{rel}.snapshot"


def in_scope(root: Path, rel: str) -> str | None:
    """Return the reason a file is out of scope, or None when it must be stamped."""
    if not rel.startswith(DOCS_DIR) or not rel.endswith(".md"):
        return "not a Markdown file under docs/"
    if rel.startswith(EXCLUDED_DIRS):
        return "templates are never stamped"
    if git(root, "check-ignore", "-q", rel).returncode == 0:
        return "ignored by Git"
    return None


def default_author(root: Path) -> str | None:
    name = git(root, "config", "user.name").stdout.strip()
    email = git(root, "config", "user.email").stdout.strip()
    if not name:
        return None
    return f"{name} <{email}>" if email else name


def begin(path: Path, root: Path, rel: str, session: str, refresh: bool = False) -> None:
    snap = snapshot_path(root, session, rel)
    if refresh:
        snap.unlink(missing_ok=True)
        snap.with_suffix(".absent").unlink(missing_ok=True)
    elif snap.exists() or snap.with_suffix(".absent").exists():
        return  # keep the earliest baseline of this session
    snap.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        snap.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        snap.with_suffix(".absent").touch()
    print(f"{rel}: snapshot taken")


def end(path: Path, root: Path, rel: str, session: str, stamp: str) -> None:
    if not path.exists():
        print(f"{rel}: deleted, nothing to stamp")
        return
    snap = snapshot_path(root, session, rel)
    absent = snap.with_suffix(".absent")
    if snap.exists():
        old = snap.read_text(encoding="utf-8").split("\n")
    elif absent.exists():
        old = None
    else:
        head = git(root, "show", f"HEAD:{rel}")
        old = head.stdout.split("\n") if head.returncode == 0 else None
        print(f"{rel}: no snapshot; compared with HEAD", file=sys.stderr)

    new = path.read_text(encoding="utf-8").split("\n")
    changed = changed_sections(old, new)
    updates = {section: stamp for section in changed}
    # A whole-file rewrite may drop the stamps of sections it did not change; restore them.
    kept = previous_stamps(old)
    for section in split_sections(new):
        if section not in updates and section.key in kept and stamp_of(new, section) != kept[section.key]:
            updates[section] = kept[section.key]

    if updates:
        path.write_text("\n".join(apply_stamps(new, updates)), encoding="utf-8")
    if changed:
        names = ", ".join(s.key[0].lstrip("# ") or "(whole file)" for s in changed)
        print(f"{rel}: stamped {len(changed)} section(s): {names}")
    else:
        print(f"{rel}: no changes")
    snap.unlink(missing_ok=True)
    absent.unlink(missing_ok=True)


def run(command: str, files: list[Path], session: str, author: str | None, at: str,
        refresh: bool = False, quiet: bool = False) -> None:
    for file in files:
        path = file.resolve()
        root = repo_root(path)
        rel = path.relative_to(root).as_posix()
        reason = in_scope(root, rel)
        if reason:
            if not quiet:
                print(f"{rel}: skipped ({reason})", file=sys.stderr)
            continue
        if command == "begin":
            begin(path, root, rel, session, refresh)
            continue
        author = author or default_author(root)
        if not author:
            sys.exit("author-stamp: no author; set git user.name or pass --author")
        stamp = (f"<!-- author-stamp: session={clean(session)} | author={clean(author)} "
                 f"| at={clean(at)} -->")
        end(path, root, rel, session, stamp)


def hook(author: str | None, at: str) -> int:
    """Claude Code hook entry point: PreToolUse snapshots, PostToolUse stamps.
    Never fails the tool call; problems are reported on stderr."""
    try:
        payload = json.load(sys.stdin)
        event = payload["hook_event_name"]
        session = payload["session_id"]
        file = payload["tool_input"]["file_path"]
    except (ValueError, KeyError, TypeError):
        return 0
    if event not in ("PreToolUse", "PostToolUse") or not file:
        return 0
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            run("begin" if event == "PreToolUse" else "end", [Path(file)], session, author, at,
                refresh=True, quiet=True)
    except (SystemExit, OSError) as exc:
        print(f"author-stamp: {exc}", file=sys.stderr)
        return 0
    stamped = [line for line in output.getvalue().splitlines() if ": stamped " in line]
    if event == "PostToolUse" and stamped:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "author-stamp updated hidden stamp comments; re-read before the next "
                                 "edit of the same file. " + " ".join(stamped),
        }}))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["begin", "end", "hook"])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--session", help="AI session ID (default: $CLAUDE_CODE_SESSION_ID)")
    parser.add_argument("--author", help='responsible person (default: git "user.name <user.email>")')
    parser.add_argument("--at", help="timestamp (default: now, ISO 8601 with offset)")
    args = parser.parse_args(argv)

    at = args.at or dt.datetime.now().astimezone().isoformat(timespec="seconds")
    if args.command == "hook":
        return hook(args.author, at)
    if not args.files:
        parser.error("begin and end need at least one file")
    session = args.session or os.environ.get("CLAUDE_CODE_SESSION_ID") or os.environ.get("CLAUDE_SESSION_ID")
    if not session:
        sys.exit("author-stamp: no session ID; pass --session")
    run(args.command, args.files, session, args.author, at)
    return 0


if __name__ == "__main__":
    sys.exit(main())
