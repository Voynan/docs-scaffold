# Architecture overview

> Lightweight arc42. Describe the system as it is today; link ADRs for the reasons and diagram files for the pictures.
> Last checked against the system: YYYY-MM-DD.

## 1. Goals and constraints

- **Quality goals:** the three to five NFRs that shape the architecture most, by ID (NFR-NNN)
- **Constraints:** {regulation, budget, team size, mandated technology}

## 2. Context

{Who and what the system talks to: users, roles, external systems. What crosses each boundary.}

Diagram: [c4-context-{system}](diagrams/c4-context-{system}.md)

## 3. Building blocks

{The containers (apps, services, databases, queues) and the responsibility of each. One short paragraph per container.}

Diagram: [c4-container-{system}](diagrams/c4-container-{system}.md)

## 4. Runtime

{The critical flows and what happens in each, step by step at the level of containers.}

Diagrams: [sequence-{flow}](diagrams/sequence-{flow}.md)

## 5. Deployment

{Where each container runs, environments, how a change reaches production. Link operations/infrastructure/ for the inventory.}

## 6. Cross-cutting concepts

{Decisions that apply everywhere, each with its ADR: multi-tenancy, authentication and authorization, error handling, logging and tracing, configuration, background jobs, internationalization.}

## 7. Risks and technical debt

| Risk or debt | Impact      | Mitigation or plan   |
| ------------ | ----------- | -------------------- |
| {statement}  | {impact}    | {action, issue link} |
