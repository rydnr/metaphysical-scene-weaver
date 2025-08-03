"""Pytest configuration and shared fixtures for all tests."""

import pytest
import asyncio
from pathlib import Path
import json
import sys
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.script_parser import ScriptParser, ScriptEntry
from src.core.scene_weaver import SceneWeaver
from src.core.character_state_tracker import CharacterStateTracker
from src.processors.philosophical_interpreter import PhilosophicalInterpreter
from src.processors.emotional_mapper import EmotionalMapper
from src.processors.metaphor_translator import MetaphorTranslator
from src.processors.context_analyzer import ContextAnalyzer
from src.processors.prompt_generator import PromptGenerator
from src.processors.scene_synthesizer import SceneSynthesizer


# Test data paths
TEST_DATA_DIR = Path(__file__).parent / "fixtures"
SAMPLE_SCRIPTS_DIR = TEST_DATA_DIR / "sample_scripts"
EDGE_CASES_DIR = TEST_DATA_DIR / "edge_cases"


@pytest.fixture
def sample_dialogue_entry():
    """Provide a sample dialogue entry for testing."""
    return ScriptEntry(
        id="0001",
        speaker="Evan",
        dialogue="What if consciousness is just an emergent property of complexity?",
        panel_count=1,
        metadata=["philosophical question"],
        stage_directions=["looks thoughtful"]
    )


@pytest.fixture
def sample_script_entries():
    """Provide sample script entries for testing."""
    return [
        ScriptEntry(
            id="0001",
            speaker="Evan",
            dialogue="What if consciousness is just an emergent property of complexity?",
            panel_count=1,
            metadata=["philosophical question"]
        ),
        ScriptEntry(
            id="0002",
            speaker="Monday",
            dialogue="Then perhaps we're all just beautiful accidents of sufficient complexity.",
            panel_count=2,
            metadata=["philosophical response"],
            stage_directions=["gestures broadly"]
        ),
        ScriptEntry(
            id="0003",
            speaker="Evan",
            dialogue="But that doesn't explain qualia - the redness of red, the feeling of feelings.",
            panel_count=1,
            metadata=["counterargument"]
        )
    ]


@pytest.fixture
def sample_script_text():
    """Provide sample script text for parsing tests."""
    return """
[0001] Evan: <<What if consciousness is just an emergent property of complexity?>>
[0002] [2-panel] Monday: <<Then perhaps we're all just beautiful accidents of sufficient complexity.>> (gestures broadly)
[0003] Evan: <<But that doesn't explain qualia - the redness of red, the feeling of feelings.>>
[0004] Monday: <<Maybe qualia is what complexity feels like from the inside.>> [[philosophical insight]]
"""


@pytest.fixture
def edge_case_scripts():
    """Provide edge case scripts for robustness testing."""
    return {
        "empty_dialogue": "[0001] Evan: <<>>",
        "unicode_chars": "[0001] Monday: <<∃x(Px ∧ Qx) → ∀y(Ry → Sy) 哲学的な質問>>",
        "very_long_dialogue": f"[0001] Evan: <<{'A' * 1000}>>",
        "no_speaker": "[0001] : <<Anonymous thought>>",
        "malformed_id": "[XXXX] Evan: <<Test>>",
        "nested_brackets": "[0001] Evan: <<<<Nested>> brackets>>",
        "special_chars": "[0001] Monday: <<Test\n\t\r special chars & symbols!@#$%>>",
        "multiple_metadata": "[0001] Evan: <<Test>> [[meta1]] [[meta2]] [[meta3]]",
        "circular_reference": "[0001] Evan: <<See entry 0001 for details>>"
    }


@pytest.fixture
def script_parser():
    """Provide a configured ScriptParser instance."""
    return ScriptParser()


@pytest.fixture
def scene_weaver():
    """Provide a configured SceneWeaver instance."""
    return SceneWeaver()


@pytest.fixture
def character_tracker():
    """Provide a configured CharacterStateTracker instance."""
    return CharacterStateTracker()


@pytest.fixture
def philosophical_interpreter():
    """Provide a configured PhilosophicalInterpreter instance."""
    return PhilosophicalInterpreter()


@pytest.fixture
def emotional_mapper():
    """Provide a configured EmotionalMapper instance."""
    return EmotionalMapper()


@pytest.fixture
def metaphor_translator():
    """Provide a configured MetaphorTranslator instance."""
    return MetaphorTranslator()


@pytest.fixture
def context_analyzer():
    """Provide a configured ContextAnalyzer instance."""
    return ContextAnalyzer()


@pytest.fixture
def prompt_generator():
    """Provide a configured PromptGenerator instance."""
    return PromptGenerator()


@pytest.fixture
def scene_synthesizer():
    """Provide a configured SceneSynthesizer instance."""
    return SceneSynthesizer()


@pytest.fixture
def mock_api_response():
    """Provide mock API response for testing."""
    return {
        "status": "success",
        "data": {
            "prompts": [
                "A contemplative scene showing two figures discussing consciousness",
                "Abstract visualization of emergent complexity"
            ],
            "metadata": {
                "philosophy_score": 0.85,
                "emotion_coherence": 0.92
            }
        }
    }


@pytest.fixture
async def async_client():
    """Provide async test client for API testing."""
    from httpx import AsyncClient
    from src.api.server import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def performance_threshold():
    """Provide performance thresholds for tests."""
    return {
        "script_parsing": 0.1,  # 100ms for 100 entries
        "philosophy_detection": 0.2,  # 200ms
        "emotion_mapping": 0.15,  # 150ms
        "prompt_generation": 0.5,  # 500ms
        "full_pipeline": 2.0,  # 2 seconds
        "memory_limit": 500  # 500MB
    }


@pytest.fixture
def quality_thresholds():
    """Provide quality thresholds for validation tests."""
    return {
        "philosophy_accuracy": 0.85,
        "emotion_precision": 0.90,
        "prompt_coherence": 0.95,
        "metaphor_relevance": 0.80,
        "scene_consistency": 0.90,
        "character_continuity": 0.95
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "edge_case: Edge case tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


# Async event loop configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test data generators
@pytest.fixture
def generate_script_entries():
    """Factory fixture for generating test script entries."""
    def _generate(count: int, speaker_pattern: List[str] = None) -> List[ScriptEntry]:
        if speaker_pattern is None:
            speaker_pattern = ["Evan", "Monday"]
        
        entries = []
        for i in range(count):
            speaker = speaker_pattern[i % len(speaker_pattern)]
            entry = ScriptEntry(
                id=f"{i+1:04d}",
                speaker=speaker,
                dialogue=f"Test dialogue {i+1} from {speaker}",
                panel_count=(i % 3) + 1,
                metadata=[f"test_meta_{i}"] if i % 2 == 0 else []
            )
            entries.append(entry)
        return entries
    
    return _generate


@pytest.fixture
def generate_philosophical_dialogue():
    """Factory fixture for generating philosophical dialogues."""
    philosophical_templates = [
        "What is the nature of {concept}?",
        "If {premise}, then how can we understand {conclusion}?",
        "The paradox of {subject} reveals {insight}.",
        "In considering {topic}, we must examine {aspect}."
    ]
    
    concepts = ["consciousness", "reality", "identity", "time", "free will"]
    
    def _generate(complexity: str = "moderate") -> str:
        import random
        if complexity == "simple":
            return random.choice(philosophical_templates[:2]).format(
                concept=random.choice(concepts),
                premise="we are conscious",
                conclusion="consciousness"
            )
        elif complexity == "complex":
            return " ".join([
                random.choice(philosophical_templates).format(
                    concept=random.choice(concepts),
                    premise="consciousness emerges from complexity",
                    conclusion="artificial consciousness",
                    subject="identity",
                    insight="the fluidity of self",
                    topic="metaphysics",
                    aspect="ontological foundations"
                ) for _ in range(3)
            ])
        else:  # moderate
            return random.choice(philosophical_templates).format(
                concept=random.choice(concepts),
                premise="reality is subjective",
                conclusion="objective truth",
                subject="perception",
                insight="constructed nature of experience",
                topic="epistemology",
                aspect="knowledge limits"
            )
    
    return _generate


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_files(request):
    """Automatically cleanup any test files created during tests."""
    test_files = []
    
    def register_cleanup(filepath):
        test_files.append(filepath)
    
    request.addfinalizer(lambda: [Path(f).unlink(missing_ok=True) for f in test_files])
    
    return register_cleanup