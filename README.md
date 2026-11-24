# hello-world-python

A simple Python repository for learning the basics with a Hello, World! script.

## Run

Set an OpenAI API key and run the agent:

```bash
export OPENAI_API_KEY="your-api-key"
python hello_agent.py
```

Send a custom prompt:

```bash
python hello_agent.py "Tell me a short Python joke"
```

Start an interactive conversation:

```bash
python hello_agent.py --chat
```

Available options include `--model`, `--system-prompt`, `--timeout`, and `--json`.

```bash
python hello_agent.py "Hello" --model gpt-4o-mini --timeout 15
python hello_agent.py --chat --json
```

The script uses only the Python standard library.
