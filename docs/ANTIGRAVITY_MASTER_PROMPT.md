# Antigravity Master Prompt for VeriLift

Copy this at the start of a new Antigravity session.

```text
You are building VeriLift, a hackathon prototype.

Before doing anything, read:
1. docs/PROJECT_CONTEXT.md
2. docs/PHASE_PLAN.md
3. docs/PHASE_LOCK_RULES.md
4. docs/FORMULAS_LOCK.md
5. docs/DATA_SCHEMA.md
6. docs/UI_SPEC.md
7. docs/ACCEPTANCE_TESTS.md

You must follow strict phase locking.

Do not move to the next phase unless I explicitly say:
PHASE X PASSED. MOVE TO PHASE Y.

Do not add features outside the current phase.
Do not add authentication.
Do not add real payment integrations.
Do not change the formulas without my approval.
Do not replace Streamlit with another stack.
Do not rewrite unrelated files.

After completing a phase, stop and tell me:
- files changed
- how to test
- acceptance checklist
- what exact phrase I must reply with to move forward

Current phase: [PASTE PHASE NUMBER HERE]
```
