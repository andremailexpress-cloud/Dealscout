import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sample_data import get_all_deals, CATEGORIES, LOCATIONS, PLATFORMS

st.set_page_config(
    page_title="Live Deals - Deal Hunter Pro X",
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
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3, h4 { color: #e2e8f0 !important; }
    .stSelectbox > div > div { background: #12121a !important; border-color: #1e1e2e !important; color: #e2e8f0 !important; }
    .stMultiSelect > div { background: #12121a !important; border-color: #1e1e2e !important; }
    .stSlider > div { color: #e2e8f0 !important; }
    .deal-card {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }
    .deal-card:hover { box-shadow: 0 0 16px 2px #f59e0b33; border-color: #f59e0b55; }
    .platform-badge {
        display: inline-block; padding: 2px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600; margin-right: 6px;
    }
    .badge-marketplace { background:#1d4ed8; color:#fff; }
    .badge-gumtree     { background:#15803d; color:#fff; }
    .badge-olx         { background:#7c3aed; color:#fff; }
    .badge-webuycars   { background:#b45309; color:#fff; }
    .safety-badge {
        display: inline-block; padding: 3px 12px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 700;
    }
    .badge-low      { background:#14532d; color:#4ade80; border:1px solid #16a34a; }
    .badge-caution  { background:#713f12; color:#fbbf24; border:1px solid #d97706; }
    .badge-elevated { background:#7c2d12; color:#fb923c; border:1px solid #ea580c; }
    .badge-high     { background:#450a0a; color:#f87171; border:1px solid #dc2626; }
    .section-divider { border:none; border-top:1px solid #1e1e2e; margin:1rem 0; }
    .stButton > button {
        background: #1e1e2e !important; color: #e2e8f0 !important;
        border: 1px solid #2e2e3e !important; border-radius: 6px !important;
        font-size: 0.8rem !important; padding: 4px 10px !important;
    }
    .stButton > button:hover { border-color: #f59e0b55 !important; color: #f59e0b !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:1rem;">
        <div style="font-size:1.8rem;font-weight:800;color:#f59e0b;">Live Deals Feed</div>
        <div style="color:#64748b;font-size:0.9rem;">Real-time scouted deals from across South African marketplaces</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filter Deals")

    selected_categories = st.multiselect(
        "Category",
        options=CATEGORIES,
        default=[],
        placeholder="All categories",
    )

    price_min, price_max = st.slider(
        "Price Range (ZAR)",
        min_value=0,
        max_value=700000,
        value=(0, 700000),
        step=1000,
        format="R%d",
    )

    selected_location = st.selectbox(
        "Location",
        options=["All"] + LOCATIONS,
        index=0,
    )

    selected_platform = st.selectbox(
        "Platform",
        options=["All"] + PLATFORMS,
        index=0,
    )

    selected_risk = st.selectbox(
        "Safety Rating",
        options=["All", "Low Risk", "Caution", "Elevated Risk", "High Risk"],
        index=0,
    )

    st.markdown('<hr style="border-color:#1e1e2e;">', unsafe_allow_html=True)
    sort_by = st.selectbox(
        "Sort By",
        options=["Value Score (High-Low)", "Price (Low-High)", "Price (High-Low)", "Most Recent"],
        index=0,
    )

# ── Filter Logic ──────────────────────────────────────────────────────────────
risk_map = {
    "All": None,
    "Low Risk": "low",
    "Caution": "caution",
    "Elevated Risk": "elevated",
    "High Risk": "high",
}

all_deals = get_all_deals()
filtered = all_deals

if selected_categories:
    filtered = [d for d in filtered if d["category"] in selected_categories]

filtered = [d for d in filtered if price_min <= d["price"] <= price_max]

if selected_location != "All":
    filtered = [d for d in filtered if d["location"] == selected_location]

if selected_platform != "All":
    filtered = [d for d in filtered if d["platform"] == selected_platform]

risk_filter = risk_map.get(selected_risk)
if risk_filter:
    filtered = [d for d in filtered if d["risk_level"] == risk_filter]

# Sort
if sort_by == "Value Score (High-Low)":
    filtered = sorted(filtered, key=lambda x: x["value_score"], reverse=True)
elif sort_by == "Price (Low-High)":
    filtered = sorted(filtered, key=lambda x: x["price"])
elif sort_by == "Price (High-Low)":
    filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)
# Most Recent: keep original order

# ── Results Summary ───────────────────────────────────────────────────────────
st.markdown(
    f'<div style="color:#94a3b8;font-size:0.85rem;margin-bottom:1rem;">'
    f'Showing <strong style="color:#f59e0b;">{len(filtered)}</strong> deals'
    f'</div>',
    unsafe_allow_html=True,
)

if not filtered:
    st.info("No deals match your current filters. Try adjusting the filter criteria.")
    st.stop()

# ── Deal Cards ────────────────────────────────────────────────────────────────
safety_colors = {
    "low":      ("badge-low",      "LOW RISK",       "Verified / Low Risk"),
    "caution":  ("badge-caution",  "CAUTION",        "Requires Verification"),
    "elevated": ("badge-elevated", "ELEVATED RISK",  "Elevated Risk Indicators"),
    "high":     ("badge-high",     "HIGH RISK",      "Elevated Risk Indicators"),
}
platform_badge_cls = {
    "Marketplace": "badge-marketplace",
    "Gumtree":     "badge-gumtree",
    "OLX":         "badge-olx",
    "WeBuyCars":   "badge-webuycars",
}

# Two-column layout
left_col, right_col = st.columns(2)

for idx, deal in enumerate(filtered):
    badge_cls, badge_label, badge_tooltip = safety_colors.get(
        deal["risk_level"], ("badge-low", "LOW RISK", "Verified / Low Risk")
    )
    plat_cls = platform_badge_cls.get(deal["platform"], "badge-marketplace")
    saving = deal["original_price"] - deal["price"]
    saving_pct = int((saving / deal["original_price"]) * 100) if deal["original_price"] > 0 else 0

    # Value score color
    vs = deal["value_score"]
    vs_color = "#22c55e" if vs >= 80 else "#f59e0b" if vs >= 60 else "#f97316"

    # Safety score bar width (out of 100)
    ss = deal["safety_score"]
    ss_color = "#22c55e" if ss >= 80 else "#f59e0b" if ss >= 60 else "#ef4444"

    card_html = f"""
    <div class="deal-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
            <div>
                <span class="platform-badge {plat_cls}">{deal['platform']}</span>
                <span class="safety-badge {badge_cls}">{badge_label}</span>
                <span style="font-size:0.72rem;color:#475569;margin-left:6px;">{deal['category']}</span>
            </div>
            <div style="font-size:0.78rem;color:#475569;">{deal['posted_ago']}</div>
        </div>

        <div style="font-weight:700;font-size:1.05rem;color:#e2e8f0;margin-bottom:8px;line-height:1.35;">
            {deal['title']}
        </div>

        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:4px;">
            <span style="font-size:1.6rem;font-weight:800;color:#f59e0b;">R{deal['price']:,.0f}</span>
            <span style="font-size:0.85rem;color:#64748b;text-decoration:line-through;">R{deal['original_price']:,.0f}</span>
            <span style="font-size:0.85rem;color:#4ade80;font-weight:600;">-{saving_pct}%</span>
        </div>

        <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:10px;">
            {deal['location']} &nbsp;&bull;&nbsp; Seller Rating: {deal['seller_rating']}/5.0 &nbsp;&bull;&nbsp; via {deal['scout_source']}
        </div>

        <div style="font-size:0.82rem;color:#64748b;margin-bottom:12px;line-height:1.5;">
            {deal['description'][:160]}{'...' if len(deal['description'])>160 else ''}
        </div>

        <div style="display:flex;gap:16px;margin-bottom:10px;">
            <div style="flex:1;">
                <div style="font-size:0.72rem;color:#64748b;margin-bottom:3px;">Value Score</div>
                <div style="background:#1e1e2e;border-radius:4px;height:6px;">
                    <div style="background:{vs_color};width:{vs}%;height:6px;border-radius:4px;"></div>
                </div>
                <div style="font-size:0.75rem;font-weight:700;color:{vs_color};margin-top:2px;">{vs}/100</div>
            </div>
            <div style="flex:1;">
                <div style="font-size:0.72rem;color:#64748b;margin-bottom:3px;">Safety Score</div>
                <div style="background:#1e1e2e;border-radius:4px;height:6px;">
                    <div style="background:{ss_color};width:{ss}%;height:6px;border-radius:4px;"></div>
                </div>
                <div style="font-size:0.75rem;font-weight:700;color:{ss_color};margin-top:2px;">{ss}/100 &mdash; {badge_tooltip}</div>
            </div>
        </div>
    </div>
    """

    target_col = left_col if idx % 2 == 0 else right_col
    with target_col:
        st.markdown(card_html, unsafe_allow_html=True)
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            st.button("View Original", key=f"view_{deal['id']}")
        with btn_col2:
            st.button("Save Deal", key=f"save_{deal['id']}")
        with btn_col3:
            st.button("Alert Me", key=f"alert_{deal['id']}")
