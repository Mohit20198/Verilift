"""
VeriLift — Synthetic Data Generator
Phase 1: Generate mathematically aligned demo data for 3 retail media networks.

Data Story:
  RetailNet A → moderate overclaim  (claimed ~20%, verified ~10%)
  RetailNet B → reliable/honest     (claimed ~14%, verified ~13%)
  RetailNet C → heavy overclaim     (claimed ~24%, verified ~7%)

All numbers are deterministic and reverse-engineered so that:
  - verified_lift = (exposed_cr - holdout_cr) / holdout_cr
  - claimed_lift is always >= verified_lift for A and C
  - RetailNet B claimed ≈ verified (small honest gap)
"""

import os
import csv
import math
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def safe_divide(a, b, default=0):
    """Return a / b, or default if b is zero or None."""
    if b is None or b == 0:
        return default
    return a / b


def round2(x):
    return round(x, 2)


def fmt_date(d):
    return d.strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Campaign definitions  (all numbers are intentional, not random)
# ---------------------------------------------------------------------------
# Each entry defines one campaign.
# holdout_cr   : base conversion rate for holdout group
# verified_lift: true incremental lift (decimal) that math will produce
# claimed_lift : what the network self-reports (decimal)
# users_exposed / users_holdout: group sizes
# avg_order_value: INR per conversion
# campaign_invoice: total invoice in INR
# base_payment_pct / performance_pool_pct: split
# start_date / end_date: campaign window

CAMPAIGNS_DEF = [
    # ── RetailNet A  (moderate overclaim, verified ~10%, claimed ~20%) ───────
    {
        "campaign_id": "CMP_A001",
        "campaign_name": "Summer Beauty Sale",
        "network_name": "RetailNet A",
        "holdout_cr": 0.100,
        "verified_lift": 0.100,   # exposed_cr → 11%
        "claimed_lift": 0.200,
        "users_exposed": 10000,
        "users_holdout": 10000,
        "avg_order_value": 1800,
        "campaign_invoice": 500000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 6, 1),
        "end_date": date(2025, 6, 30),
    },
    {
        "campaign_id": "CMP_A002",
        "campaign_name": "Monsoon Skincare Push",
        "network_name": "RetailNet A",
        "holdout_cr": 0.090,
        "verified_lift": 0.111,   # exposed_cr → 10%
        "claimed_lift": 0.200,
        "users_exposed": 12000,
        "users_holdout": 12000,
        "avg_order_value": 1600,
        "campaign_invoice": 600000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 7, 1),
        "end_date": date(2025, 7, 31),
    },
    {
        "campaign_id": "CMP_A003",
        "campaign_name": "Festive Beauty Boost",
        "network_name": "RetailNet A",
        "holdout_cr": 0.110,
        "verified_lift": 0.091,   # exposed_cr → 12%
        "claimed_lift": 0.190,
        "users_exposed": 15000,
        "users_holdout": 15000,
        "avg_order_value": 2000,
        "campaign_invoice": 750000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 10, 1),
        "end_date": date(2025, 10, 31),
    },
    {
        "campaign_id": "CMP_A004",
        "campaign_name": "Year-End Loyalty Drive",
        "network_name": "RetailNet A",
        "holdout_cr": 0.095,
        "verified_lift": 0.105,   # exposed_cr → 10.5%
        "claimed_lift": 0.210,
        "users_exposed": 11000,
        "users_holdout": 11000,
        "avg_order_value": 1700,
        "campaign_invoice": 550000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 12, 1),
        "end_date": date(2025, 12, 31),
    },

    # ── RetailNet B  (reliable, verified ~13%, claimed ~14%) ────────────────
    {
        "campaign_id": "CMP_B001",
        "campaign_name": "Spring New Customer Drive",
        "network_name": "RetailNet B",
        "holdout_cr": 0.100,
        "verified_lift": 0.130,   # exposed_cr → 11.3%
        "claimed_lift": 0.140,
        "users_exposed": 10000,
        "users_holdout": 10000,
        "avg_order_value": 1900,
        "campaign_invoice": 480000,
        "base_payment_pct": 0.60,
        "performance_pool_pct": 0.40,
        "start_date": date(2025, 3, 1),
        "end_date": date(2025, 3, 31),
    },
    {
        "campaign_id": "CMP_B002",
        "campaign_name": "Wellness Category Push",
        "network_name": "RetailNet B",
        "holdout_cr": 0.095,
        "verified_lift": 0.126,   # exposed_cr → 10.7%
        "claimed_lift": 0.135,
        "users_exposed": 13000,
        "users_holdout": 13000,
        "avg_order_value": 1750,
        "campaign_invoice": 520000,
        "base_payment_pct": 0.60,
        "performance_pool_pct": 0.40,
        "start_date": date(2025, 5, 1),
        "end_date": date(2025, 5, 31),
    },
    {
        "campaign_id": "CMP_B003",
        "campaign_name": "Back to School Essentials",
        "network_name": "RetailNet B",
        "holdout_cr": 0.105,
        "verified_lift": 0.133,   # exposed_cr → 11.9%
        "claimed_lift": 0.145,
        "users_exposed": 14000,
        "users_holdout": 14000,
        "avg_order_value": 2100,
        "campaign_invoice": 700000,
        "base_payment_pct": 0.60,
        "performance_pool_pct": 0.40,
        "start_date": date(2025, 8, 1),
        "end_date": date(2025, 8, 31),
    },
    {
        "campaign_id": "CMP_B004",
        "campaign_name": "Diwali Trust Campaign",
        "network_name": "RetailNet B",
        "holdout_cr": 0.112,
        "verified_lift": 0.125,   # exposed_cr → 12.6%
        "claimed_lift": 0.138,
        "users_exposed": 16000,
        "users_holdout": 16000,
        "avg_order_value": 2300,
        "campaign_invoice": 900000,
        "base_payment_pct": 0.60,
        "performance_pool_pct": 0.40,
        "start_date": date(2025, 10, 15),
        "end_date": date(2025, 11, 14),
    },

    # ── RetailNet C  (heavy overclaim, verified ~7%, claimed ~24%) ──────────
    {
        "campaign_id": "CMP_C001",
        "campaign_name": "Flash Sale Amplifier",
        "network_name": "RetailNet C",
        "holdout_cr": 0.100,
        "verified_lift": 0.070,   # exposed_cr → 10.7%
        "claimed_lift": 0.240,
        "users_exposed": 10000,
        "users_holdout": 10000,
        "avg_order_value": 1500,
        "campaign_invoice": 450000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 4, 1),
        "end_date": date(2025, 4, 30),
    },
    {
        "campaign_id": "CMP_C002",
        "campaign_name": "Premium Brand Showcase",
        "network_name": "RetailNet C",
        "holdout_cr": 0.090,
        "verified_lift": 0.067,   # exposed_cr → 9.6%
        "claimed_lift": 0.250,
        "users_exposed": 12000,
        "users_holdout": 12000,
        "avg_order_value": 2200,
        "campaign_invoice": 800000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 6, 15),
        "end_date": date(2025, 7, 14),
    },
    {
        "campaign_id": "CMP_C003",
        "campaign_name": "Loyalty Retargeting Blitz",
        "network_name": "RetailNet C",
        "holdout_cr": 0.115,
        "verified_lift": 0.061,   # exposed_cr → 12.2%
        "claimed_lift": 0.230,
        "users_exposed": 18000,
        "users_holdout": 18000,
        "avg_order_value": 1600,
        "campaign_invoice": 650000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 9, 1),
        "end_date": date(2025, 9, 30),
    },
    {
        "campaign_id": "CMP_C004",
        "campaign_name": "Holiday Mega Push",
        "network_name": "RetailNet C",
        "holdout_cr": 0.105,
        "verified_lift": 0.076,   # exposed_cr → 11.3%
        "claimed_lift": 0.260,
        "users_exposed": 20000,
        "users_holdout": 20000,
        "avg_order_value": 1900,
        "campaign_invoice": 1000000,
        "base_payment_pct": 0.50,
        "performance_pool_pct": 0.50,
        "start_date": date(2025, 11, 15),
        "end_date": date(2025, 12, 15),
    },
]

# ---------------------------------------------------------------------------
# Historical data for network_history.csv
# These represent PAST campaigns (pre-demo) used for reliability scoring.
# ---------------------------------------------------------------------------

HISTORY_DEF = [
    # RetailNet A — past campaigns (moderate overclaim)
    {"network_name": "RetailNet A", "campaign_id": "HIS_A001", "claimed_lift": 0.185, "verified_lift": 0.095},
    {"network_name": "RetailNet A", "campaign_id": "HIS_A002", "claimed_lift": 0.210, "verified_lift": 0.105},
    {"network_name": "RetailNet A", "campaign_id": "HIS_A003", "claimed_lift": 0.195, "verified_lift": 0.098},

    # RetailNet B — past campaigns (reliable)
    {"network_name": "RetailNet B", "campaign_id": "HIS_B001", "claimed_lift": 0.130, "verified_lift": 0.120},
    {"network_name": "RetailNet B", "campaign_id": "HIS_B002", "claimed_lift": 0.145, "verified_lift": 0.138},
    {"network_name": "RetailNet B", "campaign_id": "HIS_B003", "claimed_lift": 0.125, "verified_lift": 0.118},

    # RetailNet C — past campaigns (heavy overclaim)
    {"network_name": "RetailNet C", "campaign_id": "HIS_C001", "claimed_lift": 0.235, "verified_lift": 0.065},
    {"network_name": "RetailNet C", "campaign_id": "HIS_C002", "claimed_lift": 0.255, "verified_lift": 0.072},
    {"network_name": "RetailNet C", "campaign_id": "HIS_C003", "claimed_lift": 0.220, "verified_lift": 0.060},
]


# ---------------------------------------------------------------------------
# Generator functions
# ---------------------------------------------------------------------------

def compute_verified_lift(holdout_cr, verified_lift_target):
    """
    Reverse-engineer exposed_cr so that:
        verified_lift = (exposed_cr - holdout_cr) / holdout_cr
    → exposed_cr = holdout_cr * (1 + verified_lift_target)
    """
    exposed_cr = holdout_cr * (1 + verified_lift_target)
    return exposed_cr


def build_campaigns(definitions):
    rows = []
    for d in definitions:
        exposed_cr = compute_verified_lift(d["holdout_cr"], d["verified_lift"])

        exposed_conversions = round(d["users_exposed"] * exposed_cr)
        holdout_conversions = round(d["users_holdout"] * d["holdout_cr"])

        exposed_revenue = round2(exposed_conversions * d["avg_order_value"])
        claimed_revenue = round2(
            d["campaign_invoice"] * (1 + d["claimed_lift"]) * 2.5
        )

        rows.append({
            "campaign_id": d["campaign_id"],
            "campaign_name": d["campaign_name"],
            "network_name": d["network_name"],
            "campaign_invoice": d["campaign_invoice"],
            "claimed_lift": d["claimed_lift"],
            "claimed_revenue": claimed_revenue,
            "base_payment_pct": d["base_payment_pct"],
            "performance_pool_pct": d["performance_pool_pct"],
            "start_date": fmt_date(d["start_date"]),
            "end_date": fmt_date(d["end_date"]),
        })
    return rows


def build_test_control(definitions):
    rows = []
    for d in definitions:
        exposed_cr = compute_verified_lift(d["holdout_cr"], d["verified_lift"])
        exposed_conv = round(d["users_exposed"] * exposed_cr)
        holdout_conv = round(d["users_holdout"] * d["holdout_cr"])

        exposed_rev = round2(exposed_conv * d["avg_order_value"])
        holdout_rev = round2(holdout_conv * d["avg_order_value"])

        # New vs repeat split: exposed group has more new customers (CX benefit story)
        exposed_new = round(exposed_conv * 0.45)
        exposed_repeat = exposed_conv - exposed_new

        holdout_new = round(holdout_conv * 0.30)
        holdout_repeat = holdout_conv - holdout_new

        rows.append({
            "campaign_id": d["campaign_id"],
            "group_type": "exposed",
            "users": d["users_exposed"],
            "conversions": exposed_conv,
            "revenue": exposed_rev,
            "new_customers": exposed_new,
            "repeat_customers": exposed_repeat,
        })
        rows.append({
            "campaign_id": d["campaign_id"],
            "group_type": "holdout",
            "users": d["users_holdout"],
            "conversions": holdout_conv,
            "revenue": holdout_rev,
            "new_customers": holdout_new,
            "repeat_customers": holdout_repeat,
        })
    return rows


def build_network_history(history_def):
    rows = []
    for h in history_def:
        claimed = h["claimed_lift"]
        verified = h["verified_lift"]
        deviation = round2(
            safe_divide(abs(claimed - verified), claimed, default=0)
        )
        reliability_score = round2(max(0, min(100, 100 * (1 - deviation))))
        rows.append({
            "network_name": h["network_name"],
            "campaign_id": h["campaign_id"],
            "claimed_lift": claimed,
            "verified_lift": verified,
            "deviation": deviation,
            "reliability_score": reliability_score,
        })
    return rows


# ---------------------------------------------------------------------------
# CSV writers
# ---------------------------------------------------------------------------

def write_csv(filepath, rows, fieldnames):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [OK] Written: {filepath}  ({len(rows)} rows)")


def generate_all(output_dir="data"):
    print("\nVeriLift — Synthetic Data Generator (Phase 1)")
    print("=" * 50)

    # campaigns.csv
    campaign_rows = build_campaigns(CAMPAIGNS_DEF)
    write_csv(
        os.path.join(output_dir, "campaigns.csv"),
        campaign_rows,
        fieldnames=[
            "campaign_id", "campaign_name", "network_name",
            "campaign_invoice", "claimed_lift", "claimed_revenue",
            "base_payment_pct", "performance_pool_pct",
            "start_date", "end_date",
        ],
    )

    # test_control.csv
    tc_rows = build_test_control(CAMPAIGNS_DEF)
    write_csv(
        os.path.join(output_dir, "test_control.csv"),
        tc_rows,
        fieldnames=[
            "campaign_id", "group_type", "users",
            "conversions", "revenue", "new_customers", "repeat_customers",
        ],
    )

    # network_history.csv
    history_rows = build_network_history(HISTORY_DEF)
    write_csv(
        os.path.join(output_dir, "network_history.csv"),
        history_rows,
        fieldnames=[
            "network_name", "campaign_id", "claimed_lift",
            "verified_lift", "deviation", "reliability_score",
        ],
    )

    print("\nSummary")
    print("-" * 50)
    print(f"  Campaigns : {len(campaign_rows)} (4 per network × 3 networks)")
    print(f"  Test/ctrl : {len(tc_rows)} rows (2 per campaign)")
    print(f"  History   : {len(history_rows)} historical campaigns")

    print("\nQuick verification")
    print("-" * 50)
    _spot_check()


def _spot_check():
    """Print a quick sanity check on the key demo campaign (CMP_A001)."""
    d = CAMPAIGNS_DEF[0]  # Summer Beauty Sale — RetailNet A
    exposed_cr = d["holdout_cr"] * (1 + d["verified_lift"])
    verified = safe_divide(exposed_cr - d["holdout_cr"], d["holdout_cr"])
    ratio = safe_divide(verified, d["claimed_lift"])

    print(f"  Demo campaign : {d['campaign_name']} ({d['network_name']})")
    print(f"  Holdout CR    : {d['holdout_cr']*100:.1f}%")
    print(f"  Exposed CR    : {exposed_cr*100:.1f}%")
    print(f"  Verified lift : {verified*100:.1f}%  (target {d['verified_lift']*100:.1f}%)")
    print(f"  Claimed lift  : {d['claimed_lift']*100:.1f}%")
    print(f"  Verif ratio   : {ratio:.2f}  -> {ratio*100:.0f}% of pool released")
    print()
    print("  RetailNet story check:")
    for cdef in CAMPAIGNS_DEF:
        ecr = cdef["holdout_cr"] * (1 + cdef["verified_lift"])
        v = safe_divide(ecr - cdef["holdout_cr"], cdef["holdout_cr"])
        c = cdef["claimed_lift"]
        overclaim = safe_divide(c, v)
        print(f"  {cdef['campaign_id']}  claimed={c*100:.1f}%  verified={v*100:.1f}%  "
              f"overclaim_factor={overclaim:.2f}x")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    generate_all(output_dir="data")
