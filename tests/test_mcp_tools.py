"""MCP tools delegate to API - test tool logic with mocked HTTP."""

from unittest.mock import patch

import pytest


def test_resolve_tool_calls_api() -> None:
    try:
        from mcp_server import server
        if not getattr(server, "_MCP_AVAILABLE", False):
            pytest.skip("MCP not installed")
        resolve_business_concept = getattr(server, "resolve_business_concept", None)
        if resolve_business_concept is None:
            pytest.skip("MCP tools not registered")
    except ImportError:
        pytest.skip("mcp_server not importable")
    with patch("mcp_server.server._post") as mock_post:
        mock_post.return_value = {
            "resolution_id": "test-123",
            "status": "complete",
            "execution_plan": {},
            "resolved_concepts": {},
            "confidence_score": 0.9,
        }
        result = resolve_business_concept("APAC revenue last quarter", {"department": "finance"})
        assert result["resolution_id"] == "test-123"
        assert result["status"] == "complete"
        mock_post.assert_called_once()
        call_json = mock_post.call_args[0][1]
        assert call_json["concept"] == "APAC revenue last quarter"
        assert call_json["user_context"]["department"] == "finance"


def test_query_glossary_tool_calls_api() -> None:
    try:
        from mcp_server import server
        if not getattr(server, "_MCP_AVAILABLE", False):
            pytest.skip("MCP not installed")
        query_glossary = getattr(server, "query_glossary", None)
        if query_glossary is None:
            pytest.skip("MCP tools not registered")
    except ImportError:
        pytest.skip("mcp_server not importable")
    with patch("mcp_server.server._get") as mock_get:
        mock_get.return_value = {"terms": [{"id": "ar_g_001", "canonical_name": "revenue"}], "total": 1}
        result = query_glossary("revenue", domain="finance")
        assert result["total"] == 1
        assert result["terms"][0]["canonical_name"] == "revenue"
        mock_get.assert_called_once()
