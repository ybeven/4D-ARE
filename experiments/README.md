# 4D-ARE Synthetic Data Experiment

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run full experiment (generates 150 scenarios, runs 3 agents, evaluates)
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

## Expected Results

| Metric | Naive | ReAct | 4D-ARE |
|--------|-------|-------|--------|
| Attribution Accuracy | ~40% | ~55% | ~85% |
| Dimensional Coverage | ~30% | ~45% | ~90% |
| Structural Clarity | ~25% | ~50% | ~95% |
| Boundary Compliance | ~70% | ~75% | ~98% |

## Cost Estimate

- 150 scenarios × 3 agents = 450 API calls for agents
- 150 scenarios × 3 agents = 450 API calls for evaluation
- 150 API calls for generation
- **Total**: ~1050 API calls, approximately $15-20 USD
