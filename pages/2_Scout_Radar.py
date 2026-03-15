import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sample_data import get_all_deals, PLATFORMS, CATEGORIES

st.set_page_config(
    page_title="Scout Radar - Deal Hunter Pro X",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
        background-color: #0a0a0f;
        color: #e2e8f0;
    }
    .stApp { background-color: #0a0a0f; }
    section[data-testid="stSidebar"] { background-color: #0d0d14 !important; }
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3, h4 { color: #e2e8f0 !important; }
    .scout-card {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
        text-align: center;
    }
    .scout-card.active { border-color: #16a34a44; box-shadow: 0 0 12px #22c55e22; }
    .scout-card.idle   { border-color: #d9770644; }
    .scout-card.scanning { border-color: #f59e0b44; box-shadow: 0 0 10px #f59e0b22; }
    .status-dot {
        display: inline-block;
        width: 10px; height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .dot-active   { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
    .dot-idle     { background: #f97316; }
    .dot-scanning { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
    .metric-pill {
        display: inline-block;
        background: #1e1e2e;
        border-radius: 8px;
        padding: 6px 12px;
        margin: 4px;
        font-size: 0.8rem;
    }
    .section-divider { border:none; border-top:1px solid #1e1e2e; margin:1.5rem 0; }
    .health-indicator {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:1.8rem;font-weight:800;color:#f59e0b;">Scout Radar</div>
        <div style="color:#64748b;font-size:0.9rem;">Bot hierarchy, scout status and site performance dashboard</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Command HQ ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#12121a,#1a1206);border:1px solid #f59e0b66;border-radius:14px;padding:20px 24px;text-align:center;margin-bottom:24px;">
        <div style="font-size:0.75rem;color:#f59e0b;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px;">
            COMMAND HQ
        </div>
        <div style="font-size:1.6rem;font-weight:800;color:#e2e8f0;margin-bottom:4px;">Deal Hunter Central Intelligence</div>
        <div style="color:#64748b;font-size:0.88rem;">Orchestrates all field scouts &mdash; 24/7 autonomous operation</div>
        <div style="margin-top:12px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;">
            <span style="background:#1e1e2e;color:#22c55e;padding:4px 14px;border-radius:20px;font-size:0.78rem;font-weight:600;border:1px solid #22c55e44;">
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e;margin-right:5px;box-shadow:0 0 6px #22c55e;"></span>
                System Online
            </span>
            <span style="background:#1e1e2e;color:#f59e0b;padding:4px 14px;border-radius:20px;font-size:0.78rem;font-weight:600;">
                Uptime: 99.7%
            </span>
            <span style="background:#1e1e2e;color:#94a3b8;padding:4px 14px;border-radius:20px;font-size:0.78rem;">
                Last Sync: 14 seconds ago
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Scout Cards ───────────────────────────────────────────────────────────────
SCOUTS = [
    {
        "name": "Scout Alpha",
        "platform": "Facebook Marketplace",
        "status": "Active",
        "last_ping": "8 seconds ago",
        "deals_today": 12,
        "latency_ms": 48,
        "class": "active",
        "dot": "dot-active",
    },
    {
        "name": "Scout Bravo",
        "platform": "Gumtree",
        "status": "Scanning",
        "last_ping": "22 seconds ago",
        "deals_today": 7,
        "latency_ms": 73,
        "class": "scanning",
        "dot": "dot-scanning",
    },
    {
        "name": "Scout Charlie",
        "platform": "OLX",
        "status": "Active",
        "last_ping": "5 seconds ago",
        "deals_today": 6,
        "latency_ms": 61,
        "class": "active",
        "dot": "dot-active",
    },
    {
        "name": "Scout Delta",
        "platform": "WeBuyCars",
        "status": "Active",
        "last_ping": "31 seconds ago",
        "deals_today": 3,
        "latency_ms": 89,
        "class": "active",
        "dot": "dot-active",
    },
]

st.markdown("### Field Scouts")
scout_cols = st.columns(4)
for i, scout in enumerate(SCOUTS):
    with scout_cols[i]:
        st.markdown(
            f"""
            <div class="scout-card {scout['class']}">
                <div style="font-size:1.1rem;font-weight:800;color:#e2e8f0;margin-bottom:4px;">{scout['name']}</div>
                <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:10px;">{scout['platform']}</div>

                <div style="margin-bottom:10px;">
                    <span class="status-dot {scout['dot']}"></span>
                    <span style="font-size:0.85rem;font-weight:600;color:{'#22c55e' if scout['status']=='Active' else '#f59e0b'};">
                        {scout['status']}
                    </span>
                </div>

                <div class="metric-pill">
                    <div style="color:#64748b;font-size:0.7rem;">Last Ping</div>
                    <div style="color:#e2e8f0;font-weight:600;">{scout['last_ping']}</div>
                </div>
                <div class="metric-pill">
                    <div style="color:#64748b;font-size:0.7rem;">Deals Today</div>
                    <div style="color:#f59e0b;font-weight:700;font-size:1.1rem;">{scout['deals_today']}</div>
                </div>
                <div class="metric-pill">
                    <div style="color:#64748b;font-size:0.7rem;">Latency</div>
                    <div style="color:#22c55e;font-weight:600;">{scout['latency_ms']}ms</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Site Performance Chart ────────────────────────────────────────────────────
st.markdown("### Site Performance")

all_deals = get_all_deals()
platform_counts = {}
for d in all_deals:
    platform_counts[d["platform"]] = platform_counts.get(d["platform"], 0) + 1

df_plat = pd.DataFrame({
    "Platform": list(platform_counts.keys()),
    "Deals Found": list(platform_counts.values()),
})

col_perf, col_latency = st.columns(2)

with col_perf:
    fig = px.bar(
        df_plat,
        x="Platform",
        y="Deals Found",
        color="Deals Found",
        color_continuous_scale=["#1e1e2e", "#f59e0b"],
        title="Deals Found per Platform Today",
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

with col_latency:
    scout_names = [s["name"] for s in SCOUTS]
    latencies = [s["latency_ms"] for s in SCOUTS]
    fig2 = go.Figure(go.Bar(
        x=scout_names,
        y=latencies,
        marker_color=["#22c55e" if l < 70 else "#f59e0b" if l < 90 else "#ef4444" for l in latencies],
        text=[f"{l}ms" for l in latencies],
        textposition="outside",
    ))
    fig2.update_layout(
        title="Scout Response Latency (ms)",
        plot_bgcolor="#12121a",
        paper_bgcolor="#12121a",
        font_color="#e2e8f0",
        title_font_color="#f59e0b",
        xaxis=dict(gridcolor="#1e1e2e"),
        yaxis=dict(gridcolor="#1e1e2e", range=[0, 120]),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Category Hot List ─────────────────────────────────────────────────────────
st.markdown("### Category Hot List — Trending Today")

cat_counts = {}
for d in all_deals:
    cat_counts[d["category"]] = cat_counts.get(d["category"], 0) + 1

sorted_cats = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)

cat_cols = st.columns(5)
for i, (cat, count) in enumerate(sorted_cats):
    with cat_cols[i % 5]:
        rank_color = "#f59e0b" if i == 0 else "#94a3b8"
        st.markdown(
            f"""
            <div style="background:#12121a;border:1px solid #1e1e2e;border-radius:10px;padding:14px;text-align:center;margin-bottom:10px;">
                <div style="font-size:0.7rem;color:{rank_color};font-weight:700;letter-spacing:0.1em;">#{i+1} TRENDING</div>
                <div style="font-size:0.95rem;font-weight:700;color:#e2e8f0;margin:4px 0;">{cat}</div>
                <div style="font-size:1.4rem;font-weight:800;color:#f59e0b;">{count}</div>
                <div style="font-size:0.72rem;color:#475569;">deals scouted</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── System Health ─────────────────────────────────────────────────────────────
st.markdown("### System Health")

health_items = [
    ("Scout Network", "All 4 scouts reporting nominal", True),
    ("Data Pipeline", "Processing at 340 events/min", True),
    ("Safety Analyzer", "Risk engine operational", True),
    ("Alert System", "Telegram gateway connected", True),
    ("Database Sync", "Last write: 4 seconds ago", True),
    ("API Rate Limits", "Within safe bounds on all platforms", True),
]

hcol1, hcol2 = st.columns(2)
for idx, (label, detail, ok) in enumerate(health_items):
    indicator = (
        '<span style="color:#22c55e;font-size:1.1rem;">&#10003;</span>'
        if ok else
        '<span style="color:#ef4444;font-size:1.1rem;">&#10007;</span>'
    )
    target = hcol1 if idx % 2 == 0 else hcol2
    with target:
        st.markdown(
            f"""
            <div class="health-indicator">
                {indicator}
                <div>
                    <div style="font-size:0.9rem;font-weight:600;color:#e2e8f0;">{label}</div>
                    <div style="font-size:0.78rem;color:#64748b;">{detail}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
