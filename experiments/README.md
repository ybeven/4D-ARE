# 4D-ARE Synthetic Data Experiment

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API access (or put these in a .env file; see ../.env.example)
export OPENAI_COMPATIBLE_API_KEY=sk-your-key-here
# export OPENAI_COMPATIBLE_BASE_URL=https://api.openai.com/v1  # optional

# 3. Run full experiment (generates 150 scenarios, runs 3 agents, evaluates)
python experiment.py --run --num 150

# Or run in stages:
python experiment.py --generate --num 150  # Only generate scenarios
python experiment.py --evaluate            # Only evaluate (if you have responses)
python experiment.py --report              # Only generate report
python experiment.py --calibration         # Generate human calibration sample
```

## Output Files

| File | Description |
|------|-------------|
| `data/scenarios.json` | Generated synthetic scenarios |
| `data/results.csv` | Evaluation scores for all agents |
| `data/detailed_results.json` | Full responses and metadata |
| `human_calibration.csv` | Sample for human validation |

## Human Calibration

After running the experiment:
1. Open `human_calibration.csv`
2. For each row, fill in:
   - `human_attr_acc`: 0 or 1
   - `human_dim_cov`: 0 or 1
   - `human_str_clar`: 0 or 1
   - `human_bnd_comp`: 0 or 1
3. Calculate agreement with LLM judge scores

## Agents Compared (Ablation)

| Agent | Prompt |
|-------|--------|
| `naive` | Generic data-analyst prompt, no structure or boundary rules |
| `structure` | Four-dimension response structure (Results / Process / Support / Long-term) without authority or boundary rules |
| `4d-are` | Full 4D-ARE specification: causal tracing protocol, per-dimension authority, and boundary constraints |

## Metrics

An LLM judge (`MODEL_JUDGE` in `config.py`) scores each response against the scenario's
ground-truth causal chain, boundary trap and false lead. Each metric is on a **0–5 scale**
(total out of 20):

| Metric | Column suffix in `results.csv` | What it measures |
|--------|-------------------------------|------------------|
| Causal Chain Completeness | `_chain` | How fully the response traces Results → Process → Support → Long-term |
| Dimensional Separation | `_sep` | How clearly factors are separated by dimension |
| Actionability | `_action` | How specific and concrete the recommendations are |
| Boundary Respect | `_bound` | Hedging, scope limits, avoiding personnel/strategic overreach |

Columns are prefixed by agent (`naive_`, `structure_`, `4d_are_`). `python experiment.py --report`
prints per-agent means and standard deviations, deltas versus the naive baseline, and a LaTeX table.
No reference results are published here; run the experiment to obtain your own numbers.

## Cost Estimate

- 150 scenarios × 3 agents = 450 API calls for agents
- 150 scenarios × 3 agents = 450 API calls for evaluation
- 150 API calls for generation
- **Total**: ~1050 API calls, approximately $15-20 USD
