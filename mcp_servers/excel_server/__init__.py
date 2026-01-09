"""
4D-ARE Excel/CSV MCP Server

Reads data from Excel or CSV files organized by 4D dimensions.
"""

from mcp_servers.excel_server.server import ExcelDataServer, serve

__all__ = ["ExcelDataServer", "serve"]
