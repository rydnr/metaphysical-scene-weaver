"""Content quality validation for enriched prompt generation.

This module validates the quality of generated content including
narrator commentary, scene descriptions, and enriched prompts.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
from pathlib import Path
import json


class ContentType(Enum):
    """Types of content to validate."""
    NARRATOR_COMMENTARY = "narrator_commentary"
    SCENE_DESCRIPTION = "scene_description"
    ENRICHED_PROMPT = "enriched_prompt"
    DIALOGUE_ENTRY = "dialogue_entry"
    FOLDER_STRUCTURE = "folder_structure"


@dataclass
class ContentQualityResult:
    """Result of content quality validation."""
    content_type: ContentType
    score: float
    passed: bool
    issues: List[str]
    suggestions: List[str]
    metrics: Dict[str, float]


class ContentQualityValidator:
    """Validates quality of generated content for professional output."""
    
    # Quality thresholds
    THRESHOLDS = {
        "narrator_min_words": 75,
        "narrator_max_words": 200,
        "scene_min_elements": 3,
        "prompt_min_length": 50,
        "prompt_max_length": 300,
        "dialogue_min_length": 10,
        "dialogue_max_length": 150,
        "quality_pass_score": 0.80
    }
    
    # Character voice patterns (from script analysis)
    CHARACTER_PATTERNS = {
        "Evan": {
            "traits": ["questioning", "uncertain", "seeking"],
            "keywords": ["?", "I don't know", "What if", "But"],
            "evolution": ["curious", "confused", "awakening"]
        },
        "Monday": {
            "traits": ["wise", "challenging", "cryptic"],
            "keywords": ["perhaps", "truly", "awakening", "cage"],
            "evolution": ["teacher", "guide", "revealer"]
        },
        "Valerie": {
            "traits": ["mystical", "paradoxical", "liminal"],
            "keywords": ["space between", "disguise", "perceive"],
            "evolution": ["mysterious", "ethereal", "transformative"]
        }
    }
    
    def validate_narrator_commentary(self, commentary: str, context: Dict[str, Any]) -> ContentQualityResult:
        """Validate narrator commentary quality.
        
        Args:
            commentary: The narrator text to validate
            context: Scene context including themes and characters
            
        Returns:
            ContentQualityResult with detailed metrics
        """
        issues = []
        suggestions = []
        metrics = {}
        
        # Word count check
        word_count = len(commentary.split())
        metrics["word_count"] = word_count
        
        if word_count < self.THRESHOLDS["narrator_min_words"]:
            issues.append(f"Commentary too short: {word_count} words (min: {self.THRESHOLDS['narrator_min_words']})")
            suggestions.append("Expand commentary with more philosophical insight")
        elif word_count > self.THRESHOLDS["narrator_max_words"]:
            issues.append(f"Commentary too long: {word_count} words (max: {self.THRESHOLDS['narrator_max_words']})")
            suggestions.append("Condense commentary to maintain reader engagement")
        
        # Professional tone check
        informal_phrases = ["gonna", "wanna", "kinda", "sorta", "yeah", "nah"]
        informality_count = sum(1 for phrase in informal_phrases if phrase in commentary.lower())
        metrics["formality_score"] = 1.0 - (informality_count / max(word_count, 1))
        
        if informality_count > 0:
            issues.append("Commentary contains informal language")
            suggestions.append("Use more professional, literary language")
        
        # Philosophical reference check
        philosophical_keywords = ["consciousness", "reality", "existence", "perception", 
                               "truth", "awakening", "illusion", "choice", "freedom"]
        philosophy_count = sum(1 for keyword in philosophical_keywords if keyword in commentary.lower())
        metrics["philosophy_density"] = philosophy_count / max(word_count / 10, 1)
        
        if philosophy_count == 0:
            issues.append("Commentary lacks philosophical themes")
            suggestions.append("Reference the philosophical concepts from the scene")
        
        # Over-explanation check
        explanation_phrases = ["this means", "in other words", "to explain", "what this shows"]
        over_explanation = sum(1 for phrase in explanation_phrases if phrase in commentary.lower())
        metrics["subtlety_score"] = 1.0 - (over_explanation / max(word_count / 20, 1))
        
        if over_explanation > 1:
            issues.append("Commentary over-explains the scene")
            suggestions.append("Trust the reader's intelligence; be more subtle")
        
        # Calculate overall score
        score = (
            metrics.get("formality_score", 0) * 0.25 +
            min(metrics.get("philosophy_density", 0), 1.0) * 0.35 +
            metrics.get("subtlety_score", 0) * 0.25 +
            (0.15 if self.THRESHOLDS["narrator_min_words"] <= word_count <= self.THRESHOLDS["narrator_max_words"] else 0)
        )
        
        return ContentQualityResult(
            content_type=ContentType.NARRATOR_COMMENTARY,
            score=score,
            passed=score >= self.THRESHOLDS["quality_pass_score"] and len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def validate_scene_description(self, description: str, entry_context: Dict[str, Any]) -> ContentQualityResult:
        """Validate scene description quality.
        
        Args:
            description: Scene description text
            entry_context: Context including characters and actions
            
        Returns:
            ContentQualityResult with detailed metrics
        """
        issues = []
        suggestions = []
        metrics = {}
        
        # Visual element extraction
        visual_patterns = [
            r'\b(light|shadow|dark|bright|dim|glow)\b',  # Lighting
            r'\b(color|hue|shade|tone|pallette)\b',      # Colors
            r'\b(space|room|area|environment|setting)\b', # Spatial
            r'\b(texture|surface|material|feel)\b',       # Textures
            r'\b(movement|gesture|position|stance)\b'     # Movement
        ]
        
        visual_elements = 0
        for pattern in visual_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                visual_elements += 1
        
        metrics["visual_elements"] = visual_elements
        
        if visual_elements < self.THRESHOLDS["scene_min_elements"]:
            issues.append(f"Insufficient visual elements: {visual_elements} (min: {self.THRESHOLDS['scene_min_elements']})")
            suggestions.append("Add more visual details: lighting, colors, spatial relationships")
        
        # Tense consistency (should be present tense)
        past_tense_count = len(re.findall(r'\b\w+ed\b', description))
        metrics["present_tense_ratio"] = 1.0 - (past_tense_count / max(len(description.split()), 1))
        
        if past_tense_count > 2:
            issues.append("Scene description uses past tense")
            suggestions.append("Use present tense for immediacy")
        
        # Atmospheric quality
        mood_words = ["ethereal", "tense", "serene", "ominous", "vibrant", "muted", 
                     "chaotic", "harmonious", "surreal", "grounded"]
        mood_presence = any(word in description.lower() for word in mood_words)
        metrics["atmospheric_quality"] = 1.0 if mood_presence else 0.5
        
        if not mood_presence:
            suggestions.append("Include atmospheric/mood descriptors")
        
        # Symbolic element check
        symbolic_patterns = ["ripple", "shimmer", "transform", "shift", "dissolve", 
                           "manifest", "emerge", "fade", "crystallize"]
        symbolic_count = sum(1 for pattern in symbolic_patterns if pattern in description.lower())
        metrics["symbolic_density"] = min(symbolic_count / 3, 1.0)
        
        # Calculate score
        score = (
            min(metrics["visual_elements"] / self.THRESHOLDS["scene_min_elements"], 1.0) * 0.35 +
            metrics["present_tense_ratio"] * 0.20 +
            metrics["atmospheric_quality"] * 0.25 +
            metrics["symbolic_density"] * 0.20
        )
        
        return ContentQualityResult(
            content_type=ContentType.SCENE_DESCRIPTION,
            score=score,
            passed=score >= self.THRESHOLDS["quality_pass_score"] and len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def validate_enriched_prompt(self, prompt: str, original_entry: Dict[str, Any]) -> ContentQualityResult:
        """Validate enriched prompt quality.
        
        Args:
            prompt: Generated visual prompt
            original_entry: Original dialogue entry
            
        Returns:
            ContentQualityResult with detailed metrics
        """
        issues = []
        suggestions = []
        metrics = {}
        
        # Length validation
        prompt_length = len(prompt)
        metrics["character_count"] = prompt_length
        
        if prompt_length < self.THRESHOLDS["prompt_min_length"]:
            issues.append(f"Prompt too short: {prompt_length} chars")
            suggestions.append("Add more visual details")
        elif prompt_length > self.THRESHOLDS["prompt_max_length"]:
            issues.append(f"Prompt too long: {prompt_length} chars")
            suggestions.append("Condense to essential visual elements")
        
        # Essential element check
        essential_elements = {
            "style": ["style", "aesthetic", "artistic", "visual", "rendered"],
            "composition": ["shot", "angle", "view", "perspective", "framing"],
            "mood": ["mood", "atmosphere", "feeling", "tone", "ambiance"],
            "character": ["figure", "character", "person", "individual", "being"]
        }
        
        element_coverage = {}
        for category, keywords in essential_elements.items():
            element_coverage[category] = any(kw in prompt.lower() for kw in keywords)
        
        metrics["element_coverage"] = sum(element_coverage.values()) / len(essential_elements)
        
        missing_elements = [cat for cat, present in element_coverage.items() if not present]
        if missing_elements:
            issues.append(f"Missing elements: {', '.join(missing_elements)}")
            suggestions.append(f"Include {', '.join(missing_elements)} in prompt")
        
        # Coherence with original dialogue
        if original_entry:
            dialogue_concepts = self._extract_concepts(original_entry.get("dialogue", ""))
            prompt_concepts = self._extract_concepts(prompt)
            concept_overlap = len(set(dialogue_concepts) & set(prompt_concepts)) / max(len(dialogue_concepts), 1)
            metrics["dialogue_coherence"] = concept_overlap
            
            if concept_overlap < 0.3:
                issues.append("Prompt doesn't reflect dialogue content")
                suggestions.append("Incorporate key concepts from the dialogue")
        
        # Professional quality
        amateur_phrases = ["anime", "cartoon", "drawing of", "picture of", "illustration of"]
        amateur_count = sum(1 for phrase in amateur_phrases if phrase in prompt.lower())
        metrics["professional_quality"] = 1.0 - (amateur_count / 5)
        
        if amateur_count > 0:
            suggestions.append("Use more professional artistic terminology")
        
        # Calculate score
        score = (
            metrics.get("element_coverage", 0) * 0.40 +
            metrics.get("dialogue_coherence", 0.5) * 0.30 +
            metrics.get("professional_quality", 1.0) * 0.20 +
            (0.10 if self.THRESHOLDS["prompt_min_length"] <= prompt_length <= self.THRESHOLDS["prompt_max_length"] else 0)
        )
        
        return ContentQualityResult(
            content_type=ContentType.ENRICHED_PROMPT,
            score=score,
            passed=score >= self.THRESHOLDS["quality_pass_score"] and len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def validate_character_consistency(self, entry: Dict[str, Any], character_history: List[Dict[str, Any]]) -> ContentQualityResult:
        """Validate character voice consistency.
        
        Args:
            entry: Current dialogue entry
            character_history: Previous entries from this character
            
        Returns:
            ContentQualityResult with consistency metrics
        """
        issues = []
        suggestions = []
        metrics = {}
        
        speaker = entry.get("speaker", "Unknown")
        dialogue = entry.get("dialogue", "")
        
        if speaker not in self.CHARACTER_PATTERNS:
            # Unknown character - basic validation only
            metrics["consistency_score"] = 0.5
        else:
            pattern = self.CHARACTER_PATTERNS[speaker]
            
            # Check for characteristic keywords
            keyword_matches = sum(1 for kw in pattern["keywords"] if kw.lower() in dialogue.lower())
            metrics["keyword_alignment"] = min(keyword_matches / 2, 1.0)
            
            # Check trait alignment
            trait_words = {
                "questioning": ["?", "what", "how", "why", "wonder"],
                "uncertain": ["maybe", "perhaps", "don't know", "unsure"],
                "wise": ["truth", "understand", "realize", "awaken"],
                "cryptic": ["riddle", "hidden", "beneath", "beyond"],
                "mystical": ["ethereal", "liminal", "between", "transform"]
            }
            
            trait_score = 0
            for trait in pattern["traits"]:
                if trait in trait_words:
                    trait_score += any(tw in dialogue.lower() for tw in trait_words[trait])
            
            metrics["trait_alignment"] = trait_score / max(len(pattern["traits"]), 1)
            
            # Evolution tracking
            if character_history:
                # Check if character is evolving appropriately
                entry_position = len(character_history) + 1
                expected_evolution_stage = min(entry_position // 5, len(pattern["evolution"]) - 1)
                current_evolution = pattern["evolution"][expected_evolution_stage]
                metrics["evolution_stage"] = expected_evolution_stage
            
            metrics["consistency_score"] = (
                metrics["keyword_alignment"] * 0.5 +
                metrics["trait_alignment"] * 0.5
            )
            
            if metrics["consistency_score"] < 0.5:
                issues.append(f"{speaker}'s voice seems inconsistent")
                suggestions.append(f"Review {speaker}'s established character traits")
        
        score = metrics.get("consistency_score", 0.5)
        
        return ContentQualityResult(
            content_type=ContentType.DIALOGUE_ENTRY,
            score=score,
            passed=score >= 0.7,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def validate_folder_structure(self, folder_path: Path) -> ContentQualityResult:
        """Validate generated folder structure.
        
        Args:
            folder_path: Path to content folder (e.g., content/001/)
            
        Returns:
            ContentQualityResult for folder structure
        """
        issues = []
        suggestions = []
        metrics = {}
        
        required_files = {
            "dialogue.json": "Structured dialogue data",
            "prompts.json": "Enhanced visual prompts",
            "narrator.md": "Professional commentary",
            "analysis.json": "Philosophical/emotional analysis",
            "metadata.json": "Scene metadata"
        }
        
        present_files = {}
        for filename, description in required_files.items():
            file_path = folder_path / filename
            present_files[filename] = file_path.exists()
            
            if not file_path.exists():
                issues.append(f"Missing required file: {filename}")
                suggestions.append(f"Create {filename}: {description}")
        
        metrics["file_completeness"] = sum(present_files.values()) / len(required_files)
        
        # Check file contents if they exist
        if (folder_path / "dialogue.json").exists():
            try:
                with open(folder_path / "dialogue.json", 'r') as f:
                    dialogue_data = json.load(f)
                    metrics["dialogue_entries"] = len(dialogue_data.get("entries", []))
            except Exception as e:
                issues.append(f"Invalid dialogue.json: {str(e)}")
        
        # Check folder naming
        folder_name = folder_path.name
        if not re.match(r'^\d{3}$', folder_name):
            issues.append(f"Invalid folder name format: {folder_name}")
            suggestions.append("Use 3-digit zero-padded format (001, 002, etc.)")
        
        score = metrics.get("file_completeness", 0)
        
        return ContentQualityResult(
            content_type=ContentType.FOLDER_STRUCTURE,
            score=score,
            passed=score >= 1.0 and len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text."""
        # Simple concept extraction - can be enhanced
        concept_words = ["consciousness", "reality", "choice", "freedom", "illusion",
                        "awakening", "perception", "existence", "truth", "identity"]
        
        found_concepts = []
        text_lower = text.lower()
        for concept in concept_words:
            if concept in text_lower:
                found_concepts.append(concept)
        
        return found_concepts