# Documentation
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

Single entry point for this project's documentation. Folder and file names are in English; content is in English.

> New to the project? Start with [guides/onboarding.md](guides/onboarding.md).

## Map
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

| Folder                                  | Answers                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------ |
| [knowledge/](knowledge/README.md)       | What do we know about the product, the domain and the market?            |
| [prds/](prds/README.md)                 | Which problem does each epic solve, and how do we measure success?       |
| [stories/](stories/README.md)           | What must the system do, in verifiable terms?                            |
| [requirements/](requirements/README.md) | Which qualities and business rules apply across stories?                 |
| [pricing/](pricing/README.md)           | What do we sell, with which limits, and how do we bill it?               |
| [metrics/](metrics/README.md)           | What do we measure, and which events feed each measure?                  |
| [architecture/](architecture/README.md) | How is the system built today, and how do its parts fit together?        |
| [decisions/](decisions/README.md)       | Why is the architecture the way it is?                                   |
| [data/](data/README.md)                 | What data do we store, what does it mean, and how long do we keep it?    |
| [api/](api/README.md)                   | How do clients use our API?                                              |
| [integrations/](integrations/README.md) | What do we expect from third parties, and what happens when they fail?   |
| [security/](security/README.md)         | What are we protecting, from whom, and who may do what?                  |
| [design/](design/README.md)             | How does the product look and behave for the user?                       |
| [guides/](guides/README.md)             | How do we work on this codebase, and where does a newcomer start?        |
| [testing/](testing/README.md)           | How do we prove the system meets its requirements?                       |
| [operations/](operations/README.md)     | How do we keep production running?                                       |
| [legal/](legal/README.md)               | What do we owe users and regulators?                                     |
| [support/](support/README.md)           | How do we answer users?                                                  |
| [dev/](dev/README.md)                   | Personal working notes, outside Git.                                     |
| [_templates/](_templates/README.md)     | Starting points for new documents.                                       |

**`knowledge/` is descriptive:** it records context and evidence at a point in time and may age without the system being wrong. **Everything else is normative:** it states how the system is or must be, so a mismatch between a document and the system is a defect in one of them.

## ID conventions
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

| Artifact                | ID           | Example file                                         |
| ----------------------- | ------------ | ---------------------------------------------------- |
| User story              | `US-001`     | `stories/US-001-tenant-signup.md`                    |
| Acceptance criterion    | `US-001.AC1` | inside the story and in its tests                    |
| Non-functional req.     | `NFR-001`    | `requirements/non-functional.md`                     |
| Business rule           | `BR-001`     | `requirements/business-rules.md`                     |
| PRD                     | `PRD-001`    | `prds/PRD-001-billing.md`                            |
| Decision (ADR)          | `ADR-0001`   | `decisions/ADR-0001-schema-per-tenant.md`            |
| Research / spike        | file stem    | `knowledge/research/2026-10-payment-gateways.md`     |
| Postmortem              | file stem    | `operations/postmortems/2026-10-25-login-outage.md`  |

- **File names start with the ID**, so every ID can be found by file name alone.
- **IDs are immutable.** They are never reused or renumbered. The slug in the file name may change; the ID may not.
- **Gaps are expected.** If `US-001.AC2` is removed, the story keeps `AC1` and `AC3`; Git history explains the gap.
- **Next ID = highest existing ID + 1.** CI rejects duplicates created on parallel branches; the later PR renumbers before merging.
- **Padding is a minimum width**: three digits, four for ADRs. Numbers may grow past it (`US-1000`). Tooling sorts IDs numerically; plain file listings will misorder past the padding, which is accepted.
- **Dates follow ISO 8601** (`YYYY-MM` or `YYYY-MM-DD`). Dated documents use their file stem as their ID.

## Rules
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

- **Every folder has a `README.md`** stating its purpose, what goes in, what stays out, the naming convention and the template to use. CI enforces it, except inside `dev/`.
- **Traceability.** Each artifact cites, by ID, the artifacts it derives from. Links point upstream only; downstream views (which stories implement a PRD, which tests cover a story) are generated by CI, never maintained by hand.

  ```mermaid
  flowchart LR
    R[Research] --> PRD --> US[Story] --> AC[Acceptance criterion] --> T[Test]
    R --> ADR
    ADR --> US
    REQ[NFR / BR] --> US
    REQ --> T
  ```

- **Workflow status lives in GitHub Projects; content lives in Markdown.** The issue `[US-001] Tenant signup` links to the file, and the file does not record whether work is pending, in progress or done.
- **Lifecycle status lives in the document's front matter** when it changes how the document must be read: an ADR is `proposed`, `accepted`, `rejected`, `deprecated` or `superseded`; a research note is `current` or `superseded`; a PRD is `draft`, `approved` or `retired`.
- **Tests reference requirements by ID:** `@pytest.mark.req("US-001.AC1")` in the backend and `it("[US-001.AC1] ...")` in the frontend. NFRs and business rules verified by tests are referenced the same way (`NFR-003`). The [traceability check](../tools/trace-check/README.md) fails CI when:
  - an acceptance criterion has no test, unless it is tagged `[manual]`;
  - a test references an ID that does not exist;
  - an ID is defined twice, or a file name does not match its ID;
  - front matter does not match its schema, or cites an ID that does not exist.
- **Research and postmortems are dated and never rewritten.** Typos may be fixed; conclusions may not. When one becomes outdated, set `status: superseded` and `superseded_by:` in its front matter. Accepted ADRs follow the same rule: change them only by writing a new ADR that supersedes them.
- **Diagrams live in their own files** under [architecture/diagrams/](architecture/diagrams/README.md); documents link to them instead of embedding them, which keeps both small and lets each diagram be reviewed on its own.
- **AI changes are stamped.** Every section an AI agent changes carries a hidden comment below its heading with the session ID, the responsible person and the date and time: `<!-- author-stamp: session=... | author=... | at=... -->`. Each section keeps only its latest stamp. The [author-stamp skill](../.claude/skills/author-stamp/SKILL.md) writes them; never edit them by hand. Changes made by people without an agent are covered by Git history.
- **Docs change in the same pull request as the code they describe.** A PR that changes behavior without updating the affected document is not done.
- **Create a folder only when there is real content for it.** The other folders follow this standard on demand.

## Definition of Ready
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

A story can enter a sprint when:

1. Its PRD is `approved`.
2. Every acceptance criterion is written in EARS and has an ID.
3. The NFRs, business rules and ADRs it must respect are cited in its front matter.
4. Its open questions are answered, or explicitly deferred with a reason.
5. Its design is linked, or the story states that it has no UI.
6. The analytics events it must emit are listed in [metrics/](metrics/README.md).

## Definition of Done
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

A story is done when:

1. Every acceptance criterion has at least one passing automated test that references its ID, or is tagged `[manual]` with the verification evidence linked in the PR.
2. CI is green, including the traceability check and the documentation checks.
3. The code was reviewed and merged following [guides/](guides/README.md), with approval from the code owners of every document it touches.
4. Every NFR and business rule the story cites still holds.
5. Any structural decision taken during the work is recorded as an accepted ADR.
6. Analytics events required by [metrics/](metrics/README.md) are implemented and visible in PostHog.
7. Documents affected by the change are updated in the same PR: architecture, API overview, data dictionary, permission matrix, integrations, runbooks, privacy inventory.
8. The change is released to production (or behind a feature flag) and smoke-tested.

## Developer area
<!-- author-stamp: session=9baba3f5-a92d-43a4-97f8-09b458e7a11b | author=Kaio Vinícios <kvsgpro@outlook.com> | at=2026-10-25T15:26:33-03:00 -->

[`dev/`](dev/README.md) is personal. Git tracks only its README and the `.keep` files that create its folders; everything you write inside stays local. Anything another developer would need belongs in [guides/](guides/README.md) or in the folder that owns it.
