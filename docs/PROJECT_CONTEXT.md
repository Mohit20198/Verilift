# VeriLift Project Context

## Project Name
VeriLift

## Tagline
Pay for verified lift, not self-reported ROAS.

## Hackathon Theme
Theme 02 — AI for seamless customer experiences across channels while defining clear measures of success.

## Problem
Retail media networks often report their own campaign performance. Brands may pay based on self-reported ROAS or attributed conversions, even when many conversions may have happened without the ad.

The same platform that sells the media also reports how successful the media was. This creates a trust gap and can lead to overpayment, budget waste, and poor customer experience decisions.

## Solution
VeriLift verifies actual incremental lift using exposed vs holdout groups, compares verified lift with claimed lift, adjusts the performance-linked payout, and builds a reliability score for each retail media network.

## Customer Experience Benefit
If brands scale campaigns based on inflated attribution, they may keep retargeting customers who would have bought anyway. This creates wasted impressions, repetitive messaging, irrelevant targeting, and ad fatigue.

VeriLift helps brands scale campaigns that create genuine incremental customer value.

## MVP Scope
This is a hackathon simulation. Build:
1. Synthetic campaign dataset
2. Verified lift calculator
3. Settlement engine
4. Network reliability leaderboard
5. AI explanation panel
6. Streamlit dashboard

## Do Not Build
- Real payments
- Real escrow
- Real retail media API integrations
- Authentication
- Production database
- Complex causal inference
- Full legal settlement infrastructure

## Demo Story
A beauty brand runs campaigns across three networks:
- RetailNet A: moderate overclaim
- RetailNet B: reliable
- RetailNet C: heavy overclaim

VeriLift shows that the highest claimed lift is not always the most trustworthy. Payment is adjusted using verified lift, and the network reliability leaderboard updates.
