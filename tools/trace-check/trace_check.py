#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML>=6", "jsonschema>=4.18"]
# ///
"""Traceability check for the Voynan documentation standard.

Reads the documents under docs/ and the requirement markers in test code, then
fails when the two disagree: criteria without tests, tests citing unknown IDs,
duplicate IDs, file names that do not match their ID, invalid front matter and
folders without a README. Optionally writes the generated traceability matrix.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SCHEMAS = HERE / "schemas"

# Top-level folders of docs/ that hold no normative documents.
IGNORED_DOC_DIRS = {"_templates", "dev"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
TEST_SUFFIXES = {".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts"}

AC_LINE = re.compile(r"^\s*[-*]\s+\*\*([A-Z]+-\d+\.AC\d+)\*\*(\s+\[manual\])?")
REQ_HEADING = re.compile(r"^#{2,6}\s+((?:NFR|BR)-\d{3,})\b")
TESTABLE_ID = re.compile(r"US-\d{3,}(?:\.AC\d+)?|NFR-\d{3,}|BR-\d{3,}")
PY_MARKER = re.compile(r"\bmark\.req\(([^)]*)\)")
PY_STRING = re.compile(r"""["']([^"']*)["']""")
JS_TITLE = re.compile(r"""\b(?:it|test)(?:\.\w+)*\(\s*["'`]\[([^\]]*)\]""")


@dataclass(frozen=True)
class Kind:
    name: str
    folder: str  # relative to docs/
    file_name: re.Pattern[str]
    convention: str
    id_in_front_matter: bool
    references: tuple[str, ...]  # front matter keys that cite other IDs


KINDS = (
    Kind("story", "stories", re.compile(r"(US-\d{3,})-[a-z0-9-]+\.md"), "US-NNN-slug.md", True,
         ("prd", "requirements", "decisions")),
    Kind("prd", "prds", re.compile(r"(PRD-\d{3,})-[a-z0-9-]+\.md"), "PRD-NNN-slug.md", True,
         ("research",)),
    Kind("adr", "decisions", re.compile(r"(ADR-\d{4,})-[a-z0-9-]+\.md"), "ADR-NNNN-slug.md", True,
         ("drivers", "supersedes", "superseded_by")),
    Kind("research", "knowledge/research", re.compile(r"(\d{4}-\d{2}-[a-z0-9-]+)\.md"),
         "YYYY-MM-slug.md", False, ("superseded_by",)),
    Kind("postmortem", "operations/postmortems", re.compile(r"(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)\.md"),
         "YYYY-MM-DD-slug.md", False, ("superseded_by",)),
)
KINDS_BY_FOLDER = {kind.folder: kind for kind in KINDS}


@dataclass(frozen=True)
class Location:
    path: str
    line: int

    def __str__(self) -> str:
        return f"{self.path}:{self.line}" if self.line else self.path


@dataclass(frozen=True)
class Issue:
    location: Location
    message: str


@dataclass
class Document:
    id: str
    kind: Kind
    location: Location
    meta: dict
    front_matter: list[str]


@dataclass
class Criterion:
    id: str
    story: str
    manual: bool
    location: Location


@dataclass
class Report:
    errors: list[Issue] = field(default_factory=list)
    definitions: dict[str, Location] = field(default_factory=dict)
    documents: dict[str, Document] = field(default_factory=dict)
    criteria: dict[str, Criterion] = field(default_factory=dict)
    requirements: dict[str, Location] = field(default_factory=dict)
    references: dict[str, list[Location]] = field(default_factory=dict)

    def error(self, location: Location, message: str) -> None:
        self.errors.append(Issue(location, message))

    def define(self, id_: str, location: Location) -> bool:
        if id_ in self.definitions:
            self.error(location, f"{id_} is already defined at {self.definitions[id_]}")
            return False
        self.definitions[id_] = location
        return True


def natural_key(text: str) -> list:
    """Sort key that orders US-999 before US-1000."""
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", text)]


def check(docs: Path, test_roots: list[Path], root: Path | None = None,
          exclude: list[Path] | tuple = ()) -> Report:
    root = (root or Path.cwd()).resolve()
    docs = docs.resolve()
    report = Report()

    def rel(path: Path) -> str:
        try:
            return path.resolve().relative_to(root).as_posix()
        except ValueError:
            return path.as_posix()

    for directory, files in _walk_docs(docs):
        if "README.md" not in files:
            report.error(Location(rel(directory), 0), "folder has no README.md")
        folder = directory.relative_to(docs).as_posix()
        for name in files:
            if not name.endswith(".md") or name == "README.md":
                continue
            path = directory / name
            if folder in KINDS_BY_FOLDER:
                _read_document(report, KINDS_BY_FOLDER[folder], path, rel(path))
            elif folder == "requirements" or folder.startswith("requirements/"):
                _read_requirements(report, path, rel(path))

    _check_references(report)

    skip = {docs, HERE, *(Path(p).resolve() for p in exclude)}
    for test_root in test_roots:
        for path in _walk_sources(test_root.resolve(), skip):
            _read_markers(report, path, rel(path))

    for criterion in report.criteria.values():
        if not criterion.manual and criterion.id not in report.references:
            report.error(criterion.location,
                         f"{criterion.id} has no test (tag it [manual] if it cannot be automated)")

    report.errors.sort(key=lambda issue: (issue.location.path, issue.location.line))
    return report


def _walk_docs(docs: Path):
    for directory, dirs, files in os.walk(docs):
        current = Path(directory)
        dirs[:] = sorted(
            d for d in dirs
            if not d.startswith(".") and not (current == docs and d in IGNORED_DOC_DIRS)
        )
        yield current, sorted(files)


def _walk_sources(root: Path, skip: set[Path]):
    if root.is_file():
        yield root
        return
    for directory, dirs, files in os.walk(root):
        current = Path(directory)
        dirs[:] = sorted(
            d for d in dirs
            if d not in SKIP_DIRS and not d.startswith(".") and (current / d).resolve() not in skip
        )
        for name in sorted(files):
            if Path(name).suffix in TEST_SUFFIXES:
                yield current / name


def _read_document(report: Report, kind: Kind, path: Path, rel_path: str) -> None:
    match = kind.file_name.fullmatch(path.name)
    if not match:
        report.error(Location(rel_path, 0), f"file name does not match {kind.convention}")
        return
    doc_id = match.group(1)
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, front_matter, problem = _front_matter(lines)
    if problem:
        report.error(Location(rel_path, 1), problem)
        return

    errors = sorted(_validator(kind.name).iter_errors(meta), key=lambda e: list(e.absolute_path))
    for err in errors:
        where = ".".join(str(part) for part in err.absolute_path)
        report.error(Location(rel_path, 1), f"front matter: {where + ': ' if where else ''}{err.message}")
    if kind.id_in_front_matter and meta.get("id") not in (None, doc_id):
        report.error(Location(rel_path, _key_line(front_matter, "id")),
                     f"id {meta['id']} does not match file name {doc_id}")

    location = Location(rel_path, 1)
    if not report.define(doc_id, location):
        return
    report.documents[doc_id] = Document(doc_id, kind, location, meta if not errors else {}, front_matter)

    if kind.name == "story":
        _read_criteria(report, doc_id, lines, rel_path)


def _front_matter(lines: list[str]) -> tuple[dict, list[str], str | None]:
    if not lines or lines[0].strip() != "---":
        return {}, [], "missing YAML front matter"
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [], "unterminated YAML front matter"
    block = lines[1:end]
    try:
        meta = yaml.safe_load("\n".join(block)) or {}
    except yaml.YAMLError as exc:
        return {}, [], f"invalid YAML front matter: {getattr(exc, 'problem', exc)}"
    if not isinstance(meta, dict):
        return {}, [], "front matter must be a mapping"
    return _stringify_dates(meta), block, None


def _stringify_dates(value):
    if isinstance(value, dict):
        return {key: _stringify_dates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_stringify_dates(item) for item in value]
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    return value


_VALIDATORS: dict[str, Draft202012Validator] = {}


def _validator(kind: str) -> Draft202012Validator:
    if kind not in _VALIDATORS:
        schema = json.loads((SCHEMAS / f"{kind}.json").read_text(encoding="utf-8"))
        _VALIDATORS[kind] = Draft202012Validator(schema)
    return _VALIDATORS[kind]


def _key_line(front_matter: list[str], key: str) -> int:
    for index, line in enumerate(front_matter):
        if line.startswith(f"{key}:"):
            return index + 2  # +1 for the opening '---', +1 for 1-based lines
    return 1


def _read_criteria(report: Report, story_id: str, lines: list[str], rel_path: str) -> None:
    found = False
    for number, line in enumerate(lines, start=1):
        match = AC_LINE.match(line)
        if not match:
            continue
        found = True
        ac_id = match.group(1)
        location = Location(rel_path, number)
        if not ac_id.startswith(f"{story_id}.AC"):
            report.error(location, f"{ac_id} does not belong to {story_id}")
            continue
        if report.define(ac_id, location):
            report.criteria[ac_id] = Criterion(ac_id, story_id, bool(match.group(2)), location)
    if not found:
        report.error(Location(rel_path, 1), "story has no acceptance criteria")


def _read_requirements(report: Report, path: Path, rel_path: str) -> None:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = REQ_HEADING.match(line)
        if match and report.define(match.group(1), Location(rel_path, number)):
            report.requirements[match.group(1)] = Location(rel_path, number)


def _check_references(report: Report) -> None:
    for doc in report.documents.values():
        for key in doc.kind.references:
            value = doc.meta.get(key)
            cited = value if isinstance(value, list) else [value] if value else []
            for id_ in cited:
                if id_ not in report.definitions:
                    report.error(Location(doc.location.path, _key_line(doc.front_matter, key)),
                                 f"front matter cites unknown ID {id_}")


def _read_markers(report: Report, path: Path, rel_path: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    for number, line in enumerate(text.splitlines(), start=1):
        ids = [s for m in PY_MARKER.finditer(line) for s in PY_STRING.findall(m.group(1))]
        ids += [part for m in JS_TITLE.finditer(line) for part in m.group(1).split(",")]
        for raw in ids:
            id_ = raw.strip()
            location = Location(rel_path, number)
            if not TESTABLE_ID.fullmatch(id_):
                report.error(location, f"invalid requirement ID '{id_}'")
            elif id_ not in report.criteria and id_ not in report.requirements \
                    and id_ not in report.documents:
                report.error(location, f"unknown requirement ID {id_}")
            else:
                report.references.setdefault(id_, []).append(location)


def render_matrix(report: Report) -> str:
    def cell(items) -> str:
        items = list(items)
        return "<br>".join(str(item) for item in items) if items else "—"

    def stories_citing(key: str, id_: str) -> list[str]:
        return sorted(
            (doc.id for doc in report.documents.values()
             if doc.kind.name == "story" and id_ in _as_list(doc.meta.get(key))),
            key=natural_key,
        )

    out = [
        "# Traceability matrix",
        "",
        "Generated by tools/trace-check. Do not edit or commit this file.",
        "",
        "## Acceptance criteria",
        "",
        "| Criterion | Story | PRD | Verification |",
        "| --- | --- | --- | --- |",
    ]
    for ac_id in sorted(report.criteria, key=natural_key):
        criterion = report.criteria[ac_id]
        prd = report.documents[criterion.story].meta.get("prd", "—")
        tests = report.references.get(ac_id, [])
        verification = cell(tests) if tests else "manual" if criterion.manual else "**missing**"
        out.append(f"| {ac_id} | {criterion.story} | {prd} | {verification} |")

    out += ["", "## Requirements", "", "| Requirement | Tests | Cited by |", "| --- | --- | --- |"]
    for req_id in sorted(report.requirements, key=natural_key):
        out.append(f"| {req_id} | {cell(report.references.get(req_id, []))} "
                   f"| {cell(stories_citing('requirements', req_id))} |")

    sections = (("prd", "PRDs", "PRD", "Stories", "prd"),
                ("adr", "Decisions", "ADR", "Cited by", "decisions"))
    for kind, title, column, cited_column, key in sections:
        out += ["", f"## {title}", "", f"| {column} | {cited_column} |", "| --- | --- |"]
        ids = sorted((d.id for d in report.documents.values() if d.kind.name == kind), key=natural_key)
        for id_ in ids:
            out.append(f"| {id_} | {cell(stories_citing(key, id_))} |")

    return "\n".join(out) + "\n"


def _as_list(value) -> list:
    return value if isinstance(value, list) else [value] if value else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--docs", type=Path, default=Path("docs"), help="documentation root (default: docs)")
    parser.add_argument("--tests", type=Path, nargs="+", default=[Path(".")],
                        help="folders scanned for test markers (default: .)")
    parser.add_argument("--exclude", type=Path, nargs="*", default=[], help="folders not scanned for markers")
    parser.add_argument("--matrix", type=Path, help="write the traceability matrix to this file")
    args = parser.parse_args(argv)

    report = check(args.docs, args.tests, exclude=args.exclude)

    if args.matrix:
        args.matrix.parent.mkdir(parents=True, exist_ok=True)
        args.matrix.write_text(render_matrix(report), encoding="utf-8")

    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for issue in report.errors:
        loc = issue.location
        if in_actions:
            print(f"::error file={loc.path},line={loc.line or 1}::{issue.message}")
        else:
            print(f"{loc}: {issue.message}")

    covered = sum(1 for ac in report.criteria if ac in report.references)
    print(f"trace-check: {len(report.errors)} error(s); "
          f"{covered}/{len(report.criteria)} criteria covered by tests", file=sys.stderr)
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
