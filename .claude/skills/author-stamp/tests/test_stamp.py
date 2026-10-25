import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import stamp  # noqa: E402

AUTHOR = "Ana Souza <ana@example.com>"
DOC = """\
---
id: US-001
# Optional: a YAML comment, not a heading
prd: PRD-001
---

# US-001 — Signup

Intro.

## Context

Why.

## Acceptance criteria

- **US-001.AC1** — When x, the system shall y.

```md
## Not a heading
```
"""


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Ana Souza")
    git(tmp_path, "config", "user.email", "ana@example.com")
    (tmp_path / ".gitignore").write_text("docs/dev/**\n!docs/dev/**/\n!docs/dev/README.md\n")
    (tmp_path / "docs").mkdir()
    return tmp_path


def run(repo: Path, command: str, *files: str, at: str = "2026-10-25T10:00:00-03:00",
        session: str = "s1") -> int:
    return stamp.main([command, "--session", session, "--at", at,
                       *[str(repo / f) for f in files]])


def stamps(path: Path) -> list[str]:
    return [line for line in path.read_text().splitlines() if line.startswith("<!-- author-stamp:")]


def line_after(path: Path, heading: str) -> str:
    lines = path.read_text().splitlines()
    return lines[lines.index(heading) + 1]


def test_new_file_stamps_every_section_below_its_heading(repo):
    doc = repo / "docs/story.md"
    run(repo, "begin", "docs/story.md")
    doc.write_text(DOC)
    run(repo, "end", "docs/story.md")

    expected = (f"<!-- author-stamp: session=s1 | author={AUTHOR} "
                f"| at=2026-10-25T10:00:00-03:00 -->")
    for heading in ("# US-001 — Signup", "## Context", "## Acceptance criteria"):
        assert line_after(doc, heading) == expected
    assert len(stamps(doc)) == 3


def test_yaml_comments_and_fenced_headings_are_not_sections(repo):
    doc = repo / "docs/story.md"
    run(repo, "begin", "docs/story.md")
    doc.write_text(DOC)
    run(repo, "end", "docs/story.md")
    text = doc.read_text()
    assert "# Optional: a YAML comment, not a heading\nprd" in text
    assert "## Not a heading\n```" in text


def test_only_changed_sections_get_a_new_stamp(repo):
    doc = repo / "docs/story.md"
    run(repo, "begin", "docs/story.md")
    doc.write_text(DOC)
    run(repo, "end", "docs/story.md")

    run(repo, "begin", "docs/story.md", session="s2")
    doc.write_text(doc.read_text().replace("Why.", "Because."))
    run(repo, "end", "docs/story.md", session="s2", at="2026-10-26T09:30:00-03:00")

    assert "session=s2" in line_after(doc, "## Context")
    assert "at=2026-10-26T09:30:00-03:00" in line_after(doc, "## Context")
    assert "session=s1" in line_after(doc, "## Acceptance criteria")
    assert "session=s1" in line_after(doc, "# US-001 — Signup")


def test_a_section_keeps_only_its_latest_stamp(repo):
    doc = repo / "docs/story.md"
    for n, text in enumerate(["Why.", "Because.", "Since."], start=1):
        run(repo, "begin", "docs/story.md", session=f"s{n}")
        doc.write_text(DOC.replace("Why.", text))
        run(repo, "end", "docs/story.md", session=f"s{n}", at=f"2026-10-2{n}T10:00:00-03:00")
    assert len(stamps(doc)) == 3
    assert "session=s3" in line_after(doc, "## Context")


def test_front_matter_changes_stamp_the_first_section(repo):
    doc = repo / "docs/story.md"
    run(repo, "begin", "docs/story.md")
    doc.write_text(DOC)
    run(repo, "end", "docs/story.md")

    run(repo, "begin", "docs/story.md", session="s2")
    doc.write_text(doc.read_text().replace("PRD-001", "PRD-002"))
    run(repo, "end", "docs/story.md", session="s2")

    assert "session=s2" in line_after(doc, "# US-001 — Signup")
    assert "session=s1" in line_after(doc, "## Context")


def test_unchanged_file_is_left_untouched(repo):
    doc = repo / "docs/story.md"
    run(repo, "begin", "docs/story.md")
    doc.write_text(DOC)
    run(repo, "end", "docs/story.md")
    before = doc.read_text()

    run(repo, "begin", "docs/story.md", session="s2")
    run(repo, "end", "docs/story.md", session="s2")
    assert doc.read_text() == before


def test_without_snapshot_it_compares_with_head(repo, capsys):
    doc = repo / "docs/story.md"
    doc.write_text(DOC)
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "init")

    doc.write_text(DOC.replace("Why.", "Because."))
    run(repo, "end", "docs/story.md")

    assert stamps(doc) == [line_after(doc, "## Context")]
    assert "compared with HEAD" in capsys.readouterr().err


def test_duplicate_headings_are_tracked_separately(repo):
    doc = repo / "docs/faq.md"
    original = "# FAQ\n\n## Answer\n\nOne.\n\n## Answer\n\nTwo.\n"
    doc.write_text(original)
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "init")

    doc.write_text(original.replace("Two.", "Three."))
    run(repo, "end", "docs/faq.md")

    lines = doc.read_text().splitlines()
    assert lines[lines.index("One.") - 2] == "## Answer"
    assert lines[lines.index("Three.") - 2].startswith("<!-- author-stamp:")


def test_out_of_scope_files_are_skipped(repo, capsys):
    (repo / "docs/_templates").mkdir()
    (repo / "docs/dev").mkdir()
    for rel in ("README.md", "docs/_templates/story.md", "docs/dev/notes.md", "docs/rbac.yaml"):
        run(repo, "begin", rel)
        (repo / rel).write_text("# Title\n\nText.\n")
        run(repo, "end", rel)
        assert stamps(repo / rel) == []
    assert capsys.readouterr().err.count("skipped") == 8


def test_values_cannot_close_the_comment(repo):
    doc = repo / "docs/a.md"
    run(repo, "begin", "docs/a.md")
    doc.write_text("# A\n")
    stamp.main(["end", "--session", "x--y", "--author", "Ana -->", "--at", "t", str(doc)])
    assert line_after(doc, "# A") == "<!-- author-stamp: session=x-y | author=Ana -> | at=t -->"


def hook(monkeypatch, capsys, payload: str) -> tuple[int, str]:
    capsys.readouterr()  # discard output from earlier calls
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    code = stamp.main(["hook", "--at", "2026-10-25T11:00:00-03:00"])
    return code, capsys.readouterr().out


def hook_event(event: str, path: Path, session: str = "hook-session") -> str:
    return json.dumps({"hook_event_name": event, "session_id": session,
                       "tool_name": "Edit", "tool_input": {"file_path": str(path)}})


def test_hook_stamps_the_sections_one_tool_call_changed(repo, monkeypatch, capsys):
    doc = repo / "docs/story.md"
    run(repo, "begin", "docs/story.md")
    doc.write_text(DOC)
    run(repo, "end", "docs/story.md")

    assert hook(monkeypatch, capsys, hook_event("PreToolUse", doc)) == (0, "")
    doc.write_text(doc.read_text().replace("Why.", "Because."))
    code, out = hook(monkeypatch, capsys, hook_event("PostToolUse", doc))

    assert code == 0
    assert "session=hook-session" in line_after(doc, "## Context")
    assert "session=s1" in line_after(doc, "## Acceptance criteria")
    context = json.loads(out)["hookSpecificOutput"]
    assert context["hookEventName"] == "PostToolUse"
    assert "docs/story.md" in context["additionalContext"]


def test_hook_baseline_is_refreshed_on_every_tool_call(repo, monkeypatch, capsys):
    doc = repo / "docs/story.md"
    doc.write_text(DOC)
    hook(monkeypatch, capsys, hook_event("PreToolUse", doc))  # tool call denied: no PostToolUse
    doc.write_text(DOC.replace("Why.", "Edited by a person."))
    hook(monkeypatch, capsys, hook_event("PreToolUse", doc))
    doc.write_text(doc.read_text().replace("Intro.", "Intro, edited by the agent."))
    hook(monkeypatch, capsys, hook_event("PostToolUse", doc))

    assert stamps(doc) == [line_after(doc, "# US-001 — Signup")]


def test_hook_is_silent_for_files_out_of_scope(repo, monkeypatch, capsys):
    readme = repo / "README.md"
    readme.write_text("# Title\n")
    for event in ("PreToolUse", "PostToolUse"):
        assert hook(monkeypatch, capsys, hook_event(event, readme)) == (0, "")
    assert capsys.readouterr().err == ""
    assert stamps(readme) == []


@pytest.mark.parametrize("payload", ["", "not json", '{"hook_event_name": "PostToolUse"}'])
def test_hook_never_fails_the_tool_call(repo, monkeypatch, capsys, payload):
    assert hook(monkeypatch, capsys, payload)[0] == 0


def test_missing_session_is_an_error(repo, monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    monkeypatch.delenv("CLAUDE_SESSION_ID", raising=False)
    with pytest.raises(SystemExit):
        stamp.main(["end", str(repo / "docs/a.md")])
