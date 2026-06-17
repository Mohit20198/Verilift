"""
VeriLift — Settlement Engine
Phase 3: Calculate payment release based on verified lift.

Formulas (locked — do not change without user approval):
  base_payment                = campaign_invoice * base_payment_pct
  performance_pool            = campaign_invoice * performance_pool_pct
  verification_ratio_capped   = min(max(verification_ratio, 0), 1)
  released_performance_payment= performance_pool * verification_ratio_capped
  final_payable               = base_payment + released_performance_payment
  adjusted_amount             = campaign_invoice - final_payable

Settlement Status Rules:
  verification_ratio >= 0.90  -> Full or Near-Full Release
  0.60 to 0.89                -> Partial Release
  0.30 to 0.59                -> High Adjustment
  below 0.30                  -> Severe Discrepancy
"""

import os
import pandas as pd

from utils import safe_divide
from lift_calculator import get_lift_results, load_data


# ---------------------------------------------------------------------------
# Settlement status classifier
# ---------------------------------------------------------------------------

def classify_settlement_status(ratio_capped):
    """Return a human-readable settlement status based on capped ratio."""
    if ratio_capped is None:
        return "Uncomputable"
    if ratio_capped >= 0.90:
        return "Full / Near-Full Release"
    if ratio_capped >= 0.60:
        return "Partial Release"
    if ratio_capped >= 0.30:
        return "High Adjustment"
    return "Severe Discrepancy"


# ---------------------------------------------------------------------------
# Core settlement calculation
# ---------------------------------------------------------------------------

def calculate_settlement(lift_df: pd.DataFrame, campaigns: pd.DataFrame) -> pd.DataFrame:
    """
    Join lift results with campaign invoice data and compute settlement.

    Args:
        lift_df   : DataFrame from lift_calculator.get_lift_results()
        campaigns : DataFrame from campaigns.csv (has invoice / payment pct)

    Returns:
        DataFrame with one row per campaign containing full settlement breakdown.
    """
    # Merge lift results with campaign invoice columns
    invoice_cols = [
        "campaign_id", "campaign_name", "network_name",
        "campaign_invoice", "base_payment_pct", "performance_pool_pct",
    ]
    merged = lift_df.merge(
        campaigns[invoice_cols],
        on=["campaign_id", "campaign_name", "network_name"],
        how="left",
    )

    results = []

    for _, row in merged.iterrows():
        invoice = row.get("campaign_invoice")
        base_pct = row.get("base_payment_pct")
        perf_pct = row.get("performance_pool_pct")
        verification_ratio = row.get("verification_ratio")

        # Base payment and performance pool (locked formula)
        base_payment = safe_divide(invoice * base_pct, 1, default=0.0) if (invoice and base_pct) else 0.0
        performance_pool = safe_divide(invoice * perf_pct, 1, default=0.0) if (invoice and perf_pct) else 0.0

        # Cap verification ratio between 0 and 1
        if verification_ratio is None:
            verification_ratio_capped = None
            released_performance_payment = 0.0
        else:
            verification_ratio_capped = min(max(float(verification_ratio), 0.0), 1.0)
            released_performance_payment = performance_pool * verification_ratio_capped

        # Final payable and adjusted amount
        final_payable = base_payment + released_performance_payment
        adjusted_amount = (invoice - final_payable) if invoice else 0.0

        # Settlement status
        settlement_status = classify_settlement_status(verification_ratio_capped)

        results.append({
            # Identity
            "campaign_id": row["campaign_id"],
            "campaign_name": row["campaign_name"],
            "network_name": row["network_name"],
            # Lift (carried through for reference)
            "claimed_lift": row.get("claimed_lift"),
            "verified_lift_relative": row.get("verified_lift_relative"),
            "verification_ratio": verification_ratio,
            "overstatement_factor": row.get("overstatement_factor"),
            "lift_status": row.get("lift_status"),
            # Settlement
            "campaign_invoice": round(invoice, 2) if invoice else 0.0,
            "base_payment_pct": base_pct,
            "performance_pool_pct": perf_pct,
            "base_payment": round(base_payment, 2),
            "performance_pool": round(performance_pool, 2),
            "verification_ratio_capped": round(verification_ratio_capped, 6) if verification_ratio_capped is not None else None,
            "released_performance_payment": round(released_performance_payment, 2),
            "final_payable": round(final_payable, 2),
            "adjusted_amount": round(adjusted_amount, 2),
            "settlement_status": settlement_status,
        })

    return pd.DataFrame(results)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_settlement_results(data_dir="data") -> pd.DataFrame:
    """Load data, compute lift, compute settlement, return full DataFrame."""
    campaigns, _ = load_data(data_dir)
    lift_df = get_lift_results(data_dir)
    return calculate_settlement(lift_df, campaigns)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _print_results(df: pd.DataFrame):
    """Pretty-print settlement results for terminal verification."""
    print("\nVeriLift -- Settlement Engine (Phase 3)")
    print("=" * 80)

    for _, row in df.iterrows():
        invoice = row["campaign_invoice"]
        base = row["base_payment"]
        pool = row["performance_pool"]
        released = row["released_performance_payment"]
        payable = row["final_payable"]
        adjusted = row["adjusted_amount"]
        ratio_c = row["verification_ratio_capped"]
        status = row["settlement_status"]

        print(f"\n  {row['campaign_id']} | {row['campaign_name']} | {row['network_name']}")
        print(f"    Claimed lift    : {row['claimed_lift']*100:.1f}%  |  "
              f"Verified lift: {row['verified_lift_relative']*100:.1f}%  |  "
              f"Ratio capped: {ratio_c:.2f}" if ratio_c is not None else "    Ratio: N/A")
        print(f"    Invoice         : INR {invoice:>12,.0f}")
        print(f"    Base payment    : INR {base:>12,.0f}  ({row['base_payment_pct']*100:.0f}% guaranteed)")
        print(f"    Perf pool       : INR {pool:>12,.0f}  ({row['performance_pool_pct']*100:.0f}% at risk)")
        print(f"    Released (pool) : INR {released:>12,.0f}  ({ratio_c*100:.0f}% of pool)" if ratio_c is not None else "    Released: N/A")
        print(f"    Final payable   : INR {payable:>12,.0f}")
        print(f"    Adjusted amount : INR {adjusted:>12,.0f}")
        print(f"    Status          : {status}")

    print("\n" + "=" * 80)
    print("Network Settlement Summary")
    print("-" * 60)
    summary = df.groupby("network_name").agg(
        total_invoice=("campaign_invoice", "sum"),
        total_payable=("final_payable", "sum"),
        total_adjusted=("adjusted_amount", "sum"),
        avg_ratio=("verification_ratio_capped", "mean"),
    ).reset_index()
    for _, r in summary.iterrows():
        pct_paid = safe_divide(r["total_payable"], r["total_invoice"]) * 100
        print(f"  {r['network_name']:<15} "
              f"Invoice=INR {r['total_invoice']:>10,.0f}  "
              f"Payable=INR {r['total_payable']:>10,.0f}  "
              f"({pct_paid:.0f}% paid)  "
              f"Adjusted=INR {r['total_adjusted']:>10,.0f}")

    print("\nFormula verification (CMP_A001 — Summer Beauty Sale):")
    demo = df[df["campaign_id"] == "CMP_A001"].iloc[0]
    print(f"  Invoice             = INR {demo['campaign_invoice']:,.0f}")
    print(f"  Base payment        = INR {demo['campaign_invoice']:,.0f} x {demo['base_payment_pct']} = INR {demo['base_payment']:,.0f}")
    print(f"  Performance pool    = INR {demo['campaign_invoice']:,.0f} x {demo['performance_pool_pct']} = INR {demo['performance_pool']:,.0f}")
    print(f"  Verif ratio capped  = {demo['verification_ratio_capped']:.2f}")
    print(f"  Released payment    = INR {demo['performance_pool']:,.0f} x {demo['verification_ratio_capped']:.2f} = INR {demo['released_performance_payment']:,.0f}")
    print(f"  Final payable       = INR {demo['base_payment']:,.0f} + INR {demo['released_performance_payment']:,.0f} = INR {demo['final_payable']:,.0f}")
    print(f"  Adjusted amount     = INR {demo['campaign_invoice']:,.0f} - INR {demo['final_payable']:,.0f} = INR {demo['adjusted_amount']:,.0f}")
    print(f"  Settlement status   = {demo['settlement_status']}")


if __name__ == "__main__":
    df = get_settlement_results(data_dir="data")
    _print_results(df)
    print(f"\nTotal campaigns settled: {len(df)}")
    print("Phase 3 complete. Do not proceed to Phase 4 until user approval.")
