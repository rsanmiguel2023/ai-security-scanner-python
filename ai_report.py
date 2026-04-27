import json
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

REPORTS_DIR = Path("reports")
SCAN_FILE = REPORTS_DIR / "scan_summary.json"
OUTPUT_FILE = REPORTS_DIR / "gemini_security_report.txt"


def load_scan_results():
    if not SCAN_FILE.exists():
        raise FileNotFoundError("scan_summary.json not found. Run scanner.py first.")

    with open(SCAN_FILE, "r") as file:
        return json.load(file)


def generate_report(scan_results):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

    from google import genai

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a cybersecurity analyst.

Create a clear security report based on the following Python scan results.

Use this structure:
1. Executive Summary
2. Key Security Findings
3. Risk Level
4. Business Impact
5. Recommended Fixes
6. Priority Action Plan
7. GitHub Portfolio Summary

Scan Results:
{json.dumps(scan_results, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def main():
    scan_results = load_scan_results()
    report = generate_report(scan_results)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Gemini security report created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()