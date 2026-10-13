---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into issues.
disable-model-invocation: true
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

The issue tracker and label vocabulary should be configured in the project's `CLAUDE.md` or equivalent context file before using this skill.

Before publishing, read the **Issue tracker** section of the project's root `CLAUDE.md` — it defines the repo, the label axes (`state:`, `type:`, `area:`), the milestones and the board. Provision any missing label with `gh label create` (ignore "already exists"). Never invent a label or milestone outside that section; if the work needs one, ask. Every issue gets exactly one milestone from that list (`--milestone`) and is added to the board (`--project`). Issue titles and bodies are written in Portuguese.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes an issue reference (issue number, URL, or path) as an argument, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft the issues

Break the plan into **tracer bullet** issues, following the **Vertical slice rules**. A **wide refactor** is the exception to that rule — slice it by **expand–contract** instead (see **Wide refactors**).

Slices may be **HITL** or **AFK**. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Publish the issues to the issue tracker

For each approved slice, publish a new issue to the issue tracker using the **Issue body template**. AFK slices are born `state:ready-for-agent` ("especificado, pode começar"); HITL slices are born `state:ready-for-human`.

Publish issues in dependency order (blockers first) so you can reference real issue numbers. Link each slice natively — `gh` ≥ 2.94 does it by issue **number**:

```bash
gh issue create --title "<título>" --body-file <arquivo> \
  --label "state:ready-for-agent,type:enhancement,area:<area>" \
  --milestone "<milestone>" --project "<board>" \
  --parent <nº do PRD> --blocked-by <nº>,<nº>
```

Keep the `## Parent` and `## Blocked by` body sections as well — they are the readable fallback.

Do NOT close or modify any parent issue.

## Reference

### Vertical slice rules

Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Any prefactoring should be done first

### Wide refactors

A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own issue blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in an issue blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify issue — green is promised only there.

### Issue body template

<issue-template>
## Parent

A reference to the parent issue on the issue tracker (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced code that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype, trimmed to the decision-rich parts.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.
</issue-template>
