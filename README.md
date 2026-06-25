```markdown
# PromptBench

CLI utility to benchmark LLMs with different prompts. Compare models, measure latency, count tokens — all in one terminal command.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-6%20passed-brightgreen)

## Overview

PromptBench sends the same query to multiple LLMs simultaneously and shows a comparison table: which model is faster, how many tokens it spent, whether it returned valid JSON, and which tool it chose.

No more manual copy-pasting between ChatGPT, Groq, and DeepSeek to compare results.

## Installation

```bash
git clone https://github.com/GorkaEgor4kas/promptbench
cd promptbench
pip install -e .
```

## Configuration

Add your LLMs to `.env`:

```bash
# .env
LLM_1_NAME=Groq Llama 3 8B
LLM_1_KEY=gsk_xxx
LLM_1_BASE_URL=https://api.groq.com/openai/v1
LLM_1_MODEL=llama-3.1-8b-instant

LLM_2_NAME=DeepSeek V3
LLM_2_KEY=sk-xxx
LLM_2_BASE_URL=https://api.deepseek.com
LLM_2_MODEL=deepseek-chat
```

Add as many as you want — just increment the number.

## Usage

### Basic comparison

```bash
promptbench run "What is Python?"
```

```
Query: What is Python?
Prompt: default
LLMs: Groq Llama 3 8B, DeepSeek V3

┌──────────────────┬────────┬─────────┬────────┬────────────┬──────────┐
│ Model            │ Status │ Latency │ Tokens │ Valid JSON │ Tool     │
├──────────────────┼────────┼─────────┼────────┼────────────┼──────────┤
│ Groq Llama 3 8B  │ OK     │ 0.45s   │ 120    │ YES        │ SEARCH   │
│ DeepSeek V3      │ OK     │ 1.20s   │ 150    │ YES        │ SEARCH   │
└──────────────────┴────────┴─────────┴────────┴────────────┴──────────┘
```

### With flags

```bash
# Use a specific prompt
promptbench run "query" --prompt mnemosys

# Compare only selected models
promptbench run "query" --llm "Groq,DeepSeek"

# Run each model 5 times for consistency
promptbench run "query" --times 5

# Save results to JSON
promptbench run "query" --output results.json

# Clean output for screenshots
promptbench run "query" --clean
```

### List configured models and prompts

```bash
promptbench list
```

## Prompts

Add your own prompts in `promptbench/prompts.py`:

```python
PROMPTS = {
    "default": "You are a helpful assistant. Answer concisely.",
    "mnemosys": "You are Mnemosys, tool agent for Obsidian...",
    "my_prompt": "You are a Python expert. Always show code examples.",
}
```

Then use it: `promptbench run "query" --prompt my_prompt`

## Testing

```bash
pytest tests/ -v
```

## Tech Stack

- Python 3.11+, asyncio, httpx
- Typer + Rich for CLI and tables
- OpenAI-compatible API (Groq, DeepSeek, OpenAI)
- Pydantic for config validation

## Project Structure

```
promptbench/
├── promptbench/
│   ├── main.py          # CLI entry point
│   ├── runner.py        # Async LLM calls
│   ├── config.py        # .env parsing and client creation
│   ├── prompts.py       # System prompts
│   └── display.py       # Rich table output
├── tests/
│   ├── test_config.py
│   ├── test_runner.py
│   └── test_display.py
├── .env.example
└── pyproject.toml
```

## License

MIT
```