# Domain Customization

4D-ARE can be adapted to any business domain using `DomainTemplate`.

## Using Pre-built Templates

4D-ARE includes templates for common domains:

```python
from four_d_are import AttributionAgent
from four_d_are.prompts import (
    BANKING_TEMPLATE,
    HEALTHCARE_TEMPLATE,
    ECOMMERCE_TEMPLATE,
)

# Banking (default)
agent = AttributionAgent(template=BANKING_TEMPLATE)

# Healthcare
agent = AttributionAgent(template=HEALTHCARE_TEMPLATE)

# E-commerce
agent = AttributionAgent(template=ECOMMERCE_TEMPLATE)
```

## Creating Custom Templates

Define your own 4D structure for any domain:

```python
from four_d_are import AttributionAgent, DomainTemplate

# Manufacturing example
manufacturing = DomainTemplate(
    domain="Manufacturing Operations",

    # D_R: What results do you measure?
    results=[
        "production_yield",
        "defect_rate",
        "on_time_delivery",
        "unit_cost",
    ],

    # D_P: What operational factors drive results?
    process=[
        "cycle_time",
        "equipment_utilization",
        "quality_inspection_rate",
        "rework_rate",
    ],

    # D_S: What resources constrain operations?
    support=[
        "machine_availability",
        "skilled_labor_ratio",
        "raw_material_quality",
        "maintenance_schedule",
    ],

    # D_L: What environmental factors set context?
    longterm=[
        "supply_chain_stability",
        "technology_upgrade_cycle",
        "regulatory_compliance",
        "market_demand_forecast",
    ],

    # Boundaries: What must the agent NEVER do?
    boundaries=[
        "Never recommend equipment purchases over $100K",
        "Never suggest workforce reductions",
        "Use statistical process control language",
    ],
)

agent = AttributionAgent(template=manufacturing)
```

## Template Fields

| Field | Required | Description |
|-------|----------|-------------|
| `domain` | Yes | Domain name (e.g., "Healthcare Operations") |
| `results` | Yes | List of result metrics for D_R |
| `process` | Yes | List of process factors for D_P |
| `support` | Yes | List of support factors for D_S |
| `longterm` | Yes | List of long-term factors for D_L |
| `boundaries` | Yes | List of constraints the agent must never violate |
| `language` | No | Response language (default: "Chinese") |

## Best Practices

### 1. Be Specific with Metrics

Instead of generic names, use domain-specific terminology:

```python
# Good
results=["30_day_readmission_rate", "HCAHPS_score"]

# Avoid
results=["rate1", "score2"]
```

### 2. Match Your Data Structure

Your `DataContext` should align with your template:

```python
template = DomainTemplate(
    results=["yield", "defect_rate"],
    process=["cycle_time", "utilization"],
    ...
)

# Data should use matching keys
data = DataContext(
    results={"yield": 0.87, "defect_rate": 0.04},
    process={"cycle_time": 45, "utilization": 0.72},
    ...
)
```

### 3. Define Clear Boundaries

Boundaries should be:
- Specific and actionable
- Related to organizational authority
- Aligned with compliance requirements

```python
boundaries=[
    # Specific
    "Never recommend medication dosage changes",

    # Authority-related
    "Never suggest staff terminations",

    # Compliance-related
    "Always note data limitations for regulatory metrics",
]
```

### 4. Use Appropriate Language

Match hedging language to your domain's norms:

- Healthcare: "Evidence suggests...", "Clinical data indicates..."
- Finance: "Analysis suggests...", "Trends indicate..."
- Manufacturing: "SPC data shows...", "Process capability indicates..."

## Example Templates

### Healthcare

```python
HEALTHCARE_TEMPLATE = DomainTemplate(
    domain="Healthcare Operations",
    results=["readmission_rate", "patient_satisfaction", "mortality_rate"],
    process=["care_coordination", "treatment_adherence", "follow_up_rate"],
    support=["nurse_patient_ratio", "bed_availability", "equipment_status"],
    longterm=["population_aging", "insurance_changes", "regulatory_updates"],
    boundaries=[
        "Never recommend specific treatment decisions",
        "Never suggest staff terminations",
        "Use clinical evidence language",
    ],
)
```

### E-commerce

```python
ECOMMERCE_TEMPLATE = DomainTemplate(
    domain="E-commerce Operations",
    results=["conversion_rate", "AOV", "customer_LTV", "return_rate"],
    process=["page_load_time", "checkout_completion", "search_relevance"],
    support=["inventory_availability", "CS_capacity", "fulfillment_speed"],
    longterm=["market_trends", "competitor_pricing", "seasonal_patterns"],
    boundaries=[
        "Never recommend specific pricing decisions",
        "Never suggest personnel changes",
        "Use data-driven language with confidence levels",
    ],
)
```
