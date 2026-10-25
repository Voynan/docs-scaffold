# docs-scaffold

Standard `docs/` structure for Voynan projects: requirements, user stories, ADRs, diagrams, tests, operations, and legal, with per-folder READMEs, templates, and ID conventions for end-to-end traceability.

## What is in here

| Path                                                     | Content                                                                   |
| -------------------------------------------------------- | ------------------------------------------------------------------------- |
| [`docs/README.md`](docs/README.md)                       | The standard: folder map, ID conventions, rules, Definitions of Ready and Done |
| [`docs/_templates/`](docs/_templates/README.md)          | Templates for every document type, the RBAC matrix and `CODEOWNERS`      |
| `docs/**/README.md`                                      | One per folder: purpose, what goes in, what stays out, naming, template   |
| [`tools/trace-check/`](tools/trace-check/README.md)      | Traceability checker and front matter schemas                             |
| [`.github/workflows/docs.yml`](.github/workflows/docs.yml) | CI gates: traceability, Markdown lint, links, Mermaid rendering         |
| [`.claude/skills/author-stamp/`](.claude/skills/author-stamp/SKILL.md) | Agent skill that stamps every AI change in `docs/` with session, author and time |
| [`.claude/settings.json`](.claude/settings.json)         | Claude Code hooks that run author-stamp around every Edit and Write       |
| [`.claude/rules/`](.claude/rules/)                       | Agent instructions loaded only when working in `docs/` or in test files   |
| [`CLAUDE.md`](CLAUDE.md)                                 | The few always-loaded lines about docs, to merge into a project's `CLAUDE.md` |
| [`.markdownlint-cli2.jsonc`](.markdownlint-cli2.jsonc)   | Markdown lint rules                                                       |
| [`.gitignore`](.gitignore)                               | Keeps personal `docs/dev/` content out of Git while versioning its skeleton |

## Supported languages

The documentation, the templates and the author-stamp skill work with any language. The traceability checker reads `docs/` for any project too, but it only finds test markers in **Python** (`@pytest.mark.req("US-001.AC1")`) and **JavaScript/TypeScript** (`it("[US-001.AC1] ...")`, `test("[US-001.AC1] ...")`).

Tests written in any other language are invisible to it: every criterion they verify is reported as `has no test` and CI fails. A marker split across lines is not detected either. To support another language, extend the checker as described in [`tools/trace-check/README.md`](tools/trace-check/README.md#supported-languages).

## Adopting it in a project

### Prerequisites

- **Python 3.10+** as `python3` on every machine that runs Claude Code in the project (the author-stamp hook calls it on every edit) and in CI (installed by the workflow).
- **Node.js** to run markdownlint locally (CI installs it).
- **Git identity** set with `git config user.name` and `user.email`: stamps record it as the responsible person.

### 1. Copy the files

Copy everything from this repository into the project except `README.md`, `LICENSE` and `.git/`. Files that collide with ones the project already has are merged in step 2.

This repository is the full catalog. A project keeps only the `docs/` folders it has real content for, plus `docs/README.md`, `docs/_templates/`, `docs/guides/` and `docs/dev/`. Folder READMEs link to each other, so after removing folders, also remove their rows from the map in `docs/README.md` and the links to them in `docs/guides/onboarding.md` and the remaining READMEs. The link check in CI lists every link left behind. When a removed folder gets its first document later, copy its `README.md` back and restore its links.

### 2. Merge with the project's own files

| File | What to do |
| --- | --- |
| `.gitignore` | Append this repository's lines **before** creating anything in `docs/dev/`, so personal notes are never staged. |
| `CLAUDE.md` | Paste only the "Documentation" section into the project's `CLAUDE.md`. The "This repository" section is about the scaffold. |
| `.claude/settings.json` | Merge the `hooks` block into the project's file, keeping its existing hooks. |
| `.claude/rules/` | Keep both rule files. Adjust the `paths` in `requirement-tests.md` if the project names test files differently. |
| `.markdownlint-cli2.jsonc` | Merge the rules into any existing markdownlint config, and add generated Markdown (changelogs, API docs) to `ignores`. |
| `.github/workflows/docs.yml` | Set `--tests` to the folders that hold tests (e.g. `--tests backend frontend`) and the `push` branch if the default branch is not `main`. |

Agent guidance is split by when it is needed: the `CLAUDE.md` section is always in context, so it holds only what applies to every code change; the rules load only when the agent works in `docs/` or in test files, so they cost nothing while it works on product code.

### 3. Configure the repository

1. Copy `docs/_templates/CODEOWNERS` to `.github/CODEOWNERS` and set the real teams.
2. In the branch protection of the default branch, enable **Require review from Code Owners** and mark the jobs of the `Docs` workflow as **required status checks**. Without the second setting a failing check does not block the merge.
3. Register the `req` pytest marker as shown in [`docs/testing/README.md`](docs/testing/README.md).
4. Create the GitHub Projects board; issues are titled `[US-001] ...` and link to the story file.

### 4. Verify

```sh
pip install -r tools/trace-check/requirements.txt
python tools/trace-check/trace_check.py --tests <test folders>
npx markdownlint-cli2
```

Then open a **new** Claude Code session (hooks load at startup), ask it to edit any Markdown file in `docs/`, and check that an `<!-- author-stamp: ... -->` line appeared below the edited heading.

### Opting out of the tooling

`tools/` and `.github/` enforce the conventions; they are not required to use the documentation structure. If the conventions do not suit a project, for example because its tests are in a language the checker does not support, delete either folder:

- **Delete `tools/`** to drop the traceability checker. Also delete the `traceability` job in `.github/workflows/docs.yml` if you keep that folder, and edit the "Tests reference requirements by ID" rule in `docs/README.md`, since nothing will enforce it anymore.
- **Delete `.github/`** to drop every CI gate. The checker can still run by hand: `python tools/trace-check/trace_check.py`.

## Developing the scaffold

```sh
pip install -r tools/trace-check/requirements.txt pytest
python -m pytest tools/trace-check/tests .claude/skills/author-stamp/tests
python tools/trace-check/trace_check.py
npx markdownlint-cli2
```

## License

[MIT](LICENSE)
