# Security

What we protect, from whom, and who may do what.

## What goes here

- `threat-model.md` — assets, trust boundaries, threats (STRIDE) and mitigations
- `permissions.yaml` — the RBAC matrix: roles × resources × actions, in a machine-readable format
- `permissions.md` — what each role is for, and the reasoning behind non-obvious grants
- `owasp-checklist.md` — OWASP ASVS or Top 10 checklist with status per item and evidence

## What does not go here

- Secrets, credentials, vulnerability details not yet fixed → never in the repository
- Incident analysis → [operations/postmortems/](../operations/postmortems/README.md)

## Rules

- **`permissions.yaml` is the source of truth for authorization.** A parametrized test reads it and checks every role × resource × action against the code, so the matrix is an executable specification rather than a description that drifts:

  ```python
  MATRIX = yaml.safe_load(Path("docs/security/permissions.yaml").read_text())
  CASES = [
      (role, resource, action, role in allowed)
      for resource, actions in MATRIX["resources"].items()
      for action, allowed in actions.items()
      for role in MATRIX["roles"]
  ]

  @pytest.mark.req("NFR-NNN")  # the NFR that requires role-based access control
  @pytest.mark.parametrize("role,resource,action,expected", CASES)
  def test_permission_matrix(role, resource, action, expected):
      assert can(role, resource, action) is expected
  ```

- Changing a permission means changing `permissions.yaml` and the code in the same PR; the test fails otherwise.
- Review the threat model when a trust boundary changes: new integration, new role, new public endpoint.

## Template

[permissions.yaml](../_templates/permissions.yaml)
