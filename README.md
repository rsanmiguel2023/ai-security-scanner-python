# AI Security Scanner for Python (Gemini-Powered)

![Build Status](https://img.shields.io/github/actions/workflow/status/YOUR-USERNAME/ai-security-scanner-python/ci.yml?branch=main)
![Coverage](https://img.shields.io/badge/Coverage-Coming%20Soon-lightgrey)
![Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![License](https://img.shields.io/badge/License-MIT-2f2f2f)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![Security](https://img.shields.io/badge/Security-Static%20Analysis-6f42c1)
![AI](https://img.shields.io/badge/AI-Gemini%20API-555555)

---

## Overview

This project implements an AI-assisted security analysis pipeline that scans Python code for vulnerabilities and generates structured cybersecurity reports using the Gemini API.

The workflow integrates:

* Static code analysis
* Dependency vulnerability scanning
* AI-based risk interpretation
* Direct AI code analysis (pure AI scanner)

---

## Architecture

```text
Developer Input (Python Code)
            │
            ▼
   Static Analysis (Bandit)
            │
            ▼
 Dependency Scan (pip-audit)
            │
            ▼
   Aggregated Scan Results (JSON)
            │
            ▼
   Gemini API (AI Processing)
            │
            ▼
 AI Security Report Generation
            │
            ▼
 Reports Output (/reports folder)
            │
            ▼
 GitHub Actions CI Pipeline
```

---

## Key Features

* Static Code Analysis using Bandit
* Dependency Vulnerability Scanning using pip-audit
* AI Security Report Generation using Gemini API
* Pure AI Code Scanner (Gemini-only analysis)
* Automated CI security scanning via GitHub Actions
* Structured reporting saved in `/reports`
* Secure API key management using `.env`

---

## Continuous Integration (CI)

A GitHub Actions pipeline runs on every push and pull request.

The pipeline:

* Executes Bandit for static analysis
* Executes pip-audit for dependency vulnerabilities
* Fails the build when vulnerabilities are detected

Note:
The sample code intentionally contains insecure patterns to demonstrate detection. CI failures indicate the scanner is working correctly.

---

## Project Structure

```text
ai-security-scanner-python/
│
├── scanner.py
├── ai_report.py
├── ai_only_scanner.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── samples/
│   └── vulnerable_app.py
│
├── docs/
│   └── screenshots/
│
└── reports/
    ├── scan_summary.json
    └── gemini_security_report.txt
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-security-scanner-python.git
cd ai-security-scanner-python
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Gemini API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## How to Run

### Option 1 — Full Security Pipeline

Runs Bandit + pip-audit + AI reporting:

```bash
python scanner.py
```

Then:

```bash
python ai_report.py
```

---

### Option 2 — Pure AI Scanner

Directly analyzes code using Gemini (no Bandit/pip-audit):

```bash
python ai_only_scanner.py samples/vulnerable_app.py
```

---

## Pure AI Scanner

The pure AI scanner sends raw Python code directly to Gemini for analysis.

It provides:

* Vulnerability identification
* Explanation of risks
* Business impact
* Secure code fixes

This approach is useful for:

* Understanding vulnerabilities in plain language
* Identifying logic-level issues
* Generating remediation guidance

---

## Screenshots

### Static Code Analysis Output

![Bandit Scan](docs/screenshots/bandit_scan.png)

### Dependency Scan Output

![pip-audit](docs/screenshots/pip_audit.png)

### AI Security Report

![Gemini Report](docs/screenshots/gemini_report.png)

### CI Pipeline Execution

![GitHub Actions](docs/screenshots/github_actions.png)

---

## Sample Vulnerabilities Detected

* SQL injection
* Weak password hashing (MD5)
* Command injection
* Hardcoded credentials
* Exposed API secrets

---

## AI Report Output

The generated report includes:

* Executive Summary
* Key Security Findings
* Risk Level
* Business Impact
* Recommended Fixes
* Priority Action Plan

---

## Security Notes

* `.env` is excluded from version control
* API keys are not committed
* CI enforces security checks automatically

---

## Technologies Used

* Python
* Bandit
* pip-audit
* Rich
* Google Gemini API (`google-genai`)
* GitHub Actions

---

## Use Cases

* Cybersecurity portfolio project
* DevSecOps workflow demonstration
* AI-assisted vulnerability analysis
* Secure coding education

---

## Future Enhancements

* Streamlit dashboard
* CI artifact reports
* Coverage integration
* Severity-based CI controls

---

## Author

Roberto Alberto San Miguel
Master of Data Analytics
Toronto, Canada

---

## GitHub Description

AI-powered Python security scanner with CI pipeline, static analysis, dependency auditing, and Gemini-based reporting.
