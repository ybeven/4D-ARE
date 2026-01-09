"""
4D-ARE Excel/CSV MCP Server

Reads data from Excel or CSV files organized by 4D dimensions.

Usage:
    # Configure in .env
    MCP_SERVER_TYPE=excel
    EXCEL_FILE_PATH=./data/metrics.xlsx

    # Or for CSV
    EXCEL_FILE_PATH=./data/metrics.csv

    # Start server
    four-d-are mcp start --type excel

File Format Options:

1. Single sheet/file with dimension column:
   | dimension | metric_name      | metric_value |
   |-----------|------------------|--------------|
   | results   | retention_rate   | 0.56         |
   | process   | visit_frequency  | 2.1          |

2. Multiple sheets (Excel only):
   - Sheet "Results" for D_R
   - Sheet "Process" for D_P
   - Sheet "Support" for D_S
   - Sheet "Longterm" for D_L

3. Wide format with dimension prefixes:
   | results_retention | process_visits | support_staff | longterm_trend |
   |-------------------|----------------|---------------|----------------|
   | 0.56              | 2.1            | 0.68          | declining      |
"""

import os
from pathlib import Path
from typing import Any

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None


class ExcelDataServer:
    """
    Excel/CSV MCP Server for 4D-ARE.

    Reads metrics from Excel or CSV files organized by 4D dimensions.
    Supports multiple file formats and layouts.
    """

    def __init__(
        self,
        file_path: str | Path | None = None,
        dimension_config: dict[str, Any] | None = None,
    ):
        """
        Initialize Excel/CSV data server.

        Args:
            file_path: Path to Excel (.xlsx, .xls) or CSV file
            dimension_config: Configuration for mapping file content to dimensions
        """
        if not PANDAS_AVAILABLE:
            raise ImportError(
                "pandas is required for Excel/CSV support. "
                "Install with: pip install pandas openpyxl"
            )

        self.file_path = Path(file_path or os.getenv("EXCEL_FILE_PATH", "data.xlsx"))
        self.dimension_config = dimension_config or self._default_dimension_config()
        self._data_cache: dict[str, Any] | None = None

    def _default_dimension_config(self) -> dict[str, Any]:
        """Default configuration for reading dimensions from file."""
        return {
            "format": "auto",  # auto, sheets, column, wide
            "dimension_column": "dimension",
            "metric_name_column": "metric_name",
            "metric_value_column": "metric_value",
            "sheet_mapping": {
                "results": "Results",
                "process": "Process",
                "support": "Support",
                "longterm": "Longterm",
            },
            "prefix_mapping": {
                "results": "results_",
                "process": "process_",
                "support": "support_",
                "longterm": "longterm_",
            },
        }

    def _load_data(self) -> dict[str, dict[str, Any]]:
        """Load and parse data from file."""
        if self._data_cache is not None:
            return self._data_cache

        if not self.file_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.file_path}")

        file_ext = self.file_path.suffix.lower()

        if file_ext == ".csv":
            df = pd.read_csv(self.file_path)
            self._data_cache = self._parse_single_dataframe(df)
        elif file_ext in (".xlsx", ".xls"):
            self._data_cache = self._parse_excel()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

        return self._data_cache

    def _parse_excel(self) -> dict[str, dict[str, Any]]:
        """Parse Excel file with multiple possible formats."""
        excel_file = pd.ExcelFile(self.file_path)
        sheet_names = excel_file.sheet_names

        config = self.dimension_config
        sheet_mapping = config["sheet_mapping"]

        # Check if using multiple sheets format
        if any(sheet in sheet_names for sheet in sheet_mapping.values()):
            return self._parse_multi_sheet(excel_file, sheet_mapping)
        else:
            # Single sheet - read first sheet
            df = pd.read_excel(excel_file, sheet_name=0)
            return self._parse_single_dataframe(df)

    def _parse_multi_sheet(
        self, excel_file: Any, sheet_mapping: dict[str, str]
    ) -> dict[str, dict[str, Any]]:
        """Parse Excel with separate sheets per dimension."""
        result = {"results": {}, "process": {}, "support": {}, "longterm": {}}

        for dimension, sheet_name in sheet_mapping.items():
            if sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                result[dimension] = self._df_to_dict(df)

        return result

    def _parse_single_dataframe(self, df: Any) -> dict[str, dict[str, Any]]:
        """Parse a single DataFrame with dimension column or wide format."""
        config = self.dimension_config
        dim_col = config["dimension_column"]

        # Check for dimension column
        if dim_col in df.columns:
            return self._parse_long_format(df, config)
        else:
            return self._parse_wide_format(df, config)

    def _parse_long_format(
        self, df: Any, config: dict
    ) -> dict[str, dict[str, Any]]:
        """Parse long format with dimension column."""
        dim_col = config["dimension_column"]
        name_col = config["metric_name_column"]
        value_col = config["metric_value_column"]

        result = {"results": {}, "process": {}, "support": {}, "longterm": {}}

        for dimension in result.keys():
            dim_df = df[df[dim_col].str.lower() == dimension]
            for _, row in dim_df.iterrows():
                metric_name = row[name_col]
                metric_value = row[value_col]
                result[dimension][metric_name] = metric_value

        return result

    def _parse_wide_format(
        self, df: Any, config: dict
    ) -> dict[str, dict[str, Any]]:
        """Parse wide format with dimension prefixes in column names."""
        prefix_mapping = config["prefix_mapping"]
        result = {"results": {}, "process": {}, "support": {}, "longterm": {}}

        # Use first row of data
        if len(df) > 0:
            row = df.iloc[0]

            for col in df.columns:
                col_lower = col.lower()
                for dimension, prefix in prefix_mapping.items():
                    if col_lower.startswith(prefix):
                        metric_name = col[len(prefix):]
                        result[dimension][metric_name] = row[col]
                        break

        return result

    def _df_to_dict(self, df: Any) -> dict[str, Any]:
        """Convert DataFrame to dictionary."""
        config = self.dimension_config
        name_col = config["metric_name_column"]
        value_col = config["metric_value_column"]

        result = {}
        if name_col in df.columns and value_col in df.columns:
            for _, row in df.iterrows():
                result[row[name_col]] = row[value_col]
        elif len(df.columns) >= 2:
            # Use first two columns
            for _, row in df.iterrows():
                result[row.iloc[0]] = row.iloc[1]
        return result

    def reload(self) -> None:
        """Reload data from file."""
        self._data_cache = None
        self._load_data()

    def get_results_metrics(self) -> dict[str, Any]:
        """Get Results dimension metrics (D_R)."""
        data = self._load_data()
        return data.get("results", {})

    def get_process_metrics(self) -> dict[str, Any]:
        """Get Process dimension metrics (D_P)."""
        data = self._load_data()
        return data.get("process", {})

    def get_support_metrics(self) -> dict[str, Any]:
        """Get Support dimension metrics (D_S)."""
        data = self._load_data()
        return data.get("support", {})

    def get_longterm_metrics(self) -> dict[str, Any]:
        """Get Long-term dimension metrics (D_L)."""
        data = self._load_data()
        return data.get("longterm", {})

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all metrics organized by dimension."""
        return self._load_data()

    def query_custom(self, filter_expr: str) -> Any:
        """
        Filter data using pandas query expression.

        Args:
            filter_expr: Pandas query expression (e.g., "value > 0.5")

        Returns:
            Filtered DataFrame as list of dicts
        """
        if not self.file_path.suffix == ".csv":
            df = pd.read_excel(self.file_path)
        else:
            df = pd.read_csv(self.file_path)

        filtered = df.query(filter_expr)
        return filtered.to_dict(orient="records")


def serve(host: str = "localhost", port: int = 8003) -> None:
    """
    Start the Excel/CSV MCP server.

    Note: Full MCP implementation requires the mcp package.
    """
    print(f"Starting Excel/CSV MCP Server on {host}:{port}")
    print("\nRequired environment variables:")
    print("  EXCEL_FILE_PATH - path to Excel or CSV file")
    print("\nSupported formats:")
    print("  - .xlsx, .xls (Excel)")
    print("  - .csv (CSV)")
    print("\nFor now, use the ExcelDataServer class directly:")
    print("\n  from mcp_servers.excel_server import ExcelDataServer")
    print("  server = ExcelDataServer('data/metrics.xlsx')")
    print("  print(server.get_all_metrics())")


if __name__ == "__main__":
    serve()
