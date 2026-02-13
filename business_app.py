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
# ALL STYLING IN ONE PLACE — forces dark theme via CSS
# No config.toml needed
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ── FORCE DARK BACKGROUND ON EVERYTHING ── */
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stBottomBlockContainer"],
    .main, .block-container,
    header, footer {
        background-color: #0f1419 !important;
        color: #c9d1d9 !important;
    }
    /* Kill any white flashes */
    .stApp > header { background: transparent !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* ── FORM LABELS — bright orange ── */
    label, p, span,
    .stTextInput label, .stTextArea label,
    .stTextInput label p, .stTextArea label p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    .stFormSubmitButton label {
        color: #c9d1d9 !important;
    }
    .stTextInput > label, .stTextArea > label,
    .stTextInput > label p, .stTextArea > label p {
        color: #ff8c00 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* ── TEXT INPUTS & TEXTAREAS ── */
    input, textarea,
    .stTextInput input, .stTextArea textarea,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        color: #f0f0f0 !important;
        background-color: #1b2230 !important;
        border: 2px solid #3d4f65 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        caret-color: #ff8c00 !important;
    }
    input::placeholder, textarea::placeholder {
        color: #7a8a9e !important;
    }
    input:focus, textarea:focus {
        border-color: #ff8c00 !important;
        box-shadow: 0 0 0 3px rgba(255,140,0,0.2) !important;
    }
    /* Password eye icon */
    .stTextInput button svg { color: #8b949e !important; fill: #8b949e !important; }

    /* ── MARKDOWN TEXT ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stMarkdown span, .stMarkdown div,
    .stMarkdown td, .stMarkdown th { color: #c9d1d9 !important; }
    .stMarkdown strong, .stMarkdown b { color: #f0f6fc !important; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #f0f6fc !important; }
    .stMarkdown code { color: #7ee787 !important; background: #161b22 !important; padding: 2px 6px; border-radius: 4px; }
    .stMarkdown a { color: #58a6ff !important; }
    .stCaption, small { color: #9da5ae !important; }
    .stMarkdown hr { border-color: #30363d !important; }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] { border-color: #30363d !important; background: #161b22 !important; border-radius: 8px !important; }
    [data-testid="stExpander"] summary { background: #161b22 !important; color: #e2e8f0 !important; }
    [data-testid="stExpander"] summary span { color: #e2e8f0 !important; }
    [data-testid="stExpander"] summary svg { color: #9da5ae !important; fill: #9da5ae !important; }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: #161b22 !important; }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] span { color: #c9d1d9 !important; }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #0d1117 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li { color: #c9d1d9 !important; }
    section[data-testid="stSidebar"] strong { color: #f0f6fc !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #f0f6fc !important; }
    section[data-testid="stSidebar"] hr { border-color: #30363d !important; }
    section[data-testid="stSidebar"] .stCaption { color: #9da5ae !important; }
    /* Sidebar expanders */
    section[data-testid="stSidebar"] [data-testid="stExpander"] { background: #0d1117 !important; border-color: #21262d !important; }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary { background: #0d1117 !important; }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary span { color: #9da5ae !important; font-size: 13px !important; }

    /* ══ SIDEBAR BUTTONS — bright orange gradient ══ */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 10px 16px !important;
        width: 100% !important;
        box-shadow: 0 2px 10px rgba(255,102,0,0.35) !important;
        margin-bottom: 6px !important;
        letter-spacing: 0.3px !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #ff8533 0%, #ffa94d 100%) !important;
        box-shadow: 0 4px 16px rgba(255,102,0,0.5) !important;
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
        font-size: 14px !important;
        box-shadow: 0 2px 10px rgba(0,82,204,0.35) !important;
        cursor: pointer !important;
    }
    button[data-testid="stBaseButton-primary"]:hover,
    .stFormSubmitButton button:hover {
        box-shadow: 0 4px 16px rgba(0,82,204,0.5) !important;
    }
    /* Secondary (Logout) */
    button[data-testid="stBaseButton-secondary"] {
        color: #c9d1d9 !important;
        border-color: #30363d !important;
        background-color: #21262d !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #30363d !important;
    }

    /* ── ALERTS ── */
    [data-testid="stAlert"] p { color: inherit !important; }

    /* ── SPINNER ── */
    .stSpinner, .stSpinner > div, .stSpinner > div > span { 
        color: #ffa657 !important; 
        font-size: 15px !important;
    }
    .stSpinner > div > i { color: #ff8c00 !important; }
    /* Spinner container - add breathing room */
    .stSpinner { 
        padding: 20px 0 !important;
    }

    /* ── CODE BLOCKS ── */
    [data-testid="stCode"], pre, code { background-color: #0d1117 !important; color: #c9d1d9 !important; }

    /* ══════════════════════════════════════════════════
       CUSTOM HTML COMPONENTS
       ══════════════════════════════════════════════════ */
    .hero-banner {
        background: linear-gradient(135deg, #FF6600 0%, #0052CC 100%);
        border-radius: 14px; padding: 30px 34px; margin-bottom: 24px;
    }
    .hero-banner h1 { color: #fff !important; font-size: 28px; margin-bottom: 6px; }
    .hero-banner p { color: rgba(255,255,255,0.92) !important; font-size: 15px; margin: 0; }
    .logo-row { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }
    .logo-badge { background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; color: #fff !important; }

    .login-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 14px;
        padding: 32px; margin-bottom: 20px;
    }
    .login-card h2 { color: #f0f6fc !important; text-align: center; margin-bottom: 6px; font-size: 22px; }
    .login-card p { color: #9da5ae !important; text-align: center; font-size: 14px; }

    .metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }
    @media (max-width: 768px) { .metric-row { grid-template-columns: repeat(2, 1fr); } }
    .metric-card { background: #161b22; border: 1px solid #30363d; border-top: 1px solid #21262d; border-radius: 12px; padding: 18px; text-align: center; }
    .metric-card .mv { font-size: 28px; font-weight: 700; color: #f0f6fc; }
    .metric-card .ml { font-size: 10px; color: #9da5ae; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }
    .metric-card .ms { font-size: 11px; color: #ffa657; margin-top: 6px; }

    .value-banner { background: #161b22; border: 1px solid #1f6feb; border-left: 4px solid #1f6feb; border-radius: 10px; padding: 22px 26px; margin-bottom: 22px; }
    .value-banner h3 { color: #58a6ff !important; font-size: 16px; margin-bottom: 10px; }
    .value-banner p { color: #c9d1d9 !important; font-size: 14px; line-height: 1.65; margin: 0; }

    .speed-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 14px 0; font-size: 13px; }
    .speed-table th { text-align: left; padding: 10px 14px; color: #9da5ae; border-bottom: 2px solid #30363d; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; }
    .speed-table td { padding: 11px 14px; border-bottom: 1px solid #21262d; color: #c9d1d9; }
    .speed-table .old { color: #e5534b; font-weight: 500; }
    .speed-table .new { color: #56d364; font-weight: 600; }
    .speed-table .impact { color: #e3b341; font-size: 12px; }

    .cat-card { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 14px 16px; margin-bottom: 8px; }
    .cat-card h4 { color: #58a6ff !important; font-size: 14px; margin: 0 0 5px 0; }
    .cat-card .cat-time { font-size: 11px; color: #ffa657 !important; margin-bottom: 5px; }
    .cat-card .cat-desc { color: #9da5ae !important; font-size: 12px; line-height: 1.5; margin: 0; }

    .timing-badge { display: inline-block; background: #0d3321; border: 1px solid #238636; color: #56d364 !important; font-size: 12px; font-weight: 600; padding: 4px 14px; border-radius: 20px; margin-left: 8px; }
    .timing-compare { display: inline-block; background: #341a04; border: 1px solid #9e6a03; color: #e3b341 !important; font-size: 11px; padding: 3px 12px; border-radius: 20px; margin-left: 6px; }

    .footer-row { display: flex; justify-content: center; gap: 28px; padding: 22px 0 10px 0; border-top: 1px solid #21262d; margin-top: 36px; }
    .footer-item { color: #6e7681; font-size: 12px; }

    /* ── QUERY SECTION SEPARATOR ── */
    .query-separator {
        border-top: 1px solid #30363d;
        margin: 28px 0 24px 0;
        padding-top: 4px;
    }

    /* ── RESULTS SECTION ── */
    .results-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
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
    With MCP-powered agents, you get <strong style="color:#56d364;">real-time insights in seconds</strong>.
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
            # Try json.loads with fixed quotes
            fixed = after.replace("'", '"')
            parsed = json.loads(fixed)
            if 'content' in parsed and parsed['content']:
                return parsed['content'][0].get('text', raw_output)
    except Exception:
        pass
    
    return raw_output


if submit and query:
    start_time = time.time()
    with st.spinner(""):
        st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;padding:16px 20px;background:#1b2230;border:1px solid #3d4f65;border-radius:10px;margin:8px 0;">
            <div style="width:20px;height:20px;border:3px solid #30363d;border-top:3px solid #ff8c00;border-radius:50%;animation:spin 1s linear infinite;flex-shrink:0;"></div>
            <span style="color:#ffa657;font-size:15px;font-weight:500;">Querying Teradata via MCP + Claude — this may take 15-60 seconds...</span>
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

            if result.returncode == 0:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:12px 0 6px 0;">
                    <span style="color:#56d364;font-size:16px;font-weight:600;">✅ Analysis Complete</span>
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
            st.error("⏱️ Query timed out (>90s). Try a simpler question or run `agentcore status`.")
        except Exception as e:
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
