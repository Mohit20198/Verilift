# VeriLift Antigravity Micro-Phase Build Plan

## Project
**Product Name:** VeriLift  
**Tagline:** Pay for verified lift, not self-reported ROAS.  
**Hackathon Theme:** Theme 02 — AI for seamless customer experiences across channels while defining clear measures of success.  
**Prototype Stack:** Streamlit + Python + Pandas + Plotly + optional LLM fallback.  

---

# 0. Mandatory Antigravity Operating Rules

These rules must be followed for every phase.

## 0.1 Phase Lock Rule
Antigravity must work on **only one phase at a time**.

Do not start Phase N+1 unless Phase N has passed its acceptance checklist.

The user must explicitly approve the current phase by saying:

```text
PHASE <number> PASSED. MOVE TO PHASE <next number>.
```

If this approval is not given, Antigravity must not continue to the next phase.

## 0.2 No Scope Creep Rule
Do not add features that are not requested in the current phase.

Do not add:
- authentication
- payment gateway
- real escrow
- real API integrations
- production database
- user accounts
- complex ML models
- unrelated dashboards
- extra pages
- background workers
- unnecessary Docker setup

## 0.3 Current Phase Only Rule
When fixing bugs, only modify files related to the current phase unless a shared utility file must be updated.

If another file must be changed, explain why before changing it.

## 0.4 Formula Stability Rule
Do not change the core formulas without asking the user.

Core formulas:

```text
Exposed CR = exposed_conversions / exposed_users
Holdout CR = holdout_conversions / holdout_users
Absolute Lift = Exposed CR - Holdout CR
Verified Relative Lift = (Exposed CR - Holdout CR) / Holdout CR
Verification Ratio = Verified Relative Lift / Claimed Lift
Base Payment = Invoice × Base Payment Percentage
Performance Pool = Invoice × Performance Pool Percentage
Released Performance Payment = Performance Pool × min(Verification Ratio, 1)
Final Payable = Base Payment + Released Performance Payment
Adjusted Amount = Invoice - Final Payable
```

## 0.5 Testing Rule
Every phase must include a testable output.

Before saying a phase is complete, Antigravity must provide:
- files created/modified
- commands to run
- expected output
- acceptance checklist status

## 0.6 Fallback Rule
The AI insight feature must work even without an API key.

If no API key exists, use rule-based fallback text.

## 0.7 Demo Priority Rule
This project must stay demo-friendly.

The final prototype should explain the value in under 60 seconds and demonstrate the core flow in under 3 minutes.

---

# 1. Final MVP Scope

The final prototype has only four main screens:

1. **Overview**
2. **Campaign Verification Dashboard**
3. **Settlement Engine**
4. **Network Reliability Leaderboard**
5. **AI Insight Panel**

The core demo story:

```text
A retail media network claims 20% lift.
VeriLift independently verifies only 10% lift using exposed vs holdout data.
The performance-linked payout is reduced proportionally.
The network reliability score is updated.
AI explains why this protects marketing spend and customer experience.
```

---

# 2. Target Folder Structure

Create and maintain this exact structure:

```text
verilift/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   ├── campaigns.csv
│   ├── test_control.csv
│   └── network_history.csv
│
├── src/
│   ├── data_generator.py
│   ├── lift_calculator.py
│   ├── settlement_engine.py
│   ├── reliability_scorer.py
│   ├── ai_insights.py
│   └── utils.py
│
└── docs/
    ├── PROJECT_CONTEXT.md
    ├── PRD.md
    └── DEMO_SCRIPT.md
```

---

# 3. Master Context for Antigravity

Create `docs/PROJECT_CONTEXT.md` with this content:

```markdown
# VeriLift Project Context

## Product Name
VeriLift

## Tagline
Pay for verified lift, not self-reported ROAS.

## Theme
Theme 02 — AI for seamless customer experiences across channels while defining clear measures of success.

## Core Problem
Retail media networks often report their own campaign performance. Brands may pay based on self-reported ROAS or attributed conversions, even when many conversions may have happened without the ad.

## Core Solution
VeriLift verifies actual incremental lift using exposed vs holdout groups, compares verified lift with claimed lift, adjusts the performance-linked payout, and builds a reliability score for each retail media network.

## Customer Experience Benefit
If brands scale campaigns based on inflated attribution, they may repeatedly retarget customers who would have bought anyway. This creates wasted impressions, ad fatigue, irrelevant experiences, and poor cross-channel decisions. VeriLift helps brands scale campaigns that create real incremental customer value.

## Main Demo
A beauty brand runs campaigns on three retail media networks. All networks claim strong lift. VeriLift shows that only one network’s claimed lift matches verified lift. The settlement engine releases payment based on verified performance, and the leaderboard ranks networks by reliability.

## MVP Screens
1. Overview
2. Campaign Verification Dashboard
3. Settlement Engine
4. Network Reliability Leaderboard
5. AI Insight Panel

## Do Not Build
- authentication
- real payments
- real escrow
- real API integrations
- production databases
- complex user management
- unrelated dashboards

## Core Positioning
Measurement already exists. VeriLift adds financial consequence to measurement.
```

---

# 4. Phase-by-Phase Build Plan

---

## Phase 0 — Project Setup and Context Lock

### Goal
Create the initial project structure and lock the project context.

### Files to Create
```text
app.py
requirements.txt
README.md
.env.example
data/
src/
docs/PROJECT_CONTEXT.md
docs/PRD.md
docs/DEMO_SCRIPT.md
```

### Antigravity Prompt
```text
Read this instruction carefully and follow the Phase Lock Rule.

Build Phase 0 only for the VeriLift project.

Create the initial folder structure:
- app.py
- requirements.txt
- README.md
- .env.example
- data/
- src/
- docs/

Create docs/PROJECT_CONTEXT.md using the project context provided.
Create placeholder docs/PRD.md and docs/DEMO_SCRIPT.md.

Do not build any feature yet.
Do not generate data yet.
Do not build Streamlit UI yet.

After finishing, list files created and stop. Do not move to Phase 1.
```

### Acceptance Checklist
```text
[ ] Folder structure exists
[ ] docs/PROJECT_CONTEXT.md exists
[ ] README.md exists
[ ] requirements.txt exists
[ ] app.py exists as placeholder only
[ ] No feature logic has been added
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 0 PASSED. MOVE TO PHASE 1.
```

---

## Phase 1 — Synthetic Data Generator

### Goal
Generate realistic synthetic demo data for 3 fake retail media networks.

### Files to Create or Modify
```text
src/data_generator.py
data/campaigns.csv
data/test_control.csv
data/network_history.csv
```

### Data Story
```text
RetailNet A: medium overclaim
RetailNet B: honest/reliable
RetailNet C: heavy overclaim
```

### Required CSV Columns

#### campaigns.csv
```text
campaign_id
campaign_name
network_name
campaign_invoice
claimed_lift
claimed_revenue
base_payment_pct
performance_pool_pct
start_date
end_date
```

#### test_control.csv
```text
campaign_id
group_type
users
conversions
revenue
new_customers
repeat_customers
```

#### network_history.csv
```text
network_name
campaign_id
claimed_lift
verified_lift
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 1 only: synthetic data generation.

Create src/data_generator.py that generates:
1. data/campaigns.csv
2. data/test_control.csv
3. data/network_history.csv

Use 3 retail media networks:
- RetailNet A: moderately overstates lift
- RetailNet B: reliable/honest
- RetailNet C: heavily overstates lift

Generate at least 12 campaigns total.
Use realistic values for invoice, claimed lift, exposed users, holdout users, conversions, revenue, new customers, and repeat customers.

Add a main block so this works:
python src/data_generator.py

Do not build UI.
Do not build lift calculations yet.
After creating the data generator and CSV files, stop. Do not move to Phase 2.
```

### Command to Test
```bash
python src/data_generator.py
```

### Acceptance Checklist
```text
[ ] data/campaigns.csv exists
[ ] data/test_control.csv exists
[ ] data/network_history.csv exists
[ ] At least 12 campaigns generated
[ ] RetailNet B data looks most reliable
[ ] RetailNet C data looks most inflated
[ ] No UI was built
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 1 PASSED. MOVE TO PHASE 2.
```

---

## Phase 2 — Verified Lift Calculator

### Goal
Calculate actual verified lift using exposed vs holdout groups.

### File to Create
```text
src/lift_calculator.py
```

### Required Calculations
```text
exposed_conversion_rate
holdout_conversion_rate
absolute_lift
verified_lift_relative
claimed_lift
verification_ratio
overstatement_factor
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 2 only: verified lift calculation.

Create src/lift_calculator.py.
It should load data/campaigns.csv and data/test_control.csv, then calculate for each campaign:
- exposed_conversion_rate
- holdout_conversion_rate
- absolute_lift
- verified_lift_relative
- claimed_lift
- verification_ratio = verified_lift_relative / claimed_lift
- overstatement_factor = claimed_lift / verified_lift_relative

Handle edge cases:
- division by zero
- missing campaign rows
- negative lift
- verified lift greater than claimed lift

Return a clean Pandas DataFrame.
Add a main block so this works:
python src/lift_calculator.py

Do not build UI.
Do not build settlement logic.
After finishing, stop. Do not move to Phase 3.
```

### Command to Test
```bash
python src/lift_calculator.py
```

### Acceptance Checklist
```text
[ ] src/lift_calculator.py exists
[ ] Script runs without error
[ ] Output includes claimed_lift and verified_lift_relative
[ ] Verification ratio is calculated
[ ] Overstatement factor is calculated
[ ] Edge cases are handled safely
[ ] No settlement logic was added
[ ] No UI was built
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 2 PASSED. MOVE TO PHASE 3.
```

---

## Phase 3 — Settlement Engine

### Goal
Calculate payment release based on verified lift.

### File to Create
```text
src/settlement_engine.py
```

### Required Calculations
```text
base_payment
performance_pool
verification_ratio_capped
released_performance_payment
final_payable
adjusted_amount
settlement_status
```

### Settlement Status Rules
```text
verification_ratio >= 0.9: Full or near-full release
0.6 to 0.89: Partial release
0.3 to 0.59: High adjustment
below 0.3: Severe discrepancy
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 3 only: settlement engine.

Create src/settlement_engine.py.
It should use the output from src/lift_calculator.py and calculate:
- base_payment
- performance_pool
- verification_ratio_capped
- released_performance_payment
- final_payable
- adjusted_amount
- settlement_status

Formula:
Base Payment = invoice × base_payment_pct
Performance Pool = invoice × performance_pool_pct
Verification Ratio Capped = min(max(verified_lift / claimed_lift, 0), 1)
Released Performance Payment = performance_pool × verification_ratio_capped
Final Payable = base_payment + released_performance_payment
Adjusted Amount = invoice - final_payable

Add a main block so this works:
python src/settlement_engine.py

Do not build UI.
Do not build reliability scoring yet.
After finishing, stop. Do not move to Phase 4.
```

### Command to Test
```bash
python src/settlement_engine.py
```

### Acceptance Checklist
```text
[ ] src/settlement_engine.py exists
[ ] Script runs without error
[ ] Final payable is calculated
[ ] Adjusted amount is calculated
[ ] Verification ratio is capped between 0 and 1
[ ] Settlement status appears
[ ] Formula matches PRD
[ ] No UI was built
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 3 PASSED. MOVE TO PHASE 4.
```

---

## Phase 4 — Network Reliability Scorer

### Goal
Rank networks based on how close claimed lift is to verified lift.

### File to Create
```text
src/reliability_scorer.py
```

### Required Output Columns
```text
network_name
avg_claimed_lift
avg_verified_lift
avg_deviation
reliability_score
risk_level
recommended_contract_split
```

### Risk Rules
```text
score >= 85: Low Risk
score 60-84: Medium Risk
score 30-59: High Risk
score < 30: Severe Risk
```

### Contract Recommendation Rules
```text
Low Risk: 80% base / 20% verified performance
Medium Risk: 60% base / 40% verified performance
High Risk: 50% base / 50% verified performance
Severe Risk: 40% base / 60% verified performance
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 4 only: network reliability scoring.

Create src/reliability_scorer.py.
It should calculate reliability for each network using all campaigns:
- avg_claimed_lift
- avg_verified_lift
- avg_deviation
- reliability_score
- risk_level
- recommended_contract_split

Formula:
Deviation = abs(claimed_lift - verified_lift) / claimed_lift
Reliability Score = 100 × (1 - average_deviation)
Cap score between 0 and 100.

Add a main block so this works:
python src/reliability_scorer.py

Expected ranking:
RetailNet B highest, RetailNet A middle, RetailNet C lowest.

Do not build UI.
After finishing, stop. Do not move to Phase 5.
```

### Command to Test
```bash
python src/reliability_scorer.py
```

### Acceptance Checklist
```text
[ ] src/reliability_scorer.py exists
[ ] Script runs without error
[ ] RetailNet B ranks highest
[ ] RetailNet C ranks lowest
[ ] Risk level appears
[ ] Recommended contract split appears
[ ] No UI was built
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 4 PASSED. MOVE TO PHASE 5.
```

---

## Phase 5 — Utility Functions

### Goal
Centralize formatting and common helpers.

### File to Create
```text
src/utils.py
```

### Required Functions
```text
format_currency_inr(value)
format_percent(value)
safe_divide(a, b)
risk_badge(score_or_status)
load_csv_data()
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 5 only: utility functions.

Create src/utils.py with:
- format_currency_inr(value)
- format_percent(value)
- safe_divide(a, b)
- risk_badge(score_or_status)
- load_csv_data()

Make sure previous modules can import utilities without circular imports.
Run the previous phase scripts again to ensure nothing breaks.

Do not build UI.
After finishing, stop. Do not move to Phase 6.
```

### Commands to Test
```bash
python src/lift_calculator.py
python src/settlement_engine.py
python src/reliability_scorer.py
```

### Acceptance Checklist
```text
[ ] src/utils.py exists
[ ] Utility functions work
[ ] Previous scripts still run
[ ] No circular imports
[ ] No UI was built
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 5 PASSED. MOVE TO PHASE 6.
```

---

## Phase 6 — Streamlit Skeleton

### Goal
Create the basic Streamlit app with navigation only.

### File to Modify
```text
app.py
```

### Required Pages
```text
Overview
Campaign Verification
Settlement Engine
Reliability Leaderboard
AI Insights
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 6 only: Streamlit skeleton.

Create app.py with:
- title: VeriLift
- tagline: Pay for verified lift, not self-reported ROAS
- sidebar navigation
- pages:
  1. Overview
  2. Campaign Verification
  3. Settlement Engine
  4. Reliability Leaderboard
  5. AI Insights

Each page should show placeholder text only.
Do not connect calculations yet.
Do not add charts yet.

Make sure this runs:
streamlit run app.py

After finishing, stop. Do not move to Phase 7.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] Streamlit app launches
[ ] Sidebar navigation works
[ ] All five pages exist
[ ] Pages show placeholder content
[ ] No calculation UI yet
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 6 PASSED. MOVE TO PHASE 7.
```

---

## Phase 7 — Campaign Verification UI

### Goal
Connect verified lift calculations to the Campaign Verification page.

### File to Modify
```text
app.py
```

### Required UI Components
```text
campaign dropdown
claimed lift metric card
verified lift metric card
verification ratio metric card
overstatement factor metric card
exposed vs holdout conversion rate chart
short explanation
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 7 only: Campaign Verification screen.

Connect app.py to src/lift_calculator.py.
On the Campaign Verification page, add:
- campaign dropdown
- claimed lift metric card
- verified lift metric card
- verification ratio metric card
- overstatement factor metric card
- exposed vs holdout conversion rate bar chart using Plotly
- short explanation text

Do not build settlement UI.
Do not build reliability UI.
Do not build AI UI.

After finishing, stop. Do not move to Phase 8.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] Campaign dropdown works
[ ] Metric cards update when campaign changes
[ ] Claimed lift appears
[ ] Verified lift appears
[ ] Verification ratio appears
[ ] Overstatement factor appears
[ ] Exposed vs holdout chart appears
[ ] Other pages are not modified beyond required imports
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 7 PASSED. MOVE TO PHASE 8.
```

---

## Phase 8 — Settlement Engine UI

### Goal
Show payout calculation based on verified lift.

### File to Modify
```text
app.py
```

### Required UI Components
```text
campaign dropdown
invoice amount
base payment
performance pool
released performance payment
final payable
adjusted amount
settlement status
bar chart comparing invoice, final payable, adjusted amount
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 8 only: Settlement Engine screen.

Connect app.py to src/settlement_engine.py.
On the Settlement Engine page, add:
- campaign dropdown
- invoice amount
- base payment
- performance pool
- released performance payment
- final payable
- adjusted amount
- settlement status badge
- Plotly bar chart comparing invoice, final payable, and adjusted amount

Add this sentence:
"VeriLift releases the performance-linked payout in proportion to verified lift, not claimed lift."

Do not build reliability UI.
Do not build AI UI.
After finishing, stop. Do not move to Phase 9.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] Settlement page loads
[ ] Campaign dropdown works
[ ] Invoice amount appears
[ ] Final payable is correct
[ ] Adjusted amount is correct
[ ] Settlement status appears
[ ] Chart appears
[ ] Formula matches settlement_engine.py output
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 8 PASSED. MOVE TO PHASE 9.
```

---

## Phase 9 — Reliability Leaderboard UI

### Goal
Show long-term network reliability ranking.

### File to Modify
```text
app.py
```

### Required UI Components
```text
leaderboard table
reliability score bar chart
average claimed vs verified lift comparison
risk level badges
recommended contract split
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 9 only: Reliability Leaderboard screen.

Connect app.py to src/reliability_scorer.py.
On the Reliability Leaderboard page, add:
- leaderboard table
- reliability score bar chart
- average claimed vs verified lift comparison chart
- risk level badges
- recommended contract split column

RetailNet B should appear most reliable.
RetailNet C should appear least reliable.

Do not build AI UI.
After finishing, stop. Do not move to Phase 10.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] Reliability page loads
[ ] Leaderboard table appears
[ ] RetailNet B ranks highest
[ ] RetailNet C ranks lowest
[ ] Risk levels appear
[ ] Contract recommendations appear
[ ] Charts appear
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 9 PASSED. MOVE TO PHASE 10.
```

---

## Phase 10 — AI Insights Module

### Goal
Generate plain-English explanations with API fallback.

### File to Create
```text
src/ai_insights.py
```

### Required Functions
```text
generate_discrepancy_explanation(campaign_row)
generate_settlement_summary(settlement_row)
generate_cx_impact_summary(campaign_row)
generate_contract_recommendation(network_row)
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 10 only: AI insights module.

Create src/ai_insights.py with these functions:
- generate_discrepancy_explanation(campaign_row)
- generate_settlement_summary(settlement_row)
- generate_cx_impact_summary(campaign_row)
- generate_contract_recommendation(network_row)

Use an LLM API only if an API key exists in environment variables.
If no API key exists, return high-quality rule-based fallback text.

Do not expose API keys.
Update .env.example with the optional API key variable.

The outputs should be concise and demo-friendly.

Add a main block so this works:
python src/ai_insights.py

Do not connect this to Streamlit yet.
After finishing, stop. Do not move to Phase 11.
```

### Command to Test
```bash
python src/ai_insights.py
```

### Acceptance Checklist
```text
[ ] src/ai_insights.py exists
[ ] Script runs without API key
[ ] Fallback insights are high quality
[ ] No API key is exposed
[ ] .env.example updated
[ ] Not connected to Streamlit yet
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 10 PASSED. MOVE TO PHASE 11.
```

---

## Phase 11 — AI Insights UI

### Goal
Show AI/fallback explanations inside the app.

### File to Modify
```text
app.py
```

### Required UI Components
```text
campaign selector
discrepancy explanation
settlement summary
customer experience impact explanation
recommended next action
contract recommendation
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 11 only: AI Insights screen.

Connect app.py to src/ai_insights.py.
On the AI Insights page, add:
- campaign selector
- Discrepancy Explanation
- Settlement Summary
- Customer Experience Impact
- Recommended Next Action
- Contract Recommendation based on network reliability

The page must work without an API key using fallback insights.

Do not add new pages.
Do not change formulas.
After finishing, stop. Do not move to Phase 12.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] AI Insights page loads
[ ] Campaign selector works
[ ] Discrepancy explanation appears
[ ] Settlement summary appears
[ ] CX impact appears
[ ] Contract recommendation appears
[ ] Works without API key
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 11 PASSED. MOVE TO PHASE 12.
```

---

## Phase 12 — Overview Page Improvement

### Goal
Make the product understandable in under 30 seconds.

### File to Modify
```text
app.py
```

### Required Content
```text
Problem
Solution
Theme alignment
Customer experience benefit
Workflow
Before VeriLift vs After VeriLift
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 12 only: improve the Overview page.

The Overview page should explain VeriLift in under 30 seconds.
Add:
- Problem: retail media networks report their own performance
- Solution: VeriLift verifies incremental lift and adjusts payment
- Theme fit: clear success metric = verified incremental lift
- CX benefit: brands stop scaling campaigns that only retarget customers who would have bought anyway
- Workflow:
  1. Network claims lift
  2. VeriLift verifies lift
  3. Settlement and reliability score update
- Before VeriLift vs After VeriLift comparison

Do not change calculation logic.
Do not add pages.
After finishing, stop. Do not move to Phase 13.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] Overview explains problem clearly
[ ] Overview explains solution clearly
[ ] Theme alignment is visible
[ ] CX benefit is visible
[ ] Workflow is easy to understand
[ ] No formulas were changed
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 12 PASSED. MOVE TO PHASE 13.
```

---

## Phase 13 — UI Polish

### Goal
Make the prototype look hackathon-ready.

### Files to Modify
```text
app.py
possibly src/utils.py
```

### Required Improvements
```text
metric cards
colored risk badges
section dividers
short explanation under every chart
warning boxes for high discrepancy campaigns
success boxes for reliable networks
consistent formatting
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 13 only: UI polish.

Improve the Streamlit UI:
- clean metric cards
- colored risk badges
- section dividers
- short explanatory text under every chart
- warning boxes for high discrepancy campaigns
- success box for reliable networks
- consistent INR and percentage formatting

Do not change core formulas.
Do not add new pages.
Do not add unrelated features.
After finishing, stop. Do not move to Phase 14.
```

### Command to Test
```bash
streamlit run app.py
```

### Acceptance Checklist
```text
[ ] UI looks clean
[ ] Risk colors are understandable
[ ] Charts have explanations
[ ] Warnings appear for risky campaigns/networks
[ ] Formatting is consistent
[ ] App still runs without errors
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 13 PASSED. MOVE TO PHASE 14.
```

---

## Phase 14 — Demo Script

### Goal
Create a script for presenting the prototype.

### File to Create or Update
```text
docs/DEMO_SCRIPT.md
```

### Required Sections
```text
30-second intro
2-minute demo flow
screen-by-screen talking points
judge Q&A
final closing line
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 14 only: demo script.

Create or update docs/DEMO_SCRIPT.md.
It should include:
- 30-second intro
- 2-minute demo flow
- key lines to say on each screen
- judge Q&A
- final closing line

Use this core line:
"Measurement already exists. VeriLift adds financial consequence to measurement."

Do not modify app code.
After finishing, stop. Do not move to Phase 15.
```

### Acceptance Checklist
```text
[ ] docs/DEMO_SCRIPT.md exists
[ ] Intro is clear
[ ] Demo flow follows app screens
[ ] Judge Q&A included
[ ] Closing line included
[ ] App code was not changed
```

### Stop Condition
Do not proceed until the user says:

```text
PHASE 14 PASSED. MOVE TO PHASE 15.
```

---

## Phase 15 — Final Testing, README, and Cleanup

### Goal
Make sure the prototype is stable for demo.

### Files to Modify
```text
README.md
possibly app.py
possibly src files only if bug fixes are needed
```

### Antigravity Prompt
```text
Read docs/PROJECT_CONTEXT.md first.

Build Phase 15 only: final testing and cleanup.

Check the full VeriLift app for:
- import errors
- broken paths
- missing CSV files
- Streamlit crashes
- inconsistent numbers
- division by zero
- AI fallback issues
- unclear labels

Do not add new features.
Only fix bugs and improve reliability.

Update README.md with:
- project description
- theme alignment
- setup instructions
- how to run
- demo flow
- folder structure
- tech stack

After finishing, provide:
- final files changed
- commands to run
- final checklist
Then stop.
```

### Commands to Test
```bash
python src/data_generator.py
python src/lift_calculator.py
python src/settlement_engine.py
python src/reliability_scorer.py
python src/ai_insights.py
streamlit run app.py
```

### Final Acceptance Checklist
```text
[ ] data generation works
[ ] lift calculator works
[ ] settlement engine works
[ ] reliability scorer works
[ ] AI fallback works
[ ] Streamlit app runs
[ ] all pages load
[ ] RetailNet B appears reliable
[ ] RetailNet C appears risky
[ ] settlement math is correct
[ ] README is complete
[ ] demo script exists
[ ] no unnecessary features added
```

### Stop Condition
This is the final phase. Do not add anything else unless the user explicitly asks.

---

# 5. Final Phase Dependency Map

```text
Phase 0: Project Context
    ↓
Phase 1: Synthetic Data
    ↓
Phase 2: Verified Lift Calculator
    ↓
Phase 3: Settlement Engine
    ↓
Phase 4: Reliability Scorer
    ↓
Phase 5: Utility Functions
    ↓
Phase 6: Streamlit Skeleton
    ↓
Phase 7: Campaign Verification UI
    ↓
Phase 8: Settlement UI
    ↓
Phase 9: Reliability UI
    ↓
Phase 10: AI Insight Module
    ↓
Phase 11: AI Insight UI
    ↓
Phase 12: Overview Page
    ↓
Phase 13: UI Polish
    ↓
Phase 14: Demo Script
    ↓
Phase 15: Testing + README
```

---

# 6. Emergency Reset Prompt for Antigravity

Use this if Antigravity starts overbuilding or breaking things:

```text
Stop. You are violating the phase plan.

Read docs/PROJECT_CONTEXT.md again.
Return to the current phase only.
Do not add new features.
Do not move to the next phase.
Do not rewrite unrelated files.
Only fix the issue required to pass the current phase acceptance checklist.
After fixing, show:
1. files changed
2. what was fixed
3. how to test
4. whether the current phase acceptance checklist passes
```

---

# 7. Final Prototype Success Definition

The prototype is successful only if it can show this complete story:

```text
A retail media network claims strong lift.
VeriLift independently verifies actual lift using exposed vs holdout data.
The verified lift is lower than claimed lift.
The performance-linked payout is reduced proportionally.
The network reliability score is updated.
AI explains the discrepancy, settlement result, and customer experience benefit.
```

If this story is not clear, the prototype is not complete.

