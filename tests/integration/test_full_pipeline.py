"""Integration tests for the full Metaphysical Scene Weaver pipeline."""

import pytest
import asyncio
from pathlib import Path
from src.core.scene_weaver import SceneWeaver
from src.core.quality_validator import QualityValidator, ValidationLevel


class TestFullPipeline:
    """Integration tests for complete processing pipeline."""
    
    @pytest.mark.integration
    def test_simple_script_processing(self, scene_weaver):
        """Test processing a simple philosophical script."""
        script = """
        [0001] Evan: <<What is consciousness?>>
        [0002] Monday: <<Perhaps it's the universe experiencing itself.>>
        [0003] Evan: <<That's beautiful, but is it true?>>
        """
        
        result = scene_weaver.process_script(script)
        
        # Verify all components produced output
        assert result is not None
        assert "entries" in result
        assert "philosophical_analysis" in result
        assert "emotional_mapping" in result
        assert "prompts" in result
        assert "scene_synthesis" in result
        
        # Verify basic content
        assert len(result["entries"]) == 3
        assert any("consciousness" in str(concept).lower() 
                  for concept in result["philosophical_analysis"].get("concepts", []))
    
    @pytest.mark.integration
    def test_complex_philosophical_dialogue(self, scene_weaver):
        """Test processing complex philosophical dialogue with multiple concepts."""
        script = """
        [0001] Evan: <<If free will is an illusion, what does that mean for moral responsibility?>>
        [0002] Monday: <<Perhaps the illusion itself is necessary for the functioning of consciousness.>> (thoughtful pause)
        [0003] Evan: <<So we're trapped in a paradox - needing to believe in something that might not exist?>>
        [0004] [2-panel] Monday: <<Not trapped, dancing. The paradox is the music.>> [[philosophical metaphor]]
        """
        
        result = scene_weaver.process_script(script)
        
        # Check philosophical concepts detected
        concepts = result["philosophical_analysis"].get("concepts", [])
        concept_names = [c.get("name", "").lower() for c in concepts]
        
        assert any("free will" in c or "free_will" in c for c in concept_names)
        assert any("consciousness" in c for c in concept_names)
        assert any("paradox" in c for c in concept_names)
        
        # Check emotional progression
        emotions = result["emotional_mapping"]
        assert len(emotions) == 4
        
        # Check prompt generation
        prompts = result["prompts"]
        assert len(prompts) >= 4
        assert any("paradox" in p.lower() or "dancing" in p.lower() for p in prompts)
    
    @pytest.mark.integration
    def test_character_consistency_across_pipeline(self, scene_weaver):
        """Test character consistency throughout the pipeline."""
        script = """
        [0001] Evan: <<I'm searching for meaning in an absurd universe.>>
        [0002] Monday: <<The search itself creates the meaning, young seeker.>>
        [0003] Evan: <<But that feels like circular reasoning!>>
        [0004] Monday: <<All the best truths are circles.>> (enigmatic smile)
        [0005] Evan: <<You always speak in riddles, Monday.>>
        """
        
        result = scene_weaver.process_script(script)
        
        # Check character tracking
        character_states = result.get("character_states", {})
        assert "Evan" in character_states
        assert "Monday" in character_states
        
        # Verify character consistency in prompts
        prompts = result["prompts"]
        evan_prompts = [p for p in prompts if "Evan" in p or "searching" in p or "seeker" in p]
        monday_prompts = [p for p in prompts if "Monday" in p or "enigmatic" in p or "wise" in p]
        
        assert len(evan_prompts) >= 2
        assert len(monday_prompts) >= 2
    
    @pytest.mark.integration
    def test_metaphor_integration(self, scene_weaver):
        """Test metaphor detection and visual translation."""
        script = """
        [0001] Monday: <<Life is a river that knows its destination but forgets its source.>>
        [0002] Evan: <<And we're just drops in that river?>>
        [0003] Monday: <<We are the river dreaming it's made of drops.>>
        """
        
        result = scene_weaver.process_script(script)
        
        # Check metaphor detection
        metaphors = result.get("metaphors", [])
        assert len(metaphors) > 0
        assert any("river" in str(m).lower() for m in metaphors)
        
        # Check visual translation in prompts
        prompts = result["prompts"]
        assert any("river" in p.lower() or "water" in p.lower() or "flow" in p.lower() 
                  for p in prompts)
    
    @pytest.mark.integration
    def test_scene_synthesis_coherence(self, scene_weaver):
        """Test coherence of synthesized scenes."""
        script = """
        [0001] Evan: <<The night sky makes me feel so small.>>
        [0002] Monday: <<Or perhaps it reveals how vast you truly are.>>
        [0003] Evan: <<I never thought of it that way.>> (looks up with wonder)
        [0004] Monday: <<The stars don't diminish us. They remind us we're made of the same light.>>
        """
        
        result = scene_weaver.process_script(script)
        
        # Check scene synthesis
        synthesis = result["scene_synthesis"]
        assert "scenes" in synthesis
        
        scenes = synthesis["scenes"]
        assert len(scenes) >= 1
        
        # Verify visual coherence
        first_scene = scenes[0]
        assert "setting" in first_scene
        assert "night" in first_scene["setting"].lower() or "stars" in first_scene["setting"].lower()
    
    @pytest.mark.integration
    def test_quality_validation_integration(self, scene_weaver):
        """Test integration with quality validation system."""
        script = """
        [0001] Evan: <<What is the self?>>
        [0002] Monday: <<A story we tell about the patterns we notice.>>
        [0003] Evan: <<But who's telling the story?>>
        [0004] Monday: <<Another story, all the way down.>> (chuckles)
        """
        
        # Process script
        result = scene_weaver.process_script(script)
        
        # Validate output
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Prepare validation data
        output_data = {
            "philosophical_concepts": [c.get("name", "") for c in result["philosophical_analysis"].get("concepts", [])],
            "dialogue_text": script,
            "emotion_mappings": result["emotional_mapping"],
            "dialogue_entries": result["entries"],
            "prompts": result["prompts"]
        }
        
        report = validator.validate_complete_output(output_data)
        
        assert report.overall_score > 0.7
        assert report.passed is True
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_processing(self, scene_weaver):
        """Test concurrent processing of multiple scripts."""
        scripts = [
            "[0001] Evan: <<Is reality objective or subjective?>>",
            "[0001] Monday: <<Time is an illusion, but a persistent one.>>",
            "[0001] Evan: <<Can machines truly think?>>",
            "[0001] Monday: <<Consciousness might be substrate-independent.>>"
        ]
        
        # Process scripts concurrently
        tasks = [asyncio.create_task(
            asyncio.to_thread(scene_weaver.process_script, script)
        ) for script in scripts]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 4
        assert all(r is not None for r in results)
        assert all("prompts" in r for r in results)
    
    @pytest.mark.integration
    def test_error_recovery(self, scene_weaver):
        """Test pipeline error recovery and graceful degradation."""
        # Script with various problematic elements
        problematic_script = """
        [XXXX] : <<>>
        [0002] NoName: <<Regular dialogue>>
        [0003] 
        [0004] Evan: <<Normal entry after errors>>
        """
        
        result = scene_weaver.process_script(problematic_script)
        
        # Should still process valid entries
        assert result is not None
        assert len(result["entries"]) >= 2  # At least entries 0002 and 0004
        assert "prompts" in result
        assert len(result["prompts"]) >= 2
    
    @pytest.mark.integration
    def test_context_preservation(self, scene_weaver):
        """Test context preservation across dialogue entries."""
        script = """
        [0001] Evan: <<Let's discuss the nature of time.>>
        [0002] Monday: <<Time is a dimension we experience sequentially.>>
        [0003] Evan: <<But why only forward?>>
        [0004] Monday: <<Entropy gives time its arrow.>>
        [0005] Evan: <<So without entropy, time has no direction?>>
        """
        
        result = scene_weaver.process_script(script)
        
        # Check context tracking
        contexts = result.get("context_analysis", {})
        
        # Verify thematic consistency
        prompts = result["prompts"]
        time_related = sum(1 for p in prompts if any(
            word in p.lower() for word in ["time", "temporal", "entropy", "arrow", "direction"]
        ))
        
        assert time_related >= 3  # Most prompts should maintain temporal theme
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_script_processing(self, scene_weaver, generate_script_entries):
        """Test processing of large scripts."""
        # Generate a large script
        entries = generate_script_entries(100)
        script_lines = []
        
        for entry in entries:
            line = f"[{entry.id}] {entry.speaker}: <<{entry.dialogue}>>"
            if entry.metadata:
                line += f" [[{entry.metadata[0]}]]"
            script_lines.append(line)
        
        large_script = "\n".join(script_lines)
        
        result = scene_weaver.process_script(large_script)
        
        assert result is not None
        assert len(result["entries"]) == 100
        assert len(result["prompts"]) >= 100
        assert "philosophical_analysis" in result
        assert "emotional_mapping" in result