"""
Home.py — Landing page for the AI Security Scanner Platform.
"""

import streamlit as st

st.set_page_config(
    page_title="AI Security Scanner Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔐 AI Security Scanner Platform")

st.markdown(
    """
Welcome to the AI Security Scanner Dashboard.

This application demonstrates a DevSecOps pipeline that combines static code analysis, dependency vulnerability scanning, AI-powered security reporting, and interactive dashboard visualization.
"""
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Scanner Types", "3")
    st.caption("Bandit, pip-audit, Gemini AI")

with col2:
    st.metric("Dashboard Mode", "Active")
    st.caption("Interactive Streamlit interface")

with col3:
    st.metric("CI Integration", "Enabled")
    st.caption("GitHub Actions workflow")

st.divider()

st.subheader("Available Pages")

st.markdown(
    """
Use the sidebar to open:

- **Security Scanner Dashboard** — View vulnerabilities, charts, uploaded file scans, and AI reports.
"""
)

st.subheader("How to Use")

st.markdown("Run the security scanner:")

st.code("python scanner.py", language="bash")

st.markdown("Generate the Gemini AI security report:")

st.code("python ai_report.py", language="bash")

st.markdown("Start the Streamlit dashboard:")

st.code("streamlit run app/Home.py", language="bash")

st.subheader("Project Highlights")

st.markdown(
    """
- Hybrid security scanning using traditional tools and AI
- Bandit static code analysis
- pip-audit dependency vulnerability scanning
- Gemini-powered security report generation
- Streamlit dashboard for visualization
- GitHub Actions CI workflow
"""
)

st.info("Use the sidebar to open the Security Scanner dashboard.")