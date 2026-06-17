# Product Requirements Document

# VeriLift

## Verified Incrementality Settlement Layer for Retail Media

**Hackathon:** TeXpedition 2026 — Epsilon Campus Hackathon
**Theme Chosen:** Theme 02 — AI for seamless customer experiences across channels while defining clear measures of success
**Product Name:** VeriLift
**Tagline:** Pay for verified lift, not self-reported ROAS.
**Version:** v1.0
**Target Users:** Brands, Retail Media Buyers, Performance Marketing Teams, CMOs, Retail Media Networks
**MVP Type:** Hackathon prototype / simulation platform

---

# 1. Executive Summary

Retail media is one of the fastest-growing areas in advertising, but brands face a serious trust problem: the platform selling the media also reports the performance of that media.

A retail media network may claim:

“Your campaign generated 20% lift and 3x ROAS.”

But the brand still has one major question:

“Did this campaign actually create new customer behavior, or did it just claim credit for customers who would have purchased anyway?”

VeriLift solves this by creating a verified measurement and settlement layer for retail media campaigns.

Instead of relying only on self-reported ROAS, VeriLift compares an exposed group with a holdout group, calculates verified incremental lift, and adjusts the performance-linked payout based on the verified result.

The product also creates a reliability score for each media network over time, helping brands identify which partners consistently report performance close to independently verified outcomes.

VeriLift is not just a dashboard. It is a trust infrastructure layer that connects measurement, payment, and customer experience.

---

# 2. Theme Alignment

## 2.1 Selected Theme

**Theme 02: How can we use AI to deliver seamless customer experiences across channels while defining clear measures of success?**

VeriLift aligns with this theme by focusing on the second half of the theme:

**clear measures of success.**

Most brands currently measure retail media success using platform-reported metrics such as:

* ROAS
* attributed conversions
* attributed revenue
* click-through rate
* impression reach
* platform-specific lift

But these metrics may not always represent true incremental customer impact.

VeriLift makes success clearer by defining the core success metric as:

**verified incremental lift.**

This means brands can scale only the campaigns that genuinely influence customer behavior, instead of blindly scaling campaigns that merely capture credit for customers who were already likely to buy.

---

## 2.2 How VeriLift Improves Customer Experience

At first, VeriLift may look like a measurement or payment product, but its customer experience impact is very important.

When brands optimize based on inflated or self-reported metrics, they may keep funding campaigns that:

* repeatedly retarget loyal customers
* over-message users who were already going to buy
* create ad fatigue
* increase irrelevant impressions
* push aggressive offers to the wrong audience
* waste budget on low-value touchpoints
* ignore campaigns that actually help new or uncertain customers

VeriLift prevents this by asking:

“Did this campaign actually create new value for the customer journey?”

If verified lift is low, the brand should not scale that campaign blindly.

This helps brands redirect budget toward:

* helpful product discovery
* better education for new customers
* less repetitive retargeting
* more relevant offers
* better channel experiences
* campaigns that actually move customers forward

So VeriLift supports seamless customer experience by ensuring that the campaigns brands scale are the ones creating real incremental impact.

---

# 3. Problem Statement

## 3.1 Core Problem

Retail media campaigns are often paid based on performance numbers reported by the same network that sold the ad inventory.

This creates a conflict of interest.

The platform has an incentive to report strong performance because higher reported performance helps justify higher future ad spend.

The brand has limited visibility into whether those conversions were truly caused by the campaign.

This creates three major problems:

1. **Measurement Trust Gap**
   Brands do not fully trust self-reported performance numbers.

2. **Overpayment Risk**
   Brands may pay for conversions that would have happened even without the campaign.

3. **Poor Customer Experience Decisions**
   Brands may keep scaling campaigns that over-target the same customers instead of investing in truly helpful customer journeys.

---

## 3.2 Example Problem

A skincare brand runs a campaign on a retail media network.

The network reports:

* Claimed lift: 20%
* Claimed revenue: ₹25,00,000
* Campaign invoice: ₹10,00,000

The brand is expected to pay the full campaign amount.

But VeriLift compares exposed customers with a holdout group and finds:

* Exposed conversion rate: 11%
* Holdout conversion rate: 10%
* Verified lift: 10%

The network claimed 20% lift, but the verified lift is only 10%.

This means the network overstated campaign impact by 2x.

Without VeriLift, the brand would pay the full amount.

With VeriLift, only the verified-performance portion of payment is released proportionally.

---

# 4. Proposed Solution

## 4.1 Product Overview

VeriLift is a verified incrementality settlement layer for retail media campaigns.

It has four core functions:

1. **Verify Campaign Lift**
   Compare exposed customers and holdout customers to calculate true incremental lift.

2. **Compare Claimed vs Verified Performance**
   Show how much the network claimed versus what VeriLift verified.

3. **Adjust Payment Settlement**
   Release the performance-linked payout based on the verified-to-claimed lift ratio.

4. **Build Network Reliability Score**
   Track how close each network’s reported numbers are to verified results over multiple campaigns.

---

## 4.2 One-Line Pitch

**VeriLift helps brands pay retail media networks based on verified incremental lift, not self-reported ROAS.**

---

## 4.3 Core Innovation

Most tools stop at measurement.

They tell the brand:

“Here is what happened.”

VeriLift goes further.

It says:

“Here is the verified lift, here is how much should be paid, and here is how reliable this network is over time.”

The innovation is not just independent measurement.

The innovation is:

**measurement with financial consequence.**

---

# 5. Target Users

## 5.1 Primary User: Brand Performance Marketing Manager

**Goal:** Maximize real campaign impact and reduce wasted ad spend.
**Pain Point:** Cannot fully trust platform-reported ROAS.
**Question:**
“Which retail media network is actually creating incremental value?”

---

## 5.2 Secondary User: CMO / Marketing Head

**Goal:** Make confident budget decisions across retail media networks.
**Pain Point:** Reports from each network look impressive but are hard to verify.
**Question:**
“Which partners should we trust and scale next quarter?”

---

## 5.3 Third User: Challenger Retail Media Network

**Goal:** Compete with larger networks by proving transparency and trust.
**Pain Point:** Cannot beat large platforms on scale.
**Question:**
“How can we show brands that our reported performance is more trustworthy?”

---

# 6. Product Goals

VeriLift should:

1. Demonstrate the gap between claimed lift and verified lift.
2. Calculate verified incremental lift using exposed and holdout groups.
3. Simulate performance-linked settlement.
4. Show how payment changes when verified lift differs from claimed lift.
5. Create reliability scores for retail media networks.
6. Use AI to explain discrepancies and generate settlement summaries.
7. Connect verified measurement to better customer experience decisions.
8. Provide a clean, judge-friendly demo in under 3 minutes.

---

# 7. Non-Goals for MVP

The MVP will not:

1. Handle real money movement.
2. Create actual escrow accounts.
3. Integrate with real retail media APIs.
4. Use real customer data.
5. Perform legal contract enforcement.
6. Claim perfect causal measurement.
7. Replace Nielsen, Kantar, or other third-party measurement platforms.
8. Build a production-grade clean-room identity system.

The MVP is a working simulation of the settlement logic.

---

# 8. Key Product Modules

# Module 1: Campaign Data Simulator

## Description

Generates synthetic campaign data for multiple retail media networks.

Each campaign includes:

* campaign ID
* network name
* claimed lift
* exposed group
* holdout group
* conversions
* revenue
* campaign invoice
* base payment percentage
* performance-linked payment percentage

## Example Networks

* RetailNet A
* RetailNet B
* RetailNet C

## Purpose

To demonstrate how different networks may report different levels of lift and how verified measurement changes payment decisions.

---

# Module 2: Verified Lift Calculator

## Description

Calculates campaign lift by comparing exposed and holdout groups.

## Formula

Exposed Conversion Rate:

Exposed CR = Exposed Conversions / Exposed Users

Holdout Conversion Rate:

Holdout CR = Holdout Conversions / Holdout Users

Absolute Lift:

Absolute Lift = Exposed CR - Holdout CR

Relative Lift:

Relative Lift = (Exposed CR - Holdout CR) / Holdout CR

## Example

Exposed users: 10,000
Exposed conversions: 1,100
Exposed CR: 11%

Holdout users: 10,000
Holdout conversions: 1,000
Holdout CR: 10%

Relative Lift:

(11% - 10%) / 10% = 10%

Verified Lift = 10%

---

# Module 3: Claimed vs Verified Comparison

## Description

Compares the network’s self-reported lift with VeriLift’s independently verified lift.

## Output

| Metric               | Value |
| -------------------- | ----- |
| Claimed Lift         | 20%   |
| Verified Lift        | 10%   |
| Verification Ratio   | 50%   |
| Overstatement Factor | 2x    |

## Interpretation

If verified lift is much lower than claimed lift, the network may be over-attributing conversions.

If verified lift is close to claimed lift, the network is more reliable.

---

# Module 4: Settlement Engine

## Description

Calculates how much of the performance-linked payment should be released.

## Payment Structure

Total invoice is split into two parts:

1. **Base Payment**
   Guaranteed payment for media delivery.

2. **Verified Performance Pool**
   Payment released based on verified lift.

## Example

Campaign invoice: ₹10,00,000
Base payment: 50% = ₹5,00,000
Performance pool: 50% = ₹5,00,000

Claimed lift: 20%
Verified lift: 10%

Verification ratio:

10 / 20 = 0.5

Released performance payment:

₹5,00,000 × 0.5 = ₹2,50,000

Final paid amount:

₹5,00,000 + ₹2,50,000 = ₹7,50,000

Adjusted amount:

₹2,50,000

---

# Module 5: Network Reliability Score

## Description

Tracks how trustworthy each network is over multiple campaigns.

## Suggested Formula

Reliability Score = 100 - average percentage deviation between claimed lift and verified lift

Example:

Network A average claimed lift: 20%
Network A average verified lift: 10%

Deviation: 50%

Reliability Score: 50/100

## Output

| Network     | Avg Claimed Lift | Avg Verified Lift | Reliability Score |
| ----------- | ---------------: | ----------------: | ----------------: |
| RetailNet B |              14% |               13% |                92 |
| RetailNet A |              20% |               11% |                58 |
| RetailNet C |              24% |                7% |                31 |

## Business Value

Brands can use this score to decide which networks to trust and scale.

Networks can use this score to prove transparency.

---

# Module 6: AI Discrepancy Explainer

## Description

Uses AI to explain why claimed and verified performance may differ.

## Input to AI

* claimed lift
* verified lift
* exposed conversion rate
* holdout conversion rate
* new customer ratio
* repeat buyer ratio
* reliability history
* settlement result

## Output Example

“RetailNet A claimed 20% lift, but verified lift was only 10%. The exposed group converted only slightly better than the holdout group, suggesting that many attributed conversions may have come from customers who were already likely to buy. VeriLift recommends releasing 50% of the performance-linked payout and reviewing this network’s targeting quality before scaling future spend.”

---

# Module 7: AI Settlement Summary

## Description

Generates a neutral, business-friendly explanation of the settlement decision.

## Output Example

“Because verified lift was 50% of claimed lift, VeriLift recommends releasing 50% of the variable performance pool. The final payable amount is ₹7,50,000 out of the ₹10,00,000 campaign invoice. The remaining ₹2,50,000 should be treated as an adjustment, credit, or disputed amount depending on contract terms.”

---

# Module 8: AI Contract Recommendation

## Description

Suggests payment split based on network reliability.

## Example

If reliability score is high:

“Use 80% base payment and 20% verified performance pool.”

If reliability score is medium:

“Use 60% base payment and 40% verified performance pool.”

If reliability score is low:

“Use 50% base payment and 50% verified performance pool.”

## Purpose

This makes VeriLift useful beyond one campaign.

It becomes a long-term trust and negotiation tool.

---

# 9. MVP Screens

## Screen 1: Campaign Verification Dashboard

### Purpose

Show the gap between claimed performance and verified performance.

### Components

* campaign selector
* network name
* claimed lift
* verified lift
* exposed conversion rate
* holdout conversion rate
* overstatement factor
* verification ratio

### Example Display

Campaign: Summer Beauty Sale
Network: RetailNet A

Claimed Lift: 20%
Verified Lift: 10%
Verification Ratio: 50%
Risk Level: Medium

---

## Screen 2: Settlement Engine

### Purpose

Show how verified lift changes payment.

### Components

* total campaign invoice
* base payment amount
* performance-linked pool
* verified payout released
* adjusted / held amount
* final payable amount

### Example Display

Total Invoice: ₹10,00,000
Base Payment: ₹5,00,000
Performance Pool: ₹5,00,000
Released from Pool: ₹2,50,000
Final Payable: ₹7,50,000
Adjusted Amount: ₹2,50,000

---

## Screen 3: Network Reliability Leaderboard

### Purpose

Compare multiple retail media networks based on trustworthiness.

### Components

* network name
* average claimed lift
* average verified lift
* reliability score
* recommended payment split
* risk level

### Example Display

| Network     | Reliability | Recommended Contract    |
| ----------- | ----------: | ----------------------- |
| RetailNet B |      92/100 | 80% base / 20% verified |
| RetailNet A |      58/100 | 60% base / 40% verified |
| RetailNet C |      31/100 | 50% base / 50% verified |

---

## Screen 4: AI Insight Panel

### Purpose

Use AI to explain the result in plain English.

### Components

* discrepancy explanation
* settlement summary
* CX impact explanation
* contract recommendation
* next action

### Example Display

“RetailNet C has the largest gap between claimed and verified lift. Scaling this network may lead to wasted impressions and repeated targeting of customers who would have purchased anyway. VeriLift recommends reducing spend until the network improves verified performance quality.”

---

# 10. User Flow

## Step 1: Select Campaign

User selects a campaign from the demo dataset.

Example:

“Summer Beauty Sale — RetailNet A”

---

## Step 2: View Claimed Performance

The system shows the network-reported numbers.

Example:

Claimed lift: 20%
Claimed revenue: ₹25,00,000
Claimed ROAS: 2.5x

---

## Step 3: Verify Lift

VeriLift calculates lift using exposed and holdout groups.

Example:

Exposed CR: 11%
Holdout CR: 10%
Verified lift: 10%

---

## Step 4: Calculate Settlement

The settlement engine adjusts the performance-linked payment.

Example:

Only 50% of the performance pool is released.

---

## Step 5: Update Reliability Score

The selected network’s reliability score is updated based on the gap between claimed and verified performance.

---

## Step 6: Generate AI Explanation

AI explains the discrepancy, payout, and recommended action.

---

# 11. Data Requirements

## 11.1 Campaign Table

| Column               | Type   | Description                           |
| -------------------- | ------ | ------------------------------------- |
| campaign_id          | string | Unique campaign identifier            |
| campaign_name        | string | Campaign name                         |
| network_name         | string | Retail media network                  |
| campaign_invoice     | float  | Total invoice amount                  |
| claimed_lift         | float  | Lift reported by network              |
| claimed_revenue      | float  | Revenue reported by network           |
| base_payment_pct     | float  | Guaranteed payment percentage         |
| performance_pool_pct | float  | Performance-linked payment percentage |
| start_date           | date   | Campaign start date                   |
| end_date             | date   | Campaign end date                     |

---

## 11.2 Test-Control Table

| Column           | Type   | Description                |
| ---------------- | ------ | -------------------------- |
| campaign_id      | string | Campaign identifier        |
| group_type       | string | exposed or holdout         |
| users            | int    | Number of users in group   |
| conversions      | int    | Number of conversions      |
| revenue          | float  | Revenue generated          |
| new_customers    | int    | Number of new customers    |
| repeat_customers | int    | Number of repeat customers |

---

## 11.3 Network History Table

| Column            | Type   | Description                                  |
| ----------------- | ------ | -------------------------------------------- |
| network_name      | string | Network name                                 |
| campaign_id       | string | Campaign identifier                          |
| claimed_lift      | float  | Network-reported lift                        |
| verified_lift     | float  | VeriLift-calculated lift                     |
| deviation         | float  | Difference between claimed and verified lift |
| reliability_score | float  | Trust score                                  |

---

# 12. Success Metrics

## 12.1 Product Success Metrics

| Metric                           | Target           |
| -------------------------------- | ---------------- |
| Time to understand product value | Under 60 seconds |
| Time to run verification         | Under 5 seconds  |
| Number of simulated networks     | Minimum 3        |
| Campaigns in demo dataset        | Minimum 10       |
| AI explanation generation        | Under 10 seconds |
| Screens required for demo        | 3–4 maximum      |

---

## 12.2 Business Metrics Shown in Product

| Metric                     | Meaning                                      |
| -------------------------- | -------------------------------------------- |
| Claimed Lift               | Performance reported by network              |
| Verified Lift              | Independently calculated incremental lift    |
| Verification Ratio         | Verified lift divided by claimed lift        |
| Released Payment           | Performance-linked payout released           |
| Adjusted Amount            | Amount held, credited, or disputed           |
| Reliability Score          | Long-term trust score of network             |
| Recommended Contract Split | Suggested base/performance payment structure |

---

## 12.3 Customer Experience Metrics Connected to Theme

| Metric                    | CX Meaning                                                         |
| ------------------------- | ------------------------------------------------------------------ |
| Verified Incremental Lift | Campaign actually influenced customers                             |
| Low Verified Lift         | Campaign may be retargeting users who would have bought anyway     |
| Repeat Buyer Over-Credit  | Risk of over-targeting loyal customers                             |
| New Customer Lift         | Campaign helped acquire genuinely new customers                    |
| Reliability Score         | Helps brands choose networks that create real customer value       |
| CX Waste Signal           | Indicates spend that may create unnecessary impressions or fatigue |

---

# 13. AI Usage

VeriLift should use AI carefully.

AI should not calculate verified lift or payment directly.

Those calculations should be deterministic and auditable.

AI should be used for explanation and decision support.

## AI Use Cases

1. **Discrepancy Explanation**
   Explain why claimed and verified lift differ.

2. **Settlement Summary**
   Generate a neutral payment explanation.

3. **Contract Recommendation**
   Suggest base/performance payment split based on reliability.

4. **Customer Experience Impact Explanation**
   Explain how over-attribution can lead to over-targeting and poor CX.

5. **Executive Summary**
   Generate a CMO-friendly insight.

---

# 14. Technical Architecture

## 14.1 Recommended Hackathon Stack

| Layer           | Tool                            |
| --------------- | ------------------------------- |
| Frontend        | Streamlit                       |
| Data Processing | Python + Pandas                 |
| Visualization   | Plotly                          |
| AI Layer        | Gemini / Claude / OpenAI / Groq |
| Storage         | CSV / SQLite                    |
| Deployment      | Streamlit Cloud / Render        |

---

## 14.2 Architecture Flow

Campaign Dataset
↓
Claimed Performance Reader
↓
Exposed vs Holdout Lift Calculator
↓
Claimed vs Verified Comparison
↓
Settlement Engine
↓
Network Reliability Scorer
↓
AI Explanation Layer
↓
Dashboard UI

---

# 15. Demo Story

## Demo Setup

A beauty brand runs campaigns across three retail media networks:

* RetailNet A
* RetailNet B
* RetailNet C

All three networks claim strong lift.

At first, they all look successful.

But VeriLift verifies actual lift using holdout groups.

## Demo Reveal

RetailNet A claimed 20% lift but verified lift is only 10%.
RetailNet B claimed 14% lift and verified lift is 13%.
RetailNet C claimed 24% lift but verified lift is only 7%.

The brand realizes that RetailNet B is the most trustworthy network, even though it did not claim the highest performance.

## Final Demo Moment

The system adjusts payment:

RetailNet C does not receive the full performance-linked payout because verified lift is far below claimed lift.

The leaderboard updates and recommends a stricter contract for RetailNet C.

---

# 16. Hackathon Build Timeline

## Day 1: Core Data and Verification

Deliverables:

* synthetic campaign dataset
* exposed and holdout group generator
* verified lift calculator
* claimed vs verified comparison

---

## Day 2: Settlement and Reliability Engine

Deliverables:

* payment split logic
* settlement release calculator
* adjusted amount calculation
* reliability score calculation
* leaderboard logic

---

## Day 3: Dashboard and AI Layer

Deliverables:

* Streamlit dashboard
* campaign verification screen
* settlement screen
* reliability leaderboard
* AI explanation generation

---

## Day 4: Polish and Demo

Deliverables:

* final demo dataset
* strong UI cards
* pitch script
* README
* deployment
* fallback screenshots
* final submission video

---

# 17. Risks and Mitigations

| Risk                                              | Impact | Mitigation                                                                                       |
| ------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------ |
| Judges say independent measurement already exists | High   | Clearly say VeriLift connects measurement to settlement, not just reporting                      |
| Escrow sounds legally complex                     | Medium | Use “settlement layer” and “performance-linked payout simulation”                                |
| Theme alignment questioned                        | High   | Emphasize clear success metrics and better CX decisions                                          |
| AI usage seems weak                               | Medium | Use AI for explanations, contract recommendations, and CX impact summaries                       |
| Causal validity questioned                        | High   | Use honest language: prototype uses test-control simulation; production can use RCTs/clean rooms |
| Demo feels too financial                          | Medium | Add CX impact explanation: low verified lift means wasted targeting and customer fatigue         |
| Synthetic data looks fake                         | Medium | Use realistic noisy campaigns with different claimed vs verified gaps                            |

---

# 18. Judge Q&A Preparation

## Q1: How is this different from Nielsen or Kantar?

Answer:

“Nielsen and Kantar help measure lift. VeriLift focuses on what happens after measurement. It uses verified lift to adjust payment settlement and build network reliability scores. We are not replacing measurement vendors; we are adding a settlement and trust layer.”

---

## Q2: Why would a network agree to this?

Answer:

“Large dominant networks may not adopt this first. The entry point is challenger networks that want to prove transparency and win brand trust. A high VeriLift reliability score becomes a competitive advantage.”

---

## Q3: Is this actual escrow?

Answer:

“In the prototype, we simulate escrow-style settlement. In production, this could be implemented as invoice adjustment, credit, rebate, or performance-linked contract terms.”

---

## Q4: Is the lift calculation truly causal?

Answer:

“The MVP uses a test-control simulation with difference-in-means. In production, VeriLift can integrate with randomized holdouts, ghost bidding, clean rooms, or third-party sales lift feeds.”

---

## Q5: How does this improve customer experience?

Answer:

“If brands scale campaigns based on inflated attribution, they may keep retargeting customers who would have bought anyway, causing wasted impressions and ad fatigue. VeriLift helps brands scale only campaigns that create real incremental customer value.”

---

# 19. Final MVP Definition

The MVP is successful if it can:

1. Show claimed lift from retail media networks.
2. Calculate verified lift using exposed and holdout groups.
3. Compare claimed and verified performance.
4. Calculate payment settlement based on verified lift.
5. Update reliability scores for multiple networks.
6. Generate AI explanation and settlement summary.
7. Clearly explain the customer experience benefit.
8. Demonstrate the product value in under 3 minutes.

---

# 20. Final Pitch

Retail media brands currently pay platforms based on numbers reported by the same platforms selling the ads.

That creates a trust problem.

VeriLift solves this by independently verifying incremental lift using exposed and holdout groups, then tying performance-linked payment to verified lift instead of self-reported ROAS.

If a network claims 20% lift but VeriLift verifies only 10%, only 50% of the performance-linked payout is released.

Over time, VeriLift builds a reliability score for every network, helping brands choose partners based on trust, not just claimed performance.

This improves customer experience because brands stop scaling campaigns that merely retarget customers who would have bought anyway and start investing in campaigns that create real incremental customer value.

**VeriLift turns retail media success from a self-reported dashboard number into a trusted, measurable, and financially enforceable outcome.**

---

# 21. Final Theme Alignment Statement

VeriLift is built for Theme 02 because it creates a clear, trusted measure of success for omnichannel retail media campaigns.

In a world where customer experiences are shaped by ads, recommendations, retargeting, and retail media placements, brands need to know which campaigns actually move customers forward.

VeriLift makes the success metric clear:

**verified incremental lift.**

It then connects that metric to payment, network trust, and better customer experience decisions.

Therefore, VeriLift supports seamless customer experiences by helping brands invest only in campaigns that create genuine incremental customer value.
