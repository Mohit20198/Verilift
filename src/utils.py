"""
VeriLift — Shared Utility Functions
Phase 5: Centralised helpers used across all modules.

Functions:
  safe_divide(a, b, default=0.0)       -> Safe division, returns default if b==0
  format_currency_inr(value)           -> "INR 12,50,000" formatted string
  format_percent(value)                -> "12.5%" formatted string
  risk_badge(score_or_status)          -> Short label with risk tier
  load_csv_data(data_dir)              -> Returns (campaigns, test_control, history) DataFrames

No circular imports: this module imports only os and pandas.
"""

import os
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Safe division
# ---------------------------------------------------------------------------

def safe_divide(a, b, default=0.0):
    """
    Return a / b.
    If b is 0, None, or causes any error, return default.

    Rules (per FORMULAS_LOCK.md):
      - holdout_cr == 0      -> return default (0.0)
      - claimed_lift == 0    -> return default (0.0)
      - verified_lift == 0   -> caller should handle inf separately
    """
    try:
        if b is None or b == 0:
            return default
        return a / b
    except (TypeError, ZeroDivisionError, ValueError):
        return default


# ---------------------------------------------------------------------------
# 2. Currency formatter (INR, Indian lakh/comma style)
# ---------------------------------------------------------------------------

def format_currency_inr(value) -> str:
    """
    Format a numeric value as an Indian Rupee string.
    Example: 1250000 -> "INR 12,50,000"
    Falls back to "INR N/A" if value is None or not numeric.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "INR N/A"

    # Build Indian-style comma formatting manually
    # (Python's locale approach is environment-dependent)
    is_negative = value < 0
    value = abs(value)
    integer_part = int(value)
    decimal_part = value - integer_part

    s = str(integer_part)
    if len(s) > 3:
        # Last 3 digits, then groups of 2
        result = s[-3:]
        s = s[:-3]
        while s:
            result = s[-2:] + "," + result
            s = s[:-2]
    else:
        result = s

    formatted = f"INR {'-' if is_negative else ''}{result}"
    if decimal_part > 0:
        formatted += f".{int(round(decimal_part * 100)):02d}"
    return formatted


# ---------------------------------------------------------------------------
# 3. Percent formatter
# ---------------------------------------------------------------------------

def format_percent(value, decimals: int = 1) -> str:
    """
    Format a decimal value as a percentage string.
    Example: 0.205 -> "20.5%"
    Falls back to "N/A" if value is None or not numeric.
    """
    try:
        return f"{float(value) * 100:.{decimals}f}%"
    except (TypeError, ValueError):
        return "N/A"


# ---------------------------------------------------------------------------
# 4. Risk badge
# ---------------------------------------------------------------------------

# Reliability score thresholds (from FORMULAS_LOCK.md)
_SCORE_TIERS = [
    (85, "Low Risk",    "[LOW]"),
    (60, "Medium Risk", "[MED]"),
    (30, "High Risk",   "[HIGH]"),
    (0,  "Severe Risk", "[SEVERE]"),
]

# Settlement status labels (from FORMULAS_LOCK.md)
_STATUS_LABELS = {
    "Full / Near-Full Release": "[LOW]",
    "Partial Release":          "[MED]",
    "High Adjustment":          "[HIGH]",
    "Severe Discrepancy":       "[SEVERE]",
    "Verified":                 "[LOW]",
    "Partial":                  "[MED]",
    "High Discrepancy":         "[HIGH]",
    "Negative Lift":            "[SEVERE]",
    "Uncomputable":             "[N/A]",
    "Unknown":                  "[N/A]",
}


def risk_badge(score_or_status) -> str:
    """
    Return a short risk badge string.

    Accepts:
      - A numeric reliability score (float/int):  returns "[LOW]", "[MED]", "[HIGH]", "[SEVERE]"
      - A settlement/lift status string:           maps to corresponding badge
      - A risk level string (e.g. "Low Risk"):    maps directly

    Returns the badge label as a plain ASCII string (safe for all terminals).
    """
    # Numeric score -> tier
    if isinstance(score_or_status, (int, float)):
        score = float(score_or_status)
        for threshold, _, badge in _SCORE_TIERS:
            if score >= threshold:
                return badge
        return "[SEVERE]"

    if isinstance(score_or_status, str):
        # Direct risk level strings
        risk_level_map = {
            "Low Risk":    "[LOW]",
            "Medium Risk": "[MED]",
            "High Risk":   "[HIGH]",
            "Severe Risk": "[SEVERE]",
        }
        if score_or_status in risk_level_map:
            return risk_level_map[score_or_status]

        # Status strings
        if score_or_status in _STATUS_LABELS:
            return _STATUS_LABELS[score_or_status]

    return "[N/A]"


# ---------------------------------------------------------------------------
# 5. Centralised CSV loader
# ---------------------------------------------------------------------------

def load_csv_data(data_dir: str = "data"):
    """
    Load all three VeriLift CSV files.

    Returns:
        campaigns     (pd.DataFrame) — from data/campaigns.csv
        test_control  (pd.DataFrame) — from data/test_control.csv
        history       (pd.DataFrame) — from data/network_history.csv

    Raises FileNotFoundError if any file is missing.
    """
    paths = {
        "campaigns":    os.path.join(data_dir, "campaigns.csv"),
        "test_control": os.path.join(data_dir, "test_control.csv"),
        "history":      os.path.join(data_dir, "network_history.csv"),
    }

    for name, path in paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing data file: {path}\n"
                f"Run 'python src/data_generator.py' to generate all CSV files."
            )

    campaigns = pd.read_csv(paths["campaigns"])
    test_control = pd.read_csv(paths["test_control"])
    history = pd.read_csv(paths["history"])

    # Enforce numeric types — campaigns
    for col in ["claimed_lift", "campaign_invoice",
                "base_payment_pct", "performance_pool_pct"]:
        campaigns[col] = pd.to_numeric(campaigns[col], errors="coerce")

    # Enforce numeric types — test_control
    for col in ["users", "conversions", "revenue",
                "new_customers", "repeat_customers"]:
        test_control[col] = pd.to_numeric(test_control[col], errors="coerce")

    # Enforce numeric types — history
    for col in ["claimed_lift", "verified_lift", "deviation", "reliability_score"]:
        history[col] = pd.to_numeric(history[col], errors="coerce")

    return campaigns, test_control, history


# ---------------------------------------------------------------------------
# Self-test entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("VeriLift -- Utils self-test")
    print("=" * 40)

    # safe_divide
    assert safe_divide(10, 2) == 5.0,             "safe_divide basic"
    assert safe_divide(10, 0) == 0.0,             "safe_divide by zero"
    assert safe_divide(10, None) == 0.0,          "safe_divide None"
    assert safe_divide(10, 0, default=99) == 99,  "safe_divide custom default"
    print("  [OK] safe_divide")

    # format_currency_inr
    assert format_currency_inr(500000) == "INR 5,00,000",     "INR 5L"
    assert format_currency_inr(1250000) == "INR 12,50,000",   "INR 12.5L"
    assert format_currency_inr(None) == "INR N/A",            "INR None"
    print("  [OK] format_currency_inr")

    # format_percent
    assert format_percent(0.20) == "20.0%",   "20%"
    assert format_percent(0.105) == "10.5%",  "10.5%"
    assert format_percent(None) == "N/A",     "None"
    print("  [OK] format_percent")

    # risk_badge — numeric
    assert risk_badge(93.0) == "[LOW]",    "93 -> LOW"
    assert risk_badge(70.0) == "[MED]",    "70 -> MED"
    assert risk_badge(50.0) == "[HIGH]",   "50 -> HIGH"
    assert risk_badge(20.0) == "[SEVERE]", "20 -> SEVERE"
    # risk_badge — string status
    assert risk_badge("Low Risk") == "[LOW]",               "Low Risk string"
    assert risk_badge("Severe Discrepancy") == "[SEVERE]",  "Severe Discrepancy string"
    assert risk_badge("Verified") == "[LOW]",               "Verified string"
    print("  [OK] risk_badge")

    # load_csv_data
    campaigns, test_control, history = load_csv_data(data_dir="data")
    assert len(campaigns) == 12,     f"Expected 12 campaigns, got {len(campaigns)}"
    assert len(test_control) == 24,  f"Expected 24 tc rows, got {len(test_control)}"
    assert len(history) == 9,        f"Expected 9 history rows, got {len(history)}"
    print("  [OK] load_csv_data")

    print("\nAll utility tests passed.")
    print("Phase 5 complete. Do not proceed to Phase 6 until user approval.")
