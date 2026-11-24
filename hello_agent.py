"""A tiny AI-powered hello-world agent.

Usage:
    export OPENAI_API_KEY="your-api-key"
    python hello_agent.py
    python hello_agent.py "Tell me a joke" --model gpt-4o-mini
    python hello_agent.py --chat

The script uses Python's standard library; no extra packages are required.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_SYSTEM_PROMPT = (
    "You are a friendly AI agent. Greet the user and introduce yourself in "
    "one short sentence."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A small AI-powered chat agent")
    parser.add_argument("prompt", nargs="?", default="Hello, world!", help="Message to send")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI chat model")
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT, help="System prompt")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds")
    parser.add_argument("--chat", action="store_true", help="Start an interactive conversation")
    parser.add_argument("--json", action="store_true", help="Print the API response as JSON")
    return parser.parse_args()


def request_completion(api_key: str, model: str, messages: list[dict[str, str]], timeout: float) -> dict:
    payload = {"model": model, "messages": messages}
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def print_result(result: dict, as_json: bool) -> str:
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        content = result["choices"][0]["message"]["content"].strip()
        print(content)
    return result["choices"][0]["message"]["content"].strip()


def run_chat(api_key: str, args: argparse.Namespace) -> None:
    messages = [{"role": "system", "content": args.system_prompt}]
    print("Chat started. Enter 'exit' or 'quit' to stop.")

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChat ended.")
            return

        if prompt.lower() in {"exit", "quit"}:
            print("Chat ended.")
            return
        if not prompt:
            continue

        messages.append({"role": "user", "content": prompt})
        result = request_completion(api_key, args.model, messages, args.timeout)
        assistant_message = print_result(result, args.json)
        messages.append({"role": "assistant", "content": assistant_message})


def main() -> None:
    args = parse_args()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("Please set the OPENAI_API_KEY environment variable first.")

    try:
        if args.chat:
            run_chat(api_key, args)
        else:
            messages = [
                {"role": "system", "content": args.system_prompt},
                {"role": "user", "content": args.prompt},
            ]
            result = request_completion(api_key, args.model, messages, args.timeout)
            print_result(result, args.json)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        sys.exit(f"The AI API returned HTTP {error.code}: {details}")
    except urllib.error.URLError as error:
        sys.exit(f"Could not reach the AI API: {error.reason}")
    except (KeyError, IndexError, json.JSONDecodeError) as error:
        sys.exit(f"Unexpected API response: {error}")


if __name__ == "__main__":
    main()
