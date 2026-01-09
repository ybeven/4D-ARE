"""
4D-ARE: Attribution-Driven Agent Requirements Engineering

Build LLM agents that explain *why*, not just *what*.
"""

__version__ = "0.1.0"

from four_d_are.config import Settings, get_settings
from four_d_are.agent import AttributionAgent
from four_d_are.prompts import DomainTemplate
from four_d_are.schemas import (
    DataContext,
    ResultsMetrics,
    ProcessMetrics,
    SupportMetrics,
    LongtermMetrics,
    AnalysisResponse,
)

__all__ = [
    # Core
    "AttributionAgent",
    "DomainTemplate",
    "Settings",
    "get_settings",
    # Schemas
    "DataContext",
    "ResultsMetrics",
    "ProcessMetrics",
    "SupportMetrics",
    "LongtermMetrics",
    "AnalysisResponse",
]
