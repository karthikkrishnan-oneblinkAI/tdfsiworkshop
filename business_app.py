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

# ─── Custom CSS for polished look ───
st.markdown("""
<style>
    /* Main background and font */
    .stApp {
        background-color: #0e1117;
    }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #FF6600 0%, #0052CC 100%);
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
    }
    .hero-banner h1 {
        color: white !important;
        font-size: 28px;
        margin-bottom: 4px;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.9);
        font-size: 15px;
        margin: 0;
    }
    .logo-row {
        display: flex;
        gap: 10px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .logo-badge {
        background: rgba(255,255,255,0.18);
        padding: 5px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        color: white;
    }

    /* Metric cards */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 24px;
    }
    @media (max-width: 768px) {
        .metric-row { grid-template-columns: repeat(2, 1fr); }
    }
    .metric-card {
        background: #1a1f2e;
        border: 1px solid #2a3040;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #4ec9b0;
        margin-bottom: 2px;
    }
    .metric-card .metric-label {
        font-size: 11px;
        color: #8892a4;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card .metric-sub {
        font-size: 11px;
        color: #ff9800;
        margin-top: 4px;
    }

    /* Value proposition banner */
    .value-banner {
        background: linear-gradient(135deg, #1a3a5c 0%, #0d2137 100%);
        border: 1px solid #2980b9;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .value-banner h3 {
        color: #3498db;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .value-banner p {
        color: #bdc3c7;
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
    }

    /* Speed comparison table */
    .speed-table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 13px;
    }
    .speed-table th {
        text-align: left;
        padding: 10px 14px;
        color: #8892a4;
        border-bottom: 1px solid #2a3040;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .speed-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #1a1f2e;
        color: #d4d4d4;
    }
    .speed-table .old {
        color: #ff6b6b;
    }
    .speed-table .new {
        color: #4ec9b0;
        font-weight: 600;
    }
    .speed-table .impact {
        color: #ffd93d;
        font-size: 11px;
    }

    /* Category cards in sidebar */
    .cat-card {
        background: #1a1f2e;
        border: 1px solid #2a3040;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .cat-card h4 {
        color: #4ec9b0;
        font-size: 14px;
        margin-bottom: 6px;
    }
    .cat-card .cat-context {
        font-size: 11px;
        color: #ff9800;
        margin-bottom: 6px;
        font-style: italic;
    }
    .cat-card p {
        color: #8892a4;
        font-size: 12px;
        margin: 0;
        line-height: 1.5;
    }

    /* Insight result styling */
    .insight-box {
        background: #141820;
        border: 1px solid #2a3040;
        border-left: 4px solid #4ec9b0;
        border-radius: 0 10px 10px 0;
        padding: 24px;
        margin-top: 16px;
        line-height: 1.7;
        color: #d4d4d4;
    }

    /* Timing badge */
    .timing-badge {
        display: inline-block;
        background: #1a3a2a;
        border: 1px solid #2d6a4f;
        color: #4ec9b0;
        font-size: 12px;
        padding: 4px 12px;
        border-radius: 20px;
        margin-left: 8px;
    }
    .timing-compare {
        display: inline-block;
        background: #3d2b1f;
        border: 1px solid #664422;
        color: #ff9800;
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 20px;
        margin-left: 6px;
    }

    /* Footer */
    .footer-row {
        display: flex;
        justify-content: center;
        gap: 24px;
        padding: 20px 0 10px 0;
        border-top: 1px solid #1a1f2e;
        margin-top: 30px;
    }
    .footer-item {
        color: #556070;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Password Check ───
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div class="hero-banner" style="max-width:480px;margin:60px auto;">
        <h1>🔐 Banking Intelligence</h1>
        <p>Teradata + AWS AgentCore Workshop</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        password = st.text_input("Password:", type="password", key="password_input")
        if st.button("Login", use_container_width=True):
            if password == "workshop2026":
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    st.stop()

check_password()

# ─── Hero Banner ───
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

# ─── Key Metrics Row ───
st.markdown("""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">30s</div>
        <div class="metric-label">Avg Query Time</div>
        <div class="metric-sub">vs 2-3 days traditional</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">10K</div>
        <div class="metric-label">Customer Records</div>
        <div class="metric-sub">Real-time access</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">$765M</div>
        <div class="metric-label">Deposits Monitored</div>
        <div class="metric-sub">Churn risk scoring</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">20.4%</div>
        <div class="metric-label">Current Churn Rate</div>
        <div class="metric-sub">5% reduction = $2-5M saved</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Value Proposition ───
st.markdown("""
<div class="value-banner">
    <h3>💡 Why This Matters</h3>
    <p>Traditional analytics takes days — weekly reports, manual SQL, Excel analysis.
    With MCP-powered agents, you get <strong style="color:#4ec9b0;">real-time insights in seconds</strong>.
    Imagine detecting a complaint surge Monday morning and resolving it before customers churn,
    instead of discovering it in Friday's report.</p>
</div>
""", unsafe_allow_html=True)

# ─── Speed Comparison (collapsible) ───
with st.expander("📊 Speed Comparison: MCP vs Traditional Analytics"):
    st.markdown("""
    <table class="speed-table">
        <tr><th>Task</th><th>Traditional</th><th>With MCP Agent</th><th>Impact</th></tr>
        <tr>
            <td>Churn analysis report</td>
            <td class="old">2-3 days</td>
            <td class="new">~30 seconds</td>
            <td class="impact">Act before customers leave</td>
        </tr>
        <tr>
            <td>Geographic comparison</td>
            <td class="old">4-6 hours</td>
            <td class="new">~30 seconds</td>
            <td class="impact">Real-time market intelligence</td>
        </tr>
        <tr>
            <td>High-value customer list</td>
            <td class="old">1-2 hours</td>
            <td class="new">~30 seconds</td>
            <td class="impact">Instant retention targeting</td>
        </tr>
        <tr>
            <td>Complaint root-cause analysis</td>
            <td class="old">3-5 days</td>
            <td class="new">~30 seconds</td>
            <td class="impact">Prevent escalation</td>
        </tr>
        <tr>
            <td>Ad-hoc business question</td>
            <td class="old">"Ask IT, wait days"</td>
            <td class="new">~30 seconds</td>
            <td class="impact">Self-serve analytics for all</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table class="speed-table" style="margin-top:20px;">
        <tr><th>Business Metric</th><th>Current State</th><th>MCP-Enabled</th><th>Impact</th></tr>
        <tr>
            <td>Resolution Time</td>
            <td class="old">5-10 days</td>
            <td class="new">2-3 days</td>
            <td class="impact">40% faster</td>
        </tr>
        <tr>
            <td>Complaint-to-Churn Rate</td>
            <td class="old">15-20%</td>
            <td class="new">8-12%</td>
            <td class="impact">$2-5M savings</td>
        </tr>
        <tr>
            <td>Customer Satisfaction</td>
            <td class="old">65%</td>
            <td class="new">85%</td>
            <td class="impact">35% improvement</td>
        </tr>
        <tr>
            <td>Issue Detection</td>
            <td class="old">3-5 days</td>
            <td class="new">30 seconds</td>
            <td class="impact">Prevent escalation</td>
        </tr>
        <tr>
            <td>Response Success Rate</td>
            <td class="old">70%</td>
            <td class="new">90%</td>
            <td class="impact">25% improvement</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# SIDEBAR — Categories with business context
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 📊 Analysis Categories")
    st.caption("Click a category to load a sample question. Each shows what traditionally takes hours or days.")

    # ── Churn Analysis ──
    st.markdown("""
    <div class="cat-card">
        <h4>🚨 Churn Analysis</h4>
        <div class="cat-context">⏱ Traditional: 2-3 days → MCP: 30 seconds</div>
        <p>Identify at-risk customers before they leave. A 5% churn reduction saves $2-5M annually.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Try: Highest churn risk", key="churn_btn"):
        st.session_state.query = "Show me customers with highest churn risk and calculate the revenue impact if we lose them"
        st.rerun()
    with st.expander("More churn questions", expanded=False):
        st.markdown("""
        - Calculate revenue impact of losing top 50 at-risk customers
        - Analyze churn patterns by geography and recommend interventions
        - Find inactive customers who had high balances 6 months ago
        """)

    # ── Geographic Intelligence ──
    st.markdown("""
    <div class="cat-card">
        <h4>🌍 Geographic Intelligence</h4>
        <div class="cat-context">⏱ Traditional: 4-6 hours → MCP: 30 seconds</div>
        <p>Compare markets across France, Germany, Spain. Spot regional trends instantly.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Try: Compare markets", key="geo_btn"):
        st.session_state.query = "Compare customer metrics across France, Germany, and Spain. Which market has the highest average balance?"
        st.rerun()
    with st.expander("More geographic questions", expanded=False):
        st.markdown("""
        - Which market has highest average balance?
        - Identify geographic hotspots with highest complaint volumes
        - Analyze regional service quality patterns
        """)

    # ── Complaint Analysis ──
    st.markdown("""
    <div class="cat-card">
        <h4>📞 Complaint Analysis</h4>
        <div class="cat-context">⏱ Traditional: 3-5 days → MCP: 30 seconds</div>
        <p>15-20% of complaints lead to churn. Detect surges and root causes in real time.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Try: Complaint patterns", key="complaint_btn"):
        st.session_state.query = "Analyze complaint patterns from the last 48 hours and identify any unusual spikes by product category"
        st.rerun()
    with st.expander("More complaint questions", expanded=False):
        st.markdown("""
        - Show top 3 complaint categories driving highest churn risk
        - Find customers with unresolved complaints and high churn probability
        - Analyze complaint resolution success rates by response type
        """)

    # ── Credit Risk ──
    st.markdown("""
    <div class="cat-card">
        <h4>💳 Credit Risk</h4>
        <div class="cat-context">⏱ Traditional: 1-2 days → MCP: 30 seconds</div>
        <p>Portfolio risk analysis and lending optimization across your customer base.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Try: Credit risk portfolio", key="credit_btn"):
        st.session_state.query = "Analyze our credit risk portfolio. Show credit score distribution and identify customers suitable for credit limit increases."
        st.rerun()
    with st.expander("More credit risk questions", expanded=False):
        st.markdown("""
        - Identify customers suitable for credit limit increases
        - Show portfolio risk concentration by customer segment
        - Calculate expected losses by geographic market
        """)

    # ── High-Value Customers ──
    st.markdown("""
    <div class="cat-card">
        <h4>💎 High-Value Customers</h4>
        <div class="cat-context">⏱ Traditional: 1-2 hours → MCP: 30 seconds</div>
        <p>Protect your most valuable relationships. Target retention and cross-sell opportunities.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Try: Inactive high-value", key="wealth_btn"):
        st.session_state.query = "Find the top 20 customers by balance who have been inactive. These are high-value retention targets."
        st.rerun()
    with st.expander("More high-value questions", expanded=False):
        st.markdown("""
        - Show high-income customers with low balances — acquisition targets
        - Identify cross-selling opportunities for wealthy customers
        - Show customers suitable for private banking upgrade
        """)

    # ── Business Impact Summary ──
    st.markdown("---")
    st.markdown("### 💰 Estimated Business Impact")
    st.markdown("""
    - **Churn Prevention:** 5% reduction = **$2-5M** annual savings
    - **Analyst Productivity:** **10x** faster insights
    - **Decision Speed:** Real-time vs weekly reports
    - **Democratized Analytics:** No SQL knowledge needed
    """)

# ═══════════════════════════════════════════════════
# MAIN — Query Interface
# ═══════════════════════════════════════════════════

# Handle "Try this" button state transfer (KEY FIX)
if 'query' in st.session_state:
    st.session_state.query_input = st.session_state.query
    del st.session_state.query

query = st.text_area(
    "Your Question:",
    key="query_input",
    placeholder="Example: Show me high-value customers at churn risk — or click a category in the sidebar →",
    height=100
)

col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    submit = st.button("🔍 Get Insights", type="primary", use_container_width=True)

# ─── Response extraction ───
def extract_clean_response(raw_output):
    """Extract ONLY the assistant's text from the response"""
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
            text = match.group(1)
            text = text.replace('\\n', '\n')
            return text
        return raw_output

# ─── Query Execution ───
if submit and query:
    start_time = time.time()
    with st.spinner("🤔 Analyzing your question via Teradata MCP + Claude..."):
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
                # Success header with timing
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                    <span style="color:#4ec9b0; font-size:16px; font-weight:600;">✅ Analysis Complete</span>
                    <span class="timing-badge">⚡ {elapsed:.1f}s</span>
                    <span class="timing-compare">⏱ Traditional: hours to days</span>
                </div>
                """, unsafe_allow_html=True)

                clean_text = extract_clean_response(result.stdout)

                st.markdown("### 💡 Insights")
                st.markdown(clean_text)

                # Business context after results
                with st.expander("📈 Business Context — Why This Matters"):
                    st.markdown(f"""
                    **This query completed in {elapsed:.1f} seconds.** In a traditional analytics workflow,
                    this type of analysis would require:

                    1. **Submitting a request** to the BI team or data engineering
                    2. **Writing and validating SQL** against the data warehouse
                    3. **Building a report** in Excel or a BI tool
                    4. **Review and delivery** back to the business stakeholder

                    **Total traditional time: hours to days.** With MCP-powered agents, any business user
                    can ask questions in plain English and get actionable insights in seconds — no SQL
                    knowledge required, no ticket queue, no waiting.
                    """)

                with st.expander("🔍 Raw Response (Debug)"):
                    st.code(result.stdout, language="text")
            else:
                st.error("❌ Error running query")
                st.code(result.stderr, language="text")

        except subprocess.TimeoutExpired:
            st.error("⏱️ Query timed out (>90s). Try a simpler question or check agent status.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif submit:
    st.warning("⚠️ Please enter a question — or click a sample in the sidebar →")

# ─── Footer ───
st.markdown("""
<div class="footer-row">
    <span class="footer-item">🟠 Teradata Vantage</span>
    <span class="footer-item">☁️ AWS Bedrock AgentCore</span>
    <span class="footer-item">🤖 Claude 3.5 Sonnet</span>
    <span class="footer-item">🔧 Strands Agents SDK</span>
</div>
""", unsafe_allow_html=True)
