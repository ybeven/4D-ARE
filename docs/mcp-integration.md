# MCP Integration

4D-ARE uses the Model Context Protocol (MCP) to connect to real data sources.

## Overview

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Data Source │ ──→ │   MCP Server    │ ──→ │   4D-ARE     │
│ MySQL/PG/... │     │ (Standardized)  │     │    Agent     │
└──────────────┘     └─────────────────┘     └──────────────┘
                              │
                              ↓
                    Data organized by 4D:
                    - Results metrics
                    - Process metrics
                    - Support metrics
                    - Long-term metrics
```

## Available MCP Servers

| Server | Data Source | Status |
|--------|-------------|--------|
| `demo_server` | Static JSON | Available |
| `mysql_server` | MySQL | Available |
| `postgres_server` | PostgreSQL | Available |
| `excel_server` | Excel/CSV | Available |

## Quick Start

### 1. Using Demo Server (No Setup)

```python
from mcp_servers.demo_server import DemoDataServer

server = DemoDataServer("banking_retention")

# Get metrics by dimension
results = server.get_results_metrics()
process = server.get_process_metrics()
support = server.get_support_metrics()
longterm = server.get_longterm_metrics()
```

### 2. Using MySQL Server

Configure in `.env`:

```bash
MCP_SERVER_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=secret
MYSQL_DATABASE=analytics
```

Run with CLI:

```bash
four-d-are mcp start --type mysql
four-d-are analyze "Why is retention declining?"
```

### 3. Using PostgreSQL Server

```bash
MCP_SERVER_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_DATABASE=analytics
```

### 4. Using Excel/CSV

```bash
MCP_SERVER_TYPE=excel
EXCEL_FILE_PATH=./data/metrics.xlsx
```

## MCP Server Interface

All 4D-ARE MCP servers implement these tools:

```python
class MCPServer:
    def get_results_metrics(self) -> dict:
        """Get Results dimension metrics (D_R)."""
        ...

    def get_process_metrics(self) -> dict:
        """Get Process dimension metrics (D_P)."""
        ...

    def get_support_metrics(self) -> dict:
        """Get Support dimension metrics (D_S)."""
        ...

    def get_longterm_metrics(self) -> dict:
        """Get Long-term dimension metrics (D_L)."""
        ...

    def query_custom(self, query: str) -> dict:
        """Execute custom query (SQL or filter)."""
        ...
```

## Creating a Custom MCP Server

### 1. Create Server Directory

```
mcp_servers/
  your_server/
    __init__.py
    server.py
    pyproject.toml
```

### 2. Implement the Interface

```python
# mcp_servers/your_server/server.py
from mcp.server import Server
from mcp.types import Tool

class YourDataServer:
    def __init__(self, connection_string: str):
        self.conn = self._connect(connection_string)

    def get_results_metrics(self) -> dict:
        # Query your data source for results metrics
        return {
            "retention_rate": self._query("SELECT retention FROM metrics"),
            "target": 0.80,
        }

    def get_process_metrics(self) -> dict:
        return {
            "visit_frequency": self._query("SELECT avg(visits) FROM activity"),
        }

    # ... implement other methods
```

### 3. Register Your Server

In `.env`:

```bash
MCP_SERVER_TYPE=your_server
YOUR_SERVER_CONNECTION=your_connection_string
```

## Data Mapping

### SQL to 4D Mapping

You need to configure how your database tables map to 4D dimensions:

```python
dimension_mapping = {
    "results": {
        "table": "kpi_metrics",
        "columns": ["retention_rate", "aum_growth", "satisfaction"]
    },
    "process": {
        "table": "operational_metrics",
        "columns": ["visit_count", "cross_sell", "quality_score"]
    },
    "support": {
        "table": "resource_metrics",
        "columns": ["staff_ratio", "training_pct", "system_uptime"]
    },
    "longterm": {
        "table": "market_data",
        "columns": ["trend", "competitors", "regulations"]
    }
}
```

### Excel Column Mapping

For Excel files, specify column-to-dimension mapping:

```python
excel_mapping = {
    "results": ["A", "B", "C"],      # Columns A-C are results
    "process": ["D", "E", "F"],      # Columns D-F are process
    "support": ["G", "H"],           # Columns G-H are support
    "longterm": ["I", "J", "K"],     # Columns I-K are long-term
}
```

## Best Practices

1. **Cache Expensive Queries**: MCP servers should cache data to avoid repeated database hits.

2. **Handle Missing Data**: Return explicit `None` or default values for missing metrics.

3. **Include Metadata**: Add timestamps, data freshness indicators.

4. **Respect Rate Limits**: Implement backoff for external APIs.

5. **Secure Credentials**: Never hardcode passwords; use environment variables.
