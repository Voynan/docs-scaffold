<!-- markdownlint-disable-file first-line-heading -->
<!--
Append this entry to requirements/non-functional.md under the heading of its quality characteristic.
ISO/IEC 25010 characteristics: functional suitability, performance efficiency, compatibility,
interaction capability, reliability, security, maintainability, flexibility, safety.
-->

### NFR-NNN — {Short title}

- **Characteristic:** {ISO/IEC 25010 characteristic}
- **Requirement:** {EARS statement, e.g. "While under normal load, the API shall answer read requests within 300 ms."}
- **Fit criterion:** {Measurable threshold and conditions, e.g. "p95 ≤ 300 ms at 50 RPS over 10 minutes, staging hardware."}
- **Verification:** {load test in CI | monitoring alert | security scan | manual review} — {link}
- **Scope:** {whole system | component | endpoints}
- **Rationale:** {Why this threshold; link the source}
- **Source:** {PRD-NNN | ADR-NNNN | research note | regulation}
