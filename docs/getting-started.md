# Getting Started with 4D-ARE

This guide will help you get started with 4D-ARE in under 5 minutes.

## Installation

```bash
pip install four-d-are
```

## Prerequisites

You'll need an OpenAI API key (or compatible API):

```bash
# Create a .env file
cp .env.example .env

# Edit .env and add your API key
OPENAI_API_KEY=sk-your-key-here
```

## Quick Start

### Using Python API

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
# Run the demo (uses built-in sample data)
four-d-are demo

# Analyze with your own data
four-d-are analyze "Why is retention declining?" --data ./my_data.json

# Initialize a new project
four-d-are init
```

## Data Format

Your data should be organized into 4 dimensions:

```json
{
  "results": {
    "retention_rate": 0.56,
    "target_retention": 0.80
  },
  "process": {
    "visit_frequency": 2.1,
    "cross_sell_rate": 0.28
  },
  "support": {
    "staffing_ratio": 0.68,
    "training_completion": 0.82
  },
  "longterm": {
    "market_trend": "declining",
    "competitor_entries": 3
  }
}
```

## What You Get

Instead of a flat metric dump:

```
Retention rate: 56%
Visit frequency: 2.1
Cross-sell rate: 28%
...
```

You get a **causal attribution chain**:

```
【结果现状】Retention dropped to 56% (target: 80%)
    ↑ caused by
【流程归因】Visit frequency declined 23%, cross-sell rate low
    ↑ constrained by
【支撑背景】Staffing ratio at 68%, understaffed
    ↑ driven by
【环境背景】Market downturn, 3 new competitors entered

【综合建议】
- Increase visit frequency for high-value customers
- Review staffing allocation with management
```

## Next Steps

- [Core Concepts](concepts.md) - Understand the 4D framework
- [Domain Customization](customization.md) - Adapt to your domain
- [MCP Integration](mcp-integration.md) - Connect to real data sources
