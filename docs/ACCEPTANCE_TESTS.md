# VeriLift Acceptance Tests

Use this file after every phase and before final submission.

## Phase 1: Data Generation
Command:

```bash
python src/data_generator.py
```

Pass conditions:
- `data/campaigns.csv` exists
- `data/test_control.csv` exists
- `data/network_history.csv` exists
- Minimum 12 campaigns exist
- Each campaign has exposed and holdout rows
- RetailNet B is closest to truth
- RetailNet C heavily overclaims

## Phase 2: Lift Calculator
Command:

```bash
python src/lift_calculator.py
```

Pass conditions:
- No crash
- Calculates exposed CR
- Calculates holdout CR
- Calculates absolute lift
- Calculates relative verified lift
- Calculates verification ratio
- Handles division by zero safely

## Phase 3: Settlement Engine
Command:

```bash
python src/settlement_engine.py
```

Pass conditions:
- No crash
- Calculates base payment
- Calculates performance pool
- Calculates released payment
- Calculates final payable
- Calculates adjusted amount
- Capped payout does not exceed performance pool

## Phase 4: Reliability Scorer
Command:

```bash
python src/reliability_scorer.py
```

Pass conditions:
- No crash
- Generates reliability leaderboard
- RetailNet B ranks highest
- RetailNet C ranks lowest
- Risk levels are assigned
- Contract recommendations are present

## Phase 6+: Streamlit App
Command:

```bash
streamlit run app.py
```

Pass conditions:
- App starts
- Sidebar pages work
- No missing imports
- No missing CSV errors
- Every page loads
- Campaign dropdown works
- Metrics update by campaign

## AI Insights
Pass conditions:
- Works without API key
- Uses fallback text if API key missing
- Does not expose API keys
- Explanation is concise and business-friendly

## Final Demo Acceptance
The app must clearly show:
1. Claimed lift
2. Verified lift
3. Payment adjustment
4. Reliability leaderboard
5. AI explanation
6. Customer experience benefit

Final story must be understandable in under 3 minutes.
