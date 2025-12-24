"""Minimal MCP-like HTTP server using FastAPI.

Features added:
- Reads optional `mcp.config.json` and `.env` for runtime configuration.
- Supports provider `mock` (default) and `openai` if `OPENAI_API_KEY` is set.
- Minimal usage reporting included in responses.
"""

import json
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()  # load .env if present

app = FastAPI(title="Minimal MCP Server")


def load_config(path: str = "mcp.config.json") -> dict:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


CONFIG = load_config()


class MCPRequest(BaseModel):
    input: str
    model: Optional[str] = None


class MCPResponse(BaseModel):
    output: str
    model: str
    usage: dict


def call_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Call OpenAI if API key present; otherwise raise RuntimeError.

    This helper is intentionally minimal. It requires the `openai` package
    and the `OPENAI_API_KEY` environment variable to be set.
    """
    try:
        import openai
    except Exception as e:
        raise RuntimeError("openai package not installed") from e

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    openai.api_key = api_key
    # Use ChatCompletion when available; fall back to simple completion if needed.
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        # Extract text content safely
        if resp and "choices" in resp and len(resp.choices) > 0:
            return resp.choices[0].message.get("content", "")
    except Exception:
        # Try legacy Completion API
        try:
            resp = openai.Completion.create(model=model, prompt=prompt, max_tokens=150)
            if resp and "choices" in resp and len(resp.choices) > 0:
                return resp.choices[0].text
        except Exception as e:
            raise RuntimeError("OpenAI request failed") from e

    raise RuntimeError("OpenAI returned no content")


@app.post("/mcp", response_model=MCPResponse)
def handle_mcp(req: MCPRequest):
    if not req.input:
        raise HTTPException(status_code=400, detail="`input` is required")

    provider = CONFIG.get("provider") or os.getenv("MCP_PROVIDER") or "mock"
    model = req.model or CONFIG.get("model") or os.getenv("MCP_MODEL") or "mock-model"

    if provider == "openai":
        try:
            output_text = call_openai(req.input, model=model)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # default mock provider: deterministic echo
        output_text = f"Echo: {req.input}"

    response = MCPResponse(
        output=output_text,
        model=model,
        usage={
            "prompt_tokens": len(req.input.split()),
            "completion_tokens": len(output_text.split()),
            "provider": provider,
        },
    )
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
