# VeriLift Formula Lock

These formulas are locked for the MVP. Do not change them without explicit user approval.

## 1. Conversion Rates

Exposed Conversion Rate:

```python
exposed_cr = exposed_conversions / exposed_users
```

Holdout Conversion Rate:

```python
holdout_cr = holdout_conversions / holdout_users
```

## 2. Lift

Absolute Lift:

```python
absolute_lift = exposed_cr - holdout_cr
```

Relative Verified Lift:

```python
verified_lift_relative = (exposed_cr - holdout_cr) / holdout_cr
```

## 3. Claimed vs Verified

Verification Ratio:

```python
verification_ratio = verified_lift_relative / claimed_lift
```

Overstatement Factor:

```python
overstatement_factor = claimed_lift / verified_lift_relative
```

## 4. Settlement

Base Payment:

```python
base_payment = campaign_invoice * base_payment_pct
```

Performance Pool:

```python
performance_pool = campaign_invoice * performance_pool_pct
```

Capped Verification Ratio:

```python
verification_ratio_capped = min(max(verification_ratio, 0), 1)
```

Released Performance Payment:

```python
released_performance_payment = performance_pool * verification_ratio_capped
```

Final Payable:

```python
final_payable = base_payment + released_performance_payment
```

Adjusted Amount:

```python
adjusted_amount = campaign_invoice - final_payable
```

## 5. Reliability Score

Deviation:

```python
deviation = abs(claimed_lift - verified_lift_relative) / claimed_lift
```

Reliability Score:

```python
reliability_score = 100 * (1 - average_deviation)
```

Cap reliability score between 0 and 100.

## 6. Risk Levels

Reliability risk:

```text
score >= 85       → Low Risk
score 60 to 84    → Medium Risk
score 30 to 59    → High Risk
score < 30        → Severe Risk
```

Settlement status:

```text
verification_ratio >= 0.90      → Full or near-full release
0.60 to 0.89                    → Partial release
0.30 to 0.59                    → High adjustment
below 0.30                      → Severe discrepancy
```

## 7. Safe Division Rules

Use a `safe_divide(a, b, default=0)` helper across all calculations.
- If holdout conversion rate is 0, return 0 or N/A safely.
- If claimed lift is 0, verification ratio should be N/A or 0 safely.
- If verified lift is 0, overstatement factor should be Infinity or N/A safely.
- The app must never crash due to division by zero.
