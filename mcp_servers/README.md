# 4D-ARE MCP Servers

This directory contains MCP (Model Context Protocol) servers for connecting 4D-ARE to various data sources.

## Available Servers

| Server | Data Source | Status | Description |
|--------|-------------|--------|-------------|
| `demo_server` | Static JSON | Available | Quick demos without setup |
| `mysql_server` | MySQL | Planned | Connect to MySQL databases |
| `postgres_server` | PostgreSQL | Planned | Connect to PostgreSQL databases |
| `excel_server` | Excel/CSV | Planned | Read from spreadsheet files |

## Quick Start

### Using Demo Server

```python
from mcp_servers.demo_server import DemoDataServer

# Initialize with a scenario
server = DemoDataServer("banking_retention")

# Get metrics by dimension
results = server.get_results_metrics()
process = server.get_process_metrics()
support = server.get_support_metrics()
longterm = server.get_longterm_metrics()

# Or get all at once
all_data = server.get_all_metrics()
```

### Available Demo Scenarios

- `banking_retention`: Customer retention analysis (56% vs 80% target)
- `banking_aum`: AUM growth analysis (2% vs 8% target)
- `healthcare_readmission`: 30-day readmission rate analysis

## MCP Server Interface

All 4D-ARE MCP servers implement the following tools:

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
        """Execute a custom query (SQL for databases, filter for files)."""
        ...
```

## Creating a Custom MCP Server

To connect your own data source:

1. Create a new directory under `mcp_servers/`
2. Implement the server interface
3. Register in your `.env`:
   ```
   MCP_SERVER_TYPE=custom
   ```

Example structure:
```
mcp_servers/
  your_server/
    __init__.py
    server.py
    pyproject.toml
```

## Configuration

Set the MCP server type in your `.env`:

```bash
# Use demo server (default)
MCP_SERVER_TYPE=demo

# Use MySQL
MCP_SERVER_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=secret
MYSQL_DATABASE=analytics

# Use PostgreSQL
MCP_SERVER_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_DATABASE=analytics

# Use Excel file
MCP_SERVER_TYPE=excel
EXCEL_FILE_PATH=./data/metrics.xlsx
```
