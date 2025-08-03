"""Test utilities and helper functions for Metaphysical Scene Weaver tests."""

import random
import string
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime

from src.core.script_parser import ScriptEntry


class TestDataGenerator:
    """Generate test data for various testing scenarios."""
    
    # Philosophical concepts pool
    PHILOSOPHICAL_CONCEPTS = [
        "consciousness", "reality", "existence", "time", "space",
        "free will", "determinism", "identity", "perception", "truth",
        "knowledge", "being", "nothingness", "causality", "emergence"
    ]
    
    # Emotion pools
    BASE_EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
    COMPLEX_EMOTIONS = ["contemplation", "wonder", "confusion", "realization", "doubt"]
    
    # Character names
    CHARACTER_NAMES = ["Evan", "Monday", "Sage", "River", "Phoenix", "Echo", "Cosmos"]
    
    # Dialogue templates
    DIALOGUE_TEMPLATES = [
        "What is the nature of {concept}?",
        "I feel {emotion} when I consider {concept}.",
        "Perhaps {concept1} and {concept2} are connected.",
        "The {emotion} of understanding {concept} overwhelms me.",
        "If {concept1} is true, then what of {concept2}?"
    ]
    
    @classmethod
    def generate_philosophical_dialogue(
        cls, 
        complexity: str = "moderate",
        concepts: Optional[List[str]] = None
    ) -> str:
        """Generate philosophical dialogue of varying complexity."""
        if concepts is None:
            concepts = random.sample(cls.PHILOSOPHICAL_CONCEPTS, 
                                   k=random.randint(1, 3))
        
        if complexity == "simple":
            template = random.choice(cls.DIALOGUE_TEMPLATES[:2])
            return template.format(
                concept=random.choice(concepts),
                emotion=random.choice(cls.COMPLEX_EMOTIONS)
            )
        elif complexity == "complex":
            dialogues = []
            for _ in range(3):
                template = random.choice(cls.DIALOGUE_TEMPLATES)
                dialogue = template.format(
                    concept=random.choice(concepts),
                    concept1=random.choice(concepts),
                    concept2=random.choice(concepts),
                    emotion=random.choice(cls.COMPLEX_EMOTIONS)
                )
                dialogues.append(dialogue)
            return " ".join(dialogues)
        else:  # moderate
            template = random.choice(cls.DIALOGUE_TEMPLATES[2:])
            return template.format(
                concept1=concepts[0],
                concept2=concepts[1] if len(concepts) > 1 else concepts[0],
                emotion=random.choice(cls.COMPLEX_EMOTIONS)
            )
    
    @classmethod
    def generate_script_entry(
        cls,
        entry_id: Optional[str] = None,
        speaker: Optional[str] = None,
        include_metadata: bool = False,
        include_stage_directions: bool = False,
        panel_count: Optional[int] = None
    ) -> ScriptEntry:
        """Generate a single script entry."""
        if entry_id is None:
            entry_id = f"{random.randint(1, 9999):04d}"
        
        if speaker is None:
            speaker = random.choice(cls.CHARACTER_NAMES)
        
        dialogue = cls.generate_philosophical_dialogue()
        
        metadata = []
        if include_metadata:
            metadata.append(random.choice([
                "philosophical question",
                "emotional moment",
                "key insight",
                "turning point"
            ]))
        
        stage_directions = []
        if include_stage_directions:
            stage_directions.append(random.choice([
                "looks thoughtful",
                "pauses dramatically",
                "gestures broadly",
                "smiles enigmatically"
            ]))
        
        if panel_count is None and random.random() > 0.7:
            panel_count = random.randint(1, 3)
        
        return ScriptEntry(
            id=entry_id,
            speaker=speaker,
            dialogue=dialogue,
            panel_count=panel_count,
            metadata=metadata,
            stage_directions=stage_directions
        )
    
    @classmethod
    def generate_script_text(
        cls,
        num_entries: int,
        speakers: Optional[List[str]] = None,
        alternating: bool = True
    ) -> str:
        """Generate a complete script text."""
        if speakers is None:
            speakers = random.sample(cls.CHARACTER_NAMES, k=2)
        
        entries = []
        for i in range(num_entries):
            if alternating:
                speaker = speakers[i % len(speakers)]
            else:
                speaker = random.choice(speakers)
            
            entry = cls.generate_script_entry(
                entry_id=f"{i+1:04d}",
                speaker=speaker,
                include_metadata=random.random() > 0.7,
                include_stage_directions=random.random() > 0.8
            )
            
            # Format as script text
            text = f"[{entry.id}]"
            if entry.panel_count and entry.panel_count > 1:
                text += f" [{entry.panel_count}-panel]"
            text += f" {entry.speaker}: <<{entry.dialogue}>>"
            
            if entry.stage_directions:
                text += f" ({entry.stage_directions[0]})"
            
            if entry.metadata:
                text += f" [[{entry.metadata[0]}]]"
            
            entries.append(text)
        
        return "\n".join(entries)
    
    @classmethod
    def generate_emotion_mapping(
        cls,
        num_entries: int,
        consistent: bool = True,
        character: Optional[str] = None
    ) -> Dict[str, Dict[str, float]]:
        """Generate emotion mappings for testing."""
        mappings = {}
        
        if consistent and character:
            # Generate consistent emotions for a character
            base_emotion = random.choice(cls.COMPLEX_EMOTIONS)
            secondary_emotion = random.choice(cls.BASE_EMOTIONS)
            
            for i in range(num_entries):
                entry_id = f"{i+1:04d}"
                primary_weight = random.uniform(0.6, 0.8)
                secondary_weight = 1.0 - primary_weight
                
                mappings[entry_id] = {
                    base_emotion: primary_weight,
                    secondary_emotion: secondary_weight
                }
        else:
            # Generate varied emotions
            for i in range(num_entries):
                entry_id = f"{i+1:04d}"
                num_emotions = random.randint(1, 3)
                selected_emotions = random.sample(
                    cls.BASE_EMOTIONS + cls.COMPLEX_EMOTIONS,
                    k=num_emotions
                )
                
                # Generate weights that sum to 1.0
                weights = [random.random() for _ in selected_emotions]
                total = sum(weights)
                weights = [w / total for w in weights]
                
                mappings[entry_id] = dict(zip(selected_emotions, weights))
        
        return mappings


class TestFileManager:
    """Manage test files and temporary data."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.created_files = []
    
    def create_test_file(self, filename: str, content: str) -> Path:
        """Create a test file and track it for cleanup."""
        filepath = self.base_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        self.created_files.append(filepath)
        return filepath
    
    def cleanup(self):
        """Remove all created test files."""
        for filepath in self.created_files:
            if filepath.exists():
                filepath.unlink()
        self.created_files.clear()


class PerformanceTimer:
    """Context manager for timing test operations."""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        print(f"{self.name} took {self.duration:.4f} seconds")
    
    def assert_under(self, threshold: float):
        """Assert that the operation completed under the threshold."""
        assert self.duration is not None, "Timer not used in context"
        assert self.duration < threshold, (
            f"{self.name} took {self.duration:.4f}s, "
            f"exceeding threshold of {threshold}s"
        )


class MockAPIClient:
    """Mock API client for testing without actual server."""
    
    def __init__(self):
        self.responses = {}
        self.call_count = {}
    
    def set_response(self, endpoint: str, response: Dict[str, Any]):
        """Set mock response for an endpoint."""
        self.responses[endpoint] = response
    
    async def post(self, endpoint: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """Mock POST request."""
        self.call_count[endpoint] = self.call_count.get(endpoint, 0) + 1
        
        if endpoint in self.responses:
            return self.responses[endpoint]
        
        # Default response
        return {
            "status": "success",
            "data": {
                "process_id": "mock_" + "".join(
                    random.choices(string.ascii_lowercase, k=8)
                ),
                "entries": [],
                "prompts": []
            }
        }
    
    async def get(self, endpoint: str) -> Dict[str, Any]:
        """Mock GET request."""
        self.call_count[endpoint] = self.call_count.get(endpoint, 0) + 1
        
        if endpoint in self.responses:
            return self.responses[endpoint]
        
        # Default health check response
        if endpoint == "/health":
            return {
                "status": "healthy",
                "version": "1.0.0",
                "uptime": 12345
            }
        
        return {"status": "not_found"}


def assert_valid_emotion_mapping(emotions: Dict[str, float]):
    """Assert that emotion mapping is valid."""
    assert isinstance(emotions, dict)
    assert len(emotions) > 0
    
    # Check all values are floats between 0 and 1
    for emotion, value in emotions.items():
        assert isinstance(emotion, str)
        assert isinstance(value, (int, float))
        assert 0 <= value <= 1
    
    # Check sum is approximately 1.0
    total = sum(emotions.values())
    assert abs(total - 1.0) < 0.01, f"Emotion values sum to {total}, not 1.0"


def assert_valid_prompt(prompt: str):
    """Assert that a generated prompt is valid."""
    assert isinstance(prompt, str)
    assert len(prompt) >= 20, "Prompt too short"
    assert len(prompt) <= 500, "Prompt too long"
    
    # Should contain some expected elements
    expected_elements = ["style", "scene", "mood", "setting", "character", "visual"]
    assert any(element in prompt.lower() for element in expected_elements), \
        "Prompt missing expected visual elements"


def compare_philosophical_concepts(
    detected: List[str],
    expected: List[str],
    threshold: float = 0.7
) -> bool:
    """Compare detected concepts against expected with fuzzy matching."""
    if not detected or not expected:
        return False
    
    detected_set = set(c.lower() for c in detected)
    expected_set = set(c.lower() for c in expected)
    
    intersection = detected_set & expected_set
    union = detected_set | expected_set
    
    jaccard_similarity = len(intersection) / len(union) if union else 0
    return jaccard_similarity >= threshold