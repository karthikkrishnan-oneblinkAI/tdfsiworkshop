import streamlit as st
import subprocess
import json
import ast
import time

st.set_page_config(
    page_title="Banking Intelligence Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# LIGHT THEME — clean, professional, projector-friendly
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ── GLOBAL BASE FONT SIZE ── */
    html { font-size: 18px !important; }
    body, .stApp, .main, .block-container,
    p, span, li, td, th, label, div,
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .stMarkdown div, .stMarkdown td, .stMarkdown th {
        font-size: 16px !important;
    }

    /* ── FORCE LIGHT BACKGROUND ── */
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stBottomBlockContainer"],
    .main, .block-container,
    header, footer {
        background-color: #f8f9fb !important;
        color: #1a1a2e !important;
    }
    .stApp > header { background: transparent !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* ── FORM LABELS ── */
    label, p, span,
    .stTextInput label, .stTextArea label,
    .stTextInput label p, .stTextArea label p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    .stFormSubmitButton label {
        color: #3a3a4a !important;
    }
    .stTextInput > label, .stTextArea > label,
    .stTextInput > label p, .stTextArea > label p {
        color: #d35400 !important;
        font-weight: 700 !important;
        font-size: 17px !important;
    }

    /* ── TEXT INPUTS & TEXTAREAS ── */
    input, textarea,
    .stTextInput input, .stTextArea textarea,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        color: #1a1a2e !important;
        background-color: #ffffff !important;
        border: 1.5px solid #d0d5dd !important;
        border-radius: 8px !important;
        font-size: 17px !important;
        caret-color: #e67e22 !important;
    }
    input::placeholder, textarea::placeholder {
        color: #9ca3af !important;
    }
    input:focus, textarea:focus {
        border-color: #e67e22 !important;
        box-shadow: 0 0 0 3px rgba(230,126,34,0.15) !important;
    }
    .stTextInput button svg { color: #9ca3af !important; fill: #9ca3af !important; }

    /* ── MARKDOWN TEXT ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stMarkdown span, .stMarkdown div,
    .stMarkdown td, .stMarkdown th { color: #3a3a4a !important; }
    .stMarkdown strong, .stMarkdown b { color: #1a1a2e !important; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #1a1a2e !important; }
    .stMarkdown code { color: #c0392b !important; background: #f0f2f5 !important; padding: 2px 6px; border-radius: 4px; }
    .stMarkdown a { color: #2563eb !important; }
    .stCaption, small { color: #6b7280 !important; }
    .stMarkdown hr { border-color: #e5e7eb !important; }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] { border-color: #e5e7eb !important; background: #ffffff !important; border-radius: 8px !important; }
    [data-testid="stExpander"] summary { background: #ffffff !important; color: #1a1a2e !important; }
    [data-testid="stExpander"] summary span { color: #1a1a2e !important; }
    [data-testid="stExpander"] summary svg { color: #9ca3af !important; fill: #9ca3af !important; }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: #ffffff !important; }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] span { color: #3a3a4a !important; font-size: 16px !important; }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] td,
    section[data-testid="stSidebar"] th { color: #3a3a4a !important; font-size: 15px !important; }
    section[data-testid="stSidebar"] strong { color: #1a1a2e !important; font-size: 15px !important; }
    section[data-testid="stSidebar"] h1 { color: #1a1a2e !important; font-size: 24px !important; }
    section[data-testid="stSidebar"] h2 { color: #1a1a2e !important; font-size: 22px !important; }
    section[data-testid="stSidebar"] h3 { color: #1a1a2e !important; font-size: 20px !important; }
    section[data-testid="stSidebar"] hr { border-color: #e5e7eb !important; }
    section[data-testid="stSidebar"] .stCaption { color: #6b7280 !important; font-size: 14px !important; }
    /* Sidebar expanders */
    section[data-testid="stSidebar"] [data-testid="stExpander"] { background: #f8f9fb !important; border-color: #e5e7eb !important; }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary { background: #f8f9fb !important; }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary span { color: #6b7280 !important; font-size: 15px !important; }
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] span { font-size: 15px !important; }

    /* ══ SIDEBAR BUTTONS — Teradata orange ══ */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #e67e22 0%, #f39c12 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 16px !important;
        width: 100% !important;
        box-shadow: 0 2px 8px rgba(230,126,34,0.3) !important;
        margin-bottom: 6px !important;
        letter-spacing: 0.3px !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #f39c12 0%, #f5b041 100%) !important;
        box-shadow: 0 4px 14px rgba(230,126,34,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── MAIN BUTTONS ── */
    button[data-testid="stBaseButton-primary"],
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #0052CC 0%, #2684FF 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 0 2px 8px rgba(0,82,204,0.25) !important;
        cursor: pointer !important;
    }
    button[data-testid="stBaseButton-primary"]:hover,
    .stFormSubmitButton button:hover {
        box-shadow: 0 4px 14px rgba(0,82,204,0.4) !important;
    }
    /* Secondary (Logout) */
    button[data-testid="stBaseButton-secondary"] {
        color: #3a3a4a !important;
        border-color: #d0d5dd !important;
        background-color: #ffffff !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #f0f2f5 !important;
    }

    /* ── ALERTS ── */
    [data-testid="stAlert"] p { color: inherit !important; }

    /* ── SPINNER ── */
    .stSpinner, .stSpinner > div, .stSpinner > div > span {
        color: #e67e22 !important;
        font-size: 17px !important;
    }
    .stSpinner > div > i { color: #e67e22 !important; }
    .stSpinner { padding: 20px 0 !important; }

    /* ── CODE BLOCKS ── */
    [data-testid="stCode"], pre, code { background-color: #f0f2f5 !important; color: #1a1a2e !important; }

    /* ══════════════════════════════════════════════════
       CUSTOM HTML COMPONENTS
       ══════════════════════════════════════════════════ */
    .hero-banner {
        background: linear-gradient(135deg, #e67e22 0%, #2563eb 100%);
        border-radius: 14px; padding: 30px 34px; margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .hero-banner h1 { color: #fff !important; font-size: 32px; margin-bottom: 6px; }
    .hero-banner p { color: rgba(255,255,255,0.92) !important; font-size: 17px; margin: 0; }
    .logo-row { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }
    .logo-badge { background: rgba(255,255,255,0.22); padding: 5px 14px; border-radius: 6px; font-size: 14px; font-weight: 600; color: #fff !important; backdrop-filter: blur(4px); }

    .login-card {
        background: #ffffff; border: 1px solid #e5e7eb; border-radius: 14px;
        padding: 32px; margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .login-card h2 { color: #1a1a2e !important; text-align: center; margin-bottom: 6px; font-size: 26px; }
    .login-card p { color: #6b7280 !important; text-align: center; font-size: 16px; }

    .metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }
    @media (max-width: 768px) { .metric-row { grid-template-columns: repeat(2, 1fr); } }
    .metric-card {
        background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px;
        padding: 20px; text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .metric-card .mv { font-size: 32px; font-weight: 700; color: #1a1a2e; }
    .metric-card .ml { font-size: 13px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }
    .metric-card .ms { font-size: 13px; color: #d35400; margin-top: 6px; font-weight: 500; }

    .value-banner {
        background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb;
        border-radius: 10px; padding: 22px 26px; margin-bottom: 22px;
    }
    .value-banner h3 { color: #1e40af !important; font-size: 18px; margin-bottom: 10px; }
    .value-banner p { color: #374151 !important; font-size: 16px; line-height: 1.65; margin: 0; }

    .speed-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 14px 0; font-size: 15px; }
    .speed-table th { text-align: left; padding: 10px 14px; color: #6b7280; border-bottom: 2px solid #e5e7eb; font-size: 13px; text-transform: uppercase; letter-spacing: 0.8px; }
    .speed-table td { padding: 11px 14px; border-bottom: 1px solid #f0f2f5; color: #374151; }
    .speed-table .old { color: #dc2626; font-weight: 500; }
    .speed-table .new { color: #16a34a; font-weight: 600; }
    .speed-table .impact { color: #b45309; font-size: 14px; }

    .cat-card {
        background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px;
        padding: 14px 16px; margin-bottom: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .cat-card h4 { color: #1e40af !important; font-size: 17px; margin: 0 0 5px 0; }
    .cat-card .cat-time { font-size: 15px; color: #d35400 !important; margin-bottom: 5px; font-weight: 500; }
    .cat-card .cat-desc { color: #6b7280 !important; font-size: 15px; line-height: 1.5; margin: 0; }

    .timing-badge { display: inline-block; background: #dcfce7; border: 1px solid #86efac; color: #15803d !important; font-size: 14px; font-weight: 600; padding: 4px 14px; border-radius: 20px; margin-left: 8px; }
    .timing-compare { display: inline-block; background: #fef3c7; border: 1px solid #fcd34d; color: #b45309 !important; font-size: 13px; padding: 3px 12px; border-radius: 20px; margin-left: 6px; }

    .footer-row { display: flex; justify-content: center; gap: 28px; padding: 22px 0 10px 0; border-top: 1px solid #e5e7eb; margin-top: 36px; }
    .footer-item { color: #9ca3af; font-size: 14px; }

    /* ── QUERY SECTION SEPARATOR ── */
    .query-separator {
        border-top: 1px solid #e5e7eb;
        margin: 28px 0 24px 0;
        padding-top: 4px;
    }

    /* ── RESULTS SECTION ── */
    .results-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# PASSWORD — Enter key submits via st.form
# ═══════════════════════════════════════════════════
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    st.markdown("")
    st.markdown("""
    <div class="hero-banner" style="max-width:500px;margin:20px auto;">
        <h1 style="text-align:center;">💼 Banking Intelligence</h1>
        <p style="text-align:center;">Teradata + AWS AgentCore Workshop</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1.2, 2, 1.2])
    with col_m:
        st.markdown("""
        <div class="login-card">
            <h2>🔐 Welcome</h2>
            <p>Enter the workshop password to get started</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            password = st.text_input("Workshop Password:", type="password", key="password_input")
            submitted = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")

        if submitted:
            if password == "workshop2026":
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
    st.stop()

check_password()


# ═══════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════

col_main, col_logout = st.columns([6, 1])
with col_logout:
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("""
<div class="hero-banner">
    <h1>💼 Banking Intelligence Assistant</h1>
    <p>Ask questions about 10,000 customers and $765M in deposits — in natural language, in seconds.</p>
    <div class="logo-row">
        <span class="logo-badge">🟠 Teradata Vantage</span>
        <span class="logo-badge">☁️ AWS Bedrock AgentCore</span>
        <span class="logo-badge">🤖 Claude 3.5 Sonnet</span>
        <span class="logo-badge">🔧 MCP Protocol</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-row">
    <div class="metric-card"><div class="mv">30s</div><div class="ml">Avg Query Time</div><div class="ms">vs 2-3 days traditional</div></div>
    <div class="metric-card"><div class="mv">10K</div><div class="ml">Customer Records</div><div class="ms">Real-time access</div></div>
    <div class="metric-card"><div class="mv">$765M</div><div class="ml">Deposits Monitored</div><div class="ms">Churn risk scoring</div></div>
    <div class="metric-card"><div class="mv">20.4%</div><div class="ml">Current Churn Rate</div><div class="ms">5% reduction = $2-5M saved</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="value-banner">
    <h3>💡 Why This Matters</h3>
    <p>Traditional analytics takes days — weekly reports, manual SQL, Excel analysis.
    With MCP-powered agents, you get <strong style="color:#16a34a;">real-time insights in seconds</strong>.
    Imagine detecting a complaint surge Monday morning and resolving it before customers churn,
    instead of discovering it in Friday's report.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("📊 Speed Comparison: MCP vs Traditional Analytics"):
    st.markdown("""
    <table class="speed-table">
        <tr><th>Task</th><th>Traditional</th><th>With MCP Agent</th><th>Impact</th></tr>
        <tr><td>Churn analysis report</td><td class="old">2-3 days</td><td class="new">~30 seconds</td><td class="impact">Act before customers leave</td></tr>
        <tr><td>Geographic comparison</td><td class="old">4-6 hours</td><td class="new">~30 seconds</td><td class="impact">Real-time market intelligence</td></tr>
        <tr><td>High-value customer list</td><td class="old">1-2 hours</td><td class="new">~30 seconds</td><td class="impact">Instant retention targeting</td></tr>
        <tr><td>Complaint root-cause</td><td class="old">3-5 days</td><td class="new">~30 seconds</td><td class="impact">Prevent escalation</td></tr>
        <tr><td>Ad-hoc business question</td><td class="old">"Ask IT, wait days"</td><td class="new">~30 seconds</td><td class="impact">Self-serve for everyone</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("**Expected Business Impact:**")
    st.markdown("""
    <table class="speed-table">
        <tr><th>Metric</th><th>Current</th><th>MCP-Enabled</th><th>Impact</th></tr>
        <tr><td>Resolution Time</td><td class="old">5-10 days</td><td class="new">2-3 days</td><td class="impact">40% faster</td></tr>
        <tr><td>Complaint→Churn Rate</td><td class="old">15-20%</td><td class="new">8-12%</td><td class="impact">$2-5M savings</td></tr>
        <tr><td>Customer Satisfaction</td><td class="old">65%</td><td class="new">85%</td><td class="impact">+35% improvement</td></tr>
        <tr><td>Issue Detection</td><td class="old">3-5 days</td><td class="new">30 seconds</td><td class="impact">Prevent escalation</td></tr>
        <tr><td>Response Success Rate</td><td class="old">70%</td><td class="new">90%</td><td class="impact">+25% improvement</td></tr>
    </table>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 📊 Analysis Categories")
    st.caption("Click an orange button to load a sample query.")

    st.markdown('<div class="cat-card"><h4>🚨 Churn Analysis</h4><div class="cat-time">⏱ Traditional: 2-3 days → MCP: 30 seconds</div><p class="cat-desc">Identify at-risk customers before they leave. A 5% churn reduction saves $2-5M annually.</p></div>', unsafe_allow_html=True)
    if st.button("🔥 Try: Highest churn risk", key="churn_btn"):
        st.session_state.query = "Show me customers with highest churn risk and calculate the revenue impact if we lose them"
        st.rerun()
    with st.expander("More churn questions"):
        st.markdown("- Revenue impact of losing top 50 at-risk customers\n- Churn patterns by geography with interventions\n- Inactive customers who had high balances 6 months ago")

    st.markdown('<div class="cat-card"><h4>🌍 Geographic Intelligence</h4><div class="cat-time">⏱ Traditional: 4-6 hours → MCP: 30 seconds</div><p class="cat-desc">Compare France, Germany, Spain markets. Spot regional trends instantly.</p></div>', unsafe_allow_html=True)
    if st.button("🔥 Try: Compare markets", key="geo_btn"):
        st.session_state.query = "Compare customer metrics across France, Germany, and Spain. Which market has the highest average balance?"
        st.rerun()
    with st.expander("More geographic questions"):
        st.markdown("- Which market has highest average balance?\n- Geographic hotspots with highest complaint volumes\n- Regional service quality patterns")

    st.markdown('<div class="cat-card"><h4>📞 Complaint Analysis</h4><div class="cat-time">⏱ Traditional: 3-5 days → MCP: 30 seconds</div><p class="cat-desc">15-20% of complaints lead to churn. Detect surges and root causes in real time.</p></div>', unsafe_allow_html=True)
    if st.button("🔥 Try: Complaint patterns", key="complaint_btn"):
        st.session_state.query = "Analyze complaint patterns from the last 48 hours and identify any unusual spikes by product category"
        st.rerun()
    with st.expander("More complaint questions"):
        st.markdown("- Top 3 complaint categories driving highest churn risk\n- Customers with unresolved complaints + high churn probability\n- Complaint resolution success rates by response type")

    st.markdown('<div class="cat-card"><h4>💳 Credit Risk</h4><div class="cat-time">⏱ Traditional: 1-2 days → MCP: 30 seconds</div><p class="cat-desc">Portfolio risk analysis and lending optimization across your customer base.</p></div>', unsafe_allow_html=True)
    if st.button("🔥 Try: Credit risk portfolio", key="credit_btn"):
        st.session_state.query = "Analyze our credit risk portfolio. Show credit score distribution and identify customers suitable for credit limit increases."
        st.rerun()
    with st.expander("More credit risk questions"):
        st.markdown("- Customers suitable for credit limit increases\n- Portfolio risk concentration by segment\n- Expected losses by geographic market")

    st.markdown('<div class="cat-card"><h4>💎 High-Value Customers</h4><div class="cat-time">⏱ Traditional: 1-2 hours → MCP: 30 seconds</div><p class="cat-desc">Protect your most valuable relationships. Target retention and cross-sell.</p></div>', unsafe_allow_html=True)
    if st.button("🔥 Try: Inactive high-value", key="wealth_btn"):
        st.session_state.query = "Find the top 20 customers by balance who have been inactive. These are high-value retention targets."
        st.rerun()
    with st.expander("More high-value questions"):
        st.markdown("- High-income customers with low balances (acquisition targets)\n- Cross-selling opportunities for wealthy customers\n- Customers suitable for private banking upgrade")

    st.markdown("---")
    st.markdown("### 💰 Business Impact")
    st.markdown("- **Churn Prevention:** $2-5M saved\n- **Analyst Speed:** 10x faster\n- **Decisions:** Real-time vs weekly\n- **Access:** No SQL needed")


# ═══════════════════════════════════════════════════
# QUERY INTERFACE
# ═══════════════════════════════════════════════════
if 'query' in st.session_state:
    st.session_state.query_input = st.session_state.query
    del st.session_state.query

st.markdown('<div class="query-separator"></div>', unsafe_allow_html=True)

query = st.text_area(
    "Your Question:",
    key="query_input",
    placeholder="Example: Show me high-value customers at churn risk — or click an orange button in the sidebar →",
    height=100
)

col1, col2, col3 = st.columns([1.3, 2, 2])
with col1:
    submit = st.button("🔍 Get Insights", type="primary", use_container_width=True)


def extract_clean_response(raw_output):
    import re

    # Strategy 1: Find 'text' value using ast.literal_eval on the Response dict
    try:
        if "Response:" in raw_output:
            response_part = raw_output.split("Response:", 1)[1].strip()
            response_dict = ast.literal_eval(response_part)
            if 'content' in response_dict:
                content = response_dict['content']
                if isinstance(content, list) and len(content) > 0:
                    if 'text' in content[0]:
                        return content[0]['text']
    except Exception:
        pass

    # Strategy 2: Extract text between 'text': ' and the closing dict pattern
    try:
        match = re.search(r"'text':\s*'(.*?)'\s*}\s*]\s*}", raw_output, re.DOTALL)
        if match:
            return match.group(1).replace('\\n', '\n').replace("\\'", "'")
    except Exception:
        pass

    # Strategy 3: Try with double quotes
    try:
        match = re.search(r"'text':\s*\"(.*?)\"\s*}\s*]\s*}", raw_output, re.DOTALL)
        if match:
            return match.group(1).replace('\\n', '\n')
    except Exception:
        pass

    # Strategy 4: Just grab everything after "Response:" and clean it
    try:
        if "Response:" in raw_output:
            after = raw_output.split("Response:", 1)[1].strip()
            fixed = after.replace("'", '"')
            parsed = json.loads(fixed)
            if 'content' in parsed and parsed['content']:
                return parsed['content'][0].get('text', raw_output)
    except Exception:
        pass

    return raw_output


if submit and query:
    start_time = time.time()
    spinner_placeholder = st.empty()
    spinner_placeholder.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:16px 20px;background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;margin:8px 0;">
        <div style="width:20px;height:20px;border:3px solid #fed7aa;border-top:3px solid #e67e22;border-radius:50%;animation:spin 1s linear infinite;flex-shrink:0;"></div>
        <span style="color:#c2410c;font-size:17px;font-weight:500;">Querying Teradata via MCP + Claude — this may take 15-60 seconds...</span>
    </div>
    <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
    """, unsafe_allow_html=True)
    try:
        payload = json.dumps({"prompt": query})
        result = subprocess.run(
            ['/home/ubuntu/.local/bin/agentcore', 'invoke', payload],
            capture_output=True, text=True, timeout=90,
            cwd='/home/ubuntu/workshop/tdfsiworkshop'
        )
        elapsed = time.time() - start_time
        spinner_placeholder.empty()

        if result.returncode == 0:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:12px 0 6px 0;">
                <span style="color:#15803d;font-size:18px;font-weight:600;">✅ Analysis Complete</span>
                <span class="timing-badge">⚡ {elapsed:.1f}s</span>
                <span class="timing-compare">⏱ Traditional: hours to days</span>
            </div>
            """, unsafe_allow_html=True)

            clean_text = extract_clean_response(result.stdout)
            st.markdown("### 💡 Insights")
            st.markdown(clean_text)

            with st.expander("📈 Why This Matters — Business Context"):
                st.markdown(f"""
                **This query completed in {elapsed:.1f} seconds.** The same analysis traditionally requires:

                1. **Request submission** to BI team or data engineering
                2. **SQL authoring & validation** against the data warehouse
                3. **Report building** in Excel or a BI tool
                4. **Review & delivery** back to the stakeholder

                **Traditional total: hours to days.** With MCP agents, any business user
                gets answers in plain English — no SQL, no ticket queue, no waiting.
                """)

            with st.expander("🔍 Raw Response (Debug)"):
                st.code(result.stdout, language="text")
        else:
            st.error("❌ Error running query")
            st.code(result.stderr, language="text")

    except subprocess.TimeoutExpired:
        spinner_placeholder.empty()
        st.error("⏱️ Query timed out (>90s). Try a simpler question or run `agentcore status`.")
    except Exception as e:
        spinner_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")

elif submit:
    st.warning("⚠️ Please enter a question — or click an orange button in the sidebar →")

st.markdown("""
<div class="footer-row">
    <span class="footer-item">🟠 Teradata Vantage</span>
    <span class="footer-item">☁️ AWS Bedrock AgentCore</span>
    <span class="footer-item">🤖 Claude 3.5 Sonnet</span>
    <span class="footer-item">🔧 Strands Agents SDK</span>
</div>
""", unsafe_allow_html=True)