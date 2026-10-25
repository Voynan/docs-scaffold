import sys
from pathlib import Path
from textwrap import dedent

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import trace_check  # noqa: E402

README = "# Folder\n"

STORY = """\
---
id: US-001
title: Tenant signup
prd: PRD-001
requirements: [NFR-001]
---

# US-001 — Tenant signup

- **US-001.AC1** — When a visitor submits the form, the system shall create a tenant.
- **US-001.AC2** [manual] — The system shall show the brand colors.
"""

PRD = """\
---
id: PRD-001
title: Signup
status: approved
owner: Ana
---

# PRD-001 — Signup
"""

NFR = """\
# Non-functional requirements

### NFR-001 — Fast reads
"""

PY_TEST = """\
import pytest

@pytest.mark.req("US-001.AC1")
def test_signup():
    pass
"""


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text))


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal valid project: one PRD, one story, one NFR and one test."""
    for rel in ["docs", "docs/stories", "docs/prds", "docs/requirements"]:
        write(tmp_path, f"{rel}/README.md", README)
    write(tmp_path, "docs/stories/US-001-tenant-signup.md", STORY)
    write(tmp_path, "docs/prds/PRD-001-signup.md", PRD)
    write(tmp_path, "docs/requirements/non-functional.md", NFR)
    write(tmp_path, "src/tests/test_signup.py", PY_TEST)
    return tmp_path


def run(root: Path) -> trace_check.Report:
    return trace_check.check(docs=root / "docs", test_roots=[root / "src"], root=root)


def messages(report: trace_check.Report) -> str:
    return "\n".join(issue.message for issue in report.errors)


def test_valid_project_has_no_errors(project):
    report = run(project)
    assert report.errors == []


def test_matrix_lists_test_location_and_manual_criteria(project):
    matrix = trace_check.render_matrix(run(project))
    assert "| US-001.AC1 | US-001 | PRD-001 | src/tests/test_signup.py:3 |" in matrix
    assert "| US-001.AC2 | US-001 | PRD-001 | manual |" in matrix


def test_matrix_lists_downstream_views(project):
    matrix = trace_check.render_matrix(run(project))
    assert "| PRD-001 | US-001 |" in matrix
    assert "| NFR-001 | — | US-001 |" in matrix


def test_criterion_without_test_fails(project):
    write(project, "src/tests/test_signup.py", "def test_nothing():\n    pass\n")
    assert "US-001.AC1 has no test" in messages(run(project))


def test_test_referencing_unknown_id_fails(project):
    write(project, "src/tests/test_other.py", '@pytest.mark.req("US-001.AC9")\ndef test_x(): pass\n')
    assert "unknown requirement ID US-001.AC9" in messages(run(project))


def test_malformed_id_in_marker_fails(project):
    write(project, "src/tests/test_other.py", '@pytest.mark.req("us-1")\ndef test_x(): pass\n')
    assert "invalid requirement ID 'us-1'" in messages(run(project))


def test_js_markers_with_several_ids_count_as_coverage(project):
    write(project, "src/tests/test_signup.py", "")
    write(
        project,
        "src/web/signup.test.ts",
        'it("[US-001.AC1, NFR-001] creates a tenant", () => {});\n'
        'test.skip("[US-001.AC1] also covered", () => {});\n',
    )
    report = run(project)
    assert report.errors == []
    assert "src/web/signup.test.ts:1" in trace_check.render_matrix(report)


def test_duplicate_story_id_fails(project):
    write(project, "docs/stories/US-001-other.md", STORY)
    assert "US-001 is already defined" in messages(run(project))


def test_duplicate_requirement_heading_fails(project):
    write(project, "docs/requirements/non-functional.md", NFR + "\n### NFR-001 — Again\n")
    assert "NFR-001 is already defined" in messages(run(project))


def test_file_name_must_match_id(project):
    write(project, "docs/stories/US-002-renamed.md", STORY.replace("US-001.AC", "US-002.AC"))
    assert "id US-001 does not match file name US-002" in messages(run(project))


def test_file_name_must_follow_convention(project):
    write(project, "docs/stories/tenant-signup.md", STORY)
    assert "file name does not match US-NNN-slug.md" in messages(run(project))


def test_invalid_front_matter_fails(project):
    write(project, "docs/prds/PRD-001-signup.md", PRD.replace("approved", "done"))
    assert "front matter: status: 'done' is not one of" in messages(run(project))


def test_missing_front_matter_fails(project):
    write(project, "docs/prds/PRD-001-signup.md", "# PRD-001\n")
    assert "missing YAML front matter" in messages(run(project))


def test_reference_to_unknown_id_in_front_matter_fails(project):
    write(project, "docs/stories/US-001-tenant-signup.md", STORY.replace("NFR-001", "NFR-404"))
    assert "front matter cites unknown ID NFR-404" in messages(run(project))


def test_superseded_adr_requires_successor(project):
    write(project, "docs/decisions/README.md", README)
    write(
        project,
        "docs/decisions/ADR-0001-schema-per-tenant.md",
        """\
        ---
        id: ADR-0001
        title: Schema per tenant
        status: superseded
        date: 2026-10-25
        deciders: [Ana]
        ---
        """,
    )
    assert "front matter: 'superseded_by' is a required property" in messages(run(project))


def test_dated_documents_are_referenced_by_file_stem(project):
    write(project, "docs/knowledge/README.md", README)
    write(project, "docs/knowledge/research/README.md", README)
    write(
        project,
        "docs/knowledge/research/2026-10-payment-gateways.md",
        """\
        ---
        title: Payment gateways
        date: 2026-10-01
        author: Ana
        status: current
        ---
        """,
    )
    write(project, "docs/prds/PRD-001-signup.md", PRD.replace("owner: Ana", "owner: Ana\nresearch: [2026-10-payment-gateways]"))
    assert run(project).errors == []


def test_story_without_criteria_fails(project):
    write(project, "docs/stories/US-001-tenant-signup.md", STORY.split("- **US-001.AC1**")[0])
    assert "story has no acceptance criteria" in messages(run(project))


def test_criterion_must_belong_to_its_story(project):
    write(project, "docs/stories/US-001-tenant-signup.md", STORY.replace("US-001.AC2", "US-002.AC2"))
    assert "US-002.AC2 does not belong to US-001" in messages(run(project))


def test_folder_without_readme_fails(project):
    write(project, "docs/security/threat-model.md", "# Threat model\n")
    assert "folder has no README.md" in messages(run(project))


def test_templates_and_dev_area_are_ignored(project):
    write(project, "docs/_templates/README.md", README)
    write(project, "docs/_templates/story.md", "---\nid: US-NNN\n---\n- **US-NNN.AC1** — {x}\n")
    write(project, "docs/dev/README.md", README)
    write(project, "docs/dev/diary/2026-10-25.md", "# notes\n")
    assert run(project).errors == []


def test_excluded_paths_are_not_scanned_for_markers(project):
    write(project, "src/vendor/test_fixture.py", '@pytest.mark.req("US-999.AC1")\n')
    report = trace_check.check(
        docs=project / "docs",
        test_roots=[project / "src"],
        root=project,
        exclude=[project / "src/vendor"],
    )
    assert report.errors == []


def test_ids_sort_numerically(project):
    for number in (999, 1000):
        write(
            project,
            f"docs/stories/US-{number}-story.md",
            STORY.replace("US-001", f"US-{number}"),
        )
    write(
        project,
        "src/tests/test_more.py",
        '@pytest.mark.req("US-999.AC1", "US-1000.AC1")\ndef test_x(): pass\n',
    )
    matrix = trace_check.render_matrix(run(project))
    assert matrix.index("| US-999.AC1 ") < matrix.index("| US-1000.AC1 ")


def test_cli_writes_matrix_and_returns_failure_code(project, tmp_path, monkeypatch):
    monkeypatch.chdir(project)
    write(project, "src/tests/test_signup.py", "")
    matrix = tmp_path / "out" / "matrix.md"
    code = trace_check.main(["--docs", "docs", "--tests", "src", "--matrix", str(matrix)])
    assert code == 1
    assert matrix.read_text().startswith("# Traceability matrix")
