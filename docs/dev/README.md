# Developer area

Personal, local working space. Git tracks only this README and the empty `.keep` files that create the folders on clone; everything you write inside stays out of Git.

```text
docs/dev/                 # local, outside Git (except the README and .keep files)
├── README.md             # versioned: explains this folder and the promotion rule
├── notes.md              # personal scratchpad
├── handoff.md            # where I stopped / next step
├── til.md                # learnings (today I learned)
├── diary/                # YYYY-MM-DD.md, focused on the why
├── investigations/       # bugs in progress
├── scratch/              # SQL, .http, payloads
└── prompts/              # personal reusable prompts
```

The folders arrive with the clone. The three files are created on first use, since Git cannot version a file once and then stop tracking its changes:

```sh
touch docs/dev/notes.md docs/dev/handoff.md docs/dev/til.md
```

## Rules

- **Local and personal.** Anything another developer would need goes to [guides/](../guides/README.md).
- **Promote what becomes useful to the project:**
  - a structural decision in the diary → an ADR in [decisions/](../decisions/README.md)
  - a relevant investigation → a postmortem in [operations/postmortems/](../operations/postmortems/README.md)
  - a useful prompt → a command in `.claude/commands/`
- **Never store secrets**, even outside Git. Credentials live in the password manager or in `.env`.
- **No automatic backup.** `git clean -fdx` deletes ignored files, including everything here except the tracked skeleton. If the content has value, sync it with a separate private repository or cloud storage.
- **Do not edit or delete the `.keep` files.** They are tracked; any change to them shows up in `git status`.

## `.gitignore`

```gitignore
docs/dev/**
!docs/dev/**/
!docs/dev/README.md
!docs/dev/**/.keep
```

The second line re-includes directories, which Git requires before it can re-include files inside them; the last two lines re-include the skeleton.

## Diary template (`diary/YYYY-MM-DD.md`)

The *what* is already in `git log`; the diary records the *why*.

```markdown
# YYYY-MM-DD

## What I did
- Short summary, citing IDs when there are any (US-001.AC2, ADR-0003)

## Decisions
- What I decided and why (if it is structural → open an ADR)

## Blockers
- What got stuck or is still unanswered

## Next step
- Where to start next session (also update handoff.md)
```
