"""
4D-ARE PostgreSQL MCP Server

Connects to PostgreSQL databases and retrieves data organized by 4D dimensions.

Usage:
    # Configure in .env
    MCP_SERVER_TYPE=postgres
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=secret
    POSTGRES_DATABASE=analytics

    # Start server
    four-d-are mcp start --type postgres
"""

import os
from typing import Any

try:
    import psycopg2
    from psycopg2 import Error as PostgresError
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    PostgresError = Exception
    RealDictCursor = None


class PostgreSQLDataServer:
    """
    PostgreSQL MCP Server for 4D-ARE.

    Retrieves metrics from PostgreSQL database organized by 4D dimensions.
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
        Initialize PostgreSQL connection.

        Args:
            host: PostgreSQL host (default: from POSTGRES_HOST env var)
            port: PostgreSQL port (default: from POSTGRES_PORT env var or 5432)
            user: PostgreSQL user (default: from POSTGRES_USER env var)
            password: PostgreSQL password (default: from POSTGRES_PASSWORD env var)
            database: PostgreSQL database (default: from POSTGRES_DATABASE env var)
            dimension_config: Mapping of dimensions to tables/queries
        """
        if not POSTGRES_AVAILABLE:
            raise ImportError(
                "psycopg2 is required for PostgreSQL support. "
                "Install with: pip install psycopg2-binary"
            )

        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = port or int(os.getenv("POSTGRES_PORT", "5432"))
        self.user = user or os.getenv("POSTGRES_USER", "postgres")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "")
        self.database = database or os.getenv("POSTGRES_DATABASE", "")

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
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.database,
            )
        except PostgresError as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")

    def disconnect(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def _ensure_connected(self) -> None:
        """Ensure database connection is active."""
        if not self._connection or self._connection.closed:
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

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Convert rows to dict format
            result = {}
            for row in rows:
                row_dict = dict(row)
                if "metric_name" in row_dict and "metric_value" in row_dict:
                    result[row_dict["metric_name"]] = row_dict["metric_value"]
                else:
                    # Use first column as key, second as value
                    cols = list(row_dict.keys())
                    if len(cols) >= 2:
                        result[row_dict[cols[0]]] = row_dict[cols[1]]
                    else:
                        result.update(row_dict)
            return result

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

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


def serve(host: str = "localhost", port: int = 8002) -> None:
    """
    Start the PostgreSQL MCP server.

    Note: Full MCP implementation requires the mcp package.
    """
    print(f"Starting PostgreSQL MCP Server on {host}:{port}")
    print("\nRequired environment variables:")
    print("  POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE")
    print("\nFor now, use the PostgreSQLDataServer class directly:")
    print("\n  from mcp_servers.postgres_server import PostgreSQLDataServer")
    print("  with PostgreSQLDataServer() as server:")
    print("      print(server.get_all_metrics())")


if __name__ == "__main__":
    serve()
