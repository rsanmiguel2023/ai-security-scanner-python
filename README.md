# AI Security Scanner for Python (Gemini-Powered)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Security](https://img.shields.io/badge/Security-Static%20Analysis-blueviolet)
![AI](https://img.shields.io/badge/AI-Gemini%20API-lightgrey)

An AI-assisted security analysis tool that scans Python code for vulnerabilities and generates a professional cybersecurity report using Google’s Gemini API.

---

## Overview

This project combines static code analysis, dependency vulnerability scanning, and AI-generated reporting into a single workflow.

It simulates a real-world cybersecurity pipeline where:

* Code is scanned for security issues
* Vulnerabilities are identified
* AI translates findings into a clear, business-ready report

---

## Key Features

* Static Code Analysis using Bandit
* Dependency Vulnerability Scanning using pip-audit
* AI Security Report Generation using Gemini API
* Clean terminal output using Rich
* Automated report generation in the `/reports` folder
* Secure API key handling using `.env`

---

## Project Structure

```text
ai-security-scanner-python/
│
├── scanner.py
├── ai_report.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── samples/
│   └── vulnerable_app.py
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

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Get your API key from:
https://aistudio.google.com/app/apikey

---

## How to Run

### Step 1: Run Security Scan

```bash
python scanner.py
```

When prompted:

```
Enter folder or file to scan:
```

Type:

```
samples
```

This generates:

```
reports/scan_summary.json
```

---

### Step 2: Generate AI Security Report

```bash
python ai_report.py
```

Output:

```
reports/gemini_security_report.txt
```

---

## Sample Vulnerabilities Detected

The scanner can identify issues such as:

* Hardcoded credentials
* Unsafe `os.system()` usage
* Shell injection risks
* Vulnerable Python dependencies

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

## Security Best Practices

* `.env` file is excluded via `.gitignore`
* API keys are not committed to GitHub
* Reports can be shared without exposing secrets

---

## Technologies Used

* Python
* Bandit
* pip-audit
* Rich
* Google Gemini API (`google-genai`)
* VS Code
* GitHub

---

## Use Cases

* Learning cybersecurity fundamentals
* Demonstrating AI and security integration
* Portfolio project for data, AI, or security roles
* Code auditing and vulnerability awareness

---

## Future Enhancements

* Streamlit dashboard interface
* GitHub Actions automation
* PDF report export
* Multi-language scanning support
* CVSS scoring integration

---

## Author

Roberto Alberto San Miguel
Master of Data Analytics
Toronto, Canada

---

## GitHub Description (Short)

AI-powered Python security scanner using Bandit, pip-audit, and Gemini API to generate automated cybersecurity reports.
