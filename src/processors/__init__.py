"""Processors for transforming philosophical content into visual prompts."""

from .context_analyzer import ContextAnalyzer
from .emotional_mapper import EmotionalMapper
from .metaphor_translator import MetaphorTranslator
from .philosophical_interpreter import PhilosophicalInterpreter
from .prompt_generator import PromptGenerator
from .scene_synthesizer import SceneSynthesizer

__all__ = [
    "ContextAnalyzer",
    "EmotionalMapper",
    "MetaphorTranslator",
    "PhilosophicalInterpreter",
    "PromptGenerator",
    "SceneSynthesizer",
]