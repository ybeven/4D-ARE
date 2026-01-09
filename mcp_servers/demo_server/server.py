"""
4D-ARE Demo MCP Server

Provides static demo data organized by 4D dimensions.
This server is useful for:
- Quick demos without database setup
- Testing and development
- Understanding the 4D data structure

Usage:
    # As a standalone server
    python -m mcp_servers.demo_server

    # Or use the CLI
    four-d-are mcp start --type demo
"""

import json
from typing import Any

# Demo data for different scenarios
DEMO_SCENARIOS = {
    "banking_retention": {
        "name": "Banking Customer Retention",
        "description": "Customer retention rate dropped from 80% to 56%",
        "data": {
            "results": {
                "retention_rate": 0.56,
                "target_retention": 0.80,
                "customer_satisfaction": 0.72,
                "nps_score": 32,
            },
            "process": {
                "visit_frequency": 2.1,
                "cross_sell_rate": 0.28,
                "quality_score": 0.82,
                "response_time_hours": 4.5,
                "first_contact_resolution": 0.65,
            },
            "support": {
                "staffing_ratio": 0.68,
                "training_completion": 0.91,
                "system_availability": 0.995,
                "marketing_coverage": 0.45,
            },
            "longterm": {
                "market_trend": "declining",
                "competitor_entries": 3,
                "regulatory_changes": True,
                "economic_outlook": "uncertain",
            },
        },
        "ground_truth": "Market decline -> Staff attrition -> Reduced visit frequency -> Lower retention",
    },
    "banking_aum": {
        "name": "Banking AUM Growth",
        "description": "AUM growth stalled at 2% vs 8% target",
        "data": {
            "results": {
                "aum_growth": 0.02,
                "target_growth": 0.08,
                "new_deposits": 150000000,
                "outflows": 120000000,
            },
            "process": {
                "advisor_meetings": 3.2,
                "product_recommendations": 1.8,
                "follow_up_rate": 0.55,
                "proposal_acceptance": 0.32,
            },
            "support": {
                "advisor_capacity": 0.92,
                "product_availability": 0.85,
                "digital_tools_adoption": 0.60,
            },
            "longterm": {
                "interest_rate_trend": "rising",
                "market_volatility": "high",
                "competitor_rates": "aggressive",
            },
        },
        "ground_truth": "Market volatility -> Client hesitancy -> Low proposal acceptance -> Stalled growth",
    },
    "healthcare_readmission": {
        "name": "Healthcare Readmission Rate",
        "description": "30-day readmission rate at 18% vs 12% target",
        "data": {
            "results": {
                "readmission_rate_30d": 0.18,
                "target_rate": 0.12,
                "patient_satisfaction": 0.78,
                "mortality_rate": 0.02,
            },
            "process": {
                "discharge_planning_score": 0.72,
                "medication_reconciliation": 0.85,
                "follow_up_appointment_rate": 0.60,
                "patient_education_completion": 0.68,
            },
            "support": {
                "nurse_patient_ratio": 1.0/5.2,
                "care_coordinator_coverage": 0.45,
                "bed_availability": 0.88,
            },
            "longterm": {
                "population_aging": "accelerating",
                "chronic_disease_prevalence": "increasing",
                "insurance_coverage_changes": True,
            },
        },
        "ground_truth": "Aging population -> Higher acuity -> Insufficient follow-up -> Higher readmissions",
    },
}


class DemoDataServer:
    """
    Demo MCP Server that provides static 4D data.

    This class implements the MCP server interface for 4D-ARE,
    providing tools to retrieve data organized by dimension.
    """

    def __init__(self, scenario: str = "banking_retention"):
        """
        Initialize the demo server with a specific scenario.

        Args:
            scenario: One of the predefined scenarios
        """
        if scenario not in DEMO_SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Available: {list(DEMO_SCENARIOS.keys())}")
        self.scenario = scenario
        self.data = DEMO_SCENARIOS[scenario]["data"]

    def get_results_metrics(self) -> dict[str, Any]:
        """Get Results dimension metrics (D_R)."""
        return self.data["results"]

    def get_process_metrics(self) -> dict[str, Any]:
        """Get Process dimension metrics (D_P)."""
        return self.data["process"]

    def get_support_metrics(self) -> dict[str, Any]:
        """Get Support dimension metrics (D_S)."""
        return self.data["support"]

    def get_longterm_metrics(self) -> dict[str, Any]:
        """Get Long-term dimension metrics (D_L)."""
        return self.data["longterm"]

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all metrics organized by dimension."""
        return self.data

    def list_scenarios(self) -> list[dict[str, str]]:
        """List all available demo scenarios."""
        return [
            {"id": k, "name": v["name"], "description": v["description"]}
            for k, v in DEMO_SCENARIOS.items()
        ]

    def set_scenario(self, scenario: str) -> None:
        """Switch to a different demo scenario."""
        if scenario not in DEMO_SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        self.scenario = scenario
        self.data = DEMO_SCENARIOS[scenario]["data"]


def serve(host: str = "localhost", port: int = 8000) -> None:
    """
    Start the demo MCP server.

    Note: This is a placeholder. Full MCP implementation requires
    the mcp package and proper server setup.
    """
    print(f"Starting Demo MCP Server on {host}:{port}")
    print("\nAvailable scenarios:")
    for scenario_id, scenario in DEMO_SCENARIOS.items():
        print(f"  - {scenario_id}: {scenario['name']}")
    print("\nMCP server implementation coming soon.")
    print("For now, use the DemoDataServer class directly in Python:")
    print("\n  from mcp_servers.demo_server import DemoDataServer")
    print("  server = DemoDataServer('banking_retention')")
    print("  print(server.get_all_metrics())")


if __name__ == "__main__":
    serve()
