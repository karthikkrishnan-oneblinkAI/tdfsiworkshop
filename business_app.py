import streamlit as st
import subprocess
import json
import ast

# MUST be first Streamlit command
st.set_page_config(page_title="Banking Intelligence", page_icon="💼", layout="wide")

# Password check
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.title("🔐 Banking Intelligence Assistant")
    st.markdown("### Please enter password to continue")
    
    password = st.text_input("Password:", type="password", key="password_input")
    
    if st.button("Login"):
        if password == "workshop2026":
            st.session_state.authenticated = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Incorrect password")
    
    st.stop()

check_password()

# Header
col1, col2 = st.columns([5, 1])
with col1:
    st.title("💼 Banking Intelligence Assistant")
with col2:
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("Ask questions about customer data in natural language")

# SIDEBAR
with st.sidebar:
    st.header("📊 Example Questions")
    
    st.subheader("🚨 Churn Analysis")
    if st.button("💡 Try this", key="churn_btn"):
        st.session_state.query = "Show me customers with highest churn risk"
        st.rerun()
    st.markdown("""
    - Show me customers with highest churn risk
    - Calculate revenue impact of losing top 50 at-risk customers
    - Analyze churn patterns by geography
    - Find inactive customers who had high balances 6 months ago
    """)
    
    st.subheader("🌍 Geographic Intelligence")
    if st.button("💡 Try this", key="geo_btn"):
        st.session_state.query = "Compare customer metrics across France, Germany, and Spain"
        st.rerun()
    st.markdown("""
    - Compare customer metrics across France, Germany, Spain
    - Which market has highest average balance?
    - Identify geographic hotspots with highest complaint volumes
    """)
    
    st.subheader("📞 Complaint Analysis")
    if st.button("💡 Try this", key="complaint_btn"):
        st.session_state.query = "Analyze complaint patterns from the last 48 hours"
        st.rerun()
    st.markdown("""
    - Analyze complaint patterns from last 48 hours
    - Show top 3 complaint categories driving highest churn risk
    - Find customers with unresolved complaints
    """)
    
    st.subheader("💳 Credit Risk")
    if st.button("💡 Try this", key="credit_btn"):
        st.session_state.query = "Analyze credit risk portfolio distribution"
        st.rerun()
    st.markdown("""
    - Analyze credit risk portfolio distribution
    - Identify customers suitable for credit limit increases
    - Calculate expected losses by geographic market
    """)
    
    st.subheader("💎 High-Value Customers")
    if st.button("💡 Try this", key="wealth_btn"):
        st.session_state.query = "Find the top 20 customers by balance who have been inactive"
        st.rerun()
    st.markdown("""
    - Find top 20 customers by balance who are inactive
    - Show high-income customers with low balances
    - Identify cross-selling opportunities for wealthy customers
    """)

# Query interface — KEY FIX: set widget state directly before rendering
if 'query' in st.session_state:
    st.session_state.query_input = st.session_state.query
    del st.session_state.query

query = st.text_area(
    "Your Question:",
    key="query_input",
    placeholder="Example: Show me high-value customers at churn risk",
    height=120
)

col1, col2 = st.columns([1, 4])
with col1:
    submit = st.button("🔍 Get Insights", type="primary", use_container_width=True)

def extract_clean_response(raw_output):
    """Extract ONLY the assistant's text from the response"""
    try:
        # Look for "Response: { ... }"
        if "Response:" in raw_output:
            # Find the part after "Response:"
            response_part = raw_output.split("Response:", 1)[1].strip()
            
            # Use ast.literal_eval to parse Python dict format
            response_dict = ast.literal_eval(response_part)
            
            # Extract text from content
            if 'content' in response_dict:
                content = response_dict['content']
                if isinstance(content, list) and len(content) > 0:
                    if 'text' in content[0]:
                        return content[0]['text']
        
        return raw_output
    
    except Exception as e:
        # Fallback: try to find text between 'text': and the closing }
        import re
        match = re.search(r"'text':\s*[\"'](.+?)[\"']\s*}\s*]\s*}", raw_output, re.DOTALL)
        if match:
            text = match.group(1)
            # Unescape newlines
            text = text.replace('\\n', '\n')
            return text
        
        return raw_output

if submit and query:
    with st.spinner("🤔 Analyzing your question..."):
        try:
            payload = json.dumps({"prompt": query})
            result = subprocess.run(
                ['/home/ubuntu/.local/bin/agentcore', 'invoke', payload],
                capture_output=True,
                text=True,
                timeout=90,
                cwd='/home/ubuntu/workshop/tdfsiworkshop'
            )
            
            if result.returncode == 0:
                st.success("✅ Analysis Complete")
                
                # Extract clean text
                clean_text = extract_clean_response(result.stdout)
                
                # Display
                st.markdown("### 💡 Insights")
                st.markdown(clean_text)
                
                # Raw debug
                with st.expander("🔍 View Raw Response (Debug)"):
                    st.code(result.stdout, language="text")
            else:
                st.error("❌ Error running query")
                st.code(result.stderr, language="text")
        
        except subprocess.TimeoutExpired:
            st.error("⏱️ Query timed out (>90s)")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif submit:
    st.warning("⚠️ Please enter a question")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🟠 Teradata Vantage")
with col2:
    st.caption("☁️ AWS Bedrock AgentCore")
with col3:
    st.caption("🤖 Claude 3.5 Sonnet")