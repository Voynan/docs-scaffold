# Requirements

Requirements that cut across several stories.

## What goes here

| File                 | Content                                                        | IDs       |
| -------------------- | -------------------------------------------------------------- | --------- |
| `non-functional.md`  | Quality requirements, grouped by ISO/IEC 25010 characteristic  | `NFR-001` |
| `business-rules.md`  | Policies of the client's business, grouped by domain area      | `BR-001`  |

## What does not go here

- Behavior specific to one story → that story's acceptance criteria
- Descriptions of the business without an enforceable rule → [knowledge/domain/](../knowledge/domain/README.md)

## Rules

- Every NFR has a measurable fit criterion and a verification method. An NFR nobody can verify is a wish.
- Stories cite the NFRs and BRs they must respect; tests that verify an NFR reference its ID.
- When a file grows unwieldy, split it by characteristic or area (`non-functional/performance.md`). IDs do not change.

## Templates

[nfr.md](../_templates/nfr.md), [business-rule.md](../_templates/business-rule.md)
