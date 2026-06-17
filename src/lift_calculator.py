"""
VeriLift — Verified Lift Calculator
Phase 2: Calculate true incremental lift using exposed vs holdout groups.

Formulas (locked — do not change without user approval):
  exposed_cr              = exposed_conversions / exposed_users
  holdout_cr              = holdout_conversions / holdout_users
  absolute_lift           = exposed_cr - holdout_cr
  verified_lift_relative  = (exposed_cr - holdout_cr) / holdout_cr
  verification_ratio      = verified_lift_relative / claimed_lift
  overstatement_factor    = claimed_lift / verified_lift_relative

Edge cases handled:
  - holdout_cr == 0          -> verified_lift_relative = N/A (0.0 with flag)
  - claimed_lift == 0        -> verification_ratio = N/A (0.0 with flag)
  - verified_lift_relative == 0 -> overstatement_factor = N/A (float('inf') flagged)
  - missing campaign rows    -> skipped with warning
  - negative verified lift   -> preserved (indicates holdout outperformed exposed)
"""

import os
import pandas as pd
from utils import safe_divide, load_csv_data


# safe_divide is imported from utils.py


# ---------------------------------------------------------------------------
# Data loader
# ---------------------------------------------------------------------------

def load_data(data_dir="data"):
    """Load campaigns.csv and test_control.csv via utils.load_csv_data."""
    campaigns, test_control, _ = load_csv_data(data_dir)
    return campaigns, test_control


# ---------------------------------------------------------------------------
# Core lift calculation
# ---------------------------------------------------------------------------

def calculate_lift(campaigns: pd.DataFrame, test_control: pd.DataFrame) -> pd.DataFrame:
    """
    For each campaign, calculate all lift metrics.

    Returns a DataFrame with one row per campaign containing:
        campaign_id, campaign_name, network_name,
        exposed_users, exposed_conversions, exposed_cr,
        holdout_users, holdout_conversions, holdout_cr,
        absolute_lift, verified_lift_relative,
        claimed_lift, verification_ratio, overstatement_factor,
        lift_status, notes
    """
    results = []

    for _, camp in campaigns.iterrows():
        cid = camp["campaign_id"]
        cname = camp.get("campaign_name", "")
        network = camp.get("network_name", "")
        claimed_lift = camp.get("claimed_lift", None)

        # Pull exposed and holdout rows
        exposed_row = test_control[
            (test_control["campaign_id"] == cid) &
            (test_control["group_type"] == "exposed")
        ]
        holdout_row = test_control[
            (test_control["campaign_id"] == cid) &
            (test_control["group_type"] == "holdout")
        ]

        # Edge case: missing rows
        if exposed_row.empty or holdout_row.empty:
            print(f"  [WARN] Missing test/control rows for campaign {cid} — skipping.")
            continue

        exposed_users = exposed_row.iloc[0]["users"]
        exposed_conv = exposed_row.iloc[0]["conversions"]
        holdout_users = holdout_row.iloc[0]["users"]
        holdout_conv = holdout_row.iloc[0]["conversions"]

        # Conversion rates
        exposed_cr = safe_divide(exposed_conv, exposed_users, default=0.0)
        holdout_cr = safe_divide(holdout_conv, holdout_users, default=0.0)

        # Lift calculations
        absolute_lift = exposed_cr - holdout_cr

        # Edge case: holdout_cr == 0 → can't compute relative lift
        if holdout_cr == 0:
            verified_lift_relative = None
            notes = "holdout_cr=0; verified_lift_relative not computable"
        else:
            verified_lift_relative = safe_divide(
                exposed_cr - holdout_cr, holdout_cr, default=0.0
            )
            notes = ""

        # Edge case: claimed_lift == 0 → verification ratio not computable
        if claimed_lift is None or claimed_lift == 0:
            verification_ratio = None
            overstatement_factor = None
            notes += " | claimed_lift=0; verification_ratio not computable"
        else:
            if verified_lift_relative is None:
                verification_ratio = None
                overstatement_factor = None
            else:
                verification_ratio = safe_divide(
                    verified_lift_relative, claimed_lift, default=0.0
                )
                # Edge case: verified_lift_relative == 0 → overstatement = infinity
                if verified_lift_relative == 0:
                    overstatement_factor = float("inf")
                    notes += " | verified_lift=0; overstatement_factor=inf"
                else:
                    overstatement_factor = safe_divide(
                        claimed_lift, verified_lift_relative, default=0.0
                    )

        # Classify lift status
        if verified_lift_relative is None:
            lift_status = "Uncomputable"
        elif verified_lift_relative < 0:
            lift_status = "Negative Lift"
        elif verification_ratio is None:
            lift_status = "Unknown"
        elif verification_ratio >= 0.90:
            lift_status = "Verified"
        elif verification_ratio >= 0.60:
            lift_status = "Partial"
        elif verification_ratio >= 0.30:
            lift_status = "High Discrepancy"
        else:
            lift_status = "Severe Discrepancy"

        results.append({
            "campaign_id": cid,
            "campaign_name": cname,
            "network_name": network,
            "exposed_users": int(exposed_users),
            "exposed_conversions": int(exposed_conv),
            "exposed_cr": round(exposed_cr, 6),
            "holdout_users": int(holdout_users),
            "holdout_conversions": int(holdout_conv),
            "holdout_cr": round(holdout_cr, 6),
            "absolute_lift": round(absolute_lift, 6),
            "verified_lift_relative": round(verified_lift_relative, 6) if verified_lift_relative is not None else None,
            "claimed_lift": claimed_lift,
            "verification_ratio": round(verification_ratio, 6) if verification_ratio is not None else None,
            "overstatement_factor": round(overstatement_factor, 4) if overstatement_factor is not None and overstatement_factor != float("inf") else overstatement_factor,
            "lift_status": lift_status,
            "notes": notes.strip(" |"),
        })

    return pd.DataFrame(results)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_lift_results(data_dir="data") -> pd.DataFrame:
    """Load data and return a complete lift results DataFrame."""
    campaigns, test_control = load_data(data_dir)
    return calculate_lift(campaigns, test_control)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _print_results(df: pd.DataFrame):
    """Pretty-print the lift results for terminal verification."""
    print("\nVeriLift -- Verified Lift Calculator (Phase 2)")
    print("=" * 70)

    col_order = [
        "campaign_id", "network_name",
        "claimed_lift", "verified_lift_relative",
        "verification_ratio", "overstatement_factor", "lift_status",
    ]
    display = df[col_order].copy()

    # Format as percentages for readability
    display["claimed_lift_%"] = display["claimed_lift"].apply(
        lambda x: f"{x*100:.1f}%" if x is not None else "N/A"
    )
    display["verified_lift_%"] = display["verified_lift_relative"].apply(
        lambda x: f"{x*100:.1f}%" if x is not None else "N/A"
    )
    display["verif_ratio"] = display["verification_ratio"].apply(
        lambda x: f"{x:.2f}" if x is not None else "N/A"
    )
    display["overstatement"] = display["overstatement_factor"].apply(
        lambda x: f"{x:.2f}x" if x is not None and x != float("inf") else "inf"
    )

    out = display[["campaign_id", "network_name", "claimed_lift_%",
                   "verified_lift_%", "verif_ratio", "overstatement", "lift_status"]]
    print(out.to_string(index=False))

    print("\nNetwork Summary")
    print("-" * 50)
    summary = df.groupby("network_name").agg(
        avg_claimed=("claimed_lift", "mean"),
        avg_verified=("verified_lift_relative", "mean"),
        avg_verification_ratio=("verification_ratio", "mean"),
    ).reset_index()
    for _, row in summary.iterrows():
        print(f"  {row['network_name']:<15} "
              f"claimed={row['avg_claimed']*100:.1f}%  "
              f"verified={row['avg_verified']*100:.1f}%  "
              f"avg_ratio={row['avg_verification_ratio']:.2f}")

    print("\nEdge case check:")
    negatives = df[df["verified_lift_relative"].notna() & (df["verified_lift_relative"] < 0)]
    if negatives.empty:
        print("  No negative lift values detected.")
    else:
        print(f"  [WARN] {len(negatives)} campaign(s) with negative lift: "
              f"{list(negatives['campaign_id'])}")

    missing = df[df["verified_lift_relative"].isna()]
    if missing.empty:
        print("  No uncomputable lift values detected.")
    else:
        print(f"  [WARN] {len(missing)} campaign(s) with uncomputable lift.")


if __name__ == "__main__":
    df = get_lift_results(data_dir="data")
    _print_results(df)
    print(f"\nTotal campaigns processed: {len(df)}")
    print("Phase 2 complete. Do not proceed to Phase 3 until user approval.")
