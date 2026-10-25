# trace-check

Enforces the traceability rules of the [documentation standard](../../docs/README.md) and generates the traceability matrix.

## What it checks

| Check                     | Fails when                                                                        |
| ------------------------- | --------------------------------------------------------------------------------- |
| Coverage                  | an acceptance criterion has no test and is not tagged `[manual]`                  |
| Test references           | a test cites an ID that does not exist, or a string that is not a valid ID        |
| Uniqueness                | an ID is defined twice (two story files, two `### NFR-001` headings, ...)         |
| File names                | a file does not follow its folder's convention, or its name and `id` disagree     |
| Front matter              | it is missing, is not valid YAML, does not match its [schema](schemas/), or cites an ID that does not exist |
| Stories                   | a story has no acceptance criteria, or a criterion's ID belongs to another story  |
| Folder READMEs            | a folder under `docs/` has no `README.md` (`_templates/` and `dev/` are skipped)  |

## What it reads

| Source                                   | Defines                                    |
| ---------------------------------------- | ------------------------------------------ |
| `docs/stories/US-NNN-slug.md`            | `US-NNN` and each `- **US-NNN.ACn** —` line |
| `docs/prds/PRD-NNN-slug.md`              | `PRD-NNN`                                  |
| `docs/decisions/ADR-NNNN-slug.md`        | `ADR-NNNN`                                 |
| `docs/knowledge/research/YYYY-MM-slug.md` | the file stem                             |
| `docs/operations/postmortems/YYYY-MM-DD-slug.md` | the file stem                      |
| headings in `docs/requirements/**/*.md`  | `NFR-NNN` and `BR-NNN`                     |
| test files (`.py`, `.js`, `.ts`, ...)    | references through `@pytest.mark.req("...")` and `it("[...] ...")` / `test("[...] ...")` |

## Supported languages

Reading `docs/` works for any project. Finding test markers depends on the language, and only two are supported:

| Language                | File extensions                                         | Marker                                              |
| ----------------------- | ------------------------------------------------------- | --------------------------------------------------- |
| Python                  | `.py`                                                   | `@pytest.mark.req("US-001.AC1")` (or `@mark.req`)   |
| JavaScript / TypeScript | `.js` `.jsx` `.mjs` `.cjs` `.ts` `.tsx` `.mts` `.cts`   | `it("[US-001.AC1] ...")` or `test("[US-001.AC1] ...")`, including `it.only`, `test.skip`, ... |

- **Other languages are not scanned.** Their tests are invisible, so every criterion they verify is reported as `has no test` and CI fails. The checker errs on the side of failing, never on the side of passing.
- **A marker must fit on one line.** Markers split across lines, and titles built dynamically such as `test.each([...])("[US-001.AC1] ...")`, are not detected.
- **Adding a language** means adding its file extensions to `TEST_SUFFIXES` and a regular expression for its marker in `trace_check.py`, with a test in `tests/`.

The checker itself needs Python 3.10+ to run, whatever the project's language.

## Usage

```sh
pip install -r tools/trace-check/requirements.txt
python tools/trace-check/trace_check.py --tests backend frontend --matrix traceability.md
```

Or, with [uv](https://docs.astral.sh/uv/), without installing anything: `uv run tools/trace-check/trace_check.py`.

| Option       | Default | Meaning                                                    |
| ------------ | ------- | ---------------------------------------------------------- |
| `--docs`     | `docs`  | documentation root                                         |
| `--tests`    | `.`     | folders scanned for test markers                           |
| `--exclude`  | none    | folders not scanned (vendored code, fixtures)              |
| `--matrix`   | none    | where to write the generated matrix                        |

`.git`, `node_modules`, virtual environments, build output, `docs/` and the checker itself are never scanned for markers. Exit code is `1` when there is at least one error. Inside GitHub Actions, errors are printed as annotations on the offending lines.

## The matrix

The matrix lists every criterion with its story, PRD and the tests that verify it; every NFR and business rule with its tests and the stories that cite it; and the stories citing each PRD and ADR. It is the generated downstream view of the upstream links in front matter. CI publishes it in the job summary and as the `traceability-matrix` artifact. Do not commit it.

## Development

```sh
python -m pytest tools/trace-check/tests
```
