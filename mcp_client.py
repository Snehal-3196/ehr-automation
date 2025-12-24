"""Simple client that calls the local MCP server and prints the response."""

import json
import os
from urllib import request


def call_mcp(server_url: str, text: str):
    data = json.dumps({"input": text}).encode("utf-8")
    req = request.Request(server_url + "/mcp", data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req) as resp:
        return json.load(resp)


if __name__ == "__main__":
    url = os.getenv("MCP_URL", "http://127.0.0.1:8000")
    text = os.getenv("MCP_INPUT", "hello from client")
    res = call_mcp(url, text)
    print(json.dumps(res, indent=2))
