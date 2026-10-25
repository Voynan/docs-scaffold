# Operations

Everything that keeps the system running in production.

| Folder                                           | Content                                                         |
| ------------------------------------------------ | --------------------------------------------------------------- |
| [runbooks/](runbooks/README.md)                  | Step-by-step procedures: deploy, rollback, backup restore, secret rotation |
| [infrastructure/](infrastructure/README.md)      | Service map (Railway, R2, DNS, Sentry), environments, monthly costs |
| [observability/](observability/README.md)        | Configured alerts, dashboards and what each alert means         |
| [postmortems/](postmortems/README.md)            | Incident analyses: timeline, root cause, actions                |

## What does not go here

- Why the infrastructure is shaped this way → [decisions/](../decisions/README.md)
- Third-party contracts and failure handling → [integrations/](../integrations/README.md)
