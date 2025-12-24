"""
IntentLang - Natural Language Programming Language
Core package initialization
"""

__version__ = "1.0.0"
__author__ = "IntentLang Contributors"
__license__ = "MIT"

from .parser import IntentParser
from .interpreter import IntentInterpreter
from .logic_graph import LogicGraph

__all__ = ["IntentParser", "IntentInterpreter", "LogicGraph"]
