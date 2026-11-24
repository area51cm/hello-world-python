"""A tiny AI-powered hello-world agent.

Usage:
    export OPENAI_API_KEY="your-api-key"
    python hello_agent.py

The script uses Python's standard library; no extra packages are required.
"""

import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("Please set the OPENAI_API_KEY environment variable first.")

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly AI agent. Greet the user and introduce yourself in one short sentence.",
            },
            {"role": "user", "content": "Hello, world!"},
        ],
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        print(result["choices"][0]["message"]["content"].strip())
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        sys.exit(f"The AI API returned HTTP {error.code}: {details}")
    except urllib.error.URLError as error:
        sys.exit(f"Could not reach the AI API: {error.reason}")


if __name__ == "__main__":
    main()
