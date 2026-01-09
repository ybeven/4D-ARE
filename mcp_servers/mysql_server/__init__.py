"""
4D-ARE MySQL MCP Server

Connects to MySQL databases and retrieves data organized by 4D dimensions.
"""

from mcp_servers.mysql_server.server import MySQLDataServer, serve

__all__ = ["MySQLDataServer", "serve"]
