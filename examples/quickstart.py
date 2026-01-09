#!/usr/bin/env python3
"""
4D-ARE Quickstart Example

This example demonstrates the basic usage of 4D-ARE for attribution analysis.
Run with: python examples/quickstart.py
"""

from four_d_are import AttributionAgent, DataContext

def main():
    # Create the Attribution Agent
    agent = AttributionAgent()

    # Prepare sample data organized by 4 dimensions
    data = DataContext(
        results={
            "retention_rate": 0.56,
            "target_retention": 0.80,
            "aum_growth": 0.02,
            "target_aum_growth": 0.08,
        },
        process={
            "visit_frequency": 2.1,
            "cross_sell_rate": 0.28,
            "quality_score": 72,
        },
        support={
            "staffing_ratio": 0.68,
            "marketing_coverage": 0.45,
            "training_completion": 0.82,
        },
        longterm={
            "market_trend": "declining",
            "competitor_entries": 3,
            "regulatory_changes": "tightening",
        },
    )

    # Run the analysis
    print("=" * 60)
    print("4D-ARE Attribution Analysis")
    print("=" * 60)
    print()

    query = "Why is customer retention only 56%?"
    print(f"Query: {query}")
    print("-" * 60)

    response = agent.analyze(query=query, data_context=data)
    print(response)


if __name__ == "__main__":
    main()
