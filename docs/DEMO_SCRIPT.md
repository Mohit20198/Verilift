# VeriLift — Hackathon Demo Script (TeXpedition 2026)

**Duration:** ~3 Minutes
**Presenter Setup:** Have `app.py` running locally on `http://localhost:8507`. Keep the sidebar open.

---

## 1. The 30-Second Intro (The Hook)

**[Screen: Overview Page]**

"Good morning, judges. We are presenting VeriLift for Theme 2: AI for seamless customer experiences across channels while defining clear measures of success.

Right now, retail media networks grade their own homework. Brands pay based on self-reported ROAS, even when many of those conversions would have happened without the ad exposure. This leads to wasted budgets and poor customer experiences, as brands aggressively retarget customers who were going to buy anyway.

Measurement already exists. **VeriLift adds financial consequence to measurement.** 

VeriLift independently verifies true incremental lift using exposed vs holdout groups, and automatically adjusts the performance-linked payout based on that verification."

---

## 2. The 2-Minute Demo Flow

### A. Campaign Verification
**[Click 'Campaign Verification' in the sidebar. Select 'Summer Beauty Sale (RetailNet A)']**

"Let’s look at a live example. RetailNet A invoiced us for a Summer Beauty Sale, claiming a 20% lift. 

VeriLift independently verified this by comparing the exposed group to a control holdout group. Our math shows the true incremental lift was only 10%. 

That’s a 2x overstatement. In the old world, we would have paid their invoice in full. With VeriLift, we flag this discrepancy immediately."

### B. Settlement Engine
**[Click 'Settlement Engine' in the sidebar. Keep 'Summer Beauty Sale' selected]**

"This is where VeriLift enforces accountability. 

For this campaign, the brand guaranteed a 50% base payment. The remaining 50% was an at-risk performance pool. Because the verified lift was only half of what was claimed, our smart contract engine only releases 50% of the performance pool. 

Instead of paying the full INR 500,000 invoice, VeriLift adjusted the final payable to INR 375,000—saving the brand INR 125,000 that would have otherwise been wasted on over-attributed metrics."

### C. Network Reliability Leaderboard
**[Click 'Reliability Leaderboard' in the sidebar]**

"Over time, VeriLift aggregates these verification ratios into a Reliability Score. 

Here we can instantly see that RetailNet B is our most trustworthy partner, consistently delivering verified lift that matches their claims. RetailNet C, however, is severely overclaiming. 

This gives our marketing procurement team the exact leverage they need to re-negotiate future contracts—perhaps moving RetailNet C to a 100% performance-linked payment model."

### D. AI Insights
**[Click 'AI Insights' in the sidebar. Select 'Flash Sale Amplifier (RetailNet C)']**

"Finally, we use AI to translate this complex math into executive action. 

Our Groq-powered AI module analyzes the gap. For RetailNet C, it explains the customer experience impact: the network is wastefully retargeting existing customers. 

It recommends escalating to procurement and provides a mathematically backed future contract split based on their reliability score."

---

## 3. Judge Q&A Anticipation

**Q: "How do you get the holdout data?"**
A: "For this prototype, we simulate the exposed and holdout conversion rates. In production, we would integrate via clean rooms (like Snowflake or AWS Clean Rooms) or require networks to run 10% holdout groups via their ad-server APIs as a mandatory condition of the contract."

**Q: "Why not just use existing attribution tools like AppsFlyer or Google Analytics?"**
A: "Attribution tools only track who clicked or viewed an ad before buying. They don't prove incrementality (whether the ad *caused* the buy). Furthermore, they don't sit between the invoice and the payout. VeriLift is a settlement layer, not just a dashboard."

**Q: "Is this a smart contract on a blockchain?"**
A: "It operates with the logic of a smart contract—holding funds in a performance pool and releasing them programmatically based on a verified oracle (our calculator). However, for enterprise retail media, this can be implemented via standard fiat escrow APIs (like Stripe Connect) without needing blockchain."

---

## 4. Final Closing Line

**[Navigate back to Overview Page]**

"By paying for verified lift instead of self-reported ROAS, VeriLift protects brand budgets, forces media networks to improve their targeting, and ensures customers stop getting spammed with ads for things they were already going to buy. 

Measurement already exists. VeriLift adds financial consequence to measurement. Thank you."
