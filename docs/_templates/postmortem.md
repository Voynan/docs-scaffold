---
title: "{What failed, in a few words}"
date: YYYY-MM-DD # day the incident started
severity: SEV2 # SEV1 | SEV2 | SEV3
authors: ["{name}"]
status: current # current | superseded
---

# {What failed, in a few words}

> Blameless: describe how the system and process allowed the failure, not who caused it.
> Dated document. Do not rewrite conclusions after review.

## Summary

{Two or three sentences: what happened, impact, how it was resolved.}

## Impact

- **Users affected:** {count or share, which tenants}
- **Duration:** {start → end, UTC}
- **Data:** {lost, corrupted, exposed, or "None"}
- **SLO / NFR breached:** {NFR-NNN or SLO name, or "None"}

## Timeline (UTC)

| Time  | Event |
| ----- | ----- |
| HH:MM | {first symptom, alert, action, recovery} |

## Detection

{How we found out. How long between start and detection, and how to shorten it.}

## Root cause and contributing factors

{The causal chain. Ask "why" until you reach something the team can change.}

## Resolution

{What restored service. Link the runbook used, or note that one was missing.}

## What went well

- {Item}

## What went poorly

- {Item}

## Where we got lucky

- {Item}

## Action items

Each item is a GitHub issue; its status lives there.

| Type                       | Action   | Issue |
| -------------------------- | -------- | ----- |
| prevent / detect / mitigate | {action} | #NNN  |
