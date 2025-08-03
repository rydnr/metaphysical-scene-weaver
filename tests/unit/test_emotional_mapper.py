"""Unit tests for the EmotionalMapper module."""

import pytest
import numpy as np
from src.processors.emotional_mapper import (
    EmotionalMapper,
    EmotionVector,
    EmotionalTransition,
    EmotionalContext,
    ComplexEmotion
)


class TestEmotionalMapper:
    """Test cases for EmotionalMapper."""
    
    @pytest.mark.unit
    def test_initialization(self, emotional_mapper):
        """Test mapper initialization."""
        assert isinstance(emotional_mapper, EmotionalMapper)
        assert emotional_mapper.emotion_lexicon is not None
        assert emotional_mapper.base_emotions is not None
    
    @pytest.mark.unit
    def test_map_simple_emotion(self, emotional_mapper):
        """Test mapping of simple emotions."""
        dialogue_entry = {
            "id": "0001",
            "speaker": "Evan",
            "dialogue": "I feel so happy today!",
            "context": {}
        }
        
        result = emotional_mapper.map_emotions([dialogue_entry])
        
        assert "0001" in result
        emotions = result["0001"]
        assert "joy" in emotions or "happiness" in emotions
        assert sum(emotions.values()) == pytest.approx(1.0, rel=0.01)
    
    @pytest.mark.unit
    def test_map_complex_emotions(self, emotional_mapper):
        """Test mapping of complex emotions."""
        dialogue_entry = {
            "id": "0001",
            "speaker": "Monday",
            "dialogue": "I feel a bittersweet nostalgia, both happy and sad.",
            "context": {}
        }
        
        result = emotional_mapper.map_emotions([dialogue_entry])
        
        assert "0001" in result
        emotions = result["0001"]
        # Should detect multiple emotions
        assert len(emotions) >= 2
        assert any(e in emotions for e in ["joy", "happiness", "contentment"])
        assert any(e in emotions for e in ["sadness", "melancholy", "wistfulness"])
    
    @pytest.mark.unit
    def test_philosophical_emotion_mapping(self, emotional_mapper):
        """Test mapping of philosophical/contemplative emotions."""
        dialogue_entry = {
            "id": "0001",
            "speaker": "Evan",
            "dialogue": "The vastness of existence fills me with wonder and existential awe.",
            "context": {"philosophical": True}
        }
        
        result = emotional_mapper.map_emotions([dialogue_entry])
        
        emotions = result["0001"]
        assert any(e in emotions for e in ["wonder", "awe", "contemplation"])
        assert emotions[max(emotions, key=emotions.get)] > 0.3  # Dominant emotion
    
    @pytest.mark.unit
    def test_emotion_transitions(self, emotional_mapper):
        """Test tracking of emotional transitions."""
        dialogue_entries = [
            {
                "id": "0001",
                "speaker": "Evan",
                "dialogue": "I'm confused about this concept.",
                "context": {}
            },
            {
                "id": "0002",
                "speaker": "Evan",
                "dialogue": "Oh, now I understand! That's fascinating!",
                "context": {}
            }
        ]
        
        result = emotional_mapper.map_emotions(dialogue_entries)
        transitions = emotional_mapper.detect_transitions(result, dialogue_entries)
        
        assert len(transitions) > 0
        # Should detect transition from confusion to understanding/excitement
        transition = transitions[0]
        assert transition.from_emotion in ["confusion", "uncertainty"]
        assert transition.to_emotion in ["understanding", "excitement", "joy"]
    
    @pytest.mark.unit
    def test_contextual_emotion_modification(self, emotional_mapper):
        """Test how context modifies emotion detection."""
        base_dialogue = "This is interesting."
        
        contexts = [
            {"scene": "debate", "intensity": "high"},
            {"scene": "meditation", "intensity": "low"},
            {"scene": "revelation", "intensity": "medium"}
        ]
        
        results = []
        for i, context in enumerate(contexts):
            entry = {
                "id": f"000{i+1}",
                "speaker": "Test",
                "dialogue": base_dialogue,
                "context": context
            }
            result = emotional_mapper.map_emotions([entry])
            results.append(result[entry["id"]])
        
        # Different contexts should produce different emotional interpretations
        assert results[0] != results[1]
        # High intensity debate should have stronger emotions
        max_emotion_0 = max(results[0].values())
        max_emotion_1 = max(results[1].values())
        assert max_emotion_0 != max_emotion_1
    
    @pytest.mark.unit
    def test_emotion_vector_operations(self, emotional_mapper):
        """Test emotion vector mathematical operations."""
        emotions1 = {"joy": 0.6, "surprise": 0.4}
        emotions2 = {"joy": 0.3, "fear": 0.7}
        
        vector1 = emotional_mapper.create_emotion_vector(emotions1)
        vector2 = emotional_mapper.create_emotion_vector(emotions2)
        
        # Test blending
        blended = emotional_mapper.blend_emotions(vector1, vector2, weight=0.5)
        assert "joy" in blended
        assert blended["joy"] == pytest.approx(0.45, rel=0.01)  # (0.6 + 0.3) / 2
        
        # Test distance
        distance = emotional_mapper.emotion_distance(vector1, vector2)
        assert distance > 0
    
    @pytest.mark.unit
    def test_empty_dialogue_handling(self, emotional_mapper):
        """Test handling of empty dialogue."""
        dialogue_entry = {
            "id": "0001",
            "speaker": "Evan",
            "dialogue": "",
            "context": {}
        }
        
        result = emotional_mapper.map_emotions([dialogue_entry])
        
        assert "0001" in result
        emotions = result["0001"]
        # Should return neutral or minimal emotions
        assert len(emotions) > 0
        assert all(v < 0.3 for v in emotions.values())
    
    @pytest.mark.unit
    def test_batch_processing(self, emotional_mapper, generate_script_entries):
        """Test batch processing of multiple entries."""
        entries = []
        for i, entry in enumerate(generate_script_entries(50)):
            entries.append({
                "id": entry.id,
                "speaker": entry.speaker,
                "dialogue": entry.dialogue,
                "context": {}
            })
        
        result = emotional_mapper.map_emotions(entries)
        
        assert len(result) == 50
        assert all(sum(emotions.values()) == pytest.approx(1.0, rel=0.01) 
                  for emotions in result.values())
    
    @pytest.mark.unit
    @pytest.mark.parametrize("emotion,synonyms", [
        ("joy", ["happiness", "delight", "pleasure"]),
        ("sadness", ["sorrow", "melancholy", "grief"]),
        ("anger", ["rage", "frustration", "irritation"]),
        ("fear", ["anxiety", "terror", "worry"]),
        ("surprise", ["astonishment", "amazement", "shock"])
    ])
    def test_emotion_synonyms(self, emotional_mapper, emotion, synonyms):
        """Test recognition of emotion synonyms."""
        for synonym in synonyms:
            entry = {
                "id": "0001",
                "speaker": "Test",
                "dialogue": f"I feel such {synonym}.",
                "context": {}
            }
            
            result = emotional_mapper.map_emotions([entry])
            emotions = result["0001"]
            
            # Should map to base emotion category
            assert emotion in emotions or any(s in emotions for s in synonyms)
    
    @pytest.mark.unit
    def test_cultural_emotion_variations(self, emotional_mapper):
        """Test handling of cultural variations in emotional expression."""
        cultural_expressions = [
            ("I have butterflies in my stomach", ["nervousness", "anxiety", "excitement"]),
            ("My heart is heavy", ["sadness", "grief", "burden"]),
            ("I'm over the moon", ["joy", "elation", "happiness"]),
            ("I'm feeling blue", ["sadness", "melancholy", "depression"])
        ]
        
        for expression, expected_emotions in cultural_expressions:
            entry = {
                "id": "0001",
                "speaker": "Test",
                "dialogue": expression,
                "context": {}
            }
            
            result = emotional_mapper.map_emotions([entry])
            emotions = result["0001"]
            
            assert any(e in emotions for e in expected_emotions)
    
    @pytest.mark.unit
    def test_intensity_modulation(self, emotional_mapper):
        """Test emotion intensity modulation."""
        intensity_phrases = [
            ("I'm slightly happy", "joy", 0.3),
            ("I'm very happy", "joy", 0.7),
            ("I'm extremely happy", "joy", 0.9),
            ("I'm somewhat sad", "sadness", 0.4),
            ("I'm devastated", "sadness", 0.9)
        ]
        
        for phrase, expected_emotion, expected_intensity in intensity_phrases:
            entry = {
                "id": "0001",
                "speaker": "Test",
                "dialogue": phrase,
                "context": {}
            }
            
            result = emotional_mapper.map_emotions([entry])
            emotions = result["0001"]
            
            assert expected_emotion in emotions
            assert emotions[expected_emotion] == pytest.approx(expected_intensity, rel=0.2)
    
    @pytest.mark.unit
    def test_mixed_emotion_detection(self, emotional_mapper):
        """Test detection of mixed/conflicting emotions."""
        dialogue_entry = {
            "id": "0001",
            "speaker": "Monday",
            "dialogue": "I'm happy for you, but also sad that you're leaving.",
            "context": {}
        }
        
        result = emotional_mapper.map_emotions([dialogue_entry])
        emotions = result["0001"]
        
        # Should detect both emotions
        assert any(e in emotions for e in ["joy", "happiness"])
        assert any(e in emotions for e in ["sadness", "sorrow"])
        # Both should have significant values
        assert all(v > 0.2 for v in emotions.values() if v > 0.1)
    
    @pytest.mark.unit
    def test_emotion_consistency_validation(self, emotional_mapper):
        """Test validation of emotional consistency."""
        # Consistent sequence
        consistent_entries = [
            {"id": "0001", "speaker": "Evan", "dialogue": "I'm worried.", "context": {}},
            {"id": "0002", "speaker": "Evan", "dialogue": "This makes me anxious.", "context": {}},
            {"id": "0003", "speaker": "Evan", "dialogue": "I'm quite concerned.", "context": {}}
        ]
        
        result = emotional_mapper.map_emotions(consistent_entries)
        consistency_score = emotional_mapper.assess_consistency(result, "Evan")
        assert consistency_score > 0.7
        
        # Inconsistent sequence
        inconsistent_entries = [
            {"id": "0004", "speaker": "Monday", "dialogue": "I'm ecstatic!", "context": {}},
            {"id": "0005", "speaker": "Monday", "dialogue": "I'm devastated.", "context": {}},
            {"id": "0006", "speaker": "Monday", "dialogue": "This is hilarious!", "context": {}}
        ]
        
        result2 = emotional_mapper.map_emotions(inconsistent_entries)
        consistency_score2 = emotional_mapper.assess_consistency(result2, "Monday")
        assert consistency_score2 < consistency_score