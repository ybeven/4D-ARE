"""
4D-ARE PostgreSQL MCP Server

Connects to PostgreSQL databases and retrieves data organized by 4D dimensions.
"""

from mcp_servers.postgres_server.server import PostgreSQLDataServer, serve

__all__ = ["PostgreSQLDataServer", "serve"]
