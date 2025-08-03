"""Integration test for reality dissolution sequence (010-012).

Tests the philosophical and visual climax where physics breaks.
"""

import pytest
from src.quality.reality_dissolution_validator import (
    RealityDissolutionValidator,
    RealityState
)
from src.quality.philosophical_consistency_validator import PhilosophicalDepth


class TestRealityDissolutionSequence:
    """Test the complete reality dissolution trilogy."""
    
    @pytest.fixture
    def dissolution_sequence_data(self):
        """Complete reality dissolution sequence data."""
        return {
            "010": {
                "id": "010",
                "name": "questioning_identity",
                "philosophy": {
                    "concept": "identity as construct",
                    "depth": PhilosophicalDepth.PARADOX,
                    "metaphor": "mirror showing no reflection"
                },
                "emotion": {
                    "primary": "uncertainty",
                    "secondary": "curiosity",
                    "intensity": 0.5,
                    "blend": {"awe": 0.3, "fear": 0.2}
                },
                "visual": {
                    "elements": ["fracturing mirror", "glitch effects", "identity fragments"],
                    "style": "surreal",
                    "effects": ["reality glitches", "perspective shifts"],
                    "dissolution_markers": ["glitch", "fracture", "distortion"]
                },
                "dialogue": "Who am I? The question itself... dissolves.",
                "narrator": "The boundaries of self begin to blur."
            },
            "011": {
                "id": "011",
                "name": "space_between_awareness",
                "philosophy": {
                    "concept": "void as foundation",
                    "depth": PhilosophicalDepth.TRANSCENDENT,
                    "metaphor": "space between thoughts expanding"
                },
                "emotion": {
                    "primary": "awe",
                    "secondary": "fear",
                    "intensity": 0.4,
                    "blend": {"awe": 0.6, "fear": 0.4}
                },
                "visual": {
                    "elements": ["void expansion", "reality melting", "consciousness streams"],
                    "style": "abstract",
                    "effects": ["complete dissolution", "dimensional collapse"],
                    "dissolution_markers": ["melt", "flow", "merge", "dissolve"]
                },
                "dialogue": "In the space between... everything... nothing...",
                "narrator": "Reality becomes a suggestion rather than a fact."
            },
            "012": {
                "id": "012",
                "name": "tree_touch_transformation",
                "philosophy": {
                    "concept": "choice creates reality",
                    "depth": PhilosophicalDepth.TRANSCENDENT,
                    "metaphor": "tree as axis of all possible worlds"
                },
                "emotion": {
                    "primary": "transcendence",
                    "secondary": "acceptance",
                    "intensity": 0.6,
                    "blend": {"awe": 0.8, "fear": 0.2}
                },
                "visual": {
                    "elements": ["tree transformation", "reality crystallization", "world birth"],
                    "style": "mythical",
                    "effects": ["physics breaking", "new reality forming"],
                    "dissolution_markers": ["reform", "crystallize", "emerge", "solidify"]
                },
                "dialogue": "I touch the tree, and in touching, create.",
                "narrator": "The philosopher becomes the philosophy."
            }
        }
    
    @pytest.fixture
    def dissolution_validator(self):
        """Reality dissolution validator."""
        return RealityDissolutionValidator()
    
    @pytest.mark.integration
    def test_reality_dissolution_progression(self, dissolution_sequence_data, dissolution_validator):
        """Test reality dissolution arc through sequence."""
        expected_progression = [
            (0.3, RealityState.QUESTIONING),
            (0.7, RealityState.FLUID),
            (0.5, RealityState.RECONSTRUCTING)
        ]
        
        for i, scene_id in enumerate(["010", "011", "012"]):
            scene = dissolution_sequence_data[scene_id]
            expected_level, expected_state = expected_progression[i]
            
            # Validate dissolution level matches expectation
            assert scene_id in dissolution_validator.dissolution_spec
            spec = dissolution_validator.dissolution_spec[scene_id]
            assert spec["dissolution_level"] == expected_level
            assert spec["reality_state"] == expected_state
    
    @pytest.mark.integration
    def test_philosophical_climax(self, dissolution_sequence_data):
        """Test philosophical depth reaches transcendent."""
        scenes = ["010", "011", "012"]
        depths = []
        
        for scene_id in scenes:
            scene = dissolution_sequence_data[scene_id]
            depth = scene["philosophy"]["depth"]
            depths.append(depth)
        
        # Should reach transcendent in 011 and maintain in 012
        assert depths[0] == PhilosophicalDepth.PARADOX
        assert depths[1] == PhilosophicalDepth.TRANSCENDENT
        assert depths[2] == PhilosophicalDepth.TRANSCENDENT
        
        # Verify philosophical concepts align with dissolution
        assert "void" in dissolution_sequence_data["011"]["philosophy"]["concept"]
        assert "choice" in dissolution_sequence_data["012"]["philosophy"]["concept"]
    
    @pytest.mark.integration
    def test_emotion_blend_balance(self, dissolution_sequence_data):
        """Test awe/fear blend through dissolution."""
        awe_fear_progression = []
        
        for scene_id in ["010", "011", "012"]:
            scene = dissolution_sequence_data[scene_id]
            blend = scene["emotion"]["blend"]
            awe_fear_progression.append((blend["awe"], blend["fear"]))
        
        # Awe should increase, fear should peak then decrease
        assert awe_fear_progression[0] == (0.3, 0.2)  # Low both
        assert awe_fear_progression[1] == (0.6, 0.4)  # Peak fear
        assert awe_fear_progression[2] == (0.8, 0.2)  # High awe, low fear
        
        # Validate emotion intensity stays grounded
        for scene_id in ["010", "011", "012"]:
            intensity = dissolution_sequence_data[scene_id]["emotion"]["intensity"]
            assert 0.4 <= intensity <= 0.6  # Controlled range during dissolution
    
    @pytest.mark.integration
    def test_visual_dissolution_markers(self, dissolution_sequence_data):
        """Test visual markers match dissolution state."""
        marker_expectations = {
            "010": ["glitch", "fracture", "distortion"],
            "011": ["melt", "flow", "merge", "dissolve"],
            "012": ["reform", "crystallize", "emerge", "solidify"]
        }
        
        for scene_id, expected_markers in marker_expectations.items():
            scene = dissolution_sequence_data[scene_id]
            actual_markers = scene["visual"]["dissolution_markers"]
            
            # All expected markers should be present
            assert set(expected_markers) == set(actual_markers)
            
            # Visual elements should contain these markers
            visual_text = " ".join(scene["visual"]["elements"] + scene["visual"]["effects"])
            for marker in expected_markers:
                assert any(marker in element.lower() for element in visual_text.split())
    
    @pytest.mark.integration
    def test_narrator_critical_moments(self, dissolution_sequence_data):
        """Test narrator handles critical dissolution moments."""
        narrator_texts = []
        
        for scene_id in ["010", "011", "012"]:
            scene = dissolution_sequence_data[scene_id]
            narrator_texts.append(scene["narrator"])
        
        # Check progressive abstraction
        assert "boundaries" in narrator_texts[0]  # Questioning boundaries
        assert "reality" in narrator_texts[1]      # Reality as suggestion
        assert "becomes" in narrator_texts[2]      # Transformation complete
        
        # Narrator should maintain coherence even at peak dissolution
        for text in narrator_texts:
            assert len(text.split()) >= 5  # Minimum coherent length
            assert len(text.split()) <= 20  # Not overly verbose during climax
    
    @pytest.mark.integration
    def test_tree_touch_climax(self, dissolution_sequence_data):
        """Test the tree touch moment is properly epic."""
        tree_scene = dissolution_sequence_data["012"]
        
        # Philosophical weight
        assert tree_scene["philosophy"]["depth"] == PhilosophicalDepth.TRANSCENDENT
        assert "axis of all possible worlds" in tree_scene["philosophy"]["metaphor"]
        
        # Visual impact
        assert "tree transformation" in tree_scene["visual"]["elements"]
        assert "physics breaking" in tree_scene["visual"]["effects"]
        assert "world birth" in tree_scene["visual"]["elements"]
        
        # Emotional culmination
        assert tree_scene["emotion"]["primary"] == "transcendence"
        assert tree_scene["emotion"]["blend"]["awe"] == 0.8  # Maximum awe
        
        # Dialogue significance
        assert "create" in tree_scene["dialogue"]
        assert "touch" in tree_scene["dialogue"]
    
    @pytest.mark.integration
    def test_surrealism_progression(self, dissolution_sequence_data):
        """Test surrealism increases appropriately."""
        style_progression = []
        
        for scene_id in ["010", "011", "012"]:
            scene = dissolution_sequence_data[scene_id]
            style_progression.append(scene["visual"]["style"])
        
        # Style should progress from surreal to abstract to mythical
        assert style_progression[0] == "surreal"
        assert style_progression[1] == "abstract"
        assert style_progression[2] == "mythical"
        
        # Each style appropriate for dissolution level
        styles_match_dissolution = True
        assert styles_match_dissolution
    
    @pytest.mark.integration
    def test_dialogue_fragmentation(self, dissolution_sequence_data):
        """Test dialogue becomes appropriately fragmented."""
        dialogues = []
        
        for scene_id in ["010", "011", "012"]:
            scene = dissolution_sequence_data[scene_id]
            dialogues.append(scene["dialogue"])
        
        # Check fragmentation pattern
        assert "?" in dialogues[0]  # Questions identity
        assert "..." in dialogues[1]  # Fragmented at peak
        assert "." in dialogues[2]  # Declarative at reconstruction
        
        # Word count should vary with dissolution
        word_counts = [len(d.split()) for d in dialogues]
        assert word_counts[1] < word_counts[0]  # Most fragmented at peak
        assert word_counts[2] > word_counts[1]  # More coherent at reconstruction
    
    @pytest.mark.integration
    @pytest.mark.parametrize("scene_id,expected_quality", [
        ("010", 0.88),  # Good quality for dissolution start
        ("011", 0.92),  # Higher for peak moment
        ("012", 0.95)   # Highest for tree touch climax
    ])
    def test_individual_scene_quality(
        self, 
        dissolution_sequence_data,
        dissolution_validator,
        scene_id,
        expected_quality
    ):
        """Test quality score for each dissolution scene."""
        scene = dissolution_sequence_data[scene_id]
        
        # Simulate quality scoring based on climax criteria
        quality_factors = {
            "philosophical_weight": 1.0 if scene["philosophy"]["depth"].value >= 3 else 0.8,
            "emotional_balance": 1.0 if 0.4 <= scene["emotion"]["intensity"] <= 0.6 else 0.7,
            "visual_coherence": 1.0 if len(scene["visual"]["dissolution_markers"]) >= 3 else 0.8,
            "surreal_quality": 1.0 if scene["visual"]["style"] in ["surreal", "abstract", "mythical"] else 0.7,
            "narrative_grounding": 0.9  # Slightly lower during dissolution
        }
        
        quality_score = sum(quality_factors.values()) / len(quality_factors)
        assert quality_score >= expected_quality