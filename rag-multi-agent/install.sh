#!/bin/bash
set -e

# python3.12 is required specifically — newer versions (3.13+, and
# especially 3.14) can lack prebuilt wheels for some dependencies here
# (notably tiktoken, which then needs a Rust toolchain to build from
# source and will fail without one).
if ! command -v python3.12 &> /dev/null; then
    echo "Error: python3.12 not found on PATH."
    echo "Install it first, e.g. on macOS: brew install python@3.12"
    exit 1
fi

python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo ""
echo "Setup complete. Next steps:"
echo "  1. Create a .env file with OPENAI_API_KEY and TAVILY_API_KEY"
echo "  2. Run: .venv/bin/python main.py \"your question\""
