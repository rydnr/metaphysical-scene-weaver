"""Prompt generation engine that creates detailed scene prompts for image generation."""

from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum
from ..utils.prompt_templates import (
    PromptTemplateLibrary, PromptOptimizer, StyleMixer,
    PromptComponent, EmphasisLevel
)


class PromptStyle(Enum):
    """Different prompt generation styles."""
    COMIC_BOOK = "comic book"
    MANGA = "manga"
    GRAPHIC_NOVEL = "graphic novel"
    STORYBOARD = "storyboard"
    CONCEPT_ART = "concept art"
    CINEMATIC = "cinematic"
    ART_NOUVEAU = "art nouveau"
    SURREALIST = "surrealist"
    NEO_NOIR = "neo-noir"
    WATERCOLOR = "watercolor"
    PEN_AND_INK = "pen and ink"
    DIGITAL_PAINTING = "digital painting"


@dataclass
class PromptTemplate:
    """Template for generating prompts."""
    style_prefix: str
    composition_format: str
    character_format: str
    environment_format: str
    effects_format: str
    style_suffix: str


class PromptGenerator:
    """Generates optimized prompts for image generation from synthesized scenes."""
    
    def __init__(self, style: str = "comic book"):
        self.logger = logging.getLogger(__name__)
        self.style = PromptStyle(style.lower())
        
        # Initialize optimization components
        self.template_library = PromptTemplateLibrary()
        self.optimizer = PromptOptimizer()
        self.style_mixer = StyleMixer()
        
        # Style-specific templates
        self.templates = {
            PromptStyle.COMIC_BOOK: PromptTemplate(
                style_prefix="Comic book panel illustration,",
                composition_format="{composition_style} composition,",
                character_format="{character_description}, {expression}, {pose},",
                environment_format="{setting_description}, {atmosphere},",
                effects_format="{special_effects},",
                style_suffix="bold inks, dynamic colors, professional comic art style"
            ),
            PromptStyle.MANGA: PromptTemplate(
                style_prefix="Manga panel illustration,",
                composition_format="{composition_style} layout,",
                character_format="{character_description}, {expression}, {pose},",
                environment_format="{setting_description}, {atmosphere},",
                effects_format="{special_effects}, speed lines,",
                style_suffix="detailed linework, screentones, Japanese manga style"
            ),
            PromptStyle.GRAPHIC_NOVEL: PromptTemplate(
                style_prefix="Graphic novel illustration,",
                composition_format="{composition_style} composition,",
                character_format="{character_description}, {expression}, {pose},",
                environment_format="{setting_description}, {atmosphere},",
                effects_format="{special_effects},",
                style_suffix="painterly style, sophisticated color palette, literary graphic novel aesthetic"
            ),
            PromptStyle.CINEMATIC: PromptTemplate(
                style_prefix="Cinematic frame,",
                composition_format="{composition_style} shot,",
                character_format="{character_description}, {expression}, {pose},",
                environment_format="{setting_description}, {atmosphere},",
                effects_format="{special_effects}, depth of field,",
                style_suffix="movie still quality, cinematic lighting, photorealistic rendering"
            ),
            PromptStyle.ART_NOUVEAU: PromptTemplate(
                style_prefix="Art nouveau illustration,",
                composition_format="{composition_style} design,",
                character_format="{character_description}, {expression}, flowing {pose},",
                environment_format="{setting_description}, {atmosphere}, organic forms,",
                effects_format="{special_effects}, decorative elements,",
                style_suffix="Alphonse Mucha style, ornate borders, flowing lines, muted colors with gold accents"
            ),
            PromptStyle.SURREALIST: PromptTemplate(
                style_prefix="Surrealist painting,",
                composition_format="{composition_style} dreamscape,",
                character_format="{character_description}, {expression}, impossible {pose},",
                environment_format="{setting_description}, {atmosphere}, melting reality,",
                effects_format="{special_effects}, metaphysical elements,",
                style_suffix="Salvador Dali inspired, impossible physics, symbolic imagery, vivid contrasts"
            ),
            PromptStyle.NEO_NOIR: PromptTemplate(
                style_prefix="Neo-noir scene,",
                composition_format="{composition_style} angle,",
                character_format="{character_description}, {expression}, shadowed {pose},",
                environment_format="{setting_description}, {atmosphere}, venetian blind shadows,",
                effects_format="{special_effects}, rain-slicked surfaces,",
                style_suffix="high contrast black and white with accent colors, moody lighting, urban decay aesthetic"
            ),
            PromptStyle.WATERCOLOR: PromptTemplate(
                style_prefix="Watercolor painting,",
                composition_format="{composition_style} wash,",
                character_format="{character_description}, {expression}, fluid {pose},",
                environment_format="{setting_description}, {atmosphere}, wet-on-wet technique,",
                effects_format="{special_effects}, color bleeds,",
                style_suffix="transparent layers, soft edges, spontaneous color flows, paper texture visible"
            ),
            PromptStyle.PEN_AND_INK: PromptTemplate(
                style_prefix="Pen and ink drawing,",
                composition_format="{composition_style} sketch,",
                character_format="{character_description}, {expression}, hatched {pose},",
                environment_format="{setting_description}, {atmosphere}, crosshatched shadows,",
                effects_format="{special_effects}, stippled textures,",
                style_suffix="detailed linework, cross-hatching, high contrast, technical illustration quality"
            ),
            PromptStyle.DIGITAL_PAINTING: PromptTemplate(
                style_prefix="Digital painting artwork,",
                composition_format="{composition_style} composition,",
                character_format="{character_description}, {expression}, dynamic {pose},",
                environment_format="{setting_description}, {atmosphere}, painted details,",
                effects_format="{special_effects}, digital brush effects,",
                style_suffix="concept art quality, vibrant colors, painterly textures, professional digital art"
            )
        }
        
        # Quality enhancers
        self.quality_tags = [
            "highly detailed",
            "professional artwork",
            "trending on artstation",
            "8k resolution",
            "masterpiece"
        ]
        
        # Negative prompt components
        self.negative_components = [
            "low quality",
            "blurry",
            "distorted faces",
            "bad anatomy",
            "extra limbs",
            "text",
            "watermark",
            "signature"
        ]
        
    def generate_prompt(self, scene_data: Dict[str, Any]) -> str:
        """Generate a complete prompt from synthesized scene data."""
        # Select template
        template = self.templates.get(self.style, self.templates[PromptStyle.COMIC_BOOK])
        
        # Build prompt components
        components = []
        
        # Style prefix
        components.append(template.style_prefix)
        
        # Composition
        if scene_data.get('composition_style'):
            components.append(
                template.composition_format.format(
                    composition_style=scene_data['composition_style']
                )
            )
        
        # Character description
        character_desc = self._build_character_description(scene_data)
        if character_desc:
            components.append(character_desc)
        
        # Environment and setting
        environment_desc = self._build_environment_description(scene_data)
        if environment_desc:
            components.append(environment_desc)
        
        # Visual elements and metaphors
        visual_elements = self._build_visual_elements(scene_data)
        if visual_elements:
            components.append(visual_elements)
        
        # Special effects
        effects = self._build_special_effects(scene_data)
        if effects:
            components.append(effects)
        
        # Emotional and philosophical elements
        conceptual = self._build_conceptual_elements(scene_data)
        if conceptual:
            components.append(conceptual)
        
        # Style suffix
        components.append(template.style_suffix)
        
        # Add quality tags
        quality = self._select_quality_tags(scene_data.get('scene_complexity', 'moderate'))
        components.extend(quality)
        
        # Combine all components
        prompt = " ".join(filter(None, components))
        
        # Optimize prompt
        prompt = self._optimize_prompt(prompt, scene_data)
        
        return prompt
    
    def generate_negative_prompt(self, scene_data: Dict[str, Any]) -> str:
        """Generate negative prompt to avoid unwanted elements."""
        negative = self.negative_components.copy()
        
        # Add style-specific negatives
        if self.style == PromptStyle.COMIC_BOOK:
            negative.extend(["realistic photo", "3d render"])
        elif self.style == PromptStyle.MANGA:
            negative.extend(["western comic style", "realistic"])
        elif self.style == PromptStyle.ART_NOUVEAU:
            negative.extend(["modern style", "minimalist", "geometric abstraction"])
        elif self.style == PromptStyle.SURREALIST:
            negative.extend(["realistic", "mundane", "literal interpretation"])
        elif self.style == PromptStyle.NEO_NOIR:
            negative.extend(["bright colors", "cheerful", "flat lighting"])
        elif self.style == PromptStyle.WATERCOLOR:
            negative.extend(["hard edges", "digital artifacts", "cel shading"])
        elif self.style == PromptStyle.PEN_AND_INK:
            negative.extend(["color", "soft shading", "painterly"])
        elif self.style == PromptStyle.DIGITAL_PAINTING:
            negative.extend(["sketch", "line art", "flat colors"])
        
        # Add scene-specific negatives
        if scene_data.get('scene_complexity') == 'simple':
            negative.append("cluttered composition")
        
        return ", ".join(negative)
    
    def _build_character_description(self, scene_data: Dict[str, Any]) -> str:
        """Build character description from scene data."""
        components = []
        
        # Get character positioning
        positioning = scene_data.get('character_positioning', {})
        
        # Basic character info
        if 'character' in scene_data.get('context', {}):
            character = scene_data['context']['character']
            components.append(character.get('visual_description', ''))
        
        # Expression from emotion
        if 'emotion' in scene_data:
            expression = scene_data['emotion'].get('facial_expression', '')
            if expression:
                components.append(expression)
        
        # Body language
        if 'body_language' in scene_data.get('emotion', {}):
            pose = scene_data['emotion']['body_language'][0]
            components.append(pose)
        
        # Positioning
        if positioning:
            components.append(f"{positioning.get('placement', 'centered')} in frame")
            if positioning.get('scale') != 'medium':
                components.append(positioning['scale'])
        
        return ", ".join(filter(None, components))
    
    def _build_environment_description(self, scene_data: Dict[str, Any]) -> str:
        """Build environment description from scene data."""
        components = []
        
        setting = scene_data.get('setting', {})
        
        # Basic setting
        if setting.get('name'):
            components.append(setting['name'])
        
        # Atmospheric elements
        if setting.get('philosophical_atmosphere'):
            components.append(setting['philosophical_atmosphere'])
        
        # Emotional lighting
        if setting.get('emotional_lighting'):
            components.append(setting['emotional_lighting'])
        
        # Weather
        if setting.get('weather'):
            components.append(setting['weather'])
        
        # Time context
        time_context = setting.get('time_context')
        if time_context and time_context != 'undefined':
            components.append(f"{time_context} setting")
        
        return ", ".join(filter(None, components))
    
    def _build_visual_elements(self, scene_data: Dict[str, Any]) -> str:
        """Build visual elements from metaphors and symbols."""
        elements = []
        
        # Visual motifs
        motifs = scene_data.get('visual_motifs', [])
        if motifs:
            elements.extend(motifs[:2])  # Limit to avoid clutter
        
        # Metaphorical elements
        if 'metaphors' in scene_data:
            metaphor_visuals = scene_data['metaphors'].get('visual_elements', [])
            elements.extend(metaphor_visuals[:2])
        
        # Philosophical symbols
        if 'philosophy' in scene_data:
            symbols = scene_data['philosophy'].get('visual_symbols', [])
            elements.extend(symbols[:2])
        
        # Remove duplicates and format
        unique_elements = list(dict.fromkeys(elements))
        
        if unique_elements:
            return "featuring " + ", ".join(unique_elements[:4])
        
        return ""
    
    def _build_special_effects(self, scene_data: Dict[str, Any]) -> str:
        """Build special effects description."""
        effects = scene_data.get('special_effects', [])
        
        if not effects:
            return ""
        
        # Format effects based on style
        if self.style == PromptStyle.COMIC_BOOK:
            formatted = [f"comic {effect}" for effect in effects[:2]]
        elif self.style == PromptStyle.MANGA:
            formatted = [f"manga-style {effect}" for effect in effects[:2]]
        else:
            formatted = effects[:2]
        
        return ", ".join(formatted)
    
    def _build_conceptual_elements(self, scene_data: Dict[str, Any]) -> str:
        """Build conceptual and philosophical elements."""
        components = []
        
        # Philosophical depth
        if 'philosophy' in scene_data:
            depth = scene_data['philosophy'].get('depth_level', 0)
            if depth >= 2:
                components.append("philosophical depth")
            if depth >= 3:
                components.append("transcendent imagery")
        
        # Emotional atmosphere
        if 'emotion' in scene_data:
            colors = scene_data['emotion'].get('colors', [])
            if colors:
                components.append(f"color palette: {', '.join(colors[:2])}")
        
        # Metaphorical approach
        if 'metaphors' in scene_data:
            approach = scene_data['metaphors'].get('compositional_approach')
            if approach:
                components.append(approach)
        
        return ", ".join(components)
    
    def _select_quality_tags(self, complexity: str) -> List[str]:
        """Select appropriate quality tags based on complexity."""
        if complexity == 'simple':
            return self.quality_tags[:2]
        elif complexity == 'epic':
            return self.quality_tags
        else:
            return self.quality_tags[:3]
    
    def _optimize_prompt(self, prompt: str, scene_data: Dict[str, Any]) -> str:
        """Optimize prompt for better results."""
        # Remove redundant commas and spaces
        prompt = ", ".join(part.strip() for part in prompt.split(",") if part.strip())
        
        # Ensure important elements are front-loaded
        if scene_data.get('scene_complexity') == 'epic':
            # For complex scenes, prioritize composition and main elements
            parts = prompt.split(", ")
            # Move quality tags to end
            quality_parts = [p for p in parts if any(q in p for q in self.quality_tags)]
            other_parts = [p for p in parts if p not in quality_parts]
            prompt = ", ".join(other_parts + quality_parts)
        
        # Limit total length (some models have token limits)
        max_length = 500
        if len(prompt) > max_length:
            # Truncate while keeping essential elements
            parts = prompt.split(", ")
            essential = parts[:10]  # Keep first 10 components
            remaining = parts[10:]
            
            # Add back quality tags if removed
            for tag in self.quality_tags[:2]:
                if tag not in " ".join(essential):
                    essential.append(tag)
            
            prompt = ", ".join(essential)
        
        return prompt
    
    def generate_panel_specific_prompt(
        self,
        scene_data: Dict[str, Any],
        panel_info: Dict[str, Any]
    ) -> str:
        """Generate prompt for a specific panel in multi-panel scenes."""
        # Start with base prompt
        base_prompt = self.generate_prompt(scene_data)
        
        # Add panel-specific modifications
        panel_mods = []
        
        # Panel size
        if panel_info.get('size') == 'large':
            panel_mods.append("wide establishing shot")
        elif panel_info.get('size') == 'small':
            panel_mods.append("close-up detail")
        
        # Panel focus
        focus = panel_info.get('focus')
        if focus and focus != 'environmental':
            panel_mods.append(f"focusing on {focus}")
        
        # Panel number context
        panel_num = panel_info.get('panel_number', 1)
        total_panels = len(scene_data.get('panel_suggestions', []))
        
        if panel_num == 1 and total_panels > 1:
            panel_mods.append("establishing scene")
        elif panel_num == total_panels and total_panels > 1:
            panel_mods.append("concluding moment")
        
        # Combine modifications
        if panel_mods:
            modifications = ", ".join(panel_mods)
            # Insert after style prefix
            parts = base_prompt.split(", ", 1)
            if len(parts) == 2:
                base_prompt = f"{parts[0]}, {modifications}, {parts[1]}"
        
        return base_prompt
    
    def generate_optimized_prompt(
        self,
        scene_data: Dict[str, Any],
        optimization_level: str = "moderate",
        model_type: str = "sd"
    ) -> Tuple[str, str]:
        """Generate an optimized prompt with advanced techniques."""
        # Generate base prompt
        base_prompt = self.generate_prompt(scene_data)
        
        # Apply mood-based components
        mood = scene_data.get('emotion', {}).get('primary_emotion', 'neutral')
        mood_components = self.template_library.build_from_mood(mood)
        
        # Add mood components to prompt
        mood_text = ", ".join([comp.render() for comp in mood_components])
        if mood_text:
            base_prompt = f"{base_prompt}, {mood_text}"
        
        # Optimize based on level
        if optimization_level == "minimal":
            optimized = base_prompt
        elif optimization_level == "moderate":
            # Apply basic optimizations
            optimized = self.optimizer.remove_redundancies(base_prompt)
            key_elements = self._extract_key_elements(scene_data)
            optimized = self.optimizer.optimize_emphasis(optimized, key_elements)
        elif optimization_level == "aggressive":
            # Apply all optimizations
            optimized = self.optimizer.remove_redundancies(base_prompt)
            optimized = self.optimizer.cluster_synonyms(optimized)
            key_elements = self._extract_key_elements(scene_data)
            optimized = self.optimizer.optimize_emphasis(optimized, key_elements)
            
            # Front-load important components
            components = optimized.split(", ")
            components = self.optimizer.front_load_important(
                components,
                self.optimizer.importance_weights
            )
            optimized = ", ".join(components)
        else:
            optimized = base_prompt
        
        # Model-specific optimization
        optimized = self.optimizer.optimize_for_model(optimized, model_type)
        
        # Generate enhanced negative prompt
        negative = self.generate_enhanced_negative_prompt(scene_data, model_type)
        
        return optimized, negative
    
    def generate_enhanced_negative_prompt(
        self,
        scene_data: Dict[str, Any],
        model_type: str = "sd"
    ) -> str:
        """Generate enhanced negative prompt with context awareness."""
        # Start with base negative prompt
        negative = self.generate_negative_prompt(scene_data)
        negative_components = negative.split(", ")
        
        # Add context-aware negatives
        # Complexity-based negatives
        complexity = scene_data.get('scene_complexity', 'moderate')
        if complexity == 'epic':
            negative_components.extend([
                "simple composition", "minimal detail", "flat lighting"
            ])
        elif complexity == 'simple':
            negative_components.extend([
                "busy composition", "overwhelming detail", "chaotic"
            ])
        
        # Mood-based negatives
        mood = scene_data.get('emotion', {}).get('primary_emotion', 'neutral')
        mood_negatives = {
            'tense': ["relaxed", "peaceful", "calm"],
            'joyful': ["sad", "gloomy", "depressing"],
            'mysterious': ["obvious", "clear", "mundane"],
            'philosophical': ["superficial", "literal", "simplistic"]
        }
        
        if mood in mood_negatives:
            negative_components.extend(mood_negatives[mood])
        
        # Model-specific negatives
        if model_type == "sd":
            negative_components.extend([
                "bad hands", "bad fingers", "anatomical errors"
            ])
        elif model_type == "dalle":
            negative_components.extend([
                "tiled", "repeated patterns"
            ])
        
        # Remove duplicates and join
        unique_negatives = list(dict.fromkeys(negative_components))
        return ", ".join(unique_negatives)
    
    def generate_mixed_style_prompt(
        self,
        scene_data: Dict[str, Any],
        primary_style: str,
        secondary_style: str,
        mix_ratio: float = 0.7
    ) -> str:
        """Generate prompt with mixed artistic styles."""
        # Get style mix information
        mix_info = self.style_mixer.mix_styles(
            primary_style, secondary_style, mix_ratio
        )
        
        # Generate prompts for both styles
        self.style = PromptStyle(primary_style.lower())
        primary_prompt = self.generate_prompt(scene_data)
        
        self.style = PromptStyle(secondary_style.lower())
        secondary_prompt = self.generate_prompt(scene_data)
        
        # Extract key components from both
        primary_parts = primary_prompt.split(", ")
        secondary_parts = secondary_prompt.split(", ")
        
        # Mix based on ratio
        mixed_parts = []
        
        # Take style prefix based on mix
        if mix_ratio > 0.5:
            mixed_parts.append(f"{mix_info['blend_description']},")
        else:
            mixed_parts.append(f"{mix_info['blend_description']},")
        
        # Mix other components
        primary_count = int(len(primary_parts) * mix_ratio)
        secondary_count = int(len(secondary_parts) * (1 - mix_ratio))
        
        mixed_parts.extend(primary_parts[1:primary_count])
        mixed_parts.extend(secondary_parts[1:secondary_count])
        
        # Add mixed techniques
        techniques = mix_info['technique_mix']
        if techniques:
            mixed_parts.extend(techniques)
        
        # Add compatibility warning if needed
        if not mix_info['compatible']:
            self.logger.warning(
                f"Styles {primary_style} and {secondary_style} may not blend well"
            )
        
        return ", ".join(mixed_parts)
    
    def _extract_key_elements(self, scene_data: Dict[str, Any]) -> List[str]:
        """Extract key elements from scene data for emphasis."""
        key_elements = []
        
        # Character name or description
        if 'character' in scene_data.get('context', {}):
            character = scene_data['context']['character']
            if character.get('name'):
                key_elements.append(character['name'])
        
        # Primary emotion
        if 'emotion' in scene_data:
            emotion = scene_data['emotion'].get('primary_emotion')
            if emotion:
                key_elements.append(emotion)
        
        # Main philosophical concept
        if 'philosophy' in scene_data:
            concepts = scene_data['philosophy'].get('concepts', [])
            if concepts:
                key_elements.append(concepts[0])
        
        # Critical visual elements
        motifs = scene_data.get('visual_motifs', [])
        if motifs:
            key_elements.extend(motifs[:2])
        
        return key_elements
    
    def generate_batch_prompts(
        self,
        scene_data: Dict[str, Any],
        variations: int = 4,
        style_variations: bool = True
    ) -> List[Dict[str, str]]:
        """Generate multiple prompt variations for A/B testing."""
        prompts = []
        
        if style_variations:
            # Generate prompts in different styles
            styles = [
                PromptStyle.COMIC_BOOK, PromptStyle.CINEMATIC,
                PromptStyle.WATERCOLOR, PromptStyle.DIGITAL_PAINTING
            ]
            for i, style in enumerate(styles[:variations]):
                self.style = style
                prompt = self.generate_prompt(scene_data)
                negative = self.generate_negative_prompt(scene_data)
                
                prompts.append({
                    "id": f"style_variation_{i}",
                    "style": style.value,
                    "prompt": prompt,
                    "negative_prompt": negative,
                    "optimization": "moderate"
                })
        else:
            # Generate variations with different optimizations
            optimization_levels = ["minimal", "moderate", "aggressive"]
            model_types = ["sd", "dalle", "midjourney"]
            
            for i in range(variations):
                opt_level = optimization_levels[i % len(optimization_levels)]
                model = model_types[i % len(model_types)]
                
                prompt, negative = self.generate_optimized_prompt(
                    scene_data, opt_level, model
                )
                
                prompts.append({
                    "id": f"optimization_variation_{i}",
                    "style": self.style.value,
                    "prompt": prompt,
                    "negative_prompt": negative,
                    "optimization": opt_level,
                    "model": model
                })
        
        return prompts