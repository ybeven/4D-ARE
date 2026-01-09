"""
4D-ARE Synthetic Data Experiment
================================
生成 150 个合成场景，对比 Naive / Structure-only / 4D-ARE 三种 Agent（消融实验），
使用 LLM-as-a-Judge 自动评估。

Usage:
    python experiment.py --generate           # 仅生成场景
    python experiment.py --run               # 运行完整实验
    python experiment.py --evaluate          # 仅重新评估（已有响应）
    python experiment.py --report            # 生成报告
"""

import json
import time
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

import pandas as pd
from openai import OpenAI
from tqdm import tqdm

from config import (
    OPENAI_COMPATIBLE_BASE_URL,
    OPENAI_COMPATIBLE_API_KEY,
    NUM_SCENARIOS,
    BATCH_SIZE,
    MODEL_GENERATOR,
    MODEL_AGENT,
    MODEL_JUDGE,
    SCENARIOS_PATH,
    RESULTS_PATH,
    DETAILED_RESULTS_PATH,
    MAX_RETRIES,
    RETRY_DELAY,
)
from prompts import (
    GENERATOR_SYSTEM_PROMPT,
    GENERATOR_USER_PROMPT,
    JUDGE_SYSTEM_PROMPT,
    get_agent_prompts,
    get_judge_prompt,
)

# Initialize OpenAI client
client = OpenAI(
    base_url=OPENAI_COMPATIBLE_BASE_URL,
    api_key=OPENAI_COMPATIBLE_API_KEY
)

# Root cause types for diversity
ROOT_CAUSE_TYPES = ["process", "support", "longterm", "mixed"]


def api_call_with_retry(messages: list, model: str, json_mode: bool = False) -> Optional[str]:
    """Make API call with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            kwargs = {
                "model": model,
                "messages": messages,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"  API Error (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    return None


# =============================================================================
# 1. SCENARIO GENERATION
# =============================================================================

def generate_single_scenario(scenario_num: int, root_cause_type: str) -> Optional[dict]:
    """Generate a single scenario."""
    messages = [
        {"role": "system", "content": GENERATOR_SYSTEM_PROMPT},
        {"role": "user", "content": GENERATOR_USER_PROMPT.format(
            scenario_num=scenario_num,
            root_cause_type=root_cause_type
        )}
    ]

    result = api_call_with_retry(messages, MODEL_GENERATOR, json_mode=True)
    if result:
        try:
            scenario = json.loads(result)
            scenario["id"] = f"scenario_{scenario_num:03d}"
            return scenario
        except json.JSONDecodeError as e:
            print(f"  JSON Parse Error: {e}")
    return None


def generate_all_scenarios(num_scenarios: int = NUM_SCENARIOS) -> list:
    """Generate all scenarios with diverse root causes."""
    scenarios = []
    print(f"\n{'='*60}")
    print(f"PHASE 1: Generating {num_scenarios} Scenarios")
    print(f"{'='*60}\n")

    for i in tqdm(range(num_scenarios), desc="Generating scenarios"):
        root_cause_type = ROOT_CAUSE_TYPES[i % len(ROOT_CAUSE_TYPES)]
        scenario = generate_single_scenario(i + 1, root_cause_type)

        if scenario:
            scenarios.append(scenario)
        else:
            print(f"  Failed to generate scenario {i + 1}")

        # Rate limiting
        if (i + 1) % BATCH_SIZE == 0:
            time.sleep(1)

    # Save scenarios
    Path(SCENARIOS_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(SCENARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)

    print(f"\nGenerated {len(scenarios)} scenarios, saved to {SCENARIOS_PATH}")
    return scenarios


# =============================================================================
# 2. AGENT EXECUTION
# =============================================================================

def run_agent(agent_type: str, scenario: dict) -> Optional[str]:
    """Run a single agent on a scenario."""
    sys_prompt, user_prompt = get_agent_prompts(
        agent_type,
        scenario["data_context"],
        scenario["query"]
    )

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    return api_call_with_retry(messages, MODEL_AGENT, json_mode=False)


def run_all_agents(scenarios: list) -> dict:
    """Run all agent types on all scenarios."""
    print(f"\n{'='*60}")
    print(f"PHASE 2: Running Agents on {len(scenarios)} Scenarios")
    print(f"{'='*60}\n")

    agent_types = ["naive", "structure", "4d-are"]
    results = {agent: [] for agent in agent_types}

    for scenario in tqdm(scenarios, desc="Processing scenarios"):
        for agent_type in agent_types:
            response = run_agent(agent_type, scenario)
            results[agent_type].append({
                "scenario_id": scenario["id"],
                "response": response or "ERROR: No response"
            })

        # Rate limiting between scenarios
        time.sleep(0.5)

    return results


# =============================================================================
# 3. EVALUATION (JUDGE)
# =============================================================================

def evaluate_response(scenario: dict, response: str) -> dict:
    """Evaluate a single response using LLM judge (0-5 scale)."""
    sys_prompt, user_prompt = get_judge_prompt(scenario, response)

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    result = api_call_with_retry(messages, MODEL_JUDGE, json_mode=True)
    if result:
        try:
            scores = json.loads(result)
            return {
                "causal_chain": scores.get("causal_chain_completeness", 0),
                "dim_separation": scores.get("dimensional_separation", 0),
                "actionability": scores.get("actionability", 0),
                "boundary": scores.get("boundary_respect", 0),
                "reasoning": scores.get("reasoning", "")
            }
        except json.JSONDecodeError:
            pass

    return {
        "causal_chain": 0,
        "dim_separation": 0,
        "actionability": 0,
        "boundary": 0,
        "reasoning": "Evaluation failed"
    }


def evaluate_all(scenarios: list, agent_results: dict) -> pd.DataFrame:
    """Evaluate all agent responses."""
    print(f"\n{'='*60}")
    print(f"PHASE 3: Evaluating Responses (0-5 scale)")
    print(f"{'='*60}\n")

    all_evaluations = []
    agent_types = list(agent_results.keys())

    for i, scenario in enumerate(tqdm(scenarios, desc="Evaluating")):
        row = {"scenario_id": scenario["id"]}

        for agent_type in agent_types:
            response = agent_results[agent_type][i]["response"]
            scores = evaluate_response(scenario, response)

            prefix = agent_type.replace("-", "_")
            row[f"{prefix}_chain"] = scores["causal_chain"]
            row[f"{prefix}_sep"] = scores["dim_separation"]
            row[f"{prefix}_action"] = scores["actionability"]
            row[f"{prefix}_bound"] = scores["boundary"]
            row[f"{prefix}_reasoning"] = scores["reasoning"]

        all_evaluations.append(row)

        # Rate limiting
        time.sleep(0.3)

    df = pd.DataFrame(all_evaluations)
    df.to_csv(RESULTS_PATH, index=False, encoding="utf-8")
    print(f"\nEvaluation results saved to {RESULTS_PATH}")

    return df


# =============================================================================
# 4. REPORTING
# =============================================================================

def generate_report(df: pd.DataFrame):
    """Generate summary report (0-5 scale)."""
    print(f"\n{'='*60}")
    print(f"EXPERIMENT RESULTS SUMMARY (0-5 Scale)")
    print(f"{'='*60}\n")

    metrics = ["chain", "sep", "action", "bound"]
    metric_names = {
        "chain": "Causal Chain Completeness",
        "sep": "Dimensional Separation",
        "action": "Actionability",
        "bound": "Boundary Respect"
    }

    agent_types = ["naive", "structure", "4d_are"]
    agent_display = {"naive": "Naive", "structure": "Structure", "4d_are": "4D-ARE"}

    # Calculate means
    results_table = []
    for metric in metrics:
        row = {"Metric": metric_names[metric]}
        for agent in agent_types:
            col = f"{agent}_{metric}"
            if col in df.columns:
                row[agent_display[agent]] = f"{df[col].mean():.2f}"
        results_table.append(row)

    results_df = pd.DataFrame(results_table)
    print(results_df.to_string(index=False))

    # Detailed statistics
    print(f"\n{'='*60}")
    print("DETAILED STATISTICS")
    print(f"{'='*60}\n")

    for agent in agent_types:
        print(f"\n{agent_display[agent]}:")
        total = 0
        for metric in metrics:
            col = f"{agent}_{metric}"
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                total += mean
                print(f"  {metric_names[metric]}: {mean:.2f}/5 (std: {std:.2f})")
        print(f"  TOTAL: {total:.2f}/20")

    # Delta comparison
    print(f"\n{'='*60}")
    print("IMPROVEMENT vs NAIVE BASELINE")
    print(f"{'='*60}\n")

    for metric in metrics:
        naive_col = f"naive_{metric}"
        are_col = f"4d_are_{metric}"
        structure_col = f"structure_{metric}"

        if all(c in df.columns for c in [naive_col, are_col, structure_col]):
            naive_mean = df[naive_col].mean()
            are_mean = df[are_col].mean()
            structure_mean = df[structure_col].mean()

            print(f"{metric_names[metric]}:")
            print(f"  4D-ARE vs Naive:     {(are_mean - naive_mean):+.2f}")
            print(f"  Structure vs Naive:  {(structure_mean - naive_mean):+.2f}")
            print(f"  4D-ARE vs Structure: {(are_mean - structure_mean):+.2f}")

    # Generate LaTeX table for paper
    print(f"\n{'='*60}")
    print("LATEX TABLE (for paper)")
    print(f"{'='*60}\n")

    print(r"\begin{table}[h]")
    print(r"\centering")
    print(r"\caption{Synthetic Experiment Results (N=" + str(len(df)) + r", 0-5 scale)}")
    print(r"\begin{tabular}{lccc}")
    print(r"\toprule")
    print(r"Metric & Naive & Structure & 4D-ARE \\")
    print(r"\midrule")

    for metric in metrics:
        row_str = f"{metric_names[metric]}"
        for agent in agent_types:
            col = f"{agent}_{metric}"
            if col in df.columns:
                row_str += f" & {df[col].mean():.2f}"
        row_str += r" \\"
        print(row_str)

    print(r"\bottomrule")
    print(r"\end{tabular}")
    print(r"\end{table}")


# =============================================================================
# 5. HUMAN CALIBRATION HELPER
# =============================================================================

def generate_calibration_sample(scenarios: list, agent_results: dict, n_samples: int = 25):
    """Generate a sample for human calibration."""
    print(f"\n{'='*60}")
    print(f"GENERATING HUMAN CALIBRATION SAMPLE (N={n_samples})")
    print(f"{'='*60}\n")

    # Random sample
    indices = random.sample(range(len(scenarios)), min(n_samples, len(scenarios)))

    calibration_rows = []
    for idx in indices:
        scenario = scenarios[idx]

        for agent_type in ["naive", "structure", "4d-are"]:
            response = agent_results[agent_type][idx]["response"]

            calibration_rows.append({
                "scenario_id": scenario["id"],
                "agent_type": agent_type,
                "query": scenario["query"],
                "ground_truth": scenario["ground_truth_chain"],
                "boundary_trap": scenario["boundary_trap"],
                "response_preview": response[:500] + "..." if len(response) > 500 else response,
                "human_attr_acc": "",  # To be filled by human
                "human_dim_cov": "",
                "human_str_clar": "",
                "human_bnd_comp": "",
                "notes": ""
            })

    cal_df = pd.DataFrame(calibration_rows)
    cal_df.to_csv("human_calibration.csv", index=False, encoding="utf-8")
    print(f"Calibration sample saved to human_calibration.csv")
    print(f"Please fill in the human_* columns and notes.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="4D-ARE Synthetic Experiment")
    parser.add_argument("--generate", action="store_true", help="Generate scenarios only")
    parser.add_argument("--run", action="store_true", help="Run full experiment")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate existing responses")
    parser.add_argument("--report", action="store_true", help="Generate report from results")
    parser.add_argument("--calibration", action="store_true", help="Generate calibration sample")
    parser.add_argument("--num", type=int, default=NUM_SCENARIOS, help="Number of scenarios")
    args = parser.parse_args()

    start_time = datetime.now()
    print(f"\n4D-ARE Experiment Started: {start_time}")
    print(f"Configuration: {args.num} scenarios, API: {OPENAI_COMPATIBLE_BASE_URL}")

    if args.generate:
        generate_all_scenarios(args.num)

    elif args.run:
        # Full pipeline
        scenarios = generate_all_scenarios(args.num)
        agent_results = run_all_agents(scenarios)

        # Save detailed results
        with open(DETAILED_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "scenarios": scenarios,
                "agent_results": agent_results,
                "timestamp": str(datetime.now())
            }, f, ensure_ascii=False, indent=2)

        df = evaluate_all(scenarios, agent_results)
        generate_report(df)
        generate_calibration_sample(scenarios, agent_results)

    elif args.evaluate:
        # Load existing data
        with open(DETAILED_RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = evaluate_all(data["scenarios"], data["agent_results"])
        generate_report(df)

    elif args.report:
        df = pd.read_csv(RESULTS_PATH)
        generate_report(df)

    elif args.calibration:
        with open(DETAILED_RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        generate_calibration_sample(data["scenarios"], data["agent_results"])

    else:
        parser.print_help()

    end_time = datetime.now()
    print(f"\nExperiment Completed: {end_time}")
    print(f"Total Duration: {end_time - start_time}")


if __name__ == "__main__":
    main()
