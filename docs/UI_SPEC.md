# VeriLift UI Specification

## App Type
Single file `app.py` Streamlit dashboard.
- Use sidebar navigation.
- Do not create extra pages unless explicitly asked.
- Keep the app simple, fast, and demo-ready.

## Global Header
Title: VeriLift  
Tagline: Pay for verified lift, not self-reported ROAS.

## Sidebar Pages
1. Overview
2. Campaign Verification
3. Settlement Engine
4. Reliability Leaderboard
5. AI Insights

## Page 1: Overview
Purpose: Explain the product in under 30 seconds.

Must include:
- Problem statement
- Solution statement
- Theme alignment
- Customer experience benefit
- 3-step workflow

Workflow:
1. Network claims lift
2. VeriLift verifies lift
3. Settlement + reliability score update

## Page 2: Campaign Verification
Purpose: Show claimed vs verified performance.

Components:
- Campaign dropdown
- Network name
- Claimed lift card
- Verified lift card
- Verification ratio card
- Overstatement factor card
- Exposed vs holdout conversion rate chart
- Short insight text

## Page 3: Settlement Engine
Purpose: Show how verified lift changes payment.

Components:
- Campaign dropdown
- Total invoice
- Base payment
- Performance pool
- Released performance payment
- Final payable
- Adjusted amount
- Settlement status badge
- Bar chart: invoice vs final payable vs adjusted amount

## Page 4: Reliability Leaderboard
Purpose: Rank networks by trustworthiness.

Components:
- Network table
- Avg claimed lift
- Avg verified lift
- Reliability score
- Risk level
- Recommended contract split
- Reliability bar chart

Expected order:
1. RetailNet B best
2. RetailNet A middle
3. RetailNet C worst

## Page 5: AI Insights
Purpose: Generate business-friendly explanation.

Components:
- Campaign selector
- Discrepancy explanation
- Settlement summary
- Customer experience impact
- Recommended next action
- Contract recommendation

## Design Principles
- Clean, executive-ready UI
- Do not overload with charts
- Every chart must have a one-line explanation
- Use warnings for high discrepancy
- Use success boxes for reliable networks
- Keep the live demo under 3 minutes
