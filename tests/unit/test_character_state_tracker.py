"""Unit tests for the CharacterStateTracker module."""

import pytest
from src.core.character_state_tracker import (
    CharacterStateTracker, 
    CharacterProfile, 
    CharacterArc,
    EmotionalState,
    PhilosophicalStance,
    CharacterRelationship,
    ArchetypePattern
)


class TestCharacterStateTracker:
    """Test cases for CharacterStateTracker."""
    
    @pytest.mark.unit
    def test_initialization(self, character_tracker):
        """Test tracker initialization."""
        assert isinstance(character_tracker, CharacterStateTracker)
        assert character_tracker.profiles == {}
        assert character_tracker.relationships == {}
        assert character_tracker.global_timeline == []
    
    @pytest.mark.unit
    def test_add_character_profile(self, character_tracker):
        """Test adding a character profile."""
        profile = CharacterProfile(
            name="Evan",
            archetype=ArchetypePattern.SEEKER,
            core_traits=["curious", "introspective"],
            philosophical_leanings=["existentialism", "phenomenology"],
            emotional_baseline={"contemplation": 0.6, "wonder": 0.4}
        )
        
        character_tracker.add_character(profile)
        
        assert "Evan" in character_tracker.profiles
        assert character_tracker.profiles["Evan"] == profile
    
    @pytest.mark.unit
    def test_update_emotional_state(self, character_tracker):
        """Test updating character emotional state."""
        # Add character first
        profile = CharacterProfile(
            name="Monday",
            archetype=ArchetypePattern.SAGE,
            core_traits=["wise", "enigmatic"],
            philosophical_leanings=["zen", "absurdism"]
        )
        character_tracker.add_character(profile)
        
        # Update emotional state
        new_emotions = {"serenity": 0.7, "amusement": 0.3}
        character_tracker.update_emotional_state("Monday", "0001", new_emotions)
        
        # Check state was updated
        assert "Monday" in character_tracker.states
        assert character_tracker.states["Monday"].current_emotions == new_emotions
        assert len(character_tracker.states["Monday"].emotional_history) == 1
    
    @pytest.mark.unit
    def test_track_philosophical_evolution(self, character_tracker):
        """Test tracking philosophical stance evolution."""
        # Setup character
        profile = CharacterProfile(
            name="Evan",
            archetype=ArchetypePattern.SEEKER,
            philosophical_leanings=["existentialism"]
        )
        character_tracker.add_character(profile)
        
        # Track philosophical evolution
        stance = PhilosophicalStance(
            primary_concepts=["consciousness", "emergence"],
            certainty_level=0.7,
            contradictions=[]
        )
        character_tracker.track_philosophical_evolution("Evan", "0002", stance)
        
        # Verify tracking
        assert "Evan" in character_tracker.states
        state = character_tracker.states["Evan"]
        assert len(state.philosophical_evolution) == 1
        assert state.philosophical_evolution[0][1] == stance
    
    @pytest.mark.unit
    def test_character_relationship_tracking(self, character_tracker):
        """Test relationship tracking between characters."""
        # Add two characters
        evan = CharacterProfile(name="Evan", archetype=ArchetypePattern.SEEKER)
        monday = CharacterProfile(name="Monday", archetype=ArchetypePattern.SAGE)
        character_tracker.add_character(evan)
        character_tracker.add_character(monday)
        
        # Create relationship
        relationship = CharacterRelationship(
            character_a="Evan",
            character_b="Monday",
            relationship_type="student-teacher",
            tension_level=0.3,
            harmony_level=0.8
        )
        character_tracker.add_relationship(relationship)
        
        # Check relationship storage
        key = ("Evan", "Monday")
        assert key in character_tracker.relationships
        assert character_tracker.relationships[key] == relationship
    
    @pytest.mark.unit
    def test_get_character_state(self, character_tracker):
        """Test retrieving current character state."""
        # Setup character with state
        profile = CharacterProfile(
            name="Evan",
            archetype=ArchetypePattern.SEEKER,
            emotional_baseline={"curiosity": 0.8}
        )
        character_tracker.add_character(profile)
        character_tracker.update_emotional_state("Evan", "0001", {"wonder": 0.9})
        
        # Get state
        state = character_tracker.get_character_state("Evan")
        
        assert state is not None
        assert state.character_name == "Evan"
        assert state.current_emotions == {"wonder": 0.9}
    
    @pytest.mark.unit
    def test_predict_character_response(self, character_tracker):
        """Test character response prediction."""
        # Setup character
        profile = CharacterProfile(
            name="Monday",
            archetype=ArchetypePattern.SAGE,
            core_traits=["wise", "cryptic"],
            philosophical_leanings=["zen", "paradox"]
        )
        character_tracker.add_character(profile)
        
        # Test prediction
        context = {
            "topic": "consciousness",
            "emotional_context": {"contemplation": 0.8}
        }
        
        response = character_tracker.predict_character_response("Monday", context)
        
        assert "emotional_tendency" in response
        assert "philosophical_alignment" in response
        assert "likely_response_pattern" in response
    
    @pytest.mark.unit
    def test_character_arc_detection(self, character_tracker):
        """Test detection of character arc patterns."""
        # Setup character with evolution
        profile = CharacterProfile(
            name="Evan",
            archetype=ArchetypePattern.SEEKER
        )
        character_tracker.add_character(profile)
        
        # Simulate character evolution
        emotions_sequence = [
            {"confusion": 0.8, "curiosity": 0.2},
            {"confusion": 0.5, "curiosity": 0.5},
            {"understanding": 0.3, "curiosity": 0.7},
            {"understanding": 0.8, "satisfaction": 0.2}
        ]
        
        for i, emotions in enumerate(emotions_sequence):
            character_tracker.update_emotional_state("Evan", f"000{i+1}", emotions)
        
        # Detect arc
        arc = character_tracker.detect_character_arc("Evan")
        
        assert arc is not None
        assert arc.arc_type in ["growth", "revelation", "transformation"]
        assert arc.key_moments is not None
    
    @pytest.mark.unit
    def test_nonexistent_character_handling(self, character_tracker):
        """Test handling of operations on non-existent characters."""
        # Try to get state of non-existent character
        state = character_tracker.get_character_state("NonExistent")
        assert state is None
        
        # Try to update non-existent character
        with pytest.raises(KeyError):
            character_tracker.update_emotional_state("NonExistent", "0001", {})
    
    @pytest.mark.unit
    def test_character_consistency_validation(self, character_tracker):
        """Test validation of character consistency."""
        # Setup character
        profile = CharacterProfile(
            name="Monday",
            archetype=ArchetypePattern.SAGE,
            core_traits=["wise", "calm"],
            emotional_baseline={"serenity": 0.8, "contemplation": 0.2}
        )
        character_tracker.add_character(profile)
        
        # Test consistent behavior
        consistent_emotions = {"serenity": 0.7, "contemplation": 0.3}
        is_consistent = character_tracker.validate_consistency(
            "Monday", consistent_emotions
        )
        assert is_consistent is True
        
        # Test inconsistent behavior
        inconsistent_emotions = {"rage": 0.9, "hatred": 0.1}
        is_consistent = character_tracker.validate_consistency(
            "Monday", inconsistent_emotions
        )
        assert is_consistent is False
    
    @pytest.mark.unit
    def test_timeline_tracking(self, character_tracker):
        """Test global timeline tracking."""
        # Add characters
        evan = CharacterProfile(name="Evan", archetype=ArchetypePattern.SEEKER)
        monday = CharacterProfile(name="Monday", archetype=ArchetypePattern.SAGE)
        character_tracker.add_character(evan)
        character_tracker.add_character(monday)
        
        # Add timeline events
        character_tracker.add_timeline_event("0001", "Evan", "asked_question", 
                                           {"topic": "consciousness"})
        character_tracker.add_timeline_event("0002", "Monday", "provided_insight",
                                           {"wisdom": "emergent_complexity"})
        
        # Check timeline
        assert len(character_tracker.global_timeline) == 2
        assert character_tracker.global_timeline[0]["entry_id"] == "0001"
        assert character_tracker.global_timeline[1]["character"] == "Monday"
    
    @pytest.mark.unit
    @pytest.mark.parametrize("archetype,expected_traits", [
        (ArchetypePattern.SEEKER, ["curious", "questioning"]),
        (ArchetypePattern.SAGE, ["wise", "knowing"]),
        (ArchetypePattern.REBEL, ["challenging", "unconventional"]),
        (ArchetypePattern.INNOCENT, ["pure", "optimistic"])
    ])
    def test_archetype_patterns(self, character_tracker, archetype, expected_traits):
        """Test different archetype patterns."""
        profile = CharacterProfile(
            name="TestChar",
            archetype=archetype,
            core_traits=expected_traits
        )
        character_tracker.add_character(profile)
        
        retrieved = character_tracker.profiles["TestChar"]
        assert retrieved.archetype == archetype
        assert any(trait in retrieved.core_traits for trait in expected_traits)