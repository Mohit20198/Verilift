# AGENTS.md — VeriLift Build Rules for Antigravity

You are building **VeriLift**, a hackathon prototype for TeXpedition 2026.

## Product
**VeriLift — Verified Incrementality Settlement Layer for Retail Media**

**Tagline:** Pay for verified lift, not self-reported ROAS.

## Theme Alignment
Theme 02: AI for seamless customer experiences across channels while defining clear measures of success.

VeriLift aligns with the theme by making the success metric clear and enforceable:

- Success metric = verified incremental lift
- Payment release = based on verified lift, not claimed ROAS
- CX benefit = brands stop scaling campaigns that only retarget customers who would have bought anyway

## Strict Build Rules
1. Always read `docs/PROJECT_CONTEXT.md` before changing code.
2. Always read `docs/PHASE_PLAN.md` before starting any phase.
3. Do not move to the next phase unless the user explicitly says:
   `PHASE X PASSED. MOVE TO PHASE Y.`
4. Do not rewrite unrelated files.
5. Do not add authentication.
6. Do not add real payment/escrow integration.
7. Do not add real retail media APIs.
8. Do not replace Streamlit with React/FastAPI unless the user explicitly asks.
9. Do not change formulas unless the user explicitly approves.
10. Keep the MVP demo-focused and stable.

## MVP Screens
1. Overview
2. Campaign Verification Dashboard
3. Settlement Engine
4. Network Reliability Leaderboard
5. AI Insights

## Core Demo Story
A retail media network claims 20% lift. VeriLift verifies only 10% lift using exposed vs holdout data. The performance-linked payout is reduced proportionally. The network reliability score is updated. AI explains why this protects marketing spend and customer experience.

## Core Formula Lock
- Exposed CR = exposed_conversions / exposed_users
- Holdout CR = holdout_conversions / holdout_users
- Relative Verified Lift = (Exposed CR - Holdout CR) / Holdout CR
- Verification Ratio = verified_lift / claimed_lift
- Released Performance Payment = performance_pool × min(verification_ratio, 1)
- Final Payable = base_payment + released_performance_payment

## Quality Bar
A phase is complete only when:
- It runs without errors.
- Output matches acceptance criteria.
- No unrelated scope was added.
- The user has confirmed the phase passed.
