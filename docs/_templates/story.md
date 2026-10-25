---
id: US-NNN
title: "{Short imperative title}"
prd: PRD-NNN
# Optional: cross-cutting requirements and decisions this story must respect.
requirements: [NFR-NNN, BR-NNN]
decisions: [ADR-NNNN]
---

# US-NNN — {Short imperative title}

**As a** {role}, **I want** {capability}, **so that** {benefit}.

## Context

{Why this story exists now. Link the PRD section, research or support tickets it comes from.}

## Acceptance criteria

Write each criterion in EARS. Keep one behavior per criterion, so one failing test points to one broken behavior.

| Pattern         | Shape                                                        |
| --------------- | ------------------------------------------------------------ |
| Ubiquitous      | The {system} shall {response}.                               |
| Event-driven    | When {trigger}, the {system} shall {response}.               |
| State-driven    | While {state}, the {system} shall {response}.                |
| Unwanted        | If {condition}, then the {system} shall {response}.          |
| Optional        | Where {feature is enabled}, the {system} shall {response}.   |

- **US-NNN.AC1** — When {trigger}, the {system} shall {response}.
- **US-NNN.AC2** — If {condition}, then the {system} shall {response}.
- **US-NNN.AC3** [manual] — The {system} shall {response}.

Tag a criterion `[manual]` only when it cannot be automated; link the verification evidence in the PR.

## Analytics

{Events from metrics/ this story emits, or "None".}

## Design

{Figma link or design/ document, or "None".}

## Out of scope

- {What a reader might expect here but is deliberately left out}

## Open questions

- {Question} — {who can answer}
