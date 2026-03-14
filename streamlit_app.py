import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Ensure utils is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.sample_data import get_all_deals, get_top_deals, get_stats

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deal Hunter Pro X",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark premium theme ────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
        background-color: #0a0a0f;
        color: #e2e8f0;
    }
    .stApp { background-color: #0a0a0f; }
    section[data-testid="stSidebar"] {
        background-color: #0d0d14 !important;
        border-right: 1px solid #1e1e2e;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1, h2, h3, h4 { color: #e2e8f0 !important; }
    div[data-testid="metric-container"] {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 12px;
        padding: 16px;
    }
    .deal-card {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
        transition: box-shadow 0.2s;
    }
    .deal-card:hover {
        box-shadow: 0 0 18px 2px #f59e0b44;
        border-color: #f59e0b66;
    }
    .platform-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-marketplace { background: #1d4ed8; color: #fff; }
    .badge-gumtree     { background: #15803d; color: #fff; }
    .badge-olx         { background: #7c3aed; color: #fff; }
    .badge-webuycars   { background: #b45309; color: #fff; }
    .safety-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
    }
    .badge-low      { background:#14532d; color:#4ade80; border:1px solid #16a34a; }
    .badge-caution  { background:#713f12; color:#fbbf24; border:1px solid #d97706; }
    .badge-elevated { background:#7c2d12; color:#fb923c; border:1px solid #ea580c; }
    .badge-high     { background:#450a0a; color:#f87171; border:1px solid #dc2626; }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        line-height: 1.1;
    }
    .hero-tagline {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 400;
        text-align: center;
        margin-top: 0.4rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .section-divider { border:none; border-top:1px solid #1e1e2e; margin:1.5rem 0; }
    .subscription-banner {
        background: linear-gradient(135deg, #12121a 0%, #1a1206 100%);
        border: 1px solid #f59e0b66;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: #f59e0b !important;
        color: #0a0a0f !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        background: #fbbf24 !important;
        color: #0a0a0f !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center;padding:2rem 0 1rem;">
        <div class="hero-title">DEAL HUNTER PRO X</div>
        <div class="hero-tagline">Find it. Verify it. Secure it.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Live Stats Bar ────────────────────────────────────────────────────────────
stats = get_stats()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Deals Today", stats["total_deals"], delta="+12 vs yesterday")
with col2:
    st.metric("Active Scouts", "4", delta="All Online")
with col3:
    st.metric("Deals Flagged", stats["high_risk_count"])
with col4:
    st.metric("Subscribers Online", "41", delta="+3 today")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Top 5 Hot Deals ───────────────────────────────────────────────────────────
st.markdown("### Top 5 Hot Deals Today")

top_deals = get_top_deals(5)

safety_colors = {
    "low":      ("badge-low",      "LOW RISK"),
    "caution":  ("badge-caution",  "CAUTION"),
    "elevated": ("badge-elevated", "ELEVATED RISK"),
    "high":     ("badge-high",     "HIGH RISK"),
}
platform_badge_cls = {
    "Marketplace": "badge-marketplace",
    "Gumtree":     "badge-gumtree",
    "OLX":         "badge-olx",
    "WeBuyCars":   "badge-webuycars",
}

cols = st.columns(5)
for i, deal in enumerate(top_deals):
    badge_cls, badge_label = safety_colors.get(deal["risk_level"], ("badge-low", "LOW RISK"))
    plat_cls = platform_badge_cls.get(deal["platform"], "badge-marketplace")
    saving = deal["original_price"] - deal["price"]
    saving_pct = int((saving / deal["original_price"]) * 100)

    with cols[i]:
        st.markdown(
            f"""
            <div class="deal-card">
                <div style="margin-bottom:8px;">
                    <span class="platform-badge {plat_cls}">{deal['platform']}</span>
                    <span class="safety-badge {badge_cls}">{badge_label}</span>
                </div>
                <div style="font-weight:600;font-size:0.9rem;color:#e2e8f0;margin-bottom:6px;line-height:1.3;">
                    {deal['title'][:50]}{'...' if len(deal['title'])>50 else ''}
                </div>
                <div style="font-size:1.4rem;font-weight:800;color:#f59e0b;">R{deal['price']:,.0f}</div>
                <div style="font-size:0.78rem;color:#64748b;text-decoration:line-through;">R{deal['original_price']:,.0f}</div>
                <div style="font-size:0.82rem;color:#4ade80;margin-top:4px;">Save R{saving:,.0f} ({saving_pct}%)</div>
                <div style="font-size:0.78rem;color:#94a3b8;margin-top:6px;">{deal['location']} &middot; {deal['posted_ago']}</div>
                <div style="margin-top:8px;">
                    <span style="background:#1e1e2e;color:#f59e0b;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:600;">
                        Value Score: {deal['value_score']}/100
                    </span>
                </div>
                <div style="font-size:0.72rem;color:#475569;margin-top:6px;">via {deal['scout_source']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Site Performance Chart + Trending Categories ──────────────────────────────
st.markdown("### Platform Performance Today")
col_chart, col_categories = st.columns([3, 2])

with col_chart:
    platform_data = stats["platforms"]
    df_platforms = pd.DataFrame({
        "Platform": list(platform_data.keys()),
        "Deals Found": list(platform_data.values()),
    })
    fig = px.bar(
        df_platforms,
        x="Platform",
        y="Deals Found",
        color="Deals Found",
        color_continuous_scale=["#1e1e2e", "#f59e0b"],
        title="Deals Scouted per Platform",
    )
    fig.update_layout(
        plot_bgcolor="#12121a",
        paper_bgcolor="#12121a",
        font_color="#e2e8f0",
        title_font_color="#f59e0b",
        xaxis=dict(gridcolor="#1e1e2e"),
        yaxis=dict(gridcolor="#1e1e2e"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with col_categories:
    all_deals = get_all_deals()
    category_counts = {}
    for d in all_deals:
        category_counts[d["category"]] = category_counts.get(d["category"], 0) + 1

    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    st.markdown("**Trending Categories**")
    for cat, count in sorted_cats:
        pct = int((count / len(all_deals)) * 100)
        st.markdown(
            f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:3px;">
                    <span style="color:#e2e8f0;">{cat}</span>
                    <span style="color:#f59e0b;font-weight:600;">{count} deals</span>
                </div>
                <div style="background:#1e1e2e;border-radius:4px;height:6px;">
                    <div style="background:linear-gradient(90deg,#f59e0b,#f97316);width:{pct}%;height:6px;border-radius:4px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Subscription Banner ───────────────────────────────────────────────────────
st.markdown(
    """
    <div class="subscription-banner">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
            <div>
                <div style="font-size:0.75rem;color:#f59e0b;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">
                    ELITE MEMBERSHIP
                </div>
                <div style="font-size:1.4rem;font-weight:800;color:#e2e8f0;">
                    47 of 50 Elite Slots Filled
                </div>
                <div style="font-size:0.88rem;color:#94a3b8;margin-top:4px;">
                    Only <strong style="color:#f59e0b;">3 slots remaining</strong> at this tier.
                    Elite members receive real-time deal alerts, priority scout access,
                    and a 15% ad rebate on verified deals secured through the platform.
                </div>
            </div>
            <div>
                <div style="background:#1e1e2e;border-radius:10px;padding:12px 20px;border:1px solid #f59e0b33;text-align:center;">
                    <div style="font-size:0.75rem;color:#94a3b8;">Monthly</div>
                    <div style="font-size:2rem;font-weight:800;color:#f59e0b;">R299</div>
                    <div style="font-size:0.75rem;color:#64748b;">/ member</div>
                </div>
            </div>
        </div>
        <div style="margin-top:14px;background:#1e1e2e;border-radius:6px;height:8px;">
            <div style="background:linear-gradient(90deg,#f59e0b,#f97316);width:94%;height:8px;border-radius:6px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#64748b;margin-top:4px;">
            <span>0 slots</span><span>94% full</span><span>50 slots max</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Quick Access ──────────────────────────────────────────────────────────────
st.markdown("### Quick Access")
qcol1, qcol2, qcol3, qcol4, qcol5 = st.columns(5)
with qcol1:
    st.page_link("pages/1_Live_Deals.py", label="Live Deals Feed", icon=None)
with qcol2:
    st.page_link("pages/2_Scout_Radar.py", label="Scout Radar", icon=None)
with qcol3:
    st.page_link("pages/3_Safety_Checker.py", label="Safety Checker", icon=None)
with qcol4:
    st.page_link("pages/4_Telegram_Hub.py", label="Telegram Hub", icon=None)
with qcol5:
    st.page_link("pages/5_Strategy_Map.py", label="Strategy Map", icon=None)

st.markdown(
    """
    <div style="text-align:center;margin-top:2rem;font-size:0.75rem;color:#334155;">
        Deal Hunter Pro X &mdash; Premium Deal Intelligence Platform &mdash; South Africa
    </div>
    """,
    unsafe_allow_html=True,
)
