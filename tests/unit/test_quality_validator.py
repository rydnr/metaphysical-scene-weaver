"""Unit tests for the QualityValidator module."""

import pytest
from src.core.quality_validator import (
    QualityValidator,
    ValidationLevel,
    QualityMetric,
    ValidationResult,
    QualityReport
)


class TestQualityValidator:
    """Test cases for QualityValidator."""
    
    @pytest.mark.unit
    def test_initialization(self):
        """Test validator initialization with different levels."""
        for level in ValidationLevel:
            validator = QualityValidator(level)
            assert validator.validation_level == level
            assert validator.thresholds == validator.THRESHOLDS[level]
    
    @pytest.mark.unit
    def test_philosophy_detection_validation(self):
        """Test validation of philosophical concept detection."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Test successful detection
        detected = ["consciousness", "emergence", "reality"]
        dialogue = "What if consciousness emerges from reality itself?"
        
        result = validator.validate_philosophy_detection(detected, dialogue)
        
        assert isinstance(result, ValidationResult)
        assert result.metric == QualityMetric.PHILOSOPHY_ACCURACY
        assert result.passed is True
        assert result.score > 0.7
        
        # Test empty detection
        empty_result = validator.validate_philosophy_detection([], dialogue)
        assert empty_result.passed is False
        assert empty_result.score == 0.0
        assert len(empty_result.errors) > 0
    
    @pytest.mark.unit
    def test_philosophy_validation_with_ground_truth(self):
        """Test philosophy validation against expected concepts."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        detected = ["consciousness", "free_will", "determinism"]
        expected = ["consciousness", "free_will", "reality"]
        dialogue = "Free will and consciousness in a deterministic universe"
        
        result = validator.validate_philosophy_detection(detected, dialogue, expected)
        
        assert "precision" in result.details
        assert "recall" in result.details
        assert "f1_score" in result.details
        
        # Should have partial match
        assert result.details["precision"] > 0.5
        assert result.details["recall"] > 0.5
    
    @pytest.mark.unit
    def test_unknown_philosophical_concepts(self):
        """Test handling of unknown philosophical concepts."""
        validator = QualityValidator(ValidationLevel.LENIENT)
        
        detected = ["consciousness", "unknown_concept", "fake_philosophy"]
        dialogue = "Exploring consciousness and novel concepts"
        
        result = validator.validate_philosophy_detection(detected, dialogue)
        
        assert len(result.warnings) > 0
        assert any("unknown" in w.lower() for w in result.warnings)
        # Should still pass with valid concepts
        assert result.score > 0.3
    
    @pytest.mark.unit
    def test_emotion_mapping_validation(self):
        """Test validation of emotion mappings."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Valid emotion mapping
        emotions = {
            "0001": {"joy": 0.6, "surprise": 0.4},
            "0002": {"contemplation": 0.8, "wonder": 0.2}
        }
        entries = [
            {"id": "0001", "dialogue": "How wonderful!"},
            {"id": "0002", "dialogue": "I wonder about existence"}
        ]
        
        result = validator.validate_emotion_mapping(emotions, entries)
        
        assert result.passed is True
        assert result.score > 0.8
        assert result.metric == QualityMetric.EMOTION_PRECISION
    
    @pytest.mark.unit
    def test_invalid_emotion_probabilities(self):
        """Test detection of invalid emotion probabilities."""
        validator = QualityValidator(ValidationLevel.STRICT)
        
        # Probabilities don't sum to 1.0
        invalid_emotions = {
            "0001": {"joy": 0.6, "sadness": 0.6},  # Sum = 1.2
            "0002": {"anger": 0.3, "fear": 0.2}    # Sum = 0.5
        }
        entries = [
            {"id": "0001", "dialogue": "Test"},
            {"id": "0002", "dialogue": "Test"}
        ]
        
        result = validator.validate_emotion_mapping(invalid_emotions, entries)
        
        assert result.passed is False
        assert len(result.errors) > 0
        assert any("sum to 1.0" in e for e in result.errors)
    
    @pytest.mark.unit
    def test_unusual_emotion_distribution(self):
        """Test detection of unusual emotion distributions."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Too uniform distribution
        uniform_emotions = {
            "0001": {"joy": 0.2, "sadness": 0.2, "anger": 0.2, "fear": 0.2, "surprise": 0.2}
        }
        
        # Too peaked distribution
        peaked_emotions = {
            "0002": {"rage": 0.99, "frustration": 0.01}
        }
        
        entries = [
            {"id": "0001", "dialogue": "Test"},
            {"id": "0002", "dialogue": "Test"}
        ]
        
        uniform_result = validator.validate_emotion_mapping(uniform_emotions, entries)
        peaked_result = validator.validate_emotion_mapping(peaked_emotions, entries)
        
        # Both should have warnings
        assert len(uniform_result.warnings) > 0 or uniform_result.score < 1.0
        assert len(peaked_result.warnings) > 0 or peaked_result.score < 1.0
    
    @pytest.mark.unit
    def test_prompt_coherence_validation(self):
        """Test validation of prompt coherence."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Good prompts
        good_prompts = [
            "A contemplative scene showing two figures discussing philosophy, "
            "moody lighting with abstract thought bubbles, artistic style",
            "Wide shot of characters in deep conversation, library setting, "
            "warm colors conveying intellectual atmosphere, graphic novel style"
        ]
        
        result = validator.validate_prompt_coherence(good_prompts)
        
        assert result.passed is True
        assert result.score > 0.9
        assert result.metric == QualityMetric.PROMPT_COHERENCE
    
    @pytest.mark.unit
    def test_prompt_length_validation(self):
        """Test prompt length validation."""
        validator = QualityValidator(ValidationLevel.STRICT)
        
        # Too short prompt
        short_prompts = ["Two people talking"]
        
        # Too long prompt
        long_prompt = "A " + " very" * 200 + " detailed scene"
        long_prompts = [long_prompt]
        
        short_result = validator.validate_prompt_coherence(short_prompts)
        long_result = validator.validate_prompt_coherence(long_prompts)
        
        assert short_result.passed is False
        assert len(short_result.errors) > 0
        
        assert len(long_result.warnings) > 0
        assert long_result.score < 1.0
    
    @pytest.mark.unit
    def test_prompt_consistency_checking(self):
        """Test prompt consistency validation."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        # Inconsistent prompts (completely different)
        inconsistent_prompts = [
            "Dark gothic scene with vampires",
            "Bright sunny beach with children playing",
            "Futuristic spaceship interior"
        ]
        
        result = validator.validate_prompt_coherence(inconsistent_prompts)
        
        # Should have warnings about consistency
        assert len(result.warnings) > 0
        assert any("consistency" in w.lower() for w in result.warnings)
    
    @pytest.mark.unit
    def test_complete_output_validation(self):
        """Test validation of complete system output."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        output = {
            "philosophical_concepts": ["consciousness", "reality", "existence"],
            "dialogue_text": "What is the nature of consciousness and reality?",
            "emotion_mappings": {
                "0001": {"wonder": 0.7, "curiosity": 0.3}
            },
            "dialogue_entries": [
                {"id": "0001", "dialogue": "What is consciousness?"}
            ],
            "prompts": [
                "A figure pondering existence, abstract cosmic background, "
                "philosophical mood with swirling thoughts visualization"
            ]
        }
        
        report = validator.validate_complete_output(output)
        
        assert isinstance(report, QualityReport)
        assert report.passed is True
        assert report.overall_score > 0.7
        assert len(report.results) >= 3
        assert len(report.recommendations) == 0 or all(
            isinstance(r, str) for r in report.recommendations
        )
    
    @pytest.mark.unit
    def test_partial_output_validation(self):
        """Test validation with missing output components."""
        validator = QualityValidator(ValidationLevel.LENIENT)
        
        # Output missing some components
        partial_output = {
            "philosophical_concepts": ["time", "space"],
            "dialogue_text": "Time and space are illusions"
            # Missing emotion_mappings and prompts
        }
        
        report = validator.validate_complete_output(partial_output)
        
        assert isinstance(report, QualityReport)
        # Should still generate report with available data
        assert report.overall_score > 0
        assert len(report.results) >= 1
    
    @pytest.mark.unit
    @pytest.mark.parametrize("level,metric,threshold", [
        (ValidationLevel.LENIENT, QualityMetric.PHILOSOPHY_ACCURACY, 0.70),
        (ValidationLevel.STANDARD, QualityMetric.EMOTION_PRECISION, 0.90),
        (ValidationLevel.STRICT, QualityMetric.PROMPT_COHERENCE, 0.99)
    ])
    def test_validation_thresholds(self, level, metric, threshold):
        """Test that validation thresholds are correctly applied."""
        validator = QualityValidator(level)
        assert validator.thresholds[metric] == threshold
    
    @pytest.mark.unit
    def test_quality_report_summary(self):
        """Test quality report summary generation."""
        validator = QualityValidator(ValidationLevel.STANDARD)
        
        output = {
            "philosophical_concepts": ["being", "nothingness"],
            "dialogue_text": "To be or not to be",
            "emotion_mappings": {
                "0001": {"contemplation": 0.9, "doubt": 0.1}
            },
            "dialogue_entries": [{"id": "0001", "dialogue": "To be or not to be"}],
            "prompts": ["Hamlet contemplating existence, dramatic lighting"]
        }
        
        report = validator.validate_complete_output(output)
        
        assert "summary" in report.__dict__
        summary = report.summary
        
        # Should have scores for each validated metric
        assert len(summary) >= 3
        assert all(0 <= score <= 1 for score in summary.values())
        assert all(isinstance(key, str) for key in summary.keys())