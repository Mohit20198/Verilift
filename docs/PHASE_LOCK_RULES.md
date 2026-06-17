# Phase Lock Rules for Antigravity

Antigravity must follow these rules throughout the project.

## Golden Rule
Do not move to the next phase unless the user explicitly writes:

`PHASE X PASSED. MOVE TO PHASE Y.`

## Before Starting Any Phase
1. Read `docs/PROJECT_CONTEXT.md`.
2. Read `docs/PHASE_PLAN.md`.
3. Identify the current phase.
4. Modify only the files listed for that phase.
5. State what files will be changed before changing them.

## After Finishing Any Phase
After completing any phase, stop and provide:
1. files created/modified
2. how to test
3. expected output
4. any issues found

Do not move to the next phase unless the user explicitly says: `PHASE X PASSED. MOVE TO PHASE Y.`

## Forbidden Behaviors
- Do not jump phases.
- Do not add features not requested in the current phase.
- Do not refactor working code unless necessary.
- Do not change formulas silently.
- Do not change file structure silently.
- Do not replace the stack.
- Do not add authentication or real payment flows.

## Phase Completion Response Template
Use this exact response after completing a phase:

```text
Phase X completed.

Files changed:
- ...

How to test:
- ...

Acceptance checklist:
[ ] ...
[ ] ...
[ ] ...

Please test this phase. If it works, reply:
PHASE X PASSED. MOVE TO PHASE Y.
```
