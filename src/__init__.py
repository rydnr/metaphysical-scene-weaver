"""Metaphysical Scene Weaver - Transform philosophical dialogue into visual narratives."""

__version__ = "0.1.0"

from .core.scene_weaver import SceneWeaver
from .core.script_parser import ScriptParser
from .processors.context_analyzer import ContextAnalyzer
from .processors.philosophical_interpreter import PhilosophicalInterpreter

__all__ = [
    "SceneWeaver",
    "ScriptParser",
    "ContextAnalyzer",
    "PhilosophicalInterpreter",
]