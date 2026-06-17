"""
VeriLift — Streamlit Application
Phase 7: Campaign Verification UI connected to lift_calculator.

Pages:
  1. Overview              (Phase 6 — complete)
  2. Campaign Verification (Phase 7 — connected)
  3. Settlement Engine     (Phase 8 — connected)
  4. Reliability Leaderboard (Phase 9 — connected)
  5. AI Insights           (Phase 10/11 — connected)

Stack: single app.py — sidebar navigation — no extra pages directory.
"""

import sys
import os

# Ensure src/ is on the Python path so all modules can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Data loaders — cached so Streamlit doesn't reload on every interaction
# ---------------------------------------------------------------------------
@st.cache_data
def load_lift_data():
    """Load and return the verified lift results DataFrame."""
    try:
        from lift_calculator import get_lift_results
        return get_lift_results(data_dir="data"), None
    except Exception as e:
        return None, str(e)

@st.cache_data
def load_settlement_data():
    """Load and return the settlement results DataFrame."""
    try:
        from settlement_engine import get_settlement_results
        return get_settlement_results(data_dir="data"), None
    except Exception as e:
        return None, str(e)

@st.cache_data
def load_reliability_data():
    """Load and return the reliability leaderboard DataFrame."""
    try:
        from reliability_scorer import get_reliability_scores
        return get_reliability_scores(data_dir="data"), None
    except Exception as e:
        return None, str(e)

@st.cache_data(show_spinner="Generating AI Insights...")
def load_ai_insight(campaign_id: str):
    """Load and return insights for a specific campaign."""
    try:
        # Load prerequisite data
        lift_df, err1 = load_lift_data()
        settlement_df, err2 = load_settlement_data()
        reliability_df, err3 = load_reliability_data()
        
        if err1 or err2 or err3:
            return None, "Error loading prerequisite data for insights."

        from ai_insights import get_insights
        result = get_insights(
            campaign_id=campaign_id,
            settlement_df=settlement_df,
            lift_df=lift_df,
            reliability_df=reliability_df,
            use_ai=True
        )
        return result, None
    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------------------------
# Page config — must be the first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="VeriLift — Verified Incrementality Settlement Layer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar — global navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🔬 VeriLift")
    st.caption("Pay for verified lift, not self-reported ROAS.")
    st.divider()

    page = st.radio(
        "Navigate",
        options=[
            "Overview",
            "Campaign Verification",
            "Settlement Engine",
            "Reliability Leaderboard",
            "AI Insights",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("TeXpedition 2026 · Theme 02")
    st.caption("Hackathon Prototype — Simulation Only")


# ---------------------------------------------------------------------------
# Page 1: Overview
# ---------------------------------------------------------------------------
def page_overview():
    st.title("VeriLift")
    st.subheader("Pay for verified lift, not self-reported ROAS.")
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### The Problem")
        st.error(
            "Retail media networks grade their own homework. "
            "Brands pay based on self-reported ROAS or attributed conversions, "
            "even when many of those conversions would have happened without the ad exposure."
        )

        st.markdown("### The Solution")
        st.success(
            "**VeriLift independently verifies incremental lift** using exposed vs holdout groups. "
            "We compare the verified lift with the network's claimed lift, adjust the performance-linked "
            "payout proportionally, and build a trust score for every network."
        )

    with col2:
        st.markdown("### Theme 02 Alignment")
        st.info(
            "**AI for seamless customer experiences across channels while defining clear measures of success.**\n\n"
            "VeriLift defines the ultimate success metric: **verified incremental lift**."
        )

        st.markdown("### Customer Experience (CX) Benefit")
        st.warning(
            "When brands scale campaigns based on inflated attribution, they repeatedly retarget "
            "customers who were going to buy anyway. This creates ad fatigue and irrelevant experiences. "
            "VeriLift ensures brands only scale campaigns that create *real* incremental customer value."
        )

    st.divider()

    st.markdown("### How It Works")
    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown("#### 1. Claim")
        st.caption("Network reports 20% lift and invoices the brand.")
    with step2:
        st.markdown("#### 2. Verify")
        st.caption("VeriLift exposed vs holdout comparison reveals only 10% true lift.")
    with step3:
        st.markdown("#### 3. Settle")
        st.caption("Only 50% of the performance pool is released. Reliability score is updated.")

    st.divider()

    st.markdown("### The Paradigm Shift")
    b_col, a_col = st.columns(2)
    with b_col:
        st.markdown("**Before VeriLift**")
        st.markdown(
            """
            - Pay for attributed conversions
            - Trust self-reported ROAS
            - Budget wasted on existing intent
            """
        )
    with a_col:
        st.markdown("**After VeriLift**")
        st.markdown(
            """
            - Pay for incremental conversions
            - Trust mathematically verified lift
            - Budget drives true net-new growth
            """
        )

    st.divider()
    st.markdown("*Navigate using the sidebar to explore the full demo workflow.*")


# ---------------------------------------------------------------------------
# Page 2: Campaign Verification
# ---------------------------------------------------------------------------
def page_campaign_verification():
    st.title("Campaign Verification Dashboard")
    st.caption("Compare claimed performance with independently verified lift.")
    st.divider()

    # Load data
    lift_df, err = load_lift_data()
    if err or lift_df is None:
        st.error(f"Could not load lift data: {err}")
        st.info("Run `python src/data_generator.py` and reload.")
        return

    # ── Campaign selector ──────────────────────────────────────────────────
    campaign_options = (
        lift_df["campaign_id"] + " — " +
        lift_df["campaign_name"] + " (" +
        lift_df["network_name"] + ")"
    ).tolist()

    selected_label = st.selectbox(
        "Select Campaign",
        options=campaign_options,
        index=0,
    )
    selected_idx = campaign_options.index(selected_label)
    row = lift_df.iloc[selected_idx]

    # ── Network badge ──────────────────────────────────────────────────────
    st.markdown(f"**Network:** `{row['network_name']}`")
    st.divider()

    # ── Metric cards ───────────────────────────────────────────────────────
    claimed_pct   = row["claimed_lift"] * 100 if row["claimed_lift"] is not None else 0
    verified_pct  = row["verified_lift_relative"] * 100 if row["verified_lift_relative"] is not None else 0
    verif_ratio   = row["verification_ratio"]
    overstatement = row["overstatement_factor"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Claimed Lift",
            value=f"{claimed_pct:.1f}%",
            help="Lift reported by the retail media network.",
        )
    with col2:
        delta_val = round(verified_pct - claimed_pct, 1)
        st.metric(
            label="Verified Lift",
            value=f"{verified_pct:.1f}%",
            delta=f"{delta_val:.1f}pp vs claimed",
            delta_color="normal",
            help="Independently verified incremental lift using exposed vs holdout groups.",
        )
    with col3:
        ratio_display = f"{verif_ratio:.2f}" if verif_ratio is not None else "N/A"
        st.metric(
            label="Verification Ratio",
            value=ratio_display,
            help="Verified lift / Claimed lift. 1.0 = fully verified.",
        )
    with col4:
        if overstatement is None:
            os_display = "N/A"
        elif overstatement == float("inf"):
            os_display = "inf"
        else:
            os_display = f"{overstatement:.2f}x"
        st.metric(
            label="Overstatement Factor",
            value=os_display,
            help="Claimed lift / Verified lift. Higher = more overclaiming.",
        )

    st.divider()

    # ── Lift status alert ──────────────────────────────────────────────────
    status = row["lift_status"]
    if status in ("Verified",):
        st.success(f"Lift Status: **{status}** — Claimed and verified lift are closely aligned.")
    elif status == "Partial":
        st.warning(f"Lift Status: **{status}** — Some discrepancy between claimed and verified lift.")
    elif status in ("High Discrepancy", "Severe Discrepancy"):
        st.error(f"Lift Status: **{status}** — Large gap between claimed and verified lift detected.")
    else:
        st.info(f"Lift Status: **{status}**")

    # ── Plotly bar chart — exposed vs holdout CR ───────────────────────────
    st.markdown("#### Conversion Rate Comparison")

    exposed_cr  = row["exposed_cr"] * 100
    holdout_cr  = row["holdout_cr"] * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Exposed Group",
        x=["Exposed Group", "Holdout Group"],
        y=[exposed_cr, holdout_cr],
        marker_color=["#2563EB", "#94A3B8"],
        text=[f"{exposed_cr:.2f}%", f"{holdout_cr:.2f}%"],
        textposition="outside",
        width=0.4,
    ))
    fig.update_layout(
        title=f"Exposed vs Holdout Conversion Rate — {row['campaign_name']}",
        yaxis_title="Conversion Rate (%)",
        yaxis=dict(ticksuffix="%"),
        showlegend=False,
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"The exposed group converted at **{exposed_cr:.2f}%** vs "
        f"**{holdout_cr:.2f}%** for the holdout group — "
        f"a verified relative lift of **{verified_pct:.1f}%**."
    )

    # ── Insight text ───────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### VeriLift Insight")

    if verif_ratio is not None and verif_ratio < 0.60:
        st.markdown(
            f"> **{row['network_name']}** claimed **{claimed_pct:.1f}% lift** but "
            f"VeriLift verified only **{verified_pct:.1f}% lift** — "
            f"a **{overstatement:.1f}x overstatement**. "
            f"Many attributed conversions may have come from customers who would have "
            f"purchased without the campaign. "
            f"Only **{verif_ratio*100:.0f}%** of the performance-linked pool "
            f"should be released."
        )
    elif verif_ratio is not None and verif_ratio >= 0.90:
        st.markdown(
            f"> **{row['network_name']}** claimed **{claimed_pct:.1f}% lift** and "
            f"VeriLift verified **{verified_pct:.1f}% lift** — "
            f"a strong alignment score of **{verif_ratio:.2f}**. "
            f"This network demonstrates transparent reporting."
        )
    else:
        st.markdown(
            f"> **{row['network_name']}** claimed **{claimed_pct:.1f}% lift** and "
            f"VeriLift verified **{verified_pct:.1f}% lift** — "
            f"a partial alignment with verification ratio **{ratio_display}**."
        )


# ---------------------------------------------------------------------------
# Page 3: Settlement Engine
# ---------------------------------------------------------------------------
def page_settlement_engine():
    st.title("Settlement Engine")
    st.caption("Performance-linked payout adjusted based on verified lift.")
    st.info(
        "> *VeriLift releases the performance-linked payout in proportion "
        "to verified lift, not claimed lift.*"
    )
    st.divider()

    # Load data
    settlement_df, err = load_settlement_data()
    if err or settlement_df is None:
        st.error(f"Could not load settlement data: {err}")
        st.info("Run `python src/data_generator.py` and reload.")
        return

    # ── Campaign selector ──────────────────────────────────────────────────
    campaign_options = (
        settlement_df["campaign_id"] + " — " +
        settlement_df["campaign_name"] + " (" +
        settlement_df["network_name"] + ")"
    ).tolist()

    selected_label = st.selectbox(
        "Select Campaign",
        options=campaign_options,
        index=0,
        key="settlement_campaign_select",
    )
    selected_idx = campaign_options.index(selected_label)
    row = settlement_df.iloc[selected_idx]

    st.markdown(f"**Network:** `{row['network_name']}`")
    st.divider()

    # ── Settlement status badge ──────────────────────────────────────────────
    status = row["settlement_status"]
    if "Full" in status:
        st.success(f"Settlement Status: **{status}**")
    elif "Partial" in status:
        st.warning(f"Settlement Status: **{status}**")
    elif "High" in status:
        st.error(f"Settlement Status: **{status}**")
    elif "Severe" in status:
        st.error(f"Settlement Status: **{status}** — Significant performance pool withheld.")
    else:
        st.info(f"Settlement Status: **{status}**")

    # ── Payment metric cards ─────────────────────────────────────────────────
    invoice      = row["campaign_invoice"]
    base_pay     = row["base_payment"]
    perf_pool    = row["performance_pool"]
    released     = row["released_performance_payment"]
    final_pay    = row["final_payable"]
    adjusted     = row["adjusted_amount"]
    ratio_capped = row["verification_ratio_capped"]

    def fmt_inr(v):
        """Format as INR with Indian comma style."""
        try:
            from utils import format_currency_inr
            return format_currency_inr(v)
        except Exception:
            return f"INR {v:,.0f}"

    st.markdown("#### Payment Breakdown")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Invoice",    fmt_inr(invoice),   help="Full campaign invoice amount.")
    with col2:
        st.metric("Base Payment",     fmt_inr(base_pay),  help=f"Guaranteed {row['base_payment_pct']*100:.0f}% of invoice — always released.")
    with col3:
        st.metric("Performance Pool", fmt_inr(perf_pool), help=f"At-risk {row['performance_pool_pct']*100:.0f}% — released proportional to verified lift.")

    st.markdown("")
    col4, col5, col6 = st.columns(3)
    with col4:
        pct_released = ratio_capped * 100 if ratio_capped is not None else 0
        st.metric(
            "Released from Pool",
            fmt_inr(released),
            delta=f"{pct_released:.0f}% of pool released",
            delta_color="normal",
            help="Performance pool × verification ratio (capped 0–1).",
        )
    with col5:
        st.metric("Final Payable",    fmt_inr(final_pay), help="Base payment + Released performance payment.")
    with col6:
        st.metric(
            "Adjusted Amount",
            fmt_inr(adjusted),
            delta=f"-{adjusted/invoice*100:.0f}% of invoice" if invoice else "N/A",
            delta_color="inverse",
            help="Invoice − Final payable. Amount withheld pending verified performance.",
        )

    st.divider()

    # ── Plotly bar chart: Invoice vs Final Payable vs Adjusted ───────────────
    st.markdown("#### Settlement Breakdown Chart")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Total Invoice",
        x=["Total Invoice", "Final Payable", "Adjusted Amount"],
        y=[invoice, final_pay, adjusted],
        marker_color=["#64748B", "#16A34A", "#DC2626"],
        text=[
            fmt_inr(invoice),
            fmt_inr(final_pay),
            fmt_inr(adjusted),
        ],
        textposition="outside",
        width=0.45,
    ))
    fig.update_layout(
        title=f"Payment Settlement — {row['campaign_name']}",
        yaxis_title="Amount (INR)",
        showlegend=False,
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=60, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"Out of **{fmt_inr(invoice)}** invoiced, **{fmt_inr(final_pay)}** is payable "
        f"based on verified lift. **{fmt_inr(adjusted)}** is withheld as an adjustment."
    )

    # ── Formula trace ───────────────────────────────────────────────────────
    with st.expander("Show formula trace"):
        claimed_pct  = row["claimed_lift"] * 100 if row["claimed_lift"] is not None else 0
        verified_pct = row["verified_lift_relative"] * 100 if row["verified_lift_relative"] is not None else 0
        ratio_raw    = row["verification_ratio"]
        st.markdown(
            f"""
| Step | Calculation | Result |
|---|---|---|
| Verified lift | Exposed CR − Holdout CR / Holdout CR | **{verified_pct:.1f}%** |
| Claimed lift  | Network reported | **{claimed_pct:.1f}%** |
| Verification ratio | {verified_pct:.1f}% / {claimed_pct:.1f}% | **{ratio_raw:.2f}** (capped to {ratio_capped:.2f}) |
| Base payment  | {fmt_inr(invoice)} × {row['base_payment_pct']*100:.0f}% | **{fmt_inr(base_pay)}** |
| Performance pool | {fmt_inr(invoice)} × {row['performance_pool_pct']*100:.0f}% | **{fmt_inr(perf_pool)}** |
| Released payment | {fmt_inr(perf_pool)} × {ratio_capped:.2f} | **{fmt_inr(released)}** |
| Final payable | {fmt_inr(base_pay)} + {fmt_inr(released)} | **{fmt_inr(final_pay)}** |
| Adjusted amount | {fmt_inr(invoice)} − {fmt_inr(final_pay)} | **{fmt_inr(adjusted)}** |
            """
        )


# ---------------------------------------------------------------------------
# Page 4: Reliability Leaderboard
# ---------------------------------------------------------------------------
def page_reliability_leaderboard():
    st.title("Network Reliability Leaderboard")
    st.caption("Rank retail media networks by long-term trustworthiness.")
    st.divider()

    # Load data
    rel_df, err = load_reliability_data()
    if err or rel_df is None:
        st.error(f"Could not load reliability data: {err}")
        st.info("Run `python src/data_generator.py` and reload.")
        return

    # ── Risk badge helper ──────────────────────────────────────────────────
    BADGE_COLORS = {
        "Low Risk":    "#16A34A",
        "Medium Risk": "#CA8A04",
        "High Risk":   "#EA580C",
        "Severe Risk": "#DC2626",
    }

    def risk_chip(risk_level):
        color = BADGE_COLORS.get(risk_level, "#64748B")
        return f'<span style="background:{color};color:#fff;padding:2px 10px;border-radius:12px;font-size:0.82em;font-weight:600">{risk_level}</span>'

    # ── Summary metrics row ─────────────────────────────────────────────────
    top = rel_df.iloc[0]
    bottom = rel_df.iloc[-1]
    cols = st.columns(len(rel_df))
    for i, (_, row) in enumerate(rel_df.iterrows()):
        with cols[i]:
            medal = ["#1", "#2", "#3"][i] if i < 3 else f"#{i+1}"
            st.metric(
                label=f"{medal} {row['network_name']}",
                value=f"{row['reliability_score']:.1f} / 100",
                help=f"Based on {row['n_campaigns']} campaigns.",
            )
            st.markdown(risk_chip(row["risk_level"]), unsafe_allow_html=True)

    st.divider()

    # ── Reliability score bar chart ─────────────────────────────────────────────
    st.markdown("#### Reliability Score by Network")

    bar_colors = [
        BADGE_COLORS.get(r, "#64748B")
        for r in rel_df["risk_level"]
    ]

    fig_score = go.Figure(go.Bar(
        x=rel_df["network_name"],
        y=rel_df["reliability_score"],
        marker_color=bar_colors,
        text=[f"{s:.1f}" for s in rel_df["reliability_score"]],
        textposition="outside",
        width=0.4,
    ))
    fig_score.add_hline(
        y=85, line_dash="dot", line_color="#16A34A",
        annotation_text="Low Risk threshold (85)",
        annotation_position="top right",
    )
    fig_score.add_hline(
        y=60, line_dash="dot", line_color="#CA8A04",
        annotation_text="Medium Risk threshold (60)",
        annotation_position="top right",
    )
    fig_score.update_layout(
        title="Reliability Score (0–100) — Higher is more trustworthy",
        yaxis_title="Reliability Score",
        yaxis=dict(range=[0, 115]),
        showlegend=False,
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=40, r=40),
    )
    st.plotly_chart(fig_score, use_container_width=True)
    st.caption("A network's reliability score aggregates historical deviation between their claimed lift and VeriLift's independently verified lift.")

    # ── Claimed vs Verified lift grouped bar chart ──────────────────────────
    st.markdown("#### Claimed vs Verified Lift by Network")

    fig_lift = go.Figure()
    fig_lift.add_trace(go.Bar(
        name="Claimed Lift",
        x=rel_df["network_name"],
        y=(rel_df["avg_claimed_lift"] * 100).round(1),
        marker_color="#94A3B8",
        text=[(f"{v:.1f}%") for v in rel_df["avg_claimed_lift"] * 100],
        textposition="outside",
    ))
    fig_lift.add_trace(go.Bar(
        name="Verified Lift",
        x=rel_df["network_name"],
        y=(rel_df["avg_verified_lift"] * 100).round(1),
        marker_color="#2563EB",
        text=[(f"{v:.1f}%") for v in rel_df["avg_verified_lift"] * 100],
        textposition="outside",
    ))
    fig_lift.update_layout(
        title="Average Claimed vs Verified Lift per Network",
        yaxis_title="Lift (%)",
        yaxis=dict(ticksuffix="%"),
        barmode="group",
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=40, r=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_lift, use_container_width=True)
    st.caption("Comparison of the average lift reported by the network vs the average true incremental lift verified by VeriLift across all campaigns.")

    st.divider()

    # ── Leaderboard detail table ───────────────────────────────────────────────
    st.markdown("#### Full Leaderboard")

    for _, row in rel_df.iterrows():
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([2, 1.5, 1.5, 1.5, 3])
            with c1:
                st.markdown(f"**#{row['rank']} {row['network_name']}**")
                st.markdown(risk_chip(row["risk_level"]), unsafe_allow_html=True)
            with c2:
                st.metric("Score", f"{row['reliability_score']:.1f}")
            with c3:
                st.metric("Avg Claimed", f"{row['avg_claimed_lift']*100:.1f}%")
            with c4:
                st.metric("Avg Verified", f"{row['avg_verified_lift']*100:.1f}%")
            with c5:
                st.markdown(f"**Recommended Split**")
                st.caption(row["recommended_contract_split"])
            st.divider()

    # ── Insight ─────────────────────────────────────────────────────────────
    st.markdown("#### VeriLift Insight")
    st.markdown(
        f"> **{top['network_name']}** is the most reliable network with a score of "
        f"**{top['reliability_score']:.1f}/100** and an average overstatement of only "
        f"**{top['avg_deviation']*100:.1f}%**. "
        f"**{bottom['network_name']}** shows the highest risk with a score of "
        f"**{bottom['reliability_score']:.1f}/100** and an average deviation of "
        f"**{bottom['avg_deviation']*100:.1f}%** — indicating systematic overclaiming. "
        f"Brands should adjust future contract splits accordingly."
    )


# ---------------------------------------------------------------------------
# Page 5: AI Insights
# ---------------------------------------------------------------------------
def page_ai_insights():
    st.title("AI Insights")
    st.caption("Plain-English explanations of discrepancies, settlements, and recommendations.")
    st.divider()

    # Load campaign list from settlement data
    settlement_df, err = load_settlement_data()
    if err or settlement_df is None:
        st.error(f"Could not load data: {err}")
        return

    # ── Campaign selector ──────────────────────────────────────────────────
    campaign_options = (
        settlement_df["campaign_id"] + " — " +
        settlement_df["campaign_name"] + " (" +
        settlement_df["network_name"] + ")"
    ).tolist()

    selected_label = st.selectbox(
        "Select Campaign for Analysis",
        options=campaign_options,
        index=0,
        key="ai_campaign_select",
    )
    
    # Extract campaign_id from the selected label (it's the part before ' —')
    selected_cid = selected_label.split(" — ")[0]

    # Load insight
    insight, err = load_ai_insight(selected_cid)
    if err or insight is None:
        st.error(f"Could not generate insights: {err}")
        return

    # ── Meta badges ────────────────────────────────────────────────────────
    st.markdown(f"**Network:** `{insight.network_name}`")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if insight.insight_source == "groq-ai":
            st.success("🤖 **Source:** Groq AI")
        else:
            st.info("⚙️ **Source:** Rule-based fallback")
    with col_b:
        st.markdown(f"**Confidence:** {insight.confidence_level}")
    
    st.divider()

    # ── Insights display ───────────────────────────────────────────────────
    st.markdown("### Discrepancy Explanation")
    st.info(insight.discrepancy_explanation)
    
    st.markdown("### Settlement Summary")
    st.warning(insight.settlement_summary)
    
    st.markdown("### Customer Experience Impact")
    st.error(insight.cx_impact)
    
    st.markdown("### Recommended Action")
    st.success(insight.recommended_action)
    
    st.markdown("### Contract Recommendation")
    st.markdown(f"> {insight.contract_recommendation}")
    
    st.divider()
    with st.expander("Show AI generation notes"):
        st.caption(insight.notes)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if page == "Overview":
    page_overview()
elif page == "Campaign Verification":
    page_campaign_verification()
elif page == "Settlement Engine":
    page_settlement_engine()
elif page == "Reliability Leaderboard":
    page_reliability_leaderboard()
elif page == "AI Insights":
    page_ai_insights()
