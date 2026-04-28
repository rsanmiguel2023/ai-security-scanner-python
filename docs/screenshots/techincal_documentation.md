# Technical Documentation — AI Security Scanner

## 1. System Overview

The AI Security Scanner is a Python-based security analysis tool that integrates traditional static analysis tools with generative AI to detect, interpret, and report software vulnerabilities.

The system supports two scanning modes:

1. Traditional Scanner (Bandit + pip-audit + AI report)
2. Pure AI Scanner (Gemini-only analysis)

---

## 2. Architecture

### High-Level Flow

```text
Python Code Input
      │
      ▼
Static Analysis (Bandit)
      │
      ▼
Dependency Scan (pip-audit)
      │
      ▼
Aggregated Results (JSON)
      │
      ▼
Gemini API (AI Processing)
      │
      ▼
Security Report Output
```

### Alternative Flow (Pure AI Scanner)

```text
Python Code Input
      │
      ▼
Gemini API
      │
      ▼
AI Security Analysis Output
```

---

## 3. Components

### 3.1 scanner.py

Responsible for executing:

* Bandit (static code analysis)
* pip-audit (dependency vulnerability scanning)

Outputs:

```text
reports/scan_summary.json
```

Key responsibilities:

* Execute subprocess commands
* Parse JSON output
* Aggregate results

---

### 3.2 ai_report.py

Processes scan results and generates an AI-based security report.

Key steps:

1. Load JSON scan results
2. Construct structured prompt
3. Send prompt to Gemini API
4. Save output to file

Output:

```text
reports/gemini_security_report.txt
```

---

### 3.3 ai_only_scanner.py

Performs direct AI-based code analysis without traditional tools.

Process:

1. Reads raw Python source file
2. Sends full code to Gemini
3. Requests vulnerability analysis

Advantages:

* Detects logic-based vulnerabilities
* Provides natural language explanations
* Suggests secure code fixes

---

### 3.4 samples/

Contains intentionally vulnerable Python files used for testing detection capabilities.

Examples include:

* SQL injection
* Weak hashing (MD5)
* Command injection
* Hardcoded credentials

---

### 3.5 reports/

Stores generated outputs:

* Scan summaries (JSON)
* AI-generated reports (text)

---

## 4. Security Analysis Techniques

### 4.1 Static Analysis (Bandit)

Detects:

* Hardcoded passwords
* Unsafe system calls
* Injection risks
* Insecure libraries

---

### 4.2 Dependency Analysis (pip-audit)

Detects:

* Known vulnerabilities in dependencies
* CVE-based issues

---

### 4.3 AI-Based Analysis (Gemini)

Detects:

* Logical vulnerabilities
* Context-aware risks
* Security misconfigurations

Also provides:

* Human-readable explanations
* Remediation guidance
* Risk prioritization

---

## 5. Prompt Engineering

The AI scanner uses structured prompts to guide analysis:

* Defines role: cybersecurity analyst
* Specifies output format
* Requests vulnerability breakdown
* Requests remediation steps

This ensures consistent and actionable output.

---

## 6. Continuous Integration (CI)

GitHub Actions pipeline:

* Triggered on push and pull request
* Runs Bandit and pip-audit
* Fails build on detected vulnerabilities

Purpose:

* Enforce security checks automatically
* Prevent insecure code from being merged

---

## 7. Data Flow

```text
Input: Python source code
      │
      ▼
Scanner Execution
      │
      ▼
JSON Output (scan_summary.json)
      │
      ▼
AI Processing (Gemini)
      │
      ▼
Final Report (text file)
```

---

## 8. Error Handling

Implemented for:

* Missing API keys
* File read errors
* API connection failures
* JSON parsing issues

---

## 9. Limitations

* Static tools rely on rule-based detection
* AI analysis depends on prompt quality
* No real-time CVSS scoring
* Limited dependency resolution scope

---

## 10. Future Improvements

* Streamlit dashboard interface
* CVSS scoring integration
* PDF report export
* Multi-language support
* Severity-based CI gating

---

## 11. Technology Stack

* Python
* Bandit
* pip-audit
* Rich
* Google Gemini API (`google-genai`)
* GitHub Actions

---

## 12. Design Considerations

* Separation of concerns (scanner vs AI processing)
* Modular architecture
* Secure handling of API keys
* CI-first security enforcement

---

## 13. Summary

This system demonstrates a hybrid DevSecOps approach by combining:

* Traditional security tools
* AI-based vulnerability analysis
* Automated CI enforcement

It provides both technical detection and human-readable security insights.
