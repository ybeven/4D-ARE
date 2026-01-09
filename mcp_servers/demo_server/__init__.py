"""
4D-ARE Demo MCP Server

A simple MCP server that provides static demo data for testing and demonstration.
"""

from mcp_servers.demo_server.server import serve, DemoDataServer

__all__ = ["serve", "DemoDataServer"]
