import sys
import os

# Ensure project root is on PYTHONPATH so tests can import local modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient

from mcp_server import app


client = TestClient(app)


def test_mcp_echo():
    resp = client.post("/mcp", json={"input": "unit test"})
    assert resp.status_code == 200
    data = resp.json()
    assert "output" in data
    assert data["output"].startswith("Echo:" )
    assert data["model"] == "mock-model"


def test_mcp_missing_input():
    resp = client.post("/mcp", json={})
    # Pydantic validation results in 422 Unprocessable Entity for missing required fields
    assert resp.status_code == 422
