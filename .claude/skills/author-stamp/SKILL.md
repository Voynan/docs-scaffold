---
name: author-stamp
description: Use when creating, editing, rewriting, moving or fixing any Markdown file under docs/, including one-line fixes and edits made in passing while working on code.
---

# author-stamp

Every change an AI session makes to a Markdown file under `docs/` records who made it: the session ID, the responsible person and the date and time. The record is a hidden HTML comment right below the heading of each changed section. Untouched sections keep their stamps, and each section holds only its latest stamp.

## Edits with Edit or Write: automatic

In Claude Code, `.claude/settings.json` runs the script as a hook around every `Edit`, `Write` and `MultiEdit` call. Nothing to do: after each call the hook reports which sections it stamped. Re-read the file before editing it again, since the stamp lines changed it.

## Any other kind of change: run the script yourself

Shell commands (`sed`, `mv`, `git mv`, scripts), generated files, and agents without the hook are not covered by it. Wrap those changes:

1. **Before** changing the files, take a snapshot. This also works for files that do not exist yet:

   ```sh
   python3 "${CLAUDE_SKILL_DIR}/scripts/stamp.py" begin --session "${CLAUDE_SESSION_ID}" docs/stories/US-001-signup.md
   ```

2. **Change** the files.
3. **After** the last change, and before reporting the work as done or committing it:

   ```sh
   python3 "${CLAUDE_SKILL_DIR}/scripts/stamp.py" end --session "${CLAUDE_SESSION_ID}" docs/stories/US-001-signup.md
   ```

4. **Read the output.** The stamped sections should match the sections you meant to change.

## Stamp format

```markdown
## Context
<!-- author-stamp: session=3f9c2a71-5b8e-4d0a-9e61-7c2b4f1d8a90 | author=Ana Souza <ana@example.com> | at=2026-10-25T15:42:10-03:00 -->
```

A section runs from one heading to the next. Front matter belongs to the first section.

## Quick reference

| Situation | What to do |
| --- | --- |
| You forgot `begin` before a shell change | Run `end` anyway. It compares with `HEAD`, so uncommitted changes made earlier by someone else also get your stamp; tell the user. |
| Git `user.name` is not set | Ask the user who is responsible and pass `--author "Name <email>"`. |
| You rewrote a whole file | Nothing extra: stamps of sections whose content did not change are restored. |
| A stamp line is in the text you are editing | Leave it as it is. The script owns those lines. |
| The file is outside `docs/`, is not Markdown, is in `docs/_templates/` or is ignored by Git | The script skips it, so you can pass it anyway. |
