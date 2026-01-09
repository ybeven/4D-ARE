"""
4D-ARE MySQL MCP Server

Connects to MySQL databases and retrieves data organized by 4D dimensions.

Usage:
    # Configure in .env
    MCP_SERVER_TYPE=mysql
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=secret
    MYSQL_DATABASE=analytics

    # Start server
    four-d-are mcp start --type mysql
"""

import os
from typing import Any

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    MySQLError = Exception


class MySQLDataServer:
    """
    MySQL MCP Server for 4D-ARE.

    Retrieves metrics from MySQL database organized by 4D dimensions.
    Requires dimension-to-table mapping configuration.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
        dimension_config: dict[str, dict] | None = None,
    ):
        """
        Initialize MySQL connection.

        Args:
            host: MySQL host (default: from MYSQL_HOST env var)
            port: MySQL port (default: from MYSQL_PORT env var or 3306)
            user: MySQL user (default: from MYSQL_USER env var)
            password: MySQL password (default: from MYSQL_PASSWORD env var)
            database: MySQL database (default: from MYSQL_DATABASE env var)
            dimension_config: Mapping of dimensions to tables/queries
        """
        if not MYSQL_AVAILABLE:
            raise ImportError(
                "mysql-connector-python is required for MySQL support. "
                "Install with: pip install mysql-connector-python"
            )

        self.host = host or os.getenv("MYSQL_HOST", "localhost")
        self.port = port or int(os.getenv("MYSQL_PORT", "3306"))
        self.user = user or os.getenv("MYSQL_USER", "root")
        self.password = password or os.getenv("MYSQL_PASSWORD", "")
        self.database = database or os.getenv("MYSQL_DATABASE", "")

        self.dimension_config = dimension_config or self._default_dimension_config()
        self._connection = None

    def _default_dimension_config(self) -> dict[str, dict]:
        """Default dimension-to-table mapping (customize for your schema)."""
        return {
            "results": {
                "table": "results_metrics",
                "columns": ["metric_name", "metric_value"],
            },
            "process": {
                "table": "process_metrics",
                "columns": ["metric_name", "metric_value"],
            },
            "support": {
                "table": "support_metrics",
                "columns": ["metric_name", "metric_value"],
            },
            "longterm": {
                "table": "longterm_metrics",
                "columns": ["metric_name", "metric_value"],
            },
        }

    def connect(self) -> None:
        """Establish database connection."""
        try:
            self._connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except MySQLError as e:
            raise ConnectionError(f"Failed to connect to MySQL: {e}")

    def disconnect(self) -> None:
        """Close database connection."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None

    def _ensure_connected(self) -> None:
        """Ensure database connection is active."""
        if not self._connection or not self._connection.is_connected():
            self.connect()

    def _query_dimension(self, dimension: str) -> dict[str, Any]:
        """Query metrics for a specific dimension."""
        self._ensure_connected()

        config = self.dimension_config.get(dimension)
        if not config:
            return {}

        # Support custom query or table-based query
        if "query" in config:
            query = config["query"]
        else:
            table = config["table"]
            columns = config["columns"]
            query = f"SELECT {', '.join(columns)} FROM {table}"

        cursor = self._connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Convert rows to dict format
            result = {}
            for row in rows:
                if "metric_name" in row and "metric_value" in row:
                    result[row["metric_name"]] = row["metric_value"]
                else:
                    # Use first column as key, second as value
                    cols = list(row.keys())
                    if len(cols) >= 2:
                        result[row[cols[0]]] = row[cols[1]]
                    else:
                        result.update(row)
            return result
        finally:
            cursor.close()

    def get_results_metrics(self) -> dict[str, Any]:
        """Get Results dimension metrics (D_R)."""
        return self._query_dimension("results")

    def get_process_metrics(self) -> dict[str, Any]:
        """Get Process dimension metrics (D_P)."""
        return self._query_dimension("process")

    def get_support_metrics(self) -> dict[str, Any]:
        """Get Support dimension metrics (D_S)."""
        return self._query_dimension("support")

    def get_longterm_metrics(self) -> dict[str, Any]:
        """Get Long-term dimension metrics (D_L)."""
        return self._query_dimension("longterm")

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all metrics organized by dimension."""
        return {
            "results": self.get_results_metrics(),
            "process": self.get_process_metrics(),
            "support": self.get_support_metrics(),
            "longterm": self.get_longterm_metrics(),
        }

    def query_custom(self, query: str) -> list[dict]:
        """
        Execute a custom SQL query.

        Args:
            query: SQL query string

        Returns:
            List of result rows as dictionaries
        """
        self._ensure_connected()

        cursor = self._connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


def serve(host: str = "localhost", port: int = 8001) -> None:
    """
    Start the MySQL MCP server.

    Note: Full MCP implementation requires the mcp package.
    """
    print(f"Starting MySQL MCP Server on {host}:{port}")
    print("\nRequired environment variables:")
    print("  MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE")
    print("\nFor now, use the MySQLDataServer class directly:")
    print("\n  from mcp_servers.mysql_server import MySQLDataServer")
    print("  with MySQLDataServer() as server:")
    print("      print(server.get_all_metrics())")


if __name__ == "__main__":
    serve()
