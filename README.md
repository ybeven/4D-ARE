# 4D-ARE: Attribution-Driven Agent Requirements Engineering

> Build LLM agents that explain *why*, not just *what*.

[![PyPI version](https://img.shields.io/pypi/v/four-d-are.svg)](https://pypi.org/project/four-d-are/)
[![Python versions](https://img.shields.io/pypi/pyversions/four-d-are.svg)](https://pypi.org/project/four-d-are/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

Your LLM agent has full data access and executes flawlessly. But when asked:

> "Why is our customer retention rate only 56%?"

It returns a list of metrics instead of a causal explanation:

```
Retention rate: 56%
Visit frequency: 2.1
Cross-sell rate: 28%
...
```

**This is the Attribution Gap** - agents can report *what* happened, but struggle to explain *why*.

## The Solution

4D-ARE provides a framework for building agents that trace causal chains through 4 dimensions:

```
Results (What happened)
    ↓
Process (What we did)
    ↓
Support (What resources we had)
    ↓
Long-term (What environment we're in)
```

Instead of a metric dump, you get:

```
Results: Retention dropped to 56% (target: 80%)
    ↑ caused by
Process: Visit frequency declined 23%, cross-sell rate low
    ↑ constrained by
Support: Staffing ratio at 68%, understaffed
    ↑ driven by
Long-term: Market downturn, 3 new competitors entered
```

## Quick Start

### Installation

```bash
pip install four-d-are
```

### Basic Usage

```python
from four_d_are import AttributionAgent, DataContext

# Create agent
agent = AttributionAgent()

# Prepare your data organized by 4D
data = DataContext(
    results={"retention_rate": 0.56, "target": 0.80},
    process={"visit_frequency": 2.1, "cross_sell_rate": 0.28},
    support={"staffing_ratio": 0.68},
    longterm={"market_trend": "declining", "competitor_entries": 3}
)

# Run analysis
response = agent.analyze(
    query="Why is customer retention only 56%?",
    data_context=data
)
print(response)
```

### Using CLI

```bash
# Quick demo
four-d-are demo

# Analyze with your data
four-d-are analyze "Why is retention declining?" --data ./my_data.json

# Initialize a new project
four-d-are init
```

## Key Features

### 4-Dimensional Analysis

Every analysis traces the causal chain through:
- **D_R (Results)**: Observable outcomes - display only
- **D_P (Process)**: Operational factors - interpret + recommend
- **D_S (Support)**: Resource factors - suggest for review
- **D_L (Long-term)**: Environmental factors - context only

### Domain Customization

Adapt 4D-ARE to any domain with custom templates:

```python
from four_d_are import AttributionAgent, DomainTemplate

# Healthcare domain
healthcare = DomainTemplate(
    domain="Healthcare Operations",
    results=["readmission_rate", "patient_satisfaction"],
    process=["care_coordination", "follow_up_rate"],
    support=["nurse_patient_ratio", "bed_availability"],
    longterm=["population_aging", "insurance_changes"],
    boundaries=["Never recommend specific treatments"]
)

agent = AttributionAgent(template=healthcare)
```

Pre-built templates available: `BANKING_TEMPLATE`, `HEALTHCARE_TEMPLATE`, `ECOMMERCE_TEMPLATE`

### MCP Data Integration

Connect to real data sources via MCP (Model Context Protocol):

```bash
# Configure data source
export MCP_SERVER_TYPE=mysql
export MYSQL_HOST=localhost
export MYSQL_DATABASE=analytics

# Run with MCP
four-d-are mcp start --type mysql
four-d-are analyze "Why are sales down?"
```

## How It Works

4D-ARE solves the attribution gap at **design time**, not runtime:

| Approach | When | What |
|----------|------|------|
| ReAct, CoT | Runtime | *How* to reason step-by-step |
| **4D-ARE** | Design time | *What* to reason about |

The framework specifies:
1. **Dimensions**: What categories of factors to consider
2. **Authority Levels**: What actions the agent can recommend
3. **Boundaries**: What the agent must NOT do

## Configuration

Create a `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_AGENT=gpt-4o

# MCP Configuration
MCP_SERVER_TYPE=demo  # demo | mysql | postgres | excel
```

## Documentation

- [Getting Started](docs/getting-started.md)
- [Core Concepts](docs/concepts.md)
- [Domain Customization](docs/customization.md)
- [MCP Integration](docs/mcp-integration.md)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
