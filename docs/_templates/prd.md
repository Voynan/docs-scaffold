---
id: PRD-NNN
title: "{Epic name}"
status: draft # draft | approved | retired
owner: "{name}"
# Optional: research and knowledge this PRD builds on.
research: [YYYY-MM-slug]
---

# PRD-NNN — {Epic name}

## Problem

{Who has the problem, how it shows up today, and the evidence that it is worth solving. Describe the problem, not the solution.}

## Goals

- {Outcome the epic must achieve}

## Non-goals

- {Outcome a reader might expect but this epic will not pursue}

## Success metrics

| Metric   | Baseline | Target | Source (event / query)  | Measured at        |
| -------- | -------- | ------ | ----------------------- | ------------------ |
| {metric} | {value}  | {value} | {PostHog event or query} | {date or milestone} |

## Users

{Personas from knowledge/product/ affected by this epic.}

## Scope

### In scope

- {Capability}

### Out of scope

- {Capability}

## Constraints and dependencies

- {Regulation, deadline, third party, NFR or ADR that limits the solution}

## Risks and assumptions

| Assumption or risk | Impact if wrong | How we will validate |
| ------------------ | --------------- | -------------------- |
| {statement}        | {impact}        | {experiment or check} |

## Release plan

{Milestones or phases, and what ships in each.}

## Open questions

- {Question} — {who can answer}

---

Stories that implement this PRD cite `prd: PRD-NNN`; their list comes from the epic in GitHub Projects or from the generated traceability matrix, not from this file.
