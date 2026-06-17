# VeriLift

## Tagline
Pay for verified lift, not self-reported ROAS.

## Hackathon
TeXpedition 2026 — Epsilon Campus Hackathon

## Theme
Theme 02 — AI for seamless customer experiences across channels while defining clear measures of success.

## Problem
Retail media networks often report their own campaign performance. Brands may pay based on self-reported ROAS even when conversions may have happened without the ad.

## Solution
VeriLift verifies incremental lift using exposed vs holdout groups, adjusts performance-linked payout based on verified lift, and builds a reliability score for each network.

## MVP Features
- Synthetic campaign data
- Claimed vs verified lift comparison
- Settlement engine
- Network reliability leaderboard
- AI insight panel
- Customer experience impact explanation

## How to Run

```bash
pip install -r requirements.txt
python src/data_generator.py
streamlit run app.py
```

## Demo Story
A beauty brand runs campaigns across RetailNet A, B, and C. All claim strong performance, but VeriLift shows that RetailNet B is the most trustworthy because its claimed lift is closest to verified lift. The settlement engine adjusts payout based on verified performance.

## Core Line
Measurement already exists. VeriLift adds financial consequence to measurement.
