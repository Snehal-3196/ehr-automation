# Playwright example

This repository contains a minimal Playwright Python script that opens
`https://www.google.com` using Chromium.

Setup and run (macOS, bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Install browser binaries used by Playwright
python -m playwright install

# Run the script (opens a visible browser by default)
python login.py
```

To run headless (no browser UI), edit `login.py` and set `open_google(headless=True)` or run with an env flag.
````markdown
# Playwright example

This repository contains a minimal Playwright Python script that opens
`https://www.google.com` using Chromium.

Setup and run (macOS, bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Install browser binaries used by Playwright
python -m playwright install

# Run the script (opens a visible browser by default)
python login.py
```

To run headless (no browser UI), edit `login.py` and set `open_google(headless=True)` or run with an env flag.

Minimal MCP server
------------------

This repo now includes a minimal MCP-like server in `mcp_server.py` (FastAPI).

Run the server locally:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn mcp_server:app --reload
```

Test the endpoint:

```bash
curl -s -X POST "http://127.0.0.1:8000/mcp" -H "Content-Type: application/json" -d '{"input":"hello"}' | jq
```

You should get a JSON response echoing the input.
````


Configuration and usage
-----------------------

Files added:
- `mcp.config.json`: optional JSON config for provider and default model.
- `.env.example`: env template. Copy to `.env` and set `OPENAI_API_KEY` if using OpenAI.
- `mcp_client.py`: example client that posts to the server.
- `tests/test_mcp.py`: pytest tests for the mock provider.

Quick setup (after previous steps):

```bash
# install any new deps
source .venv/bin/activate
python -m pip install -r requirements.txt

# run server
uvicorn mcp_server:app --reload

# run client example
python mcp_client.py

# run tests
pytest -q
```

To use OpenAI as the provider, set `MCP_PROVIDER=openai` and `OPENAI_API_KEY` in `.env` or `mcp.config.json`, then restart the server. The server will attempt to call the OpenAI API (the `openai` package must be installed).
