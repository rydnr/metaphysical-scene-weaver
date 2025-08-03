"""Reusable prompt templates and components for image generation."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EmphasisLevel(Enum):
    """Emphasis levels for prompt components."""
    SUBTLE = 1
    MODERATE = 2
    STRONG = 3
    EXTREME = 4


class AspectRatio(Enum):
    """Common aspect ratios for image generation."""
    SQUARE = "1:1"
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    WIDE = "21:9"
    TALL = "9:21"
    GOLDEN = "1.618:1"


@dataclass
class PromptComponent:
    """Reusable prompt component with metadata."""
    text: str
    category: str
    emphasis: EmphasisLevel = EmphasisLevel.MODERATE
    weight: float = 1.0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def render(self, emphasis_brackets: bool = True) -> str:
        """Render component with optional emphasis."""
        if not emphasis_brackets:
            return self.text
        
        # Apply emphasis using bracket notation
        if self.emphasis == EmphasisLevel.SUBTLE:
            return self.text
        elif self.emphasis == EmphasisLevel.MODERATE:
            return f"({self.text})"
        elif self.emphasis == EmphasisLevel.STRONG:
            return f"(({self.text}))"
        elif self.emphasis == EmphasisLevel.EXTREME:
            return f"((({self.text})))"
        
        return self.text


class PromptTemplateLibrary:
    """Library of reusable prompt components and templates."""
    
    def __init__(self):
        # Lighting components
        self.lighting_components = {
            "dramatic": PromptComponent(
                "dramatic lighting, chiaroscuro, strong shadows",
                "lighting", EmphasisLevel.STRONG, tags=["mood", "contrast"]
            ),
            "soft": PromptComponent(
                "soft diffused lighting, gentle glow",
                "lighting", EmphasisLevel.MODERATE, tags=["peaceful", "dreamy"]
            ),
            "golden_hour": PromptComponent(
                "golden hour lighting, warm sunset glow, long shadows",
                "lighting", EmphasisLevel.MODERATE, tags=["warm", "nostalgic"]
            ),
            "neon": PromptComponent(
                "neon lighting, cyberpunk glow, fluorescent colors",
                "lighting", EmphasisLevel.STRONG, tags=["urban", "futuristic"]
            ),
            "ethereal": PromptComponent(
                "ethereal lighting, supernatural glow, otherworldly radiance",
                "lighting", EmphasisLevel.STRONG, tags=["mystical", "spiritual"]
            ),
            "film_noir": PromptComponent(
                "film noir lighting, venetian blind shadows, stark contrasts",
                "lighting", EmphasisLevel.STRONG, tags=["noir", "dramatic"]
            )
        }
        
        # Atmosphere components
        self.atmosphere_components = {
            "mystical": PromptComponent(
                "mystical atmosphere, otherworldly presence, magical aura",
                "atmosphere", EmphasisLevel.STRONG, tags=["fantasy", "spiritual"]
            ),
            "oppressive": PromptComponent(
                "oppressive atmosphere, heavy air, sense of dread",
                "atmosphere", EmphasisLevel.STRONG, tags=["dark", "horror"]
            ),
            "serene": PromptComponent(
                "serene atmosphere, peaceful tranquility, calm presence",
                "atmosphere", EmphasisLevel.MODERATE, tags=["peaceful", "meditative"]
            ),
            "chaotic": PromptComponent(
                "chaotic atmosphere, swirling energy, dynamic motion",
                "atmosphere", EmphasisLevel.STRONG, tags=["action", "intense"]
            ),
            "melancholic": PromptComponent(
                "melancholic atmosphere, wistful mood, quiet sadness",
                "atmosphere", EmphasisLevel.MODERATE, tags=["emotional", "introspective"]
            ),
            "transcendent": PromptComponent(
                "transcendent atmosphere, elevated consciousness, spiritual awakening",
                "atmosphere", EmphasisLevel.EXTREME, tags=["philosophical", "spiritual"]
            )
        }
        
        # Composition components
        self.composition_components = {
            "rule_of_thirds": PromptComponent(
                "rule of thirds composition, balanced layout",
                "composition", EmphasisLevel.MODERATE, tags=["classical", "balanced"]
            ),
            "symmetrical": PromptComponent(
                "perfectly symmetrical composition, mirror balance",
                "composition", EmphasisLevel.STRONG, tags=["formal", "stable"]
            ),
            "dynamic_diagonal": PromptComponent(
                "dynamic diagonal composition, tilted perspective",
                "composition", EmphasisLevel.STRONG, tags=["action", "movement"]
            ),
            "spiral": PromptComponent(
                "spiral composition, fibonacci sequence, golden ratio",
                "composition", EmphasisLevel.STRONG, tags=["natural", "flowing"]
            ),
            "centered": PromptComponent(
                "centered composition, focal point emphasis",
                "composition", EmphasisLevel.MODERATE, tags=["focus", "simple"]
            ),
            "layered": PromptComponent(
                "layered composition, foreground midground background",
                "composition", EmphasisLevel.MODERATE, tags=["depth", "complex"]
            )
        }
        
        # Camera angle components
        self.camera_components = {
            "low_angle": PromptComponent(
                "low angle shot, looking up, heroic perspective",
                "camera", EmphasisLevel.MODERATE, tags=["dramatic", "powerful"]
            ),
            "high_angle": PromptComponent(
                "high angle shot, looking down, vulnerable perspective",
                "camera", EmphasisLevel.MODERATE, tags=["dramatic", "weak"]
            ),
            "dutch_angle": PromptComponent(
                "dutch angle, tilted camera, disorienting view",
                "camera", EmphasisLevel.STRONG, tags=["unsettling", "dynamic"]
            ),
            "aerial": PromptComponent(
                "aerial view, bird's eye perspective, overhead shot",
                "camera", EmphasisLevel.STRONG, tags=["epic", "establishing"]
            ),
            "close_up": PromptComponent(
                "extreme close-up, intimate detail, macro view",
                "camera", EmphasisLevel.STRONG, tags=["intimate", "detail"]
            ),
            "wide_shot": PromptComponent(
                "wide establishing shot, panoramic view",
                "camera", EmphasisLevel.MODERATE, tags=["epic", "context"]
            )
        }
        
        # Color palette components
        self.color_components = {
            "monochromatic": PromptComponent(
                "monochromatic color scheme, tonal variations",
                "color", EmphasisLevel.MODERATE, tags=["unified", "sophisticated"]
            ),
            "complementary": PromptComponent(
                "complementary colors, vibrant contrasts",
                "color", EmphasisLevel.MODERATE, tags=["vibrant", "balanced"]
            ),
            "cool_tones": PromptComponent(
                "cool color palette, blues and greens, calming tones",
                "color", EmphasisLevel.MODERATE, tags=["calm", "professional"]
            ),
            "warm_tones": PromptComponent(
                "warm color palette, reds and oranges, inviting tones",
                "color", EmphasisLevel.MODERATE, tags=["cozy", "energetic"]
            ),
            "pastel": PromptComponent(
                "soft pastel colors, gentle hues, dreamy palette",
                "color", EmphasisLevel.MODERATE, tags=["soft", "dreamy"]
            ),
            "noir": PromptComponent(
                "noir color scheme, black and white with red accents",
                "color", EmphasisLevel.STRONG, tags=["dramatic", "classic"]
            )
        }
        
        # Texture components
        self.texture_components = {
            "rough": PromptComponent(
                "rough textures, gritty surface, tactile quality",
                "texture", EmphasisLevel.MODERATE, tags=["raw", "organic"]
            ),
            "smooth": PromptComponent(
                "smooth polished surfaces, sleek finish",
                "texture", EmphasisLevel.MODERATE, tags=["modern", "clean"]
            ),
            "organic": PromptComponent(
                "organic textures, natural patterns, living surfaces",
                "texture", EmphasisLevel.MODERATE, tags=["natural", "flowing"]
            ),
            "metallic": PromptComponent(
                "metallic textures, reflective surfaces, chrome finish",
                "texture", EmphasisLevel.MODERATE, tags=["tech", "modern"]
            ),
            "weathered": PromptComponent(
                "weathered textures, aged patina, worn surfaces",
                "texture", EmphasisLevel.MODERATE, tags=["vintage", "story"]
            )
        }
        
        # Special effects components
        self.effect_components = {
            "particle": PromptComponent(
                "particle effects, floating motes, atmospheric dust",
                "effects", EmphasisLevel.MODERATE, tags=["atmosphere", "magical"]
            ),
            "motion_blur": PromptComponent(
                "motion blur, speed lines, dynamic movement",
                "effects", EmphasisLevel.MODERATE, tags=["action", "speed"]
            ),
            "lens_flare": PromptComponent(
                "lens flare, light streaks, cinematic glare",
                "effects", EmphasisLevel.SUBTLE, tags=["cinematic", "bright"]
            ),
            "smoke": PromptComponent(
                "atmospheric smoke, fog effects, misty ambiance",
                "effects", EmphasisLevel.MODERATE, tags=["atmosphere", "mystery"]
            ),
            "energy": PromptComponent(
                "energy effects, glowing auras, power manifestation",
                "effects", EmphasisLevel.STRONG, tags=["power", "magical"]
            ),
            "shatter": PromptComponent(
                "shattered fragments, breaking apart, destruction",
                "effects", EmphasisLevel.STRONG, tags=["action", "dramatic"]
            )
        }
        
        # Philosophical visual metaphors
        self.philosophical_components = {
            "duality": PromptComponent(
                "visual duality, yin-yang balance, opposing forces",
                "philosophical", EmphasisLevel.STRONG, tags=["balance", "contrast"]
            ),
            "transcendence": PromptComponent(
                "transcendent imagery, ascending forms, spiritual elevation",
                "philosophical", EmphasisLevel.EXTREME, tags=["spiritual", "uplifting"]
            ),
            "interconnection": PromptComponent(
                "interconnected elements, web of relationships, unity",
                "philosophical", EmphasisLevel.STRONG, tags=["unity", "connection"]
            ),
            "impermanence": PromptComponent(
                "impermanent forms, dissolving boundaries, transient beauty",
                "philosophical", EmphasisLevel.STRONG, tags=["temporal", "fleeting"]
            ),
            "emergence": PromptComponent(
                "emergent patterns, self-organizing forms, complexity",
                "philosophical", EmphasisLevel.STRONG, tags=["growth", "complexity"]
            ),
            "void": PromptComponent(
                "void spaces, negative space emphasis, emptiness",
                "philosophical", EmphasisLevel.STRONG, tags=["minimal", "zen"]
            )
        }
    
    def get_component(self, category: str, name: str) -> Optional[PromptComponent]:
        """Get a specific component by category and name."""
        category_map = {
            "lighting": self.lighting_components,
            "atmosphere": self.atmosphere_components,
            "composition": self.composition_components,
            "camera": self.camera_components,
            "color": self.color_components,
            "texture": self.texture_components,
            "effects": self.effect_components,
            "philosophical": self.philosophical_components
        }
        
        components = category_map.get(category, {})
        return components.get(name)
    
    def get_components_by_tags(self, tags: List[str]) -> List[PromptComponent]:
        """Get all components matching any of the given tags."""
        matching = []
        all_components = [
            *self.lighting_components.values(),
            *self.atmosphere_components.values(),
            *self.composition_components.values(),
            *self.camera_components.values(),
            *self.color_components.values(),
            *self.texture_components.values(),
            *self.effect_components.values(),
            *self.philosophical_components.values()
        ]
        
        for component in all_components:
            if any(tag in component.tags for tag in tags):
                matching.append(component)
        
        return matching
    
    def build_from_mood(self, mood: str) -> List[PromptComponent]:
        """Build a component set based on mood."""
        mood_mappings = {
            "dark": ["dramatic", "oppressive", "noir", "rough"],
            "light": ["soft", "serene", "pastel", "smooth"],
            "energetic": ["chaotic", "dynamic_diagonal", "warm_tones", "motion_blur"],
            "mysterious": ["mystical", "ethereal", "smoke", "void"],
            "romantic": ["golden_hour", "soft", "warm_tones", "lens_flare"],
            "philosophical": ["transcendent", "duality", "interconnection", "emergence"]
        }
        
        component_names = mood_mappings.get(mood.lower(), [])
        components = []
        
        for name in component_names:
            # Search all categories for the component
            for category in ["lighting", "atmosphere", "composition", "camera", 
                           "color", "texture", "effects", "philosophical"]:
                comp = self.get_component(category, name)
                if comp:
                    components.append(comp)
                    break
        
        return components


class PromptOptimizer:
    """Optimizes prompts for better generation results."""
    
    def __init__(self):
        # Token weights for importance
        self.importance_weights = {
            "subject": 3.0,
            "style": 2.5,
            "composition": 2.0,
            "lighting": 1.8,
            "atmosphere": 1.5,
            "details": 1.2,
            "quality": 1.0
        }
        
        # Semantic clusters for related terms
        self.semantic_clusters = {
            "lighting": {
                "bright": ["luminous", "radiant", "glowing", "illuminated"],
                "dark": ["shadowy", "dim", "obscured", "tenebrous"],
                "dramatic": ["chiaroscuro", "contrasted", "theatrical", "stark"]
            },
            "atmosphere": {
                "peaceful": ["serene", "tranquil", "calm", "quiet"],
                "intense": ["dramatic", "powerful", "overwhelming", "extreme"],
                "mysterious": ["enigmatic", "cryptic", "mystical", "arcane"]
            },
            "quality": {
                "detailed": ["intricate", "elaborate", "complex", "refined"],
                "professional": ["masterful", "expert", "polished", "sophisticated"],
                "artistic": ["creative", "expressive", "stylized", "aesthetic"]
            }
        }
    
    def optimize_emphasis(self, prompt: str, key_elements: List[str]) -> str:
        """Add emphasis to key elements in the prompt."""
        optimized = prompt
        
        for element in key_elements:
            if element in optimized and f"({element})" not in optimized:
                # Add moderate emphasis
                optimized = optimized.replace(element, f"({element})")
        
        return optimized
    
    def cluster_synonyms(self, prompt: str, preserve_original: bool = True) -> str:
        """Replace terms with semantically similar but more effective ones."""
        words = prompt.split()
        optimized_words = []
        
        for word in words:
            replaced = False
            
            # Check if word belongs to any semantic cluster
            for category, clusters in self.semantic_clusters.items():
                for key, synonyms in clusters.items():
                    if word.lower() in [s.lower() for s in synonyms]:
                        # Use the cluster key as the primary term
                        if preserve_original:
                            optimized_words.append(f"{key} ({word})")
                        else:
                            optimized_words.append(key)
                        replaced = True
                        break
                if replaced:
                    break
            
            if not replaced:
                optimized_words.append(word)
        
        return " ".join(optimized_words)
    
    def front_load_important(self, components: List[str], importance_map: Dict[str, float]) -> List[str]:
        """Reorder components by importance for front-loading."""
        # Create tuples of (component, importance_score)
        scored_components = []
        
        for comp in components:
            # Determine component type and assign score
            score = 1.0  # default
            for key, weight in importance_map.items():
                if key.lower() in comp.lower():
                    score = weight
                    break
            scored_components.append((comp, score))
        
        # Sort by score (descending)
        scored_components.sort(key=lambda x: x[1], reverse=True)
        
        # Return just the components
        return [comp for comp, _ in scored_components]
    
    def remove_redundancies(self, prompt: str) -> str:
        """Remove redundant terms and phrases."""
        # Split into components
        components = [c.strip() for c in prompt.split(",")]
        
        # Track seen concepts
        seen_concepts = set()
        filtered_components = []
        
        for comp in components:
            # Extract key concepts (simplified approach)
            key_words = set(comp.lower().split())
            
            # Check for significant overlap
            if not seen_concepts or len(key_words & seen_concepts) < len(key_words) * 0.5:
                filtered_components.append(comp)
                seen_concepts.update(key_words)
        
        return ", ".join(filtered_components)
    
    def optimize_for_model(self, prompt: str, model_type: str = "sd") -> str:
        """Optimize prompt for specific model types."""
        if model_type == "sd":  # Stable Diffusion
            # SD responds well to quality tags at the end
            quality_tags = ["masterpiece", "best quality", "highly detailed"]
            if not any(tag in prompt.lower() for tag in quality_tags):
                prompt += f", {', '.join(quality_tags[:2])}"
        
        elif model_type == "dalle":  # DALL-E
            # DALL-E prefers natural language descriptions
            prompt = prompt.replace("((", "(").replace("))", ")")
            prompt = prompt.replace(",", ", ")  # Ensure proper spacing
        
        elif model_type == "midjourney":  # Midjourney
            # Midjourney responds well to style references
            if "--" not in prompt:
                prompt += " --stylize 100 --quality 2"
        
        return prompt


class StyleMixer:
    """Mixes multiple art styles for hybrid approaches."""
    
    def __init__(self):
        self.style_compatibility = {
            "comic book": ["manga", "graphic novel", "pen and ink"],
            "watercolor": ["pen and ink", "digital painting"],
            "art nouveau": ["surrealist", "graphic novel"],
            "neo-noir": ["comic book", "graphic novel", "cinematic"],
            "cinematic": ["digital painting", "neo-noir"],
            "surrealist": ["art nouveau", "digital painting"]
        }
    
    def mix_styles(
        self,
        primary_style: str,
        secondary_style: str,
        ratio: float = 0.7
    ) -> Dict[str, Any]:
        """Mix two styles with a given ratio (0-1, where 1 = all primary)."""
        # Check compatibility
        compatible = self._check_compatibility(primary_style, secondary_style)
        
        mix_result = {
            "primary_style": primary_style,
            "secondary_style": secondary_style,
            "ratio": ratio,
            "compatible": compatible,
            "blend_description": self._generate_blend_description(
                primary_style, secondary_style, ratio
            ),
            "technique_mix": self._mix_techniques(primary_style, secondary_style, ratio),
            "recommended_elements": self._get_recommended_elements(
                primary_style, secondary_style
            )
        }
        
        return mix_result
    
    def _check_compatibility(self, style1: str, style2: str) -> bool:
        """Check if two styles are compatible for mixing."""
        return (style2 in self.style_compatibility.get(style1, []) or
                style1 in self.style_compatibility.get(style2, []))
    
    def _generate_blend_description(
        self,
        primary: str,
        secondary: str,
        ratio: float
    ) -> str:
        """Generate a description of the blended style."""
        if ratio >= 0.8:
            return f"{primary} style with subtle {secondary} influences"
        elif ratio >= 0.6:
            return f"predominantly {primary} with {secondary} elements"
        elif ratio >= 0.4:
            return f"balanced blend of {primary} and {secondary} styles"
        else:
            return f"{secondary} style with {primary} touches"
    
    def _mix_techniques(
        self,
        primary: str,
        secondary: str,
        ratio: float
    ) -> List[str]:
        """Mix technical approaches from both styles."""
        techniques = []
        
        # Define technique mappings
        style_techniques = {
            "watercolor": ["wet-on-wet", "color bleeds", "transparent layers"],
            "pen and ink": ["cross-hatching", "stippling", "line weight variation"],
            "comic book": ["bold inks", "dynamic panels", "speech bubbles"],
            "surrealist": ["impossible physics", "dream logic", "symbolic imagery"],
            "art nouveau": ["organic forms", "decorative borders", "flowing lines"]
        }
        
        primary_techs = style_techniques.get(primary, [])
        secondary_techs = style_techniques.get(secondary, [])
        
        # Mix based on ratio
        primary_count = int(len(primary_techs) * ratio)
        secondary_count = int(len(secondary_techs) * (1 - ratio))
        
        techniques.extend(primary_techs[:primary_count])
        techniques.extend(secondary_techs[:secondary_count])
        
        return techniques
    
    def _get_recommended_elements(self, style1: str, style2: str) -> Dict[str, List[str]]:
        """Get recommended visual elements for style combination."""
        recommendations = {
            "avoid": [],
            "emphasize": [],
            "balance": []
        }
        
        # Style-specific recommendations
        if "watercolor" in [style1, style2] and "pen and ink" in [style1, style2]:
            recommendations["emphasize"].extend(["line and wash technique", "selective coloring"])
            recommendations["balance"].extend(["wet and dry media", "detail and flow"])
        
        if "comic book" in [style1, style2] and "noir" in [style1, style2]:
            recommendations["emphasize"].extend(["dramatic shadows", "limited color palette"])
            recommendations["avoid"].extend(["bright colors", "soft lighting"])
        
        return recommendations