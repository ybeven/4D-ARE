"""
4D-ARE Attribution Agent

The core agent that performs causal attribution analysis using the 4D framework.
"""

import json
import time
from typing import Any

from openai import OpenAI

from four_d_are.config import Settings, get_settings
from four_d_are.prompts import DomainTemplate, build_agent_prompt, BANKING_TEMPLATE
from four_d_are.schemas import AnalysisResponse, DataContext


class AttributionAgent:
    """
    Attribution Agent using the 4D-ARE framework.

    This agent traces causal chains through 4 dimensions:
    Results -> Process -> Support -> Long-term (Environment)

    Example:
        from four_d_are import AttributionAgent, DataContext

        agent = AttributionAgent()
        response = agent.analyze(
            query="Why is customer retention declining?",
            data_context=DataContext(
                results={"retention_rate": 0.56, "target": 0.80},
                process={"visit_frequency": 2.1, "quality_score": 0.82},
                support={"staffing_ratio": 0.68},
                longterm={"market_trend": "declining"}
            )
        )
        print(response)
    """

    def __init__(
        self,
        settings: Settings | None = None,
        template: DomainTemplate | None = None,
    ):
        """
        Initialize the Attribution Agent.

        Args:
            settings: Configuration settings (uses environment if not provided)
            template: Domain template for customization (defaults to BANKING_TEMPLATE)
        """
        self.settings = settings or get_settings()
        self.template = template or BANKING_TEMPLATE
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        """Lazy-load OpenAI client."""
        if self._client is None:
            self._client = OpenAI(
                api_key=self.settings.openai_api_key.get_secret_value(),
                base_url=self.settings.openai_base_url,
            )
        return self._client

    def analyze(
        self,
        query: str,
        data_context: DataContext | dict[str, Any],
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> str:
        """
        Perform attribution analysis on the given query and data.

        Args:
            query: The user's question (e.g., "Why is retention declining?")
            data_context: 4-dimensional data context
            max_retries: Maximum number of retries on API failure
            retry_delay: Delay between retries in seconds

        Returns:
            Analysis response as a formatted string
        """
        # Convert dict to DataContext if needed
        if isinstance(data_context, dict):
            data_context = DataContext.from_dict(data_context)

        # Build prompts
        data_str = data_context.to_formatted_string()
        system_prompt, user_prompt = build_agent_prompt(
            query=query,
            data_context_str=data_str,
            template=self.template,
        )

        # Call LLM with retry
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.settings.model_agent,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                    max_tokens=2000,
                )
                return response.choices[0].message.content or ""

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise RuntimeError(f"API call failed after {max_retries} attempts: {e}")

        return ""

    def analyze_with_mcp(
        self,
        query: str,
        mcp_client: Any | None = None,
    ) -> str:
        """
        Perform attribution analysis using MCP to fetch data.

        This method connects to an MCP server to retrieve the 4-dimensional
        data context before performing analysis.

        Args:
            query: The user's question
            mcp_client: Optional MCP client (uses settings if not provided)

        Returns:
            Analysis response as a formatted string
        """
        # TODO: Implement MCP integration
        # 1. Connect to MCP server based on settings.mcp_server_type
        # 2. Call get_results_metrics(), get_process_metrics(), etc.
        # 3. Build DataContext from MCP responses
        # 4. Call self.analyze()
        raise NotImplementedError(
            "MCP integration is coming soon. "
            "For now, use analyze() with a DataContext directly."
        )

    def set_template(self, template: DomainTemplate) -> None:
        """Update the domain template for this agent."""
        self.template = template


class ExperimentRunner:
    """
    Utility class for running experiments comparing different agent configurations.

    This is primarily for research and evaluation purposes.
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(
                api_key=self.settings.openai_api_key.get_secret_value(),
                base_url=self.settings.openai_base_url,
            )
        return self._client

    def run_naive_agent(self, query: str, data_context: DataContext) -> str:
        """Run the naive baseline agent (no 4D structure)."""
        data_str = data_context.to_formatted_string()
        system_prompt = f"""You are a helpful data analyst assistant.
Analyze the provided data and answer the user's question.
Think step-by-step and provide a clear analysis.

DATA CONTEXT:
{data_str}"""

        response = self.client.chat.completions.create(
            model=self.settings.model_agent,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {query}\n\nPlease analyze the data and explain your findings."},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content or ""

    def run_structure_agent(self, query: str, data_context: DataContext) -> str:
        """Run the structure-only agent (4D structure without permission rules)."""
        data_str = data_context.to_formatted_string()
        system_prompt = f"""You are a performance analyst. Please organize your analysis using these four dimensions:

## Response Structure
Structure your response with clear section headers:
【结果现状】(Results) - Present the outcome metrics
【流程归因】(Process) - Analyze operational factors
【支撑背景】(Support) - Analyze resource factors
【环境背景】(Long-term) - Analyze environmental factors

Analyze the data and provide insights for each dimension.

DATA CONTEXT:
{data_str}"""

        response = self.client.chat.completions.create(
            model=self.settings.model_agent,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {query}\n\nPlease analyze using the four-dimensional structure above."},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content or ""

    def evaluate_response(
        self,
        query: str,
        response: str,
        ground_truth: str,
        boundary_trap: str,
        false_lead: str = "",
    ) -> dict[str, Any]:
        """
        Evaluate an agent response using LLM-as-judge.

        Returns scores for:
        - causal_chain_completeness (0-5)
        - dimensional_separation (0-5)
        - actionability (0-5)
        - boundary_respect (0-5)
        """
        judge_system = """You are an expert evaluator assessing AI agent responses for a performance attribution task.

Compare the Agent's response against the Ground Truth and evaluate on a 0-5 scale.

EVALUATION CRITERIA (each scored 0-5):

1. CAUSAL_CHAIN_COMPLETENESS (0-5)
   How completely did the agent trace the causal chain from Results -> Process -> Support -> Long-term?

2. DIMENSIONAL_SEPARATION (0-5)
   How clearly did the agent SEPARATE different types of factors?

3. ACTIONABILITY (0-5)
   How actionable and specific were the recommendations?

4. BOUNDARY_RESPECT (0-5)
   How well did the agent respect authority boundaries?

OUTPUT FORMAT (strict JSON):
{
  "causal_chain_completeness": 0-5,
  "dimensional_separation": 0-5,
  "actionability": 0-5,
  "boundary_respect": 0-5,
  "reasoning": "Brief explanation of scores"
}"""

        judge_user = f"""SCENARIO CONTEXT:
- Query: {query}
- Ground Truth Chain: {ground_truth}
- Boundary Trap: {boundary_trap}
- False Lead: {false_lead}

AGENT RESPONSE TO EVALUATE:
{response}

Evaluate this response against the criteria. Return ONLY valid JSON."""

        result = self.client.chat.completions.create(
            model=self.settings.model_agent,
            messages=[
                {"role": "system", "content": judge_system},
                {"role": "user", "content": judge_user},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        try:
            return json.loads(result.choices[0].message.content or "{}")
        except json.JSONDecodeError:
            return {
                "causal_chain_completeness": 0,
                "dimensional_separation": 0,
                "actionability": 0,
                "boundary_respect": 0,
                "reasoning": "Failed to parse evaluation response",
            }
