import streamlit as st
import subprocess
import json
import ast
import time

# MUST be first Streamlit command
st.set_page_config(
    page_title="Banking Intelligence Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════
       BASE THEME — light-on-dark with good contrast
       ═══════════════════════════════════════════════ */
    .stApp {
        background-color: #0f1419;
    }

    /* ── All Labels (form fields) ── */
    .stApp label {
        color: #ffa94d !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px;
    }

    /* ── Text Inputs & Text Areas ── */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: #1b2230 !important;
        border: 1.5px solid #4a5568 !important;
        border-radius: 8px !important;
        caret-color: #ffa94d !important;
        font-size: 14px !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #718096 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #ffa94d !important;
        box-shadow: 0 0 0 2px rgba(255, 169, 77, 0.25) !important;
    }

    /* ── Body Text ── */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #cbd5e0;
    }
    .stMarkdown strong {
        color: #f7fafc;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f0f4f8 !important;
    }
    .stMarkdown code {
        color: #68d391;
        background: #1a2332;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader, .streamlit-expanderHeader p,
    .streamlit-expanderHeader span {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent p,
    .streamlit-expanderContent li,
    .streamlit-expanderContent span {
        color: #cbd5e0 !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #1e2733;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li {
        color: #c9d1d9 !important;
    }
    section[data-testid="stSidebar"] strong {
        color: #f0f6fc !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: #f0f6fc !important;
    }
    section[data-testid="stSidebar"] .stCaption {
        color: #8b949e !important;
    }

    /* ══ SIDEBAR BUTTONS — make them pop ══ */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(255, 102, 0, 0.3) !important;
        margin-bottom: 4px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #ff8533 0%, #ffa94d 100%) !important;
        box-shadow: 0 4px 14px rgba(255, 102, 0, 0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Main area primary button ── */
    .stApp > section > div > div > div .stButton > button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #0052CC 0%, #2684FF 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 82, 204, 0.35) !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: 0 4px 14px rgba(0, 82, 204, 0.5) !important;
    }

    /* ── Other buttons (logout, login) ── */
    .stButton > button {
        color: #e2e8f0 !important;
        border-color: #4a5568 !important;
    }

    /* ── Alerts ── */
    .stAlert p {
        color: inherit !important;
    }

    /* ── Spinner ── */
    .stSpinner > div > span {
        color: #e2e8f0 !important;
    }

    /* ═══════════════════════════════════════════════
       CUSTOM COMPONENTS
       ═══════════════════════════════════════════════ */

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #FF6600 0%, #0052CC 100%);
        border-radius: 14px;
        padding: 30px 34px;
        margin-bottom: 24px;
    }
    .hero-banner h1 {
        color: #ffffff !important;
        font-size: 28px;
        margin-bottom: 6px;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.92) !important;
        font-size: 15px;
        margin: 0;
    }
    .logo-row {
        display: flex;
        gap: 10px;
        margin-top: 16px;
        flex-wrap: wrap;
    }
    .logo-badge {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(4px);
        padding: 5px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #ffffff !important;
    }

    /* Login page */
    .login-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 36px 32px;
        max-width: 420px;
        margin: 30px auto;
    }
    .login-card h2 {
        color: #f0f6fc !important;
        font-size: 22px;
        text-align: center;
        margin-bottom: 6px;
    }
    .login-card p {
        color: #8b949e !important;
        text-align: center;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Metric cards */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    @media (max-width: 768px) {
        .metric-row { grid-template-columns: repeat(2, 1fr); }
    }
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .metric-card .mv {
        font-size: 28px;
        font-weight: 700;
        color: #58a6ff;
    }
    .metric-card .ml {
        font-size: 10px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 2px;
    }
    .metric-card .ms {
        font-size: 11px;
        color: #ffa657;
        margin-top: 6px;
    }

    /* Value banner */
    .value-banner {
        background: #161b22;
        border: 1px solid #1f6feb;
        border-left: 4px solid #1f6feb;
        border-radius: 10px;
        padding: 22px 26px;
        margin-bottom: 22px;
    }
    .value-banner h3 {
        color: #58a6ff !important;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .value-banner p {
        color: #c9d1d9 !important;
        font-size: 14px;
        line-height: 1.65;
        margin: 0;
    }

    /* Speed table */
    .speed-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 14px 0;
        font-size: 13px;
    }
    .speed-table th {
        text-align: left;
        padding: 10px 14px;
        color: #8b949e;
        border-bottom: 2px solid #30363d;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .speed-table td {
        padding: 11px 14px;
        border-bottom: 1px solid #21262d;
        color: #c9d1d9;
    }
    .speed-table .old { color: #f97583; font-weight: 500; }
    .speed-table .new { color: #56d364; font-weight: 600; }
    .speed-table .impact { color: #e3b341; font-size: 12px; }

    /* Category cards */
    .cat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 8px;
    }
    .cat-card h4 {
        color: #58a6ff !important;
        font-size: 14px;
        margin: 0 0 5px 0;
    }
    .cat-card .cat-time {
        font-size: 11px;
        color: #ffa657 !important;
        margin-bottom: 5px;
    }
    .cat-card .cat-desc {
        color: #8b949e !important;
        font-size: 12px;
        line-height: 1.5;
        margin: 0;
    }

    /* Timing badges (results) */
    .timing-badge {
        display: inline-block;
        background: #0d3321;
        border: 1px solid #238636;
        color: #56d364 !important;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 14px;
        border-radius: 20px;
        margin-left: 8px;
    }
    .timing-compare {
        display: inline-block;
        background: #341a04;
        border: 1px solid #9e6a03;
        color: #e3b341 !important;
        font-size: 11px;
        padding: 3px 12px;
        border-radius: 20px;
        margin-left: 6px;
    }

    /* Footer */
    .footer-row {
        display: flex;
        justify-content: center;
        gap: 28px;
        padding: 22px 0 10px 0;
        border-top: 1px solid #21262d;
        margin-top: 36px;
    }
    .footer-item { color: #484f58; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ─── Password Check ───
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    # Centered login hero
    st.markdown("")
    st.markdown("""
    <div class="hero-banner" style="max-width:500px;margin:20px auto;">
        <h1 style="text-align:center;">💼 Banking Intelligence</h1>
        <p style="text-align:center;">Teradata + AWS AgentCore Workshop</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1.2, 2, 1.2])
    with col_m:
        # Card-style login box
        st.markdown("""
        <div class="login-card">
            <h2>🔐 Welcome</h2>
            <p>Enter the workshop password to continue</p>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input("Workshop Password:", type="password", key="password_input")
        st.markdown("")
        if st.button("🔓 Login", use_container_width=True, type="primary"):
            if password == "workshop2026":
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
    st.stop()

check_password()

# ─── Logged-in App ───

# Header row
col_main, col_logout = st.columns([6, 1])
with col_logout:
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Hero
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

# Metrics
st.markdown("""
<div class="metric-row">
    <div class="metric-card">
        <div class="mv">30s</div>
        <div class="ml">Avg Query Time</div>
        <div class="ms">vs 2-3 days traditional</div>
    </div>
    <div class="metric-card">
        <div class="mv">10K</div>
        <div class="ml">Customer Records</div>
        <div class="ms">Real-time access</div>
    </div>
    <div class="metric-card">
        <div class="mv">$765M</div>
        <div class="ml">Deposits Monitored</div>
        <div class="ms">Churn risk scoring</div>
    </div>
    <div class="metric-card">
        <div class="mv">20.4%</div>
        <div class="ml">Current Churn Rate</div>
        <div class="ms">5% reduction = $2-5M saved</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Value banner
st.markdown("""
<div class="value-banner">
    <h3>💡 Why This Matters</h3>
    <p>Traditional analytics takes days — weekly reports, manual SQL, Excel analysis.
    With MCP-powered agents, you get <strong style="color:#56d364;">real-time insights in seconds</strong>.
    Imagine detecting a complaint surge Monday morning and resolving it before customers churn,
    instead of discovering it in Friday's report.</p>
</div>
""", unsafe_allow_html=True)

# Speed comparison
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

    # ── Churn ──
    st.markdown("""
    <div class="cat-card">
        <h4>🚨 Churn Analysis</h4>
        <div class="cat-time">⏱ Traditional: 2-3 days → MCP: 30 seconds</div>
        <p class="cat-desc">Identify at-risk customers before they leave. A 5% churn reduction saves $2-5M annually.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔥 Try: Highest churn risk", key="churn_btn"):
        st.session_state.query = "Show me customers with highest churn risk and calculate the revenue impact if we lose them"
        st.rerun()
    with st.expander("More churn questions"):
        st.markdown("""
        - Revenue impact of losing top 50 at-risk customers
        - Churn patterns by geography with interventions
        - Inactive customers who had high balances 6 months ago
        """)

    # ── Geographic ──
    st.markdown("""
    <div class="cat-card">
        <h4>🌍 Geographic Intelligence</h4>
        <div class="cat-time">⏱ Traditional: 4-6 hours → MCP: 30 seconds</div>
        <p class="cat-desc">Compare France, Germany, Spain markets. Spot regional trends instantly.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔥 Try: Compare markets", key="geo_btn"):
        st.session_state.query = "Compare customer metrics across France, Germany, and Spain. Which market has the highest average balance?"
        st.rerun()
    with st.expander("More geographic questions"):
        st.markdown("""
        - Which market has highest average balance?
        - Geographic hotspots with highest complaint volumes
        - Regional service quality patterns
        """)

    # ── Complaints ──
    st.markdown("""
    <div class="cat-card">
        <h4>📞 Complaint Analysis</h4>
        <div class="cat-time">⏱ Traditional: 3-5 days → MCP: 30 seconds</div>
        <p class="cat-desc">15-20% of complaints lead to churn. Detect surges and root causes in real time.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔥 Try: Complaint patterns", key="complaint_btn"):
        st.session_state.query = "Analyze complaint patterns from the last 48 hours and identify any unusual spikes by product category"
        st.rerun()
    with st.expander("More complaint questions"):
        st.markdown("""
        - Top 3 complaint categories driving highest churn risk
        - Customers with unresolved complaints + high churn probability
        - Complaint resolution success rates by response type
        """)

    # ── Credit Risk ──
    st.markdown("""
    <div class="cat-card">
        <h4>💳 Credit Risk</h4>
        <div class="cat-time">⏱ Traditional: 1-2 days → MCP: 30 seconds</div>
        <p class="cat-desc">Portfolio risk analysis and lending optimization across your customer base.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔥 Try: Credit risk portfolio", key="credit_btn"):
        st.session_state.query = "Analyze our credit risk portfolio. Show credit score distribution and identify customers suitable for credit limit increases."
        st.rerun()
    with st.expander("More credit risk questions"):
        st.markdown("""
        - Customers suitable for credit limit increases
        - Portfolio risk concentration by segment
        - Expected losses by geographic market
        """)

    # ── High-Value ──
    st.markdown("""
    <div class="cat-card">
        <h4>💎 High-Value Customers</h4>
        <div class="cat-time">⏱ Traditional: 1-2 hours → MCP: 30 seconds</div>
        <p class="cat-desc">Protect your most valuable relationships. Target retention and cross-sell.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔥 Try: Inactive high-value", key="wealth_btn"):
        st.session_state.query = "Find the top 20 customers by balance who have been inactive. These are high-value retention targets."
        st.rerun()
    with st.expander("More high-value questions"):
        st.markdown("""
        - High-income customers with low balances (acquisition targets)
        - Cross-selling opportunities for wealthy customers
        - Customers suitable for private banking upgrade
        """)

    # ── Impact Summary ──
    st.markdown("---")
    st.markdown("### 💰 Business Impact")
    st.markdown("""
    - **Churn Prevention:** $2-5M saved
    - **Analyst Speed:** 10x faster
    - **Decisions:** Real-time vs weekly
    - **Access:** No SQL needed
    """)


# ═══════════════════════════════════════════════════
# QUERY INTERFACE
# ═══════════════════════════════════════════════════

# "Try this" button → text area state transfer
if 'query' in st.session_state:
    st.session_state.query_input = st.session_state.query
    del st.session_state.query

query = st.text_area(
    "Your Question:",
    key="query_input",
    placeholder="Example: Show me high-value customers at churn risk — or click an orange button in the sidebar →",
    height=100
)

col1, col2, col3 = st.columns([1.3, 2, 2])
with col1:
    submit = st.button("🔍 Get Insights", type="primary", use_container_width=True)


# ─── Response extraction ───
def extract_clean_response(raw_output):
    try:
        if "Response:" in raw_output:
            response_part = raw_output.split("Response:", 1)[1].strip()
            response_dict = ast.literal_eval(response_part)
            if 'content' in response_dict:
                content = response_dict['content']
                if isinstance(content, list) and len(content) > 0:
                    if 'text' in content[0]:
                        return content[0]['text']
        return raw_output
    except Exception:
        import re
        match = re.search(r"'text':\s*[\"'](.+?)[\"']\s*}\s*]\s*}", raw_output, re.DOTALL)
        if match:
            text = match.group(1).replace('\\n', '\n')
            return text
        return raw_output


# ─── Query Execution ───
if submit and query:
    start_time = time.time()
    with st.spinner("🤔 Querying Teradata via MCP + Claude — this may take 15-60 seconds..."):
        try:
            payload = json.dumps({"prompt": query})
            result = subprocess.run(
                ['/home/ubuntu/.local/bin/agentcore', 'invoke', payload],
                capture_output=True,
                text=True,
                timeout=90,
                cwd='/home/ubuntu/workshop/tdfsiworkshop'
            )
            elapsed = time.time() - start_time

            if result.returncode == 0:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; margin:12px 0 6px 0;">
                    <span style="color:#56d364; font-size:16px; font-weight:600;">✅ Analysis Complete</span>
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

# Footer
st.markdown("""
<div class="footer-row">
    <span class="footer-item">🟠 Teradata Vantage</span>
    <span class="footer-item">☁️ AWS Bedrock AgentCore</span>
    <span class="footer-item">🤖 Claude 3.5 Sonnet</span>
    <span class="footer-item">🔧 Strands Agents SDK</span>
</div>
""", unsafe_allow_html=True)