---
paths:
  - "**/test_*.py"
  - "**/*_test.py"
  - "**/conftest.py"
  - "**/*.test.{js,jsx,mjs,cjs,ts,tsx,mts,cts}"
  - "**/*.spec.{js,jsx,mjs,cjs,ts,tsx,mts,cts}"
---

# Tests and requirement IDs

Tests prove the acceptance criteria in `docs/stories/`. The traceability check fails CI when a criterion has no test or a test cites an ID that does not exist.

- A test that verifies an acceptance criterion, NFR or business rule references its ID:
  - Python: `@pytest.mark.req("US-001.AC1")`, several allowed: `req("US-001.AC1", "NFR-002")`
  - JavaScript/TypeScript: `it("[US-001.AC1] ...")` or `test("[US-001.AC1] ...")`, several allowed: `[US-001.AC1, US-001.AC2]`
- Keep the marker on one line; markers split across lines or in dynamic titles such as `test.each(...)` are not detected.
- Cite only IDs that exist in `docs/`. When a behavior has no criterion yet, add the criterion to its story first.
- Run `python tools/trace-check/trace_check.py --tests <test folders>` before reporting work as done.
