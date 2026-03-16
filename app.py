import streamlit as st
import time
from market_research_agent import MarketResearchAgent
from financial_agent import FinancialAgent
from strategy_agent import StrategyAgent
from visualizations import (
    create_roi_chart,
    create_strategy_radar,
    create_revenue_waterfall,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategic Intelligence Platform",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    [data-testid="stAppViewContainer"] { background: #0f0f1a; }
    [data-testid="stSidebar"] { background: #13131f; border-right: 1px solid #2a2a3d; }
    h1, h2, h3 { color: #e8d5a3 !important; }

    /* Agent cards */
    .agent-card {
        background: #1a1a2e;
        border: 1px solid #2a2a3d;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .agent-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #2a2a3d;
    }
    .agent-title { font-size: 14px; font-weight: 600; color: #e8d5a3; }
    .agent-role  { font-size: 11px; color: #7a7a9a; }
    .agent-output { font-size: 13px; color: #c8c8e0; line-height: 1.7; }

    /* Status badges */
    .badge-idle    { background:#2a2a3d; color:#7a7a9a; padding:3px 10px; border-radius:20px; font-size:11px; }
    .badge-running { background:#3d3200; color:#ef9f27; padding:3px 10px; border-radius:20px; font-size:11px; }
    .badge-done    { background:#1a3020; color:#639922; padding:3px 10px; border-radius:20px; font-size:11px; }

    /* Metric cards */
    .metric-box {
        background: #1a1a2e;
        border: 1px solid #2a2a3d;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-label { font-size: 11px; color: #7a7a9a; text-transform: uppercase; letter-spacing: 0.07em; }
    .metric-value { font-size: 28px; font-weight: 700; color: #e8d5a3; margin-top: 4px; }

    /* Final recommendation */
    .final-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0d1520 100%);
        border: 1px solid #3a3a5a;
        border-radius: 14px;
        padding: 1.5rem;
    }
    .final-card p { color: #c8c8e0; line-height: 1.8; font-size: 14px; }

    /* Workflow stepper */
    .stepper { display: flex; align-items: center; gap: 0; margin: 1rem 0; }
    .step { display: flex; align-items: center; gap: 8px; }
    .step-num {
        width: 26px; height: 26px; border-radius: 50%;
        background: #2a2a3d; color: #7a7a9a;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 600;
    }
    .step-num.active  { background: #ef9f27; color: #fff; }
    .step-num.done    { background: #639922; color: #fff; }
    .step-label { font-size: 12px; color: #7a7a9a; }
    .step-arrow { color: #3a3a5a; margin: 0 8px; font-size: 18px; }

    /* Divider */
    hr { border-color: #2a2a3d !important; }

    /* Streamlit overrides */
    .stButton > button {
        background: #e8d5a3 !important;
        color: #0f0f1a !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
        width: 100%;
    }
    .stButton > button:hover { background: #f5e6b8 !important; }
    .stTextArea textarea { background: #1a1a2e !important; color: #e8e8f0 !important; border: 1px solid #2a2a3d !important; }
    .stSelectbox > div > div { background: #1a1a2e !important; color: #e8e8f0 !important; border: 1px solid #2a2a3d !important; }
    .stSpinner > div { color: #e8d5a3 !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✦ Strategic Intelligence")
    st.markdown("<p style='color:#7a7a9a;font-size:13px;'>Multi-agent AI consulting system</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### Input Panel")

    industry = st.selectbox(
        "Industry",
        [
            "Travel & Hospitality",
            "Financial Services",
            "Technology / SaaS",
            "E-commerce & Retail",
            "Healthcare",
            "Manufacturing",
            "Education",
        ],
    )

    problem = st.text_area(
        "Business problem",
        value="How can a travel startup increase revenue by 20% in the next 12 months?",
        height=130,
        placeholder="Describe your business challenge...",
    )

    budget_range = st.select_slider(
        "Budget range (USD)",
        options=["< $50K", "$50K–$200K", "$200K–$1M", "$1M–$5M", "> $5M"],
        value="$50K–$200K",
    )

    timeline = st.selectbox(
        "Implementation timeline",
        ["3 months", "6 months", "12 months", "18–24 months"],
        index=2,
    )

    st.markdown("---")
    run_btn = st.button("▶  Run Full Analysis", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <p style='color:#7a7a9a;font-size:11px;'>
    <b style='color:#e8d5a3'>Agent 1</b> → Market Research<br>
    <b style='color:#e8d5a3'>Agent 2</b> → Financial Analysis<br>
    <b style='color:#e8d5a3'>Agent 3</b> → Strategy Synthesis
    </p>
    """, unsafe_allow_html=True)


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown("<h1 style='margin-bottom:0'>Strategic Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#7a7a9a;margin-top:4px'>AI-powered consulting · Multi-agent analysis · Data-driven strategy</p>", unsafe_allow_html=True)
st.markdown("---")

# Workflow stepper (static display)
st.markdown("""
<div class="stepper">
  <div class="step">
    <div class="step-num" id="s1">1</div>
    <span class="step-label">Market Research</span>
  </div>
  <span class="step-arrow">›</span>
  <div class="step">
    <div class="step-num" id="s2">2</div>
    <span class="step-label">Financial Analysis</span>
  </div>
  <span class="step-arrow">›</span>
  <div class="step">
    <div class="step-num" id="s3">3</div>
    <span class="step-label">Strategy Synthesis</span>
  </div>
  <span class="step-arrow">›</span>
  <div class="step">
    <div class="step-num" id="s4">4</div>
    <span class="step-label">Final Report</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Agent output columns ──────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📊 Market Research Analyst")
    market_placeholder = st.empty()
    market_placeholder.markdown(
        "<div class='agent-card'><span class='badge-idle'>Idle</span><br><br>"
        "<p style='color:#7a7a9a;font-size:13px'>Awaiting analysis run...</p></div>",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown("#### 💹 Financial Analyst")
    finance_placeholder = st.empty()
    finance_placeholder.markdown(
        "<div class='agent-card'><span class='badge-idle'>Idle</span><br><br>"
        "<p style='color:#7a7a9a;font-size:13px'>Awaiting market insights...</p></div>",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown("#### 🎯 Strategy Consultant")
    strategy_placeholder = st.empty()
    strategy_placeholder.markdown(
        "<div class='agent-card'><span class='badge-idle'>Idle</span><br><br>"
        "<p style='color:#7a7a9a;font-size:13px'>Awaiting financial data...</p></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Charts row ────────────────────────────────────────────────────────────────
st.markdown("#### 📈 Financial Dashboard")
chart_col1, chart_col2, chart_col3 = st.columns(3)
roi_chart_ph    = chart_col1.empty()
radar_chart_ph  = chart_col2.empty()
waterfall_ph    = chart_col3.empty()

st.markdown("---")

# ── Final recommendation ──────────────────────────────────────────────────────
st.markdown("#### ✦ Final Strategic Recommendation")
metrics_ph      = st.empty()
final_rec_ph    = st.empty()
final_rec_ph.markdown(
    "<div class='final-card'><p style='color:#7a7a9a'>Run an analysis to generate your executive consulting report.</p></div>",
    unsafe_allow_html=True,
)


# ── Run Analysis ──────────────────────────────────────────────────────────────
if run_btn:
    if not problem.strip():
        st.warning("Please enter a business problem.")
        st.stop()

    context = {
        "industry": industry,
        "problem": problem,
        "budget": budget_range,
        "timeline": timeline,
    }

    # ---------- AGENT 1: Market Research ----------
    market_placeholder.markdown(
        "<div class='agent-card'><span class='badge-running'>⟳ Running</span><br><br>"
        "<p style='color:#ef9f27;font-size:13px'>Analyzing industry trends...</p></div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Agent 1: Market Research in progress..."):
        agent1 = MarketResearchAgent()
        market_result = agent1.analyze(context)

    market_placeholder.markdown(
        f"<div class='agent-card'>"
        f"<span class='badge-done'>✓ Complete</span><br><br>"
        f"<div class='agent-output'>{market_result['html']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ---------- AGENT 2: Financial Analysis ----------
    finance_placeholder.markdown(
        "<div class='agent-card'><span class='badge-running'>⟳ Running</span><br><br>"
        "<p style='color:#ef9f27;font-size:13px'>Modeling ROI projections...</p></div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Agent 2: Financial Analysis in progress..."):
        agent2 = FinancialAgent()
        finance_result = agent2.analyze(context, market_result["raw"])

    finance_placeholder.markdown(
        f"<div class='agent-card'>"
        f"<span class='badge-done'>✓ Complete</span><br><br>"
        f"<div class='agent-output'>{finance_result['html']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Charts
    if finance_result.get("strategies"):
        strategies = finance_result["strategies"]
        roi_chart_ph.plotly_chart(
            create_roi_chart(strategies), use_container_width=True, config={"displayModeBar": False}
        )
        radar_chart_ph.plotly_chart(
            create_strategy_radar(strategies), use_container_width=True, config={"displayModeBar": False}
        )
        waterfall_ph.plotly_chart(
            create_revenue_waterfall(strategies), use_container_width=True, config={"displayModeBar": False}
        )

    # ---------- AGENT 3: Strategy Synthesis ----------
    strategy_placeholder.markdown(
        "<div class='agent-card'><span class='badge-running'>⟳ Running</span><br><br>"
        "<p style='color:#ef9f27;font-size:13px'>Synthesizing recommendations...</p></div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Agent 3: Strategy Synthesis in progress..."):
        agent3 = StrategyAgent()
        strategy_result = agent3.analyze(context, market_result["raw"], finance_result["raw"])

    strategy_placeholder.markdown(
        f"<div class='agent-card'>"
        f"<span class='badge-done'>✓ Complete</span><br><br>"
        f"<div class='agent-output'>{strategy_result['summary_html']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ---------- METRICS ROW ----------
    metrics = strategy_result.get("metrics", {})
    m1, m2, m3, m4 = st.columns(4)
    for col, label, value in [
        (m1, "Revenue Gain",     metrics.get("revenue_gain", "–")),
        (m2, "Impl. Cost",       metrics.get("impl_cost",    "–")),
        (m3, "ROI",              metrics.get("roi",          "–")),
        (m4, "Payback Period",   metrics.get("payback",      "–")),
    ]:
        col.markdown(
            f"<div class='metric-box'>"
            f"<div class='metric-label'>{label}</div>"
            f"<div class='metric-value'>{value}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ---------- FINAL RECOMMENDATION ----------
    final_rec_ph.markdown(
        f"<div class='final-card'>{strategy_result['full_html']}</div>",
        unsafe_allow_html=True,
    )

    st.success("✦ Analysis complete — full consulting report generated.")
