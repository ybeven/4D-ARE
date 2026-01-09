# Core Concepts

## The Attribution Gap

Traditional LLM agents can report **what** happened but struggle to explain **why**. When asked "Why is retention low?", they return metrics instead of causal explanations.

4D-ARE bridges this gap by structuring analysis through 4 causal dimensions.

## The 4 Dimensions

```
D_R (Results)     →  What happened (Observable outcomes)
    ↓
D_P (Process)     →  What we did (Operational factors)
    ↓
D_S (Support)     →  What resources we had (Capability factors)
    ↓
D_L (Long-term)   →  What environment we're in (External factors)
```

### D_R: Results Dimension

**What**: Observable outcome metrics that triggered the analysis.

**Authority Level**: Display only - present the numbers without interpretation.

**Examples**:
- Retention rate: 56%
- AUM growth: 2%
- Customer satisfaction: 72

### D_P: Process Dimension

**What**: Controllable operational factors that directly influence results.

**Authority Level**: Interpret + Recommend - explain causes and suggest specific actions.

**Examples**:
- Visit frequency
- Cross-sell rate
- Quality score
- Response time

### D_S: Support Dimension

**What**: Resource and capability factors that constrain process execution.

**Authority Level**: Display + Suggest for review - identify issues but defer decisions to management.

**Examples**:
- Staffing ratio
- Training completion
- System availability
- Marketing coverage

### D_L: Long-term Dimension

**What**: External and structural factors that set the operating environment.

**Authority Level**: Context only - no recommendations, just background.

**Examples**:
- Market trends
- Competitor actions
- Regulatory changes
- Economic cycles

## Authority Levels

4D-ARE implements **graduated authority** - the agent has different levels of autonomy for different dimensions:

| Dimension | Authority | What the Agent Can Do |
|-----------|-----------|----------------------|
| Results | Display | Show metrics, no interpretation |
| Process | Interpret + Recommend | Explain causes, suggest specific actions |
| Support | Suggest | Identify issues, recommend review |
| Long-term | Context | Provide background only |

This design prevents the agent from overstepping into areas requiring human judgment (personnel decisions, strategic allocation, etc.).

## Boundary Constraints

Every domain template includes **boundary rules** that the agent must never cross:

```python
boundaries = [
    "Never recommend on personnel matters",
    "Never make strategic resource decisions",
    "Use hedged language for inferences",
]
```

These constraints are encoded into the system prompt and enforced by the LLM.

## Design-time vs Runtime

| Approach | When | What |
|----------|------|------|
| ReAct, CoT | Runtime | *How* to reason step-by-step |
| **4D-ARE** | Design time | *What* to reason about |

4D-ARE doesn't replace runtime reasoning techniques - it specifies the **knowledge structure** that runtime reasoning operates within.

## Causal Tracing Protocol

When the agent receives a query:

1. **Display** the result gap (D_R) - "Retention is 56% vs 80% target"
2. **Trace** to Process factors (D_P) - "Visit frequency declined 23%"
3. **Trace** to Support factors (D_S) - "Staffing ratio at 68%"
4. **Contextualize** with Long-term factors (D_L) - "Market downturn, new competitors"

This produces a complete causal chain from symptom to root cause.
