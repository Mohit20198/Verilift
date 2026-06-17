"""
VeriLift — AI Insights Module
Phase 10: Generate plain-English insights from lift, settlement, and reliability data.

This module works in two modes:
  1. Rule-based (always available, no API key required) — deterministic, fast, demo-safe.
  2. Gemini AI (optional) — activates only if GOOGLE_API_KEY is set in .env

Insight categories:
  1. discrepancy_explanation  — why claimed and verified lift differ
  2. settlement_summary       — what was released and why
  3. cx_impact                — customer experience implications
  4. recommended_action       — what the brand should do next
  5. contract_recommendation  — suggested payment split for future campaigns

Public API:
  get_insights(campaign_id, settlement_df, lift_df, reliability_df) -> InsightResult dict
"""

import os
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Result structure
# ---------------------------------------------------------------------------

@dataclass
class InsightResult:
    campaign_id: str
    campaign_name: str
    network_name: str
    discrepancy_explanation: str
    settlement_summary: str
    cx_impact: str
    recommended_action: str
    contract_recommendation: str
    insight_source: str          # "rule-based" or "gemini-ai"
    confidence_level: str        # "High" / "Medium" / "Low"
    notes: str = ""

    def to_dict(self):
        return asdict(self)


# ---------------------------------------------------------------------------
# Rule-based insight engine
# ---------------------------------------------------------------------------

def _classify_discrepancy(verification_ratio) -> str:
    """Return a short label for the discrepancy level."""
    if verification_ratio is None:
        return "unknown"
    if verification_ratio >= 0.90:
        return "minimal"
    if verification_ratio >= 0.60:
        return "moderate"
    if verification_ratio >= 0.30:
        return "significant"
    return "severe"


def _generate_discrepancy_explanation(row: dict) -> str:
    claimed     = row.get("claimed_lift", 0) or 0
    verified    = row.get("verified_lift_relative", 0) or 0
    overstate   = row.get("overstatement_factor")
    ratio       = row.get("verification_ratio", 0) or 0
    network     = row.get("network_name", "The network")
    camp_name   = row.get("campaign_name", "this campaign")
    level       = _classify_discrepancy(ratio)

    claimed_pct  = claimed * 100
    verified_pct = verified * 100

    if level == "minimal":
        return (
            f"{network} claimed **{claimed_pct:.1f}% lift** and VeriLift verified "
            f"**{verified_pct:.1f}% lift** for '{camp_name}'. This is a strong alignment — "
            f"the network's measurement methodology appears reliable and the reported "
            f"performance closely reflects the true incremental impact of the campaign."
        )
    elif level == "moderate":
        return (
            f"{network} claimed **{claimed_pct:.1f}% lift** but VeriLift verified "
            f"**{verified_pct:.1f}% lift** for '{camp_name}'. A moderate discrepancy of "
            f"**{(claimed_pct - verified_pct):.1f} percentage points** was detected. "
            f"This may reflect attribution window differences, last-touch vs incremental "
            f"measurement, or partial retargeting of customers who would have converted anyway."
        )
    elif level == "significant":
        os_str = f"{overstate:.1f}x" if overstate and overstate != float("inf") else "significantly"
        return (
            f"{network} claimed **{claimed_pct:.1f}% lift** but VeriLift verified only "
            f"**{verified_pct:.1f}% lift** for '{camp_name}'. The network is overstating "
            f"performance by approximately **{os_str}**. A large share of attributed "
            f"conversions likely came from customers who would have purchased regardless of "
            f"the campaign — a pattern known as 'retargeting inflation'."
        )
    else:  # severe
        os_str = f"{overstate:.1f}x" if overstate and overstate != float("inf") else "dramatically"
        return (
            f"{network} claimed **{claimed_pct:.1f}% lift** but VeriLift verified only "
            f"**{verified_pct:.1f}% lift** for '{camp_name}' — an overstatement of "
            f"**{os_str}**. This is a severe discrepancy. The campaign appears to have "
            f"primarily retargeted existing customers who would have converted without any "
            f"ad exposure. Self-reported ROAS for this campaign cannot be trusted for "
            f"future budget decisions."
        )


def _generate_settlement_summary(row: dict) -> str:
    network      = row.get("network_name", "The network")
    invoice      = row.get("campaign_invoice", 0) or 0
    base_pay     = row.get("base_payment", 0) or 0
    pool         = row.get("performance_pool", 0) or 0
    released     = row.get("released_performance_payment", 0) or 0
    final_pay    = row.get("final_payable", 0) or 0
    adjusted     = row.get("adjusted_amount", 0) or 0
    ratio_capped = row.get("verification_ratio_capped", 0) or 0
    status       = row.get("settlement_status", "")

    pct_released = ratio_capped * 100
    pct_withheld = 100 - pct_released

    return (
        f"Total invoice: **INR {invoice:,.0f}**. "
        f"The guaranteed base payment of **INR {base_pay:,.0f}** is released in full. "
        f"From the performance pool of **INR {pool:,.0f}**, "
        f"**{pct_released:.0f}%** (INR {released:,.0f}) is released based on a verification "
        f"ratio of **{ratio_capped:.2f}**. "
        f"**INR {adjusted:,.0f}** ({pct_withheld:.0f}% of the pool) is withheld as a "
        f"performance adjustment. Final payable to {network}: **INR {final_pay:,.0f}**. "
        f"Settlement status: **{status}**."
    )


def _generate_cx_impact(row: dict, reliability_row: Optional[dict] = None) -> str:
    ratio    = row.get("verification_ratio", 0) or 0
    verified = row.get("verified_lift_relative", 0) or 0
    network  = row.get("network_name", "The network")
    level    = _classify_discrepancy(ratio)

    rel_score = reliability_row.get("reliability_score") if reliability_row else None

    if level == "minimal":
        return (
            f"This campaign delivered genuine incremental value. Customers in the exposed "
            f"group were meaningfully more likely to convert than those in the holdout — "
            f"a **{verified*100:.1f}% verified lift** indicates the campaign reached the "
            f"right audience at the right time. Brand spend is creating real CX impact, "
            f"not just inflating attributed revenue."
        )
    elif level in ("moderate",):
        return (
            f"A portion of the campaign budget reached customers who were likely to convert "
            f"anyway. While some genuine lift was delivered (**{verified*100:.1f}%**), "
            f"a meaningful share of attributed conversions came from high-intent shoppers "
            f"who did not need ad nudging. This represents a CX efficiency opportunity — "
            f"tighter audience targeting could improve true incremental reach."
        )
    else:
        return (
            f"The majority of this campaign's attributed conversions came from customers "
            f"who would have purchased without ad exposure — a pattern known as "
            f"'wasteful retargeting'. This harms CX by over-messaging existing intent, "
            f"consuming budget that could reach genuinely new or at-risk customers, and "
            f"inflating ROAS figures that lead to poor future budget allocation. "
            f"VeriLift's verified lift of only **{verified*100:.1f}%** exposes this gap "
            f"before it compounds across future campaigns."
            + (
                f" {network}'s reliability score of **{rel_score:.1f}/100** suggests "
                f"this is a recurring pattern across campaigns."
                if rel_score is not None and rel_score < 60 else ""
            )
        )


def _generate_recommended_action(row: dict, reliability_row: Optional[dict] = None) -> str:
    ratio   = row.get("verification_ratio", 0) or 0
    network = row.get("network_name", "the network")
    level   = _classify_discrepancy(ratio)

    if level == "minimal":
        return (
            f"Continue investing in {network} with confidence. The verification ratio of "
            f"**{ratio:.2f}** demonstrates transparent and reliable performance measurement. "
            f"Consider increasing the performance pool allocation in future contracts to "
            f"reward this trustworthy reporting."
        )
    elif level == "moderate":
        return (
            f"Request attribution methodology documentation from {network}. Investigate "
            f"whether campaign targeting is over-indexing on high-intent repeat customers "
            f"vs genuinely incremental new audiences. Recommend running a prospecting-focused "
            f"campaign variant alongside a retargeting test to compare verified lift across "
            f"audience types."
        )
    elif level == "significant":
        return (
            f"Require {network} to improve audience segmentation — specifically, reduce "
            f"retargeting of recent purchasers and high-intent repeat visitors. Before the "
            f"next campaign, negotiate a holdout group requirement into the contract SLA. "
            f"Consider reducing the total campaign budget until measurement methodology "
            f"is reviewed and verified lift improves above 60% of claimed lift."
        )
    else:
        return (
            f"Escalate to procurement review. {network.title()}'s measurement methodology "
            f"is producing severely overstated results. Pause new campaign launches until "
            f"a third-party attribution audit is completed. Restructure any existing contract "
            f"to require **100% performance-linked payment** with VeriLift verification as the "
            f"sole settlement trigger. Consider placing {network} on a network reliability "
            f"watch list for at least two consecutive verified campaigns before restoring "
            f"standard payment terms."
        )


def _generate_contract_recommendation(row: dict, reliability_row: Optional[dict] = None) -> str:
    ratio   = row.get("verification_ratio", 0) or 0
    network = row.get("network_name", "the network")
    level   = _classify_discrepancy(ratio)

    if reliability_row:
        split = reliability_row.get("recommended_contract_split", "50% base / 50% verified performance")
        risk  = reliability_row.get("risk_level", "Unknown")
        score = reliability_row.get("reliability_score", 0)
        return (
            f"Based on {network}'s overall reliability score of **{score:.1f}/100** "
            f"({risk}), the recommended future contract structure is: "
            f"**{split}**. "
            f"This means the guaranteed base payment is reduced proportionally to the "
            f"network's historical tendency to overstate performance, protecting brand "
            f"spend while still incentivising the network to improve measurement quality."
        )

    # Fallback if no reliability row
    splits = {
        "minimal":     "80% base / 20% verified performance",
        "moderate":    "60% base / 40% verified performance",
        "significant": "50% base / 50% verified performance",
        "severe":      "40% base / 60% verified performance",
    }
    recommended = splits.get(level, "50% base / 50% verified performance")
    return (
        f"For future campaigns with {network}, apply a contract split of "
        f"**{recommended}**. This structure ensures the brand only pays full value "
        f"when performance is independently verified, creating a direct financial "
        f"incentive for accurate measurement."
    )


def generate_rule_based_insights(
    campaign_row: dict,
    reliability_row: Optional[dict] = None,
) -> InsightResult:
    """
    Generate all 5 insight categories using rule-based logic.
    Never fails — always returns a complete InsightResult.
    """
    return InsightResult(
        campaign_id=campaign_row.get("campaign_id", ""),
        campaign_name=campaign_row.get("campaign_name", ""),
        network_name=campaign_row.get("network_name", ""),
        discrepancy_explanation=_generate_discrepancy_explanation(campaign_row),
        settlement_summary=_generate_settlement_summary(campaign_row),
        cx_impact=_generate_cx_impact(campaign_row, reliability_row),
        recommended_action=_generate_recommended_action(campaign_row, reliability_row),
        contract_recommendation=_generate_contract_recommendation(campaign_row, reliability_row),
        insight_source="rule-based",
        confidence_level="High",
        notes="Generated from verified lift and settlement data using locked VeriLift formulas.",
    )


# ---------------------------------------------------------------------------
# Optional: Groq AI enhancement
# ---------------------------------------------------------------------------

def _try_load_groq_key() -> Optional[str]:
    """Try to load GROQ_API_KEY from .env or environment."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    return os.environ.get("GROQ_API_KEY")


def _build_groq_prompt(campaign_row: dict, rule_insights: InsightResult) -> str:
    """Build a concise prompt for Groq to enhance the rule-based insights."""
    claimed   = (campaign_row.get("claimed_lift", 0) or 0) * 100
    verified  = (campaign_row.get("verified_lift_relative", 0) or 0) * 100
    ratio     = campaign_row.get("verification_ratio", 0) or 0
    network   = campaign_row.get("network_name", "")
    camp      = campaign_row.get("campaign_name", "")
    invoice   = campaign_row.get("campaign_invoice", 0) or 0
    final_pay = campaign_row.get("final_payable", 0) or 0

    return f"""You are VeriLift's AI analyst. A retail media brand needs insights about a campaign.

Campaign: {camp} | Network: {network}
Claimed Lift: {claimed:.1f}% | Verified Lift: {verified:.1f}% | Verification Ratio: {ratio:.2f}
Invoice: INR {invoice:,.0f} | Final Payable: INR {final_pay:,.0f}

The following rule-based insights have been generated. Rewrite each one in a more engaging, executive-friendly tone (1-2 sentences each). Keep all numbers exactly as stated. Do not add new facts.

DISCREPANCY: {rule_insights.discrepancy_explanation}
SETTLEMENT: {rule_insights.settlement_summary}
CX IMPACT: {rule_insights.cx_impact}
RECOMMENDED ACTION: {rule_insights.recommended_action}
CONTRACT: {rule_insights.contract_recommendation}

Respond in this exact JSON format:
{{
  "discrepancy_explanation": "...",
  "settlement_summary": "...",
  "cx_impact": "...",
  "recommended_action": "...",
  "contract_recommendation": "..."
}}"""


def _try_groq_enhance(
    campaign_row: dict,
    rule_insights: InsightResult,
    api_key: str,
) -> InsightResult:
    """Try to enhance insights using Groq. Falls back to rule-based on any error."""
    try:
        import json
        from groq import Groq

        client = Groq(api_key=api_key)
        prompt = _build_groq_prompt(campaign_row, rule_insights)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        text = chat_completion.choices[0].message.content
        data = json.loads(text)

        return InsightResult(
            campaign_id=rule_insights.campaign_id,
            campaign_name=rule_insights.campaign_name,
            network_name=rule_insights.network_name,
            discrepancy_explanation=data.get("discrepancy_explanation", rule_insights.discrepancy_explanation),
            settlement_summary=data.get("settlement_summary", rule_insights.settlement_summary),
            cx_impact=data.get("cx_impact", rule_insights.cx_impact),
            recommended_action=data.get("recommended_action", rule_insights.recommended_action),
            contract_recommendation=data.get("contract_recommendation", rule_insights.contract_recommendation),
            insight_source="groq-ai",
            confidence_level="High",
            notes="Enhanced by Groq AI from VeriLift verified data.",
        )
    except Exception as e:
        rule_insights.notes += f" | Groq enhancement failed: {str(e)[:80]}"
        return rule_insights


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_insights(
    campaign_id: str,
    settlement_df,
    lift_df,
    reliability_df,
    use_ai: bool = True,
) -> InsightResult:
    """
    Generate complete insights for a campaign.

    Args:
        campaign_id     : Campaign ID string (e.g. 'CMP_A001')
        settlement_df   : DataFrame from settlement_engine.get_settlement_results()
        lift_df         : DataFrame from lift_calculator.get_lift_results()
        reliability_df  : DataFrame from reliability_scorer.get_reliability_scores()
        use_ai          : If True, try Gemini enhancement (falls back to rule-based)

    Returns:
        InsightResult dataclass (always succeeds)
    """
    import pandas as pd

    # Pull settlement row
    s_rows = settlement_df[settlement_df["campaign_id"] == campaign_id]
    if s_rows.empty:
        return InsightResult(
            campaign_id=campaign_id,
            campaign_name="Unknown",
            network_name="Unknown",
            discrepancy_explanation="No data found for this campaign.",
            settlement_summary="No settlement data found.",
            cx_impact="No data available.",
            recommended_action="Run data_generator.py to generate campaign data.",
            contract_recommendation="N/A",
            insight_source="rule-based",
            confidence_level="Low",
            notes="Campaign not found in settlement data.",
        )
    campaign_row = s_rows.iloc[0].to_dict()

    # Pull reliability row for this network
    network = campaign_row.get("network_name")
    r_rows = reliability_df[reliability_df["network_name"] == network] if reliability_df is not None else None
    reliability_row = r_rows.iloc[0].to_dict() if (r_rows is not None and not r_rows.empty) else None

    # Generate rule-based insights first (always safe)
    rule_insights = generate_rule_based_insights(campaign_row, reliability_row)

    # Try Groq enhancement if requested
    if use_ai:
        api_key = _try_load_groq_key()
        if api_key:
            return _try_groq_enhance(campaign_row, rule_insights, api_key)

    return rule_insights


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))

    from settlement_engine import get_settlement_results
    from lift_calculator import get_lift_results
    from reliability_scorer import get_reliability_scores

    print("\nVeriLift -- AI Insights Module (Phase 10)")
    print("=" * 60)

    settlement_df  = get_settlement_results(data_dir="data")
    lift_df        = get_lift_results(data_dir="data")
    reliability_df = get_reliability_scores(data_dir="data")

    test_campaigns = ["CMP_A001", "CMP_B001", "CMP_C001"]

    for cid in test_campaigns:
        result = get_insights(cid, settlement_df, lift_df, reliability_df, use_ai=True)
        print(f"\n{'='*60}")
        print(f"Campaign  : {result.campaign_id} | {result.campaign_name}")
        print(f"Network   : {result.network_name}")
        print(f"Source    : {result.insight_source}")
        print(f"Confidence: {result.confidence_level}")
        print(f"\n[1] DISCREPANCY EXPLANATION")
        print(f"    {result.discrepancy_explanation}")
        print(f"\n[2] SETTLEMENT SUMMARY")
        print(f"    {result.settlement_summary}")
        print(f"\n[3] CX IMPACT")
        print(f"    {result.cx_impact}")
        print(f"\n[4] RECOMMENDED ACTION")
        print(f"    {result.recommended_action}")
        print(f"\n[5] CONTRACT RECOMMENDATION")
        print(f"    {result.contract_recommendation}")

    print(f"\n{'='*60}")
    api_key = _try_load_groq_key()
    print(f"GROQ_API_KEY present: {'Yes' if api_key else 'No (rule-based mode)'}")
    print("Phase 10 complete. Do not proceed to Phase 11 until user approval.")
