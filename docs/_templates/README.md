# Templates

Starting points for new documents. Copy the file into the target folder, rename it following that folder's convention, and replace every `{placeholder}`.

| Template                                                 | Use for                                 | Copy to                                       |
| -------------------------------------------------------- | --------------------------------------- | --------------------------------------------- |
| [story.md](story.md)                                     | A user story with acceptance criteria   | `stories/US-NNN-slug.md`                      |
| [prd.md](prd.md)                                         | One epic's problem, goals and scope     | `prds/PRD-NNN-slug.md`                        |
| [adr.md](adr.md)                                         | One architectural decision              | `decisions/ADR-NNNN-slug.md`                  |
| [research.md](research.md)                               | A dated research note or spike          | `knowledge/research/YYYY-MM-slug.md`          |
| [nfr.md](nfr.md)                                         | One entry of the NFR catalog            | append to `requirements/non-functional.md`    |
| [business-rule.md](business-rule.md)                     | One entry of the business rule catalog  | append to `requirements/business-rules.md`    |
| [architecture-overview.md](architecture-overview.md)     | The current architecture description    | `architecture/overview.md`                    |
| [diagram.md](diagram.md)                                 | One Mermaid diagram                     | `architecture/diagrams/<kind>-<subject>.md`   |
| [permissions.yaml](permissions.yaml)                     | The RBAC matrix, read by tests          | `security/permissions.yaml`                   |
| [postmortem.md](postmortem.md)                           | One incident analysis                   | `operations/postmortems/YYYY-MM-DD-slug.md`   |
| [CODEOWNERS](CODEOWNERS)                                 | Required reviewers per folder           | `.github/CODEOWNERS`                          |

The diary template lives in [dev/README.md](../dev/README.md) because diaries are never versioned.

## Front matter

Templates start with YAML front matter. Keep its keys: the [traceability check](../../tools/trace-check/README.md) validates them against a schema and resolves every ID they cite. Remove optional keys you do not use instead of leaving placeholders behind.

Placeholders use braces (`{name}`), not angle brackets: GitHub hides `<name>` as an unknown HTML tag. Inside front matter, quote values that contain braces.
