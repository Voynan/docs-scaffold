# CLAUDE.md

## Documentation

This project follows the Voynan docs standard ([`docs/README.md`](docs/README.md)). Detailed rules load from `.claude/rules/` when working in `docs/` or in test files.

- A change that alters behavior updates the affected documents in `docs/` in the same change.
- Before reporting work as done, run `python tools/trace-check/trace_check.py --tests <test folders>` and fix every error.

## This repository

This is the scaffold itself, not a product. Also run `python -m pytest tools/trace-check/tests .claude/skills/author-stamp/tests` and `npx markdownlint-cli2`.
