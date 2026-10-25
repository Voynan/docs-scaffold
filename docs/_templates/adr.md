---
id: ADR-NNNN
title: "{Decision stated as a short noun phrase}"
status: proposed # proposed | accepted | rejected | deprecated | superseded
date: YYYY-MM-DD
deciders: ["{name}"]
# Optional: what this decision builds on or replaces.
drivers: [NFR-NNN, PRD-NNN, YYYY-MM-research-slug]
supersedes: ADR-NNNN
superseded_by: ADR-NNNN
---

# ADR-NNNN — {Decision stated as a short noun phrase}

## Context

{The forces at play: the problem, constraints, quality requirements and facts that make a decision necessary. Write it so a reader who was not there understands why this mattered.}

## Decision drivers

- {Driver, preferably an NFR or business rule ID}

## Considered options

1. **{Option A}** — {one-line summary}
2. **{Option B}** — {one-line summary}
3. **{Option C}** — {one-line summary}

| Driver   | Option A | Option B | Option C |
| -------- | -------- | -------- | -------- |
| {driver} | {+ / − / ±, short note} | | |

## Decision

We will {decision}, because {the drivers that tipped the balance}.

## Consequences

- **Positive:** {what becomes easier}
- **Negative:** {what becomes harder, the debt we accept}
- **Follow-up:** {work this decision creates, as issues}

## Verification

{How we will know the decision is being followed and still holds: a test, a lint rule, a metric, a review checkpoint.}
