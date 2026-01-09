#!/usr/bin/env python3
"""
4D-ARE Custom Domain Example

This example shows how to customize 4D-ARE for different domains
(Healthcare, E-commerce) using DomainTemplate.

Run with: python examples/custom_domain.py
"""

from four_d_are import AttributionAgent, DataContext, DomainTemplate
from four_d_are.prompts import HEALTHCARE_TEMPLATE, ECOMMERCE_TEMPLATE


def healthcare_example():
    """Example: Healthcare domain analysis."""
    print("=" * 60)
    print("Healthcare Domain Example")
    print("=" * 60)

    # Use pre-built healthcare template
    agent = AttributionAgent(template=HEALTHCARE_TEMPLATE)

    data = DataContext(
        results={
            "readmission_rate": 0.18,
            "target_readmission": 0.10,
            "patient_satisfaction": 72,
            "target_satisfaction": 85,
        },
        process={
            "follow_up_rate": 0.65,
            "care_coordination_score": 68,
            "treatment_adherence": 0.72,
        },
        support={
            "nurse_patient_ratio": 0.75,
            "bed_occupancy": 0.92,
            "equipment_availability": 0.88,
        },
        longterm={
            "population_aging": "increasing",
            "insurance_changes": "restrictive",
            "staff_shortage": "regional",
        },
    )

    query = "Why is our 30-day readmission rate at 18% instead of the target 10%?"
    print(f"\nQuery: {query}\n")

    response = agent.analyze(query=query, data_context=data)
    print(response)


def ecommerce_example():
    """Example: E-commerce domain analysis."""
    print("\n" + "=" * 60)
    print("E-commerce Domain Example")
    print("=" * 60)

    # Use pre-built e-commerce template
    agent = AttributionAgent(template=ECOMMERCE_TEMPLATE)

    data = DataContext(
        results={
            "conversion_rate": 0.021,
            "target_conversion": 0.035,
            "average_order_value": 85,
            "return_rate": 0.12,
        },
        process={
            "page_load_time": 3.2,
            "checkout_completion": 0.45,
            "search_relevance": 0.68,
            "recommendation_ctr": 0.08,
        },
        support={
            "inventory_availability": 0.82,
            "customer_service_wait": 12,
            "platform_uptime": 0.995,
        },
        longterm={
            "market_competition": "intensifying",
            "consumer_spending": "cautious",
            "seasonal_factor": "post_holiday_slump",
        },
    )

    query = "Why is our conversion rate only 2.1% vs the 3.5% target?"
    print(f"\nQuery: {query}\n")

    response = agent.analyze(query=query, data_context=data)
    print(response)


def custom_domain_example():
    """Example: Create a fully custom domain template."""
    print("\n" + "=" * 60)
    print("Custom Domain Example: Manufacturing")
    print("=" * 60)

    # Create custom template for manufacturing
    manufacturing_template = DomainTemplate(
        domain="Manufacturing Operations",
        results=[
            "production_yield",
            "defect_rate",
            "on_time_delivery",
            "unit_cost",
        ],
        process=[
            "cycle_time",
            "equipment_utilization",
            "quality_inspection_rate",
            "rework_rate",
        ],
        support=[
            "machine_availability",
            "skilled_labor_ratio",
            "raw_material_quality",
            "maintenance_schedule",
        ],
        longterm=[
            "supply_chain_stability",
            "technology_upgrade_cycle",
            "regulatory_compliance",
            "market_demand_forecast",
        ],
        boundaries=[
            "Never recommend specific equipment purchases over $100K",
            "Never suggest workforce reductions",
            "Use statistical process control language where applicable",
        ],
    )

    agent = AttributionAgent(template=manufacturing_template)

    data = DataContext(
        results={
            "production_yield": 0.87,
            "target_yield": 0.95,
            "defect_rate": 0.042,
            "on_time_delivery": 0.78,
        },
        process={
            "cycle_time_variance": 0.15,
            "equipment_utilization": 0.72,
            "inspection_rate": 0.91,
        },
        support={
            "machine_availability": 0.85,
            "skilled_labor_ratio": 0.62,
            "raw_material_quality_score": 78,
        },
        longterm={
            "supply_chain": "disrupted",
            "technology_age": "5+ years",
            "demand_trend": "increasing",
        },
    )

    query = "Why is our production yield at 87% instead of the 95% target?"
    print(f"\nQuery: {query}\n")

    response = agent.analyze(query=query, data_context=data)
    print(response)


if __name__ == "__main__":
    healthcare_example()
    ecommerce_example()
    custom_domain_example()
