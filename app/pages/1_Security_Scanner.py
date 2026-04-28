"""
1_Security_Scanner.py — Streamlit dashboard for AI Security Scanner.

Features:
- KPI cards for total vulnerabilities
- Severity counts for High / Medium / Low
- Bar charts for Bandit and pip-audit findings
- Upload Python file and run Bandit scan inside the UI

Run from project root:
    streamlit run app/Home.py
"""

from pathlib import Path
import json
import subprocess
import tempfile

import pandas as pd
import plotly.express as px
import streamlit as st


# Page Config
st.set_page_config(
    page_title="AI Security Scanner",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# CSS styling
st.markdown(
    """
    <style>
    .scanner-banner {
        background: linear-gradient(135deg, #0f2440 0%, #1a3660 100%);
        border-left: 5px solid #7986CB;
        border-radius: 10px;
        padding: 22px 28px;
        margin-bottom: 18px;
    }
    .scanner-banner-title {
        color: #f0c040;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 0 0 10px 0;
    }
    .scanner-banner-body {
        color: #e8eaf0;
        font-size: 1.0rem;
        line-height: 1.75;
        margin: 0;
    }
    .scanner-note {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Paths
ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

BANDIT_PATH = REPORTS / "bandit_report.json"
PIP_PATH = REPORTS / "pip_audit_report.json"
AI_PATH = REPORTS / "gemini_security_report.txt"


# Helper functions
def load_json(path: Path) -> dict:
    """Safely load a JSON file."""
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def load_text(path: Path) -> str:
    """Safely load a text file."""
    if not path.exists():
        return ""

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception:
        return ""


def parse_bandit_results(data: dict) -> pd.DataFrame:
    """Convert Bandit JSON output into a DataFrame."""
    rows = []

    for item in data.get("results", []):
        rows.append(
            {
                "severity": item.get("issue_severity", "UNKNOWN"),
                "confidence": item.get("issue_confidence", "UNKNOWN"),
                "issue": item.get("issue_text", "N/A"),
                "test_id": item.get("test_id", "N/A"),
                "file": item.get("filename", "N/A"),
                "line": item.get("line_number", "N/A"),
            }
        )

    return pd.DataFrame(rows)


def parse_pip_audit_results(data: dict) -> pd.DataFrame:
    """Convert pip-audit JSON output into a DataFrame."""
    rows = []

    for dependency in data.get("dependencies", []):
        package = dependency.get("name", "N/A")
        version = dependency.get("version", "N/A")

        for vuln in dependency.get("vulns", []):
            fix_versions = vuln.get("fix_versions", [])
            if isinstance(fix_versions, list):
                fix_versions = ", ".join(fix_versions)

            rows.append(
                {
                    "package": package,
                    "version": version,
                    "vulnerability_id": vuln.get("id", "N/A"),
                    "fix_versions": fix_versions or "N/A",
                    "description": vuln.get("description", "N/A"),
                }
            )

    return pd.DataFrame(rows)


def count_bandit_severity(bandit_df: pd.DataFrame) -> dict:
    """Return severity counts from Bandit results."""
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    if bandit_df.empty or "severity" not in bandit_df.columns:
        return counts

    values = bandit_df["severity"].str.upper().value_counts().to_dict()

    for key in counts:
        counts[key] = int(values.get(key, 0))

    return counts


def run_bandit_on_uploaded_file(uploaded_file) -> tuple[pd.DataFrame, str]:
    """
    Save uploaded file temporarily and run Bandit on it.
    Returns the parsed Bandit DataFrame and raw command output.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / uploaded_file.name
        temp_path.write_bytes(uploaded_file.getvalue())

        output_path = Path(temp_dir) / "bandit_upload_report.json"

        command = [
            "bandit",
            "-r",
            str(temp_path),
            "-f",
            "json",
            "-o",
            str(output_path),
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        raw_output = (result.stdout or "") + "\n" + (result.stderr or "")

        if output_path.exists():
            uploaded_data = load_json(output_path)
            return parse_bandit_results(uploaded_data), raw_output

        return pd.DataFrame(), raw_output


# Load existing reports
bandit_data = load_json(BANDIT_PATH)
pip_data = load_json(PIP_PATH)
ai_report = load_text(AI_PATH)

bandit_df = parse_bandit_results(bandit_data)
pip_df = parse_pip_audit_results(pip_data)

severity_counts = count_bandit_severity(bandit_df)

total_bandit = len(bandit_df)
total_pip = len(pip_df)
total_issues = total_bandit + total_pip


# Header
st.title("🔐 AI Security Scanner Dashboard")

st.markdown(
    """
    <div class="scanner-banner">
        <p class="scanner-banner-title">Security Intelligence Dashboard</p>
        <p class="scanner-banner-body">
            This dashboard summarizes Python application security findings from static code analysis,
            dependency vulnerability scanning, and AI-generated security reporting. It supports both
            report review and direct file upload scanning inside the Streamlit interface.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Issues", total_issues)
kpi2.metric("Code Vulnerabilities", total_bandit)
kpi3.metric("Dependency Vulnerabilities", total_pip)
kpi4.metric("High Severity", severity_counts["HIGH"])

sev1, sev2, sev3 = st.columns(3)

sev1.metric("High", severity_counts["HIGH"])
sev2.metric("Medium", severity_counts["MEDIUM"])
sev3.metric("Low", severity_counts["LOW"])

st.divider()


# Tabs
tab_overview, tab_bandit, tab_pip, tab_ai, tab_upload = st.tabs(
    [
        "Overview",
        "Code Scan",
        "Dependency Scan",
        "AI Report",
        "Upload & Scan",
    ]
)


# Overview Tab
with tab_overview:
    st.subheader("Security Findings Overview")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        severity_chart_df = pd.DataFrame(
            {
                "Severity": ["High", "Medium", "Low"],
                "Count": [
                    severity_counts["HIGH"],
                    severity_counts["MEDIUM"],
                    severity_counts["LOW"],
                ],
            }
        )

        fig = px.bar(
            severity_chart_df,
            x="Severity",
            y="Count",
            text="Count",
            title="Code Vulnerabilities by Severity",
        )
        fig.update_layout(yaxis_title="Number of Findings", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        source_chart_df = pd.DataFrame(
            {
                "Source": ["Bandit Code Scan", "pip-audit Dependency Scan"],
                "Count": [total_bandit, total_pip],
            }
        )

        fig = px.bar(
            source_chart_df,
            x="Source",
            y="Count",
            text="Count",
            title="Findings by Scanner Source",
        )
        fig.update_layout(yaxis_title="Number of Findings", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="scanner-note">
        <strong>Interpretation:</strong> Bandit findings represent risks in the Python source code,
        while pip-audit findings represent vulnerable installed packages. The two scanners cover
        different parts of the security workflow.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Bandit Tab
with tab_bandit:
    st.subheader("Static Code Analysis Results")

    if bandit_df.empty:
        st.success("No Bandit findings found or no Bandit report is available.")
        st.caption("Run `python scanner.py` first to generate `reports/bandit_report.json`.")
    else:
        severity_filter = st.multiselect(
            "Filter by severity",
            options=["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM", "LOW"],
        )

        filtered_bandit = bandit_df[
            bandit_df["severity"].str.upper().isin(severity_filter)
        ]

        st.dataframe(
            filtered_bandit[
                ["severity", "confidence", "test_id", "issue", "file", "line"]
            ],
            use_container_width=True,
        )

        st.markdown("### Finding Details")

        for _, row in filtered_bandit.iterrows():
            with st.expander(f"{row['severity']} — {row['issue']}"):
                st.write(f"**Confidence:** {row['confidence']}")
                st.write(f"**Test ID:** {row['test_id']}")
                st.write(f"**File:** {row['file']}")
                st.write(f"**Line:** {row['line']}")


# pip-audit Tab
with tab_pip:
    st.subheader("Dependency Vulnerability Results")

    if pip_df.empty:
        st.success("No dependency vulnerabilities found or no pip-audit report is available.")
        st.caption("Run `python scanner.py` first to generate `reports/pip_audit_report.json`.")
    else:
        package_counts = (
            pip_df.groupby("package")
            .size()
            .reset_index(name="vulnerability_count")
            .sort_values("vulnerability_count", ascending=False)
        )

        fig = px.bar(
            package_counts,
            x="package",
            y="vulnerability_count",
            text="vulnerability_count",
            title="Dependency Vulnerabilities by Package",
        )
        fig.update_layout(xaxis_title="Package", yaxis_title="Number of Vulnerabilities")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(pip_df, use_container_width=True)

        st.markdown("### Vulnerability Details")

        for _, row in pip_df.iterrows():
            with st.expander(f"{row['package']} {row['version']} — {row['vulnerability_id']}"):
                st.write(f"**Fix Versions:** {row['fix_versions']}")
                st.write(row["description"])


# AI Report Tab
with tab_ai:
    st.subheader("AI-Generated Security Report")

    if ai_report:
        st.text_area("Gemini Security Report", ai_report, height=550)
    else:
        st.warning("No Gemini report found.")
        st.caption("Run `python ai_report.py` first to generate `reports/gemini_security_report.txt`.")


# Upload and Scan Tab
with tab_upload:
    st.subheader("Upload Python File and Run Bandit Scan")

    st.markdown(
        """
        Upload a `.py` file to scan it directly from the dashboard.  
        This scan runs Bandit against the uploaded file and displays the findings immediately.
        """
    )

    uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

    if uploaded_file is not None:
        st.info(f"Uploaded file: {uploaded_file.name}")

        if st.button("Run Security Scan on Uploaded File"):
            with st.spinner("Running Bandit scan..."):
                uploaded_df, raw_output = run_bandit_on_uploaded_file(uploaded_file)

            if uploaded_df.empty:
                st.success("No vulnerabilities found in the uploaded file.")
                if raw_output.strip():
                    with st.expander("Raw scanner output"):
                        st.code(raw_output)
            else:
                upload_severity = count_bandit_severity(uploaded_df)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Uploaded File Issues", len(uploaded_df))
                c2.metric("High", upload_severity["HIGH"])
                c3.metric("Medium", upload_severity["MEDIUM"])
                c4.metric("Low", upload_severity["LOW"])

                upload_chart_df = pd.DataFrame(
                    {
                        "Severity": ["High", "Medium", "Low"],
                        "Count": [
                            upload_severity["HIGH"],
                            upload_severity["MEDIUM"],
                            upload_severity["LOW"],
                        ],
                    }
                )

                fig = px.bar(
                    upload_chart_df,
                    x="Severity",
                    y="Count",
                    text="Count",
                    title="Uploaded File Vulnerabilities by Severity",
                )
                fig.update_layout(yaxis_title="Number of Findings", xaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(uploaded_df, use_container_width=True)

                st.markdown("### Uploaded File Finding Details")

                for _, row in uploaded_df.iterrows():
                    with st.expander(f"{row['severity']} — {row['issue']}"):
                        st.write(f"**Confidence:** {row['confidence']}")
                        st.write(f"**Test ID:** {row['test_id']}")
                        st.write(f"**File:** {row['file']}")
                        st.write(f"**Line:** {row['line']}")

                if raw_output.strip():
                    with st.expander("Raw scanner output"):
                        st.code(raw_output)
