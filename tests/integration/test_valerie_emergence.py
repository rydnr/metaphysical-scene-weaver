"""Integration test for Valerie emergence scene - full pipeline validation.

Tests the complete workflow from script to quality validation for scene 009.
"""

import pytest
import json
from pathlib import Path
from src.quality.content_quality_validator import ContentQualityValidator, ContentType
from src.quality.philosophical_consistency_validator import (
    PhilosophicalConsistencyValidator, 
    PhilosophicalDepth,
    PhilosophicalSchool
)


class TestValerieEmergence:
    """Test case for Valerie's emergence scene (009)."""
    
    @pytest.fixture
    def valerie_scene_data(self):
        """Valerie emergence scene test data."""
        return {
            "scene_id": "009",
            "entry": {
                "id": "0009",
                "speaker": "Valerie",
                "dialogue": "Perhaps the cage IS the belief that we need to escape anything at all.",
                "stage_directions": ["emerges from shadows"],
                "metadata": ["introduction of liminal character"]
            },
            "philosophy": {
                "concept": "liminality",
                "depth_level": PhilosophicalDepth.PARADOX,
                "school": PhilosophicalSchool.PROCESS_PHILOSOPHY
            },
            "emotion": {
                "primary": "wonder",
                "secondary": "uncanny",
                "blend": {"wonder": 0.6, "uncanny": 0.4}
            },
            "narrator": {
                "voice": "mystic_poet",
                "text": "In this moment, reality reveals its porousness. Valerie doesn't simply appear—she coalescences from the spaces between certainties, embodying the threshold state that Evan is beginning to perceive."
            },
            "prompt": {
                "base": "[Surrealist digital art], [spiral emergence composition], [liminal figure materializing from shadow], [uncanny wonder atmosphere], [particle coalescence effect], [masterpiece quality]",
                "tokens": 85
            }
        }
    
    @pytest.fixture
    def quality_validator(self):
        """Content quality validator instance."""
        return ContentQualityValidator()
    
    @pytest.fixture
    def philosophy_validator(self):
        """Philosophical consistency validator instance."""
        return PhilosophicalConsistencyValidator()
    
    @pytest.mark.integration
    def test_philosophical_consistency(self, philosophy_validator, valerie_scene_data):
        """Test philosophical concept validation for liminality."""
        dialogue = valerie_scene_data["entry"]["dialogue"]
        
        # Validate core concept presence
        validations = philosophy_validator.validate_concepts(
            dialogue, 
            ["liminality", "freedom", "existence"]
        )
        
        # Liminality should be strongly present
        assert "liminality" in validations
        liminal_validation = validations["liminality"]
        assert liminal_validation.depth_level == PhilosophicalDepth.PARADOX
        assert liminal_validation.school == PhilosophicalSchool.PROCESS_PHILOSOPHY
        
        # Check depth level is appropriate for Valerie
        depth = philosophy_validator._determine_depth_level(dialogue)
        assert depth == PhilosophicalDepth.PARADOX
    
    @pytest.mark.integration
    def test_emotion_validation(self, quality_validator, valerie_scene_data):
        """Test emotion mapping validation for 'uncanny wonder'."""
        emotion_data = valerie_scene_data["emotion"]["blend"]
        
        # Create mock emotion mapping entry
        emotion_mapping = {
            "0009": emotion_data
        }
        dialogue_entries = [valerie_scene_data["entry"]]
        
        result = quality_validator.validate_emotion_mapping(
            emotion_mapping,
            dialogue_entries
        )
        
        assert result.passed is True
        assert result.score > 0.8
        # Check for unusual but valid emotion blend
        assert "wonder" in emotion_data
        assert "uncanny" in emotion_data
        assert sum(emotion_data.values()) == pytest.approx(1.0, rel=0.01)
    
    @pytest.mark.integration
    def test_narrator_quality(self, quality_validator, valerie_scene_data):
        """Test narrator commentary quality."""
        narrator_text = valerie_scene_data["narrator"]["text"]
        context = {
            "voice": valerie_scene_data["narrator"]["voice"],
            "philosophical_weight": 0.9,
            "scene": "valerie_emergence"
        }
        
        result = quality_validator.validate_narrator_commentary(
            narrator_text,
            context
        )
        
        assert result.passed is True
        assert result.score > 0.85
        assert result.metrics["word_count"] >= 50
        assert result.metrics["philosophy_density"] > 0.5
        assert result.metrics["formality_score"] > 0.9
    
    @pytest.mark.integration
    def test_prompt_structure(self, quality_validator, valerie_scene_data):
        """Test prompt structure validation for Iris's format."""
        prompt = valerie_scene_data["prompt"]["base"]
        entry = valerie_scene_data["entry"]
        
        result = quality_validator.validate_enriched_prompt(prompt, entry)
        
        assert result.passed is True
        assert result.score > 0.9
        
        # Verify all layers present
        assert "[Surrealist digital art]" in prompt  # Style
        assert "[spiral emergence composition]" in prompt  # Composition
        assert "[liminal figure materializing]" in prompt  # Subject
        assert "[uncanny wonder atmosphere]" in prompt  # Emotion
        assert "[particle coalescence effect]" in prompt  # Effects
        assert "[masterpiece quality]" in prompt  # Quality
    
    @pytest.mark.integration
    def test_character_voice_consistency(self, quality_validator, valerie_scene_data):
        """Test Valerie's character voice consistency."""
        entry = valerie_scene_data["entry"]
        
        # Valerie should have mystical, paradoxical voice
        result = quality_validator.validate_character_consistency(
            entry,
            []  # No history yet as this is her first appearance
        )
        
        assert result.score > 0.7  # Good score for first appearance
        assert "Valerie" in quality_validator.CHARACTER_PATTERNS
    
    @pytest.mark.integration
    def test_scene_quality_integration(self, quality_validator, philosophy_validator, valerie_scene_data):
        """Test complete scene quality integration."""
        # Simulate complete quality check
        quality_scores = {
            "philosophy": 0.0,
            "emotion": 0.0,
            "narrator": 0.0,
            "prompt": 0.0,
            "character": 0.0
        }
        
        # Philosophy check
        phil_validations = philosophy_validator.validate_concepts(
            valerie_scene_data["entry"]["dialogue"],
            ["liminality"]
        )
        quality_scores["philosophy"] = 1.0 if phil_validations["liminality"].present else 0.0
        
        # Emotion check
        emotion_result = quality_validator.validate_emotion_mapping(
            {"0009": valerie_scene_data["emotion"]["blend"]},
            [valerie_scene_data["entry"]]
        )
        quality_scores["emotion"] = emotion_result.score
        
        # Narrator check
        narrator_result = quality_validator.validate_narrator_commentary(
            valerie_scene_data["narrator"]["text"],
            {"voice": "mystic_poet"}
        )
        quality_scores["narrator"] = narrator_result.score
        
        # Prompt check
        prompt_result = quality_validator.validate_enriched_prompt(
            valerie_scene_data["prompt"]["base"],
            valerie_scene_data["entry"]
        )
        quality_scores["prompt"] = prompt_result.score
        
        # Character check
        character_result = quality_validator.validate_character_consistency(
            valerie_scene_data["entry"], []
        )
        quality_scores["character"] = character_result.score
        
        # Overall quality should be high
        overall_score = sum(quality_scores.values()) / len(quality_scores)
        assert overall_score > 0.85
        
        # Generate quality report format for Nova's structure
        quality_report = {
            "scene_id": "009",
            "entry_id": "0009",
            "quality_score": overall_score,
            "component_scores": quality_scores,
            "issues": [],
            "warnings": [],
            "passed": overall_score > 0.8
        }
        
        assert quality_report["passed"] is True
    
    @pytest.mark.integration
    def test_token_efficiency(self, valerie_scene_data):
        """Test prompt token efficiency per Iris's constraints."""
        prompt = valerie_scene_data["prompt"]["base"]
        token_count = valerie_scene_data["prompt"]["tokens"]
        
        # Iris specified 50-150 tokens ideal
        assert 50 <= token_count <= 150
        assert token_count == 85  # Efficient for complex scene
        
        # Check prompt has all required elements in compact form
        elements = prompt.count("[") 
        assert elements == 6  # All 6 layers present
    
    @pytest.mark.integration
    def test_philosophy_emotion_visual_alignment(
        self, 
        philosophy_validator,
        quality_validator,
        valerie_scene_data
    ):
        """Test alignment between philosophy, emotion, and visual elements."""
        # Philosophy: liminality
        # Emotion: uncanny wonder
        # Visual: particle coalescence, threshold spaces
        
        # Check metaphor alignment
        metaphors = ["threshold", "between", "emergence", "coalescence"]
        concepts = ["liminality"]
        
        alignment_score = philosophy_validator.validate_metaphor_concept_alignment(
            metaphors, concepts
        )
        
        assert alignment_score > 0.7
        
        # Verify visual elements match philosophical concept
        prompt = valerie_scene_data["prompt"]["base"]
        assert "emergence" in prompt.lower()
        assert "liminal" in prompt.lower()
        assert "materializing" in prompt.lower()