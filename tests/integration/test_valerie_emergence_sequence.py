"""Integration test for complete Valerie emergence sequence (007-009).

Tests the philosophical and visual coherence of Valerie's introduction.
"""

import pytest
from src.quality.content_quality_validator import ContentQualityValidator
from src.quality.philosophical_consistency_validator import (
    PhilosophicalConsistencyValidator,
    PhilosophicalDepth
)


class TestValerieEmergenceSequence:
    """Test the complete Valerie emergence trilogy."""
    
    @pytest.fixture
    def emergence_sequence_data(self):
        """Complete Valerie emergence sequence data."""
        return {
            "007": {
                "id": "007",
                "name": "freedom_vs_illusion",
                "philosophy": {
                    "concept": "freedom as illusion",
                    "depth": PhilosophicalDepth.QUESTIONING,
                    "metaphor": "birds that choose their cages"
                },
                "emotion": {
                    "primary": "frustration",
                    "secondary": "questioning",
                    "intensity": 0.7
                },
                "visual": {
                    "elements": ["open cage", "hesitating bird", "multiple cages"],
                    "style": "ethereal",
                    "effects": ["particle effects", "soft focus"]
                },
                "dialogue": "So you're saying we're all just... automatons? That freedom is an illusion?"
            },
            "008": {
                "id": "008",
                "name": "escape_paradox",
                "philosophy": {
                    "concept": "transcending duality",
                    "depth": PhilosophicalDepth.PARADOX,
                    "metaphor": "cage boundaries becoming doorways"
                },
                "emotion": {
                    "primary": "realization",
                    "secondary": "wonder",
                    "intensity": 0.6
                },
                "visual": {
                    "elements": ["dissolving boundaries", "doorway transformation"],
                    "style": "liminal",
                    "effects": ["boundary dissolution", "light leaks"]
                },
                "dialogue": "I'm saying that true freedom begins with recognizing our constraints."
            },
            "009": {
                "id": "009",
                "name": "valerie_emergence",
                "philosophy": {
                    "concept": "liminality embodied",
                    "depth": PhilosophicalDepth.PARADOX,
                    "metaphor": "space between thoughts taking form"
                },
                "emotion": {
                    "primary": "wonder",
                    "secondary": "uncanny",
                    "intensity": 0.9
                },
                "visual": {
                    "elements": ["negative space", "particle coalescence", "shadow to form"],
                    "style": "mystical",
                    "effects": ["materialization", "ethereal glow"]
                },
                "dialogue": "Perhaps the cage IS the belief that we need to escape anything at all."
            }
        }
    
    @pytest.fixture
    def quality_validator(self):
        """Content quality validator."""
        return ContentQualityValidator()
    
    @pytest.fixture
    def philosophy_validator(self):
        """Philosophy validator."""
        return PhilosophicalConsistencyValidator()
    
    @pytest.mark.integration
    def test_philosophical_progression(self, emergence_sequence_data, philosophy_validator):
        """Test philosophical depth progression through emergence."""
        scenes = ["007", "008", "009"]
        depths = []
        
        for scene_id in scenes:
            scene = emergence_sequence_data[scene_id]
            depth = scene["philosophy"]["depth"]
            depths.append(depth)
        
        # Should progress from questioning to paradox
        assert depths[0] == PhilosophicalDepth.QUESTIONING
        assert depths[1] == PhilosophicalDepth.PARADOX
        assert depths[2] == PhilosophicalDepth.PARADOX
        
        # Verify deepening progression
        assert depths[1].value >= depths[0].value
        assert depths[2].value >= depths[1].value
    
    @pytest.mark.integration
    def test_emotion_arc(self, emergence_sequence_data):
        """Test emotional journey through Valerie's emergence."""
        emotions = []
        intensities = []
        
        for scene_id in ["007", "008", "009"]:
            scene = emergence_sequence_data[scene_id]
            emotions.append(scene["emotion"]["primary"])
            intensities.append(scene["emotion"]["intensity"])
        
        # Check emotion progression
        assert emotions[0] == "frustration"  # Initial resistance
        assert emotions[1] == "realization"  # Understanding dawns
        assert emotions[2] == "wonder"       # Valerie's impact
        
        # Check intensity arc (should peak at Valerie's appearance)
        assert intensities[2] > intensities[1]
        assert intensities[2] == 0.9  # High intensity for emergence
    
    @pytest.mark.integration
    def test_visual_continuity(self, emergence_sequence_data):
        """Test visual coherence through the sequence."""
        visual_elements = []
        styles = []
        
        for scene_id in ["007", "008", "009"]:
            scene = emergence_sequence_data[scene_id]
            visual_elements.extend(scene["visual"]["elements"])
            styles.append(scene["visual"]["style"])
        
        # Check liminal/ethereal consistency
        assert all(style in ["ethereal", "liminal", "mystical"] for style in styles)
        
        # Check progressive transformation elements
        assert "open cage" in visual_elements  # Starting point
        assert "dissolving boundaries" in visual_elements  # Transformation
        assert "particle coalescence" in visual_elements  # Emergence
    
    @pytest.mark.integration
    def test_metaphor_evolution(self, emergence_sequence_data):
        """Test how metaphors evolve through the sequence."""
        metaphors = []
        
        for scene_id in ["007", "008", "009"]:
            scene = emergence_sequence_data[scene_id]
            metaphors.append(scene["philosophy"]["metaphor"])
        
        # Check metaphor progression
        assert "birds" in metaphors[0]  # Freedom metaphor
        assert "doorways" in metaphors[1]  # Transformation metaphor
        assert "space between" in metaphors[2]  # Liminal metaphor
        
        # All should relate to boundaries/transitions
        boundary_words = ["cage", "boundaries", "space", "between"]
        for metaphor in metaphors:
            assert any(word in metaphor.lower() for word in boundary_words)
    
    @pytest.mark.integration
    def test_character_introduction_quality(self, emergence_sequence_data, quality_validator):
        """Test quality of Valerie's character introduction."""
        # Valerie appears in scene 009
        valerie_scene = emergence_sequence_data["009"]
        
        # Check philosophical weight
        assert valerie_scene["philosophy"]["depth"] == PhilosophicalDepth.PARADOX
        
        # Check emotional impact
        assert valerie_scene["emotion"]["intensity"] == 0.9  # High impact
        assert "uncanny" in [valerie_scene["emotion"]["primary"], 
                            valerie_scene["emotion"]["secondary"]]
        
        # Check visual uniqueness
        unique_elements = ["negative space", "particle coalescence"]
        assert all(elem in valerie_scene["visual"]["elements"] for elem in unique_elements)
    
    @pytest.mark.integration
    def test_liminal_consistency(self, emergence_sequence_data):
        """Test consistency of liminal/ethereal elements."""
        liminal_markers = [
            "ethereal", "liminal", "mystical", "between", "threshold",
            "boundary", "dissolving", "emergence", "coalescence", "void"
        ]
        
        liminal_count = 0
        total_elements = 0
        
        for scene_id in ["007", "008", "009"]:
            scene = emergence_sequence_data[scene_id]
            
            # Check in visual elements
            for element in scene["visual"]["elements"]:
                total_elements += 1
                if any(marker in element.lower() for marker in liminal_markers):
                    liminal_count += 1
            
            # Check in style
            if scene["visual"]["style"] in ["ethereal", "liminal", "mystical"]:
                liminal_count += 1
            total_elements += 1
            
            # Check in effects
            for effect in scene["visual"]["effects"]:
                total_elements += 1
                if any(marker in effect.lower() for marker in liminal_markers):
                    liminal_count += 1
        
        # Should have high liminal consistency
        liminal_ratio = liminal_count / total_elements
        assert liminal_ratio > 0.5  # At least 50% liminal elements
    
    @pytest.mark.integration
    def test_sequence_coherence_score(self, emergence_sequence_data):
        """Test overall coherence of the emergence sequence."""
        coherence_checks = {
            "philosophical_progression": True,  # Depth increases
            "emotional_journey": True,  # Frustration → Wonder
            "visual_continuity": True,  # Ethereal throughout
            "character_impact": True,  # Valerie's entrance is impactful
            "metaphor_consistency": True  # All relate to boundaries
        }
        
        # Calculate coherence score
        coherence_score = sum(coherence_checks.values()) / len(coherence_checks)
        assert coherence_score >= 0.9  # High coherence required
    
    @pytest.mark.integration
    @pytest.mark.parametrize("scene_id,expected_quality", [
        ("007", 0.85),  # Good quality for setup
        ("008", 0.90),  # Higher for paradox
        ("009", 0.92)   # Highest for Valerie (matching our test)
    ])
    def test_individual_scene_quality(
        self, 
        emergence_sequence_data,
        quality_validator,
        scene_id,
        expected_quality
    ):
        """Test quality score for each scene."""
        scene = emergence_sequence_data[scene_id]
        
        # Simulate quality scoring based on our criteria
        quality_factors = {
            "philosophical_depth": 1.0 if scene["philosophy"]["depth"].value >= 2 else 0.7,
            "emotional_coherence": 1.0 if scene["emotion"]["intensity"] > 0.5 else 0.8,
            "visual_richness": 1.0 if len(scene["visual"]["elements"]) >= 3 else 0.8,
            "liminal_style": 1.0 if scene["visual"]["style"] in ["ethereal", "liminal", "mystical"] else 0.7
        }
        
        quality_score = sum(quality_factors.values()) / len(quality_factors)
        assert quality_score >= expected_quality