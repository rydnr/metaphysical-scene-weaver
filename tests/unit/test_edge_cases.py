"""Comprehensive edge case tests for Metaphysical Scene Weaver."""

import pytest
import json
from pathlib import Path
from src.core.script_parser import ScriptParser
from src.processors.philosophical_interpreter import PhilosophicalInterpreter
from src.processors.emotional_mapper import EmotionalMapper
from src.core.scene_weaver import SceneWeaver
from src.core.quality_validator import QualityValidator, ValidationLevel


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    @pytest.fixture
    def edge_cases_data(self):
        """Load edge cases from fixture file."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "edge_cases.json"
        with open(fixture_path, 'r') as f:
            return json.load(f)
    
    @pytest.mark.edge_case
    @pytest.mark.parametrize("case_name,case_data", [
        ("empty_dialogue", {"input": "[0001] Evan: <<>>"}),
        ("empty_speaker", {"input": "[0001] : <<Hello world>>"}),
        ("empty_script", {"input": ""})
    ])
    def test_empty_inputs(self, script_parser, case_name, case_data):
        """Test handling of various empty inputs."""
        result = script_parser.parse_text(case_data["input"])
        
        if case_name == "empty_script":
            assert len(result) == 0
        else:
            # Should handle gracefully without crashing
            assert isinstance(result, list)
            if len(result) > 0:
                entry = result[0]
                if case_name == "empty_dialogue":
                    assert entry.dialogue == ""
                elif case_name == "empty_speaker":
                    assert entry.speaker in ["", "Unknown", None]
    
    @pytest.mark.edge_case
    def test_unicode_philosophical_symbols(self, script_parser, philosophical_interpreter):
        """Test parsing of unicode mathematical/logical symbols."""
        text = "[0001] Monday: <<∃x(Px ∧ Qx) → ∀y(Ry → Sy) - formal logic of existence>>"
        
        # Parser should handle unicode
        entries = script_parser.parse_text(text)
        assert len(entries) == 1
        assert "∃" in entries[0].dialogue
        assert "∀" in entries[0].dialogue
        
        # Philosophy interpreter should recognize logical notation
        result = philosophical_interpreter.interpret(entries[0].dialogue)
        assert len(result.concepts) > 0
        assert any(c.name.lower() in ["logic", "existence", "formal logic"] 
                  for c in result.concepts)
    
    @pytest.mark.edge_case
    def test_multilingual_content(self, script_parser, emotional_mapper):
        """Test handling of multilingual dialogue."""
        text = "[0001] Evan: <<什么是意识？ What is consciousness? Qu'est-ce que la conscience?>>"
        
        entries = script_parser.parse_text(text)
        assert len(entries) == 1
        
        # Should extract emotions despite mixed languages
        emotion_result = emotional_mapper.map_emotions([{
            "id": entries[0].id,
            "speaker": entries[0].speaker,
            "dialogue": entries[0].dialogue,
            "context": {}
        }])
        
        assert entries[0].id in emotion_result
        emotions = emotion_result[entries[0].id]
        assert len(emotions) > 0
        assert sum(emotions.values()) == pytest.approx(1.0, rel=0.01)
    
    @pytest.mark.edge_case
    def test_emoji_emotion_detection(self, emotional_mapper):
        """Test emotion detection from emojis."""
        test_cases = [
            ("😊😊😊", ["joy", "happiness"]),
            ("😢😭", ["sadness", "sorrow"]),
            ("😡🤬", ["anger", "rage"]),
            ("😨😱", ["fear", "terror"]),
            ("🤔💭", ["contemplation", "thinking"])
        ]
        
        for emojis, expected_emotions in test_cases:
            entry = {
                "id": "0001",
                "speaker": "Test",
                "dialogue": f"I feel {emojis}",
                "context": {}
            }
            
            result = emotional_mapper.map_emotions([entry])
            emotions = result["0001"]
            
            assert any(e in emotions for e in expected_emotions)
    
    @pytest.mark.edge_case
    def test_malformed_entry_recovery(self, script_parser):
        """Test recovery from various malformed entries."""
        malformed_scripts = [
            "[XXXX] Evan: <<Test>>",  # Invalid ID
            "0001 Evan: <<Missing brackets>>",  # Missing brackets
            "[0001] Evan: <<<<Nested>> markers>>",  # Nested markers
            "[0001] Evan: <<Unclosed dialogue",  # Unclosed dialogue
            "[0001] [0002] Evan: <<Multiple IDs>>",  # Multiple IDs
        ]
        
        for script in malformed_scripts:
            # Should not crash
            result = script_parser.parse_text(script)
            assert isinstance(result, list)
            # May or may not parse successfully, but shouldn't raise exception
    
    @pytest.mark.edge_case
    @pytest.mark.slow
    def test_very_long_dialogue(self, script_parser, scene_weaver):
        """Test handling of extremely long dialogue entries."""
        # Create a very long philosophical monologue
        long_text = " ".join([
            "The nature of consciousness and its relationship to physical reality"
            "has puzzled philosophers for millennia."
        ] * 100)  # ~1000 words
        
        script = f"[0001] Evan: <<{long_text}>>"
        
        # Parser should handle without issues
        entries = script_parser.parse_text(script)
        assert len(entries) == 1
        assert len(entries[0].dialogue) > 1000
        
        # Full pipeline should process (might truncate)
        result = scene_weaver.process_script(script)
        assert result is not None
        assert "prompts" in result
    
    @pytest.mark.edge_case
    def test_circular_references(self, script_parser, context_analyzer):
        """Test handling of circular references in dialogue."""
        script = """
        [0001] Evan: <<As I said in entry 0001, recursion is strange.>>
        [0002] Monday: <<See my response in 0003.>>
        [0003] Monday: <<As I mentioned in 0002, it's all connected.>>
        """
        
        entries = script_parser.parse_text(script)
        assert len(entries) == 3
        
        # Context analyzer should handle circular refs without infinite loops
        context = context_analyzer.analyze_context(entries)
        assert context is not None
        # Should detect the circular reference pattern
    
    @pytest.mark.edge_case
    def test_contradictory_metadata(self, script_parser):
        """Test handling of contradictory metadata."""
        test_cases = [
            "[0001] [2-panel] [3-panel] Evan: <<Multiple panel counts>>",
            "[0001] Evan: <<Happy!>> [[sadness]] [[joy]]",
            "[0001] Evan: <<Test>> (smiles) (frowns)"
        ]
        
        for script in test_cases:
            entries = script_parser.parse_text(script)
            assert len(entries) > 0
            # Should pick one interpretation consistently
    
    @pytest.mark.edge_case
    def test_duplicate_entry_ids(self, script_parser):
        """Test handling of duplicate entry IDs."""
        script = """
        [0001] Evan: <<First entry>>
        [0001] Monday: <<Duplicate ID>>
        [0002] Evan: <<Normal entry>>
        """
        
        entries = script_parser.parse_text(script)
        # Should handle duplicates (rename, skip, or merge)
        assert len(entries) >= 2
        # All entries should have unique IDs after processing
        ids = [e.id for e in entries]
        assert len(ids) == len(set(ids))
    
    @pytest.mark.edge_case
    def test_nonsense_philosophy(self, philosophical_interpreter):
        """Test handling of nonsensical philosophical statements."""
        nonsense_statements = [
            "Colorless green ideas sleep furiously in the void of meaning.",
            "The Thursday of consciousness walks backwards through time's door.",
            "If nothing is everything, then purple equals democracy."
        ]
        
        for statement in nonsense_statements:
            result = philosophical_interpreter.interpret(statement)
            
            # Should attempt interpretation
            assert result is not None
            # But with low confidence
            assert result.confidence < 0.5
            # Might extract some concepts
            if result.concepts:
                # Concepts should have low confidence too
                assert all(c.confidence < 0.6 for c in result.concepts)
    
    @pytest.mark.edge_case
    def test_emotional_overload(self, emotional_mapper):
        """Test handling of too many emotions in one entry."""
        entry = {
            "id": "0001",
            "speaker": "Evan",
            "dialogue": "I'm happy, sad, angry, fearful, surprised, disgusted, "
                       "contemplative, confused, excited, and exhausted!",
            "context": {}
        }
        
        result = emotional_mapper.map_emotions([entry])
        emotions = result["0001"]
        
        # Should include multiple emotions
        assert len(emotions) >= 5
        # But still sum to 1.0
        assert sum(emotions.values()) == pytest.approx(1.0, rel=0.01)
        # No single emotion should dominate completely
        assert all(v < 0.5 for v in emotions.values())
    
    @pytest.mark.edge_case
    def test_character_personality_inconsistency(self, character_tracker):
        """Test detection of character personality shifts."""
        # Setup wise sage character
        from src.core.character_state_tracker import CharacterProfile, ArchetypePattern
        
        profile = CharacterProfile(
            name="Monday",
            archetype=ArchetypePattern.SAGE,
            core_traits=["wise", "calm", "knowing"],
            emotional_baseline={"serenity": 0.7, "contemplation": 0.3}
        )
        character_tracker.add_character(profile)
        
        # Test consistent behavior
        character_tracker.update_emotional_state(
            "Monday", "0001", {"serenity": 0.6, "contemplation": 0.4}
        )
        
        # Test inconsistent behavior
        is_consistent = character_tracker.validate_consistency(
            "Monday", {"rage": 0.8, "hatred": 0.2}
        )
        assert is_consistent is False
    
    @pytest.mark.edge_case
    def test_missing_character_introduction(self, scene_weaver):
        """Test handling of characters appearing without introduction."""
        script = """
        [0001] Evan: <<Who are you?>>
        [0050] Mysterious_Stranger: <<I've been here all along.>>
        [0051] Evan: <<But you just appeared!>>
        """
        
        result = scene_weaver.process_script(script)
        
        # Should handle new character gracefully
        assert result is not None
        assert "character_states" in result
        assert "Mysterious_Stranger" in result["character_states"]
    
    @pytest.mark.edge_case
    @pytest.mark.performance
    def test_rapid_speaker_alternation(self, script_parser, performance_threshold):
        """Test performance with rapid speaker changes."""
        speakers = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        entries = []
        
        for i in range(100):
            speaker = speakers[i % len(speakers)]
            entries.append(f"[{i+1:04d}] {speaker}: <<Quick statement {i}>>")
        
        script = "\n".join(entries)
        
        import time
        start = time.time()
        result = script_parser.parse_text(script)
        elapsed = time.time() - start
        
        assert len(result) == 100
        assert elapsed < performance_threshold["script_parsing"] * 2
    
    @pytest.mark.edge_case
    def test_deeply_nested_philosophy(self, philosophical_interpreter):
        """Test handling of deeply nested philosophical concepts."""
        # Build nested philosophical statement
        concepts = ["consciousness", "emergence", "complexity", "understanding", 
                   "reality", "perception", "knowledge", "existence"]
        
        statement = "If"
        for i, concept in enumerate(concepts):
            statement += f" ({concept} implies"
        statement += " truth" + ")" * len(concepts)
        
        result = philosophical_interpreter.interpret(statement)
        
        # Should parse without stack overflow
        assert result is not None
        # Should identify multiple concepts
        assert len(result.concepts) >= 3
    
    @pytest.mark.edge_case
    def test_quality_validation_edge_cases(self):
        """Test quality validator with edge case outputs."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Test with empty data
        empty_output = {
            "philosophical_concepts": [],
            "dialogue_text": "",
            "emotion_mappings": {},
            "prompts": []
        }
        
        report = validator.validate_complete_output(empty_output)
        assert report.passed is False
        assert report.overall_score < 0.5
        
        # Test with invalid emotion probabilities
        invalid_emotions = {
            "emotion_mappings": {
                "0001": {"joy": 0.6, "sadness": 0.6}  # Sum > 1.0
            },
            "dialogue_entries": [{"id": "0001", "dialogue": "Test"}]
        }
        
        emotion_result = validator.validate_emotion_mapping(
            invalid_emotions["emotion_mappings"],
            invalid_emotions["dialogue_entries"]
        )
        assert emotion_result.passed is False
        assert len(emotion_result.errors) > 0