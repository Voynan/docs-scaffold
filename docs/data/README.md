# Data

The data model, what each field means and how long we keep it.

## What goes here

- `schema.dbml` — the data model in DBML, **generated** from the migrated database
- `dictionary.md` — each table and column: meaning, allowed values, personal data flag
- `retention.md` — retention period and deletion method per data category

## What does not go here

- Migrations → the application code
- Legal basis for processing personal data → [legal/privacy/](../legal/privacy/README.md), which this folder references

## Rules

- **Migrations are the source of truth for the schema.** `schema.dbml` is derived from them and never edited by hand; two hand-maintained models always drift. Regenerate it after applying migrations to a local database:

  ```sh
  npx @dbml/cli db2dbml postgres "$DATABASE_URL" -o docs/data/schema.dbml
  ```

  CI can enforce freshness by running the migrations on an ephemeral database, regenerating the file and failing on `git diff --exit-code docs/data/schema.dbml`.
- `dictionary.md` explains meaning, which the schema cannot. Types and constraints are read from `schema.dbml`; do not repeat them.
- Columns holding personal data are flagged in the dictionary and listed in the privacy inventory.
