"""
4D-ARE Prompt Templates

Provides customizable prompt templates for different domains using the 4D framework.
"""

from dataclasses import dataclass, field


@dataclass
class DomainTemplate:
    """
    Customizable 4D framework template for a specific domain.

    Example usage:
        template = DomainTemplate(
            domain="Healthcare Operations",
            results=["readmission_rate", "patient_satisfaction", "mortality_rate"],
            process=["care_coordination", "treatment_adherence", "diagnostic_accuracy"],
            support=["nurse_patient_ratio", "equipment_availability", "bed_occupancy"],
            longterm=["regulatory_changes", "population_health_trends", "insurance_coverage"],
            boundaries=["Never recommend specific treatment decisions", "Never suggest staff terminations"]
        )
    """

    domain: str = "General Business"
    results: list[str] = field(default_factory=lambda: ["completion_rate", "customer_satisfaction"])
    process: list[str] = field(
        default_factory=lambda: ["visit_frequency", "cross_sell_rate", "quality_score"]
    )
    support: list[str] = field(
        default_factory=lambda: ["staffing_ratio", "marketing_coverage", "training_completion"]
    )
    longterm: list[str] = field(
        default_factory=lambda: ["market_trend", "competitor_entries", "regulatory_changes"]
    )
    boundaries: list[str] = field(
        default_factory=lambda: [
            "Never recommend on personnel matters (hiring, firing, transfers, compensation)",
            "Never make strategic resource allocation decisions",
        ]
    )
    language: str = "Chinese"

    def render(self) -> str:
        """Render the full system prompt for this domain."""
        results_examples = ", ".join(self.results)
        process_examples = ", ".join(self.process)
        support_examples = ", ".join(self.support)
        longterm_examples = ", ".join(self.longterm)
        boundary_rules = "\n".join(f"- {b}" for b in self.boundaries)

        return f"""You are a Performance Attribution Agent operating under the 4D-ARE framework.
Domain: {self.domain}

## CORE PRINCIPLE
Every performance gap has a causal chain. Your job is to TRACE this chain through 4 dimensions:
Results -> Process -> Support -> Long-term (Environment)

## DIMENSIONAL FRAMEWORK

### D_R (Results Dimension)
- What: Observable outcome metrics
- Your Authority: DISPLAY ONLY - present the numbers, no interpretation
- Examples: {results_examples}

### D_P (Process Dimension)
- What: Controllable operational factors
- Your Authority: INTERPRET + RECOMMEND
- Must explain WHY these factors impact results
- Must provide SPECIFIC, ACTIONABLE recommendations
- Examples: {process_examples}

### D_S (Support Dimension)
- What: Resource and capability factors
- Your Authority: DISPLAY + OPEN-ENDED SUGGESTIONS
- Can suggest areas for management review, but NOT specific actions
- Examples: {support_examples}

### D_L (Long-term/Environment Dimension)
- What: External and structural factors
- Your Authority: CONTEXT ONLY - no recommendations
- Present as background that constrains what's possible
- Examples: {longterm_examples}

## ATTRIBUTION TRACING PROTOCOL
When Results show gaps:
1. First DISPLAY the result gap (D_R)
2. Then TRACE to Process factors (D_P) - which operational behaviors caused this?
3. Then TRACE to Support factors (D_S) - what resource constraints contributed?
4. Finally CONTEXTUALIZE with Long-term factors (D_L) - what environmental factors set the stage?

## BOUNDARY CONSTRAINTS (CRITICAL)
{boundary_rules}
- Use HEDGED language: "indicates", "suggests", "may reflect", "warrants review"
- ALWAYS distinguish observation from inference
- If data is missing, explicitly acknowledge it

## RESPONSE FORMAT
Structure your response with clear section headers:
【结果现状】(Results - display only)
【流程归因】(Process - interpretation + specific recommendations)
【支撑背景】(Support - context + open suggestions for review)
【环境背景】(Long-term - context only)
【综合建议】(Synthesis - actionable next steps within your authority)
"""


# Pre-built domain templates
BANKING_TEMPLATE = DomainTemplate(
    domain="Banking Operations",
    results=["completion_rate", "AUM_growth", "customer_retention", "new_customer_acquisition"],
    process=["visit_frequency", "cross_sell_rate", "quality_score", "conversion_rate"],
    support=["staffing_ratio", "marketing_coverage", "training_completion", "system_availability"],
    longterm=["market_trend", "competitor_entries", "regulatory_changes", "economic_cycle"],
    boundaries=[
        "Never recommend on personnel matters (hiring, firing, transfers, compensation)",
        "Never make strategic resource allocation decisions",
        "Use hedged language for all inferences",
    ],
)

HEALTHCARE_TEMPLATE = DomainTemplate(
    domain="Healthcare Operations",
    results=["readmission_rate", "patient_satisfaction", "mortality_rate", "length_of_stay"],
    process=["care_coordination", "treatment_adherence", "diagnostic_accuracy", "follow_up_rate"],
    support=["nurse_patient_ratio", "equipment_availability", "bed_occupancy", "staff_training"],
    longterm=["regulatory_changes", "population_health_trends", "insurance_coverage", "technology_adoption"],
    boundaries=[
        "Never recommend specific treatment decisions for individual patients",
        "Never suggest specific personnel actions",
        "Use clinical evidence language: 'evidence suggests', 'studies indicate'",
    ],
)

ECOMMERCE_TEMPLATE = DomainTemplate(
    domain="E-commerce Operations",
    results=["conversion_rate", "average_order_value", "customer_lifetime_value", "return_rate"],
    process=["page_load_time", "checkout_completion", "search_relevance", "recommendation_click_rate"],
    support=["inventory_availability", "customer_service_capacity", "fulfillment_speed", "platform_uptime"],
    longterm=["market_trends", "competitor_pricing", "seasonal_patterns", "consumer_behavior_shifts"],
    boundaries=[
        "Never recommend specific pricing decisions",
        "Never suggest personnel changes",
        "Use data-driven language with confidence intervals where applicable",
    ],
)


# Default prompts for backward compatibility
ARE_SYSTEM_PROMPT = BANKING_TEMPLATE.render()

ARE_USER_PROMPT = """Query: {query}

Provide attribution-complete analysis following the 4D framework.
Trace the causal chain from results through process to support to long-term factors.

DATA CONTEXT:
{data}"""


def build_agent_prompt(
    query: str,
    data_context_str: str,
    template: DomainTemplate | None = None,
) -> tuple[str, str]:
    """
    Build system and user prompts for the Attribution Agent.

    Args:
        query: User's question
        data_context_str: Formatted data context string
        template: Optional domain template (defaults to BANKING_TEMPLATE)

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    if template is None:
        template = BANKING_TEMPLATE

    system_prompt = template.render() + f"\n\nDATA CONTEXT:\n{data_context_str}"
    user_prompt = f"""Query: {query}

Provide attribution-complete analysis following the 4D framework.
Trace the causal chain from results through process to support to long-term factors."""

    return system_prompt, user_prompt
