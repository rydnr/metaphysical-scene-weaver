"""Quality validation system for Metaphysical Scene Weaver outputs.

This module provides comprehensive validation for all outputs of the system,
ensuring consistency, accuracy, and quality across philosophical interpretations,
emotional mappings, and generated prompts.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
from collections import Counter
import numpy as np


class ValidationLevel(Enum):
    """Validation strictness levels."""
    LENIENT = "lenient"
    STANDARD = "standard"
    STRICT = "strict"


class QualityMetric(Enum):
    """Quality metrics for validation."""
    PHILOSOPHY_ACCURACY = "philosophy_accuracy"
    EMOTION_PRECISION = "emotion_precision"
    PROMPT_COHERENCE = "prompt_coherence"
    METAPHOR_RELEVANCE = "metaphor_relevance"
    SCENE_CONSISTENCY = "scene_consistency"
    CHARACTER_CONTINUITY = "character_continuity"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    metric: QualityMetric
    passed: bool
    score: float
    details: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


@dataclass
class QualityReport:
    """Comprehensive quality report for validated content."""
    overall_score: float
    passed: bool
    results: List[ValidationResult]
    summary: Dict[str, float]
    recommendations: List[str]


class QualityValidator:
    """Main quality validation system."""
    
    # Quality thresholds
    THRESHOLDS = {
        ValidationLevel.LENIENT: {
            QualityMetric.PHILOSOPHY_ACCURACY: 0.70,
            QualityMetric.EMOTION_PRECISION: 0.75,
            QualityMetric.PROMPT_COHERENCE: 0.80,
            QualityMetric.METAPHOR_RELEVANCE: 0.65,
            QualityMetric.SCENE_CONSISTENCY: 0.75,
            QualityMetric.CHARACTER_CONTINUITY: 0.80,
        },
        ValidationLevel.STANDARD: {
            QualityMetric.PHILOSOPHY_ACCURACY: 0.85,
            QualityMetric.EMOTION_PRECISION: 0.90,
            QualityMetric.PROMPT_COHERENCE: 0.95,
            QualityMetric.METAPHOR_RELEVANCE: 0.80,
            QualityMetric.SCENE_CONSISTENCY: 0.90,
            QualityMetric.CHARACTER_CONTINUITY: 0.95,
        },
        ValidationLevel.STRICT: {
            QualityMetric.PHILOSOPHY_ACCURACY: 0.95,
            QualityMetric.EMOTION_PRECISION: 0.98,
            QualityMetric.PROMPT_COHERENCE: 0.99,
            QualityMetric.METAPHOR_RELEVANCE: 0.90,
            QualityMetric.SCENE_CONSISTENCY: 0.95,
            QualityMetric.CHARACTER_CONTINUITY: 0.99,
        }
    }
    
    # Known philosophical concepts for validation
    PHILOSOPHICAL_CONCEPTS = {
        "identity", "consciousness", "reality", "perception", "time",
        "existence", "being", "knowing", "truth", "meaning", "purpose",
        "causality", "determinism", "free will", "morality", "ethics",
        "aesthetics", "metaphysics", "epistemology", "ontology", "logic"
    }
    
    # Valid emotion categories
    EMOTION_CATEGORIES = {
        "primary": {"joy", "sadness", "anger", "fear", "surprise", "disgust"},
        "complex": {"contemplation", "wonder", "confusion", "realization", "doubt"},
        "social": {"empathy", "shame", "pride", "guilt", "embarrassment"}
    }
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        """Initialize the quality validator.
        
        Args:
            validation_level: Strictness level for validation
        """
        self.validation_level = validation_level
        self.thresholds = self.THRESHOLDS[validation_level]
    
    def validate_philosophy_detection(
        self,
        detected_concepts: List[str],
        dialogue_text: str,
        expected_concepts: Optional[List[str]] = None
    ) -> ValidationResult:
        """Validate philosophical concept detection accuracy.
        
        Args:
            detected_concepts: Concepts identified by the system
            dialogue_text: Original dialogue text
            expected_concepts: Ground truth concepts (if available)
            
        Returns:
            ValidationResult with accuracy metrics
        """
        errors = []
        warnings = []
        details = {}
        
        # Check for empty detection
        if not detected_concepts:
            errors.append("No philosophical concepts detected")
            return ValidationResult(
                metric=QualityMetric.PHILOSOPHY_ACCURACY,
                passed=False,
                score=0.0,
                details=details,
                errors=errors,
                warnings=warnings
            )
        
        # Validate against known concepts
        valid_concepts = [c for c in detected_concepts if c.lower() in self.PHILOSOPHICAL_CONCEPTS]
        invalid_concepts = [c for c in detected_concepts if c.lower() not in self.PHILOSOPHICAL_CONCEPTS]
        
        if invalid_concepts:
            warnings.append(f"Unknown philosophical concepts: {invalid_concepts}")
        
        # Calculate relevance score
        dialogue_lower = dialogue_text.lower()
        relevance_scores = []
        for concept in valid_concepts:
            # Check if concept or related terms appear in dialogue
            if concept.lower() in dialogue_lower:
                relevance_scores.append(1.0)
            else:
                # Check for semantic similarity (simplified)
                relevance_scores.append(0.5)
        
        relevance_score = np.mean(relevance_scores) if relevance_scores else 0.0
        
        # If expected concepts provided, calculate accuracy
        if expected_concepts:
            detected_set = set(c.lower() for c in detected_concepts)
            expected_set = set(c.lower() for c in expected_concepts)
            
            precision = len(detected_set & expected_set) / len(detected_set) if detected_set else 0.0
            recall = len(detected_set & expected_set) / len(expected_set) if expected_set else 0.0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            details["precision"] = precision
            details["recall"] = recall
            details["f1_score"] = f1_score
            score = f1_score
        else:
            score = relevance_score
        
        details["valid_concepts"] = valid_concepts
        details["relevance_score"] = relevance_score
        
        passed = score >= self.thresholds[QualityMetric.PHILOSOPHY_ACCURACY]
        
        return ValidationResult(
            metric=QualityMetric.PHILOSOPHY_ACCURACY,
            passed=passed,
            score=score,
            details=details,
            errors=errors,
            warnings=warnings
        )
    
    def validate_emotion_mapping(
        self,
        emotion_mappings: Dict[str, Dict[str, float]],
        dialogue_entries: List[Dict[str, str]]
    ) -> ValidationResult:
        """Validate emotion classification precision.
        
        Args:
            emotion_mappings: Emotion classifications per entry
            dialogue_entries: Original dialogue entries
            
        Returns:
            ValidationResult with precision metrics
        """
        errors = []
        warnings = []
        details = {}
        
        if not emotion_mappings:
            errors.append("No emotion mappings provided")
            return ValidationResult(
                metric=QualityMetric.EMOTION_PRECISION,
                passed=False,
                score=0.0,
                details=details,
                errors=errors,
                warnings=warnings
            )
        
        valid_emotions = set()
        for category in self.EMOTION_CATEGORIES.values():
            valid_emotions.update(category)
        
        precision_scores = []
        
        for entry_id, emotions in emotion_mappings.items():
            # Check emotion validity
            invalid_emotions = [e for e in emotions.keys() if e not in valid_emotions]
            if invalid_emotions:
                warnings.append(f"Invalid emotions in entry {entry_id}: {invalid_emotions}")
            
            # Check probability distribution
            total_prob = sum(emotions.values())
            if abs(total_prob - 1.0) > 0.01:
                errors.append(f"Emotion probabilities don't sum to 1.0 in entry {entry_id}: {total_prob}")
            
            # Check for reasonable distribution (not too uniform or too peaked)
            probs = list(emotions.values())
            entropy = -sum(p * np.log(p + 1e-10) for p in probs if p > 0)
            max_entropy = np.log(len(probs))
            normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
            
            # Score based on distribution quality
            if 0.3 <= normalized_entropy <= 0.8:
                precision_scores.append(1.0)
            else:
                precision_scores.append(0.7)
                warnings.append(f"Unusual emotion distribution in entry {entry_id}")
        
        score = np.mean(precision_scores) if precision_scores else 0.0
        details["average_precision"] = score
        details["total_entries"] = len(emotion_mappings)
        
        passed = score >= self.thresholds[QualityMetric.EMOTION_PRECISION]
        
        return ValidationResult(
            metric=QualityMetric.EMOTION_PRECISION,
            passed=passed,
            score=score,
            details=details,
            errors=errors,
            warnings=warnings
        )
    
    def validate_prompt_coherence(
        self,
        prompts: List[str],
        scene_context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate generated prompt coherence and quality.
        
        Args:
            prompts: Generated visual prompts
            scene_context: Optional scene context for validation
            
        Returns:
            ValidationResult with coherence metrics
        """
        errors = []
        warnings = []
        details = {}
        
        if not prompts:
            errors.append("No prompts provided")
            return ValidationResult(
                metric=QualityMetric.PROMPT_COHERENCE,
                passed=False,
                score=0.0,
                details=details,
                errors=errors,
                warnings=warnings
            )
        
        coherence_scores = []
        
        for i, prompt in enumerate(prompts):
            prompt_score = 1.0
            
            # Check length
            if len(prompt) < 20:
                errors.append(f"Prompt {i} too short: {len(prompt)} characters")
                prompt_score *= 0.5
            elif len(prompt) > 500:
                warnings.append(f"Prompt {i} may be too long: {len(prompt)} characters")
                prompt_score *= 0.9
            
            # Check for required elements
            required_elements = ["style", "scene", "mood"]
            missing_elements = []
            for element in required_elements:
                if element not in prompt.lower():
                    missing_elements.append(element)
            
            if missing_elements:
                warnings.append(f"Prompt {i} missing elements: {missing_elements}")
                prompt_score *= 0.8
            
            # Check for consistency markers
            if i > 0:
                # Simple consistency check with previous prompt
                prev_prompt = prompts[i-1]
                common_words = set(prompt.lower().split()) & set(prev_prompt.lower().split())
                consistency_ratio = len(common_words) / max(len(prompt.split()), len(prev_prompt.split()))
                
                if consistency_ratio < 0.1:
                    warnings.append(f"Low consistency between prompts {i-1} and {i}")
                    prompt_score *= 0.9
            
            coherence_scores.append(prompt_score)
        
        score = np.mean(coherence_scores) if coherence_scores else 0.0
        details["prompt_count"] = len(prompts)
        details["individual_scores"] = coherence_scores
        
        passed = score >= self.thresholds[QualityMetric.PROMPT_COHERENCE]
        
        return ValidationResult(
            metric=QualityMetric.PROMPT_COHERENCE,
            passed=passed,
            score=score,
            details=details,
            errors=errors,
            warnings=warnings
        )
    
    def validate_complete_output(
        self,
        output_data: Dict[str, Any],
        input_data: Optional[Dict[str, Any]] = None
    ) -> QualityReport:
        """Perform comprehensive validation of complete system output.
        
        Args:
            output_data: Complete output from the system
            input_data: Original input data for comparison
            
        Returns:
            QualityReport with all validation results
        """
        results = []
        
        # Validate philosophy detection
        if "philosophical_concepts" in output_data:
            philosophy_result = self.validate_philosophy_detection(
                output_data["philosophical_concepts"],
                output_data.get("dialogue_text", ""),
                input_data.get("expected_concepts") if input_data else None
            )
            results.append(philosophy_result)
        
        # Validate emotion mapping
        if "emotion_mappings" in output_data:
            emotion_result = self.validate_emotion_mapping(
                output_data["emotion_mappings"],
                output_data.get("dialogue_entries", [])
            )
            results.append(emotion_result)
        
        # Validate prompt coherence
        if "prompts" in output_data:
            prompt_result = self.validate_prompt_coherence(
                output_data["prompts"],
                output_data.get("scene_context")
            )
            results.append(prompt_result)
        
        # Calculate overall score
        if results:
            overall_score = np.mean([r.score for r in results])
            passed = all(r.passed for r in results)
        else:
            overall_score = 0.0
            passed = False
        
        # Generate summary
        summary = {
            result.metric.value: result.score
            for result in results
        }
        
        # Generate recommendations
        recommendations = []
        for result in results:
            if not result.passed:
                recommendations.append(f"Improve {result.metric.value}: score {result.score:.2f}")
            if result.warnings:
                recommendations.extend(result.warnings[:2])  # Top 2 warnings
        
        return QualityReport(
            overall_score=overall_score,
            passed=passed,
            results=results,
            summary=summary,
            recommendations=recommendations
        )