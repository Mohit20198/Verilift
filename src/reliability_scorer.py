"""
VeriLift — Network Reliability Scorer
Phase 4: Rank retail media networks by how closely their claimed lift
         matches independently verified lift, across all campaigns.

Uses BOTH:
  - data/network_history.csv  (past campaigns — historical record)
  - Current campaign results  (from lift_calculator.py — live demo campaigns)

Formula (locked — do not change without user approval):
  Deviation per campaign = abs(claimed_lift - verified_lift) / claimed_lift
  Reliability Score      = 100 * (1 - average_deviation)
  Score is capped between 0 and 100.

Risk Levels:
  score >= 85   -> Low Risk
  60 to 84      -> Medium Risk
  30 to 59      -> High Risk
  below 30      -> Severe Risk

Contract Recommendations:
  Low Risk      -> 80% base / 20% verified performance
  Medium Risk   -> 60% base / 40% verified performance
  High Risk     -> 50% base / 50% verified performance
  Severe Risk   -> 40% base / 60% verified performance

Expected ranking: RetailNet B (highest) > RetailNet A (middle) > RetailNet C (lowest)
"""

import os
import pandas as pd

from utils import safe_divide
from lift_calculator import get_lift_results, load_data


# ---------------------------------------------------------------------------
# Risk and contract classifiers
# ---------------------------------------------------------------------------

def classify_risk_level(score: float) -> str:
    """Return risk tier based on reliability score."""
    if score >= 85:
        return "Low Risk"
    if score >= 60:
        return "Medium Risk"
    if score >= 30:
        return "High Risk"
    return "Severe Risk"


def recommend_contract_split(risk_level: str) -> str:
    """Return recommended payment split based on risk level."""
    mapping = {
        "Low Risk":     "80% base / 20% verified performance",
        "Medium Risk":  "60% base / 40% verified performance",
        "High Risk":    "50% base / 50% verified performance",
        "Severe Risk":  "40% base / 60% verified performance",
    }
    return mapping.get(risk_level, "50% base / 50% verified performance")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_history(data_dir: str = "data") -> pd.DataFrame:
    """Load network_history.csv (past campaigns for historical scoring)."""
    path = os.path.join(data_dir, "network_history.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing: {path}. Run src/data_generator.py first."
        )
    df = pd.read_csv(path)
    df["claimed_lift"] = pd.to_numeric(df["claimed_lift"], errors="coerce")
    df["verified_lift"] = pd.to_numeric(df["verified_lift"], errors="coerce")
    return df


def build_combined_records(data_dir: str = "data") -> pd.DataFrame:
    """
    Combine historical records (network_history.csv) with current verified
    lift results (from lift_calculator) into a unified DataFrame.

    Each row has: network_name, campaign_id, claimed_lift, verified_lift, source
    """
    # --- Historical records ---
    history = load_history(data_dir)
    history_records = history[["network_name", "campaign_id",
                                "claimed_lift", "verified_lift"]].copy()
    history_records["source"] = "historical"

    # --- Current campaign results ---
    lift_df = get_lift_results(data_dir)
    current_records = lift_df[["network_name", "campaign_id",
                                "claimed_lift", "verified_lift_relative"]].copy()
    current_records = current_records.rename(
        columns={"verified_lift_relative": "verified_lift"}
    )
    # Only include campaigns where both values are available
    current_records = current_records.dropna(
        subset=["claimed_lift", "verified_lift"]
    )
    current_records["source"] = "current"

    # Combine
    combined = pd.concat([history_records, current_records], ignore_index=True)
    return combined


# ---------------------------------------------------------------------------
# Core reliability calculation
# ---------------------------------------------------------------------------

def calculate_reliability(combined: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate per-network reliability scores from combined historical +
    current campaign data.

    Returns a DataFrame sorted by reliability_score descending.
    """
    results = []

    for network_name, group in combined.groupby("network_name"):
        n_campaigns = len(group)

        avg_claimed = group["claimed_lift"].mean()
        avg_verified = group["verified_lift"].mean()

        # Per-campaign deviation, then average
        group = group.copy()
        group["deviation"] = group.apply(
            lambda r: safe_divide(
                abs(r["claimed_lift"] - r["verified_lift"]),
                r["claimed_lift"],
                default=0.0,
            ),
            axis=1,
        )
        avg_deviation = group["deviation"].mean()

        # Reliability score, capped 0–100
        raw_score = 100.0 * (1.0 - avg_deviation)
        reliability_score = round(max(0.0, min(100.0, raw_score)), 2)

        risk_level = classify_risk_level(reliability_score)
        contract_split = recommend_contract_split(risk_level)

        results.append({
            "network_name": network_name,
            "n_campaigns": n_campaigns,
            "avg_claimed_lift": round(avg_claimed, 6),
            "avg_verified_lift": round(avg_verified, 6),
            "avg_deviation": round(avg_deviation, 6),
            "reliability_score": reliability_score,
            "risk_level": risk_level,
            "recommended_contract_split": contract_split,
        })

    df = pd.DataFrame(results)
    df = df.sort_values("reliability_score", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_reliability_scores(data_dir: str = "data") -> pd.DataFrame:
    """Load all data, compute, and return the reliability leaderboard."""
    combined = build_combined_records(data_dir)
    return calculate_reliability(combined)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _print_results(df: pd.DataFrame):
    print("\nVeriLift -- Network Reliability Leaderboard (Phase 4)")
    print("=" * 70)
    print(f"{'Rank':<5} {'Network':<15} {'Claimed':>9} {'Verified':>9} "
          f"{'Score':>7} {'Risk':<18} {'Contract Split'}")
    print("-" * 70)

    for _, row in df.iterrows():
        print(
            f"  #{row['rank']:<3} "
            f"{row['network_name']:<15} "
            f"{row['avg_claimed_lift']*100:>7.1f}%  "
            f"{row['avg_verified_lift']*100:>7.1f}%  "
            f"{row['reliability_score']:>6.1f}  "
            f"{row['risk_level']:<18} "
            f"{row['recommended_contract_split']}"
        )

    print("\nDetailed breakdown:")
    print("-" * 70)
    for _, row in df.iterrows():
        print(f"\n  {row['network_name']}  (based on {row['n_campaigns']} campaigns)")
        print(f"    Avg Claimed Lift     : {row['avg_claimed_lift']*100:.1f}%")
        print(f"    Avg Verified Lift    : {row['avg_verified_lift']*100:.1f}%")
        print(f"    Avg Deviation        : {row['avg_deviation']*100:.1f}%")
        print(f"    Reliability Score    : {row['reliability_score']:.1f} / 100")
        print(f"    Risk Level           : {row['risk_level']}")
        print(f"    Recommended Split    : {row['recommended_contract_split']}")

    print("\nStory check:")
    top = df.iloc[0]["network_name"]
    bottom = df.iloc[-1]["network_name"]
    result = "[PASS]" if top == "RetailNet B" and bottom == "RetailNet C" else "[FAIL]"
    print(f"  {result}  Top = {top}  |  Bottom = {bottom}")
    print(f"  Expected: Top = RetailNet B  |  Bottom = RetailNet C")


if __name__ == "__main__":
    df = get_reliability_scores(data_dir="data")
    _print_results(df)
    print(f"\nTotal networks scored: {len(df)}")
    print("Phase 4 complete. Do not proceed to Phase 5 until user approval.")
