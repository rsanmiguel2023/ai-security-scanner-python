import os
import sys
from dotenv import load_dotenv
import google.genai as genai


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

security_prompt = """
You are a security expert. Analyze this code for vulnerabilities.

For each issue, provide:
1. Vulnerability type
2. Why it is vulnerable (1 sentence)
3. Impact (1 sentence)
4. Secure code fix

Be concise.

Code:
{code}
"""

# File path from command line: python scanner.py <file_path>
if len(sys.argv) < 2:
    print("Usage: python scanner.py <file_path>")
    sys.exit(1)

code_path = sys.argv[1]
with open(code_path, "r") as f:
    code = f.read()

prompt = security_prompt.format(code=code)

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )
    print(response.text)
except Exception as e:
    print(f"❌ Connection failed: {e}")
