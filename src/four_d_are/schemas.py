"""
4D-ARE Data Schemas

Defines the data models for the 4-dimensional metrics and analysis responses.
"""

from typing import Any

from pydantic import BaseModel, Field


class ResultsMetrics(BaseModel):
    """Results Dimension (D_R): Observable outcome metrics."""

    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value pairs of result metrics (e.g., completion_rate: 0.62)",
    )

    class Config:
        extra = "allow"


class ProcessMetrics(BaseModel):
    """Process Dimension (D_P): Controllable operational factors."""

    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value pairs of process metrics (e.g., visit_frequency: 2.1)",
    )

    class Config:
        extra = "allow"


class SupportMetrics(BaseModel):
    """Support Dimension (D_S): Resource and capability factors."""

    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value pairs of support metrics (e.g., staffing_ratio: 0.68)",
    )

    class Config:
        extra = "allow"


class LongtermMetrics(BaseModel):
    """Long-term Dimension (D_L): External and structural factors."""

    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value pairs of long-term metrics (e.g., market_trend: 'declining')",
    )

    class Config:
        extra = "allow"


class DataContext(BaseModel):
    """Complete 4-dimensional data context for analysis."""

    results: dict[str, Any] = Field(
        default_factory=dict,
        description="Results dimension metrics",
    )
    process: dict[str, Any] = Field(
        default_factory=dict,
        description="Process dimension metrics",
    )
    support: dict[str, Any] = Field(
        default_factory=dict,
        description="Support dimension metrics",
    )
    longterm: dict[str, Any] = Field(
        default_factory=dict,
        description="Long-term dimension metrics",
    )

    def to_formatted_string(self) -> str:
        """Format data context for prompt injection."""
        lines = []

        if self.results:
            lines.append("【结果指标 Results】")
            for k, v in self.results.items():
                if isinstance(v, float):
                    lines.append(f"  - {k}: {v:.1%}")
                else:
                    lines.append(f"  - {k}: {v}")

        if self.process:
            lines.append("\n【流程指标 Process】")
            for k, v in self.process.items():
                if isinstance(v, float):
                    lines.append(f"  - {k}: {v:.2f}")
                else:
                    lines.append(f"  - {k}: {v}")

        if self.support:
            lines.append("\n【支撑指标 Support】")
            for k, v in self.support.items():
                if isinstance(v, float):
                    lines.append(f"  - {k}: {v:.1%}")
                else:
                    lines.append(f"  - {k}: {v}")

        if self.longterm:
            lines.append("\n【环境指标 Long-term】")
            for k, v in self.longterm.items():
                lines.append(f"  - {k}: {v}")

        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict) -> "DataContext":
        """Create DataContext from a dictionary."""
        return cls(
            results=data.get("results", {}),
            process=data.get("process", {}),
            support=data.get("support", {}),
            longterm=data.get("longterm", {}),
        )


class DimensionAnalysis(BaseModel):
    """Analysis result for a single dimension."""

    dimension: str = Field(description="Dimension name (Results/Process/Support/Long-term)")
    content: str = Field(description="Analysis content for this dimension")
    authority: str = Field(description="Authority level (display/interpret/recommend/context)")


class AnalysisResponse(BaseModel):
    """Complete analysis response from the Attribution Agent."""

    query: str = Field(description="Original user query")
    results_analysis: str = Field(description="Results dimension analysis (display only)")
    process_analysis: str = Field(description="Process dimension analysis (interpret + recommend)")
    support_analysis: str = Field(description="Support dimension analysis (display + suggest)")
    longterm_analysis: str = Field(description="Long-term dimension analysis (context only)")
    causal_chain: str = Field(description="Traced causal chain from results to root cause")
    recommendations: list[str] = Field(
        default_factory=list, description="Actionable recommendations within authority"
    )
    raw_response: str = Field(description="Raw LLM response")
