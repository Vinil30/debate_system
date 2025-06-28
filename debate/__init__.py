"""
Multi-Agent Debate System using LangGraph

This package implements a structured debate between two AI agents with memory and judging capabilities.
"""

from .agents import DebateAgent
from .memory import DebateMemory
from .judge import DebateJudge
from .nodes import UserInputNode, AgentNode, RoundControlNode, JudgeNode
from .graph import DebateGraph

__all__ = [
    'DebateAgent',
    'DebateMemory',
    'DebateJudge',
    'UserInputNode',
    'AgentNode',
    'RoundControlNode',
    'DebateGraph',
    'JudgeNode'
]

__version__ = '0.1.0'