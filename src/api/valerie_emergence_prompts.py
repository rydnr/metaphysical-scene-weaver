"""Specialized prompt generation for Valerie's emergence sequence (scenes 007-009)."""

from typing import Dict, List, Any
from dataclasses import dataclass
from batch_prompt_generator import SceneData, IntegratedPromptPipeline


class ValerieEmergenceGenerator:
    """Generator for the liminal emergence sequence."""
    
    def __init__(self):
        self.pipeline = IntegratedPromptPipeline()
        
    def create_emergence_scenes(self) -> List[SceneData]:
        """Create scene data for Valerie's emergence trilogy."""
        
        scenes = [
            # Scene 007: Freedom vs Illusion
            SceneData(
                scene_id="007_freedom_illusion",
                entry_number=7,
                dialogue="So you're saying we're all just... automatons? That freedom is an illusion?",
                character="Evan",
                panel_type="3-panel",
                philosophical_concept="freedom as illusion",
                depth_level=2,
                metaphors=[
                    "birds choosing their cages",
                    "open doors leading to new prisons",
                    "keys that lock instead of unlock"
                ],
                primary_emotion="frustrated yearning",
                emotion_intensity=0.7,
                color_palette=["caged gold", "illusory blue", "freedom violet"],
                atmospheric_effects=[
                    "particle trails showing paths",
                    "multiple cage options floating",
                    "hesitation visualization"
                ],
                folder_path="content/007_freedom_illusion",
                narrator_voice="mystic poet",
                visual_notes="Evan gestures wildly, frustrated"
            ),
            
            # Scene 008: Escape Paradox
            SceneData(
                scene_id="008_escape_paradox",
                entry_number=8,
                dialogue="I'm saying that true freedom begins with recognizing our constraints. You cannot escape a cage you don't know exists.",
                character="Monday",
                panel_type="single",
                philosophical_concept="transcending duality",
                depth_level=3,
                metaphors=[
                    "cage boundaries becoming doorways",
                    "prison bars transforming to light beams",
                    "escape routes leading back to center"
                ],
                primary_emotion="paradoxical wisdom",
                emotion_intensity=0.6,
                color_palette=["boundary dissolution purple", "doorway light", "paradox silver"],
                atmospheric_effects=[
                    "boundaries shimmering and shifting",
                    "dual nature visible simultaneously",
                    "transformation particles"
                ],
                folder_path="content/008_escape_paradox",
                narrator_voice="sage",
                visual_notes="Monday's knowing expression"
            ),
            
            # Scene 009: Valerie's Emergence
            SceneData(
                scene_id="009_valerie_emergence",
                entry_number=9,
                dialogue="Perhaps the cage IS the belief that we need to escape anything at all.",
                character="Valerie",
                panel_type="single",
                philosophical_concept="liminality embodied",
                depth_level=3,
                metaphors=[
                    "space between thoughts taking form",
                    "negative space becoming positive",
                    "void birthing presence"
                ],
                primary_emotion="uncanny wonder",
                emotion_intensity=0.9,
                color_palette=["shadow purple", "emergence gold", "liminal silver"],
                atmospheric_effects=[
                    "particles coalescing from nothing",
                    "shadow solidifying into form",
                    "reality rippling at emergence point"
                ],
                folder_path="content/009_valerie_emergence",
                narrator_voice="mystic poet",
                visual_notes="Valerie emerges from shadows"
            )
        ]
        
        return scenes
    
    def generate_emergence_prompts(self) -> Dict[str, Any]:
        """Generate specialized prompts for emergence scenes."""
        
        scenes = self.create_emergence_scenes()
        results = []
        
        for scene in scenes:
            # Create ethereal base prompt
            base_prompt = self._create_ethereal_base(scene)
            
            # Create liminal variations
            variations = self._create_liminal_variations(scene, base_prompt)
            
            # Package for API
            scene_result = {
                "scene_id": scene.scene_id,
                "base_prompt": base_prompt,
                "variations": variations,
                "special_notes": self._get_emergence_instructions(scene),
                "particle_effects": self._get_particle_specifications(scene)
            }
            
            results.append(scene_result)
            
        return {
            "sequence": "valerie_emergence",
            "scenes": results,
            "transition_notes": self._create_emergence_transitions(),
            "style_guide": self._create_ethereal_style_guide()
        }
    
    def _create_ethereal_base(self, scene: SceneData) -> str:
        """Create ethereal base prompt for emergence scenes."""
        
        # Ethereal style emphasis
        style = "Ethereal digital art with particle effects and translucent elements"
        
        # Liminal composition
        if scene.scene_id == "009_valerie_emergence":
            composition = "emergence composition, negative space transforming"
        elif scene.depth_level >= 3:
            composition = "paradoxical perspective, dual realities visible"
        else:
            composition = "floating elements composition, dreamlike arrangement"
        
        # Character with philosophical state
        character = f"{scene.character} embodying {scene.philosophical_concept}"
        
        # Enhanced emotion with liminal quality
        emotion = f"{scene.primary_emotion}, liminal atmosphere"
        
        # Ethereal effects
        effects = ", ".join([
            "particle systems",
            "translucent boundaries",
            *scene.metaphors[:2],
            *scene.atmospheric_effects[:2]
        ])
        
        # Quality with ethereal emphasis
        quality = "otherworldly quality, luminous rendering, professional digital art"
        
        return f"{style}, {composition}, {character}, {emotion}, {effects}, {quality}"
    
    def _create_liminal_variations(
        self, 
        scene: SceneData, 
        base_prompt: str
    ) -> List[Dict[str, str]]:
        """Create variations emphasizing liminal aspects."""
        
        variations = []
        
        # Variation 1: Particle emphasis
        particle_prompt = base_prompt.replace(
            "particle systems",
            "elaborate particle systems, consciousness particles visible"
        )
        variations.append({
            "type": "particle_emphasis",
            "prompt": particle_prompt,
            "focus": "Materialization through particles"
        })
        
        # Variation 2: Boundary emphasis
        boundary_prompt = base_prompt.replace(
            "translucent boundaries",
            "boundaries dissolving and reforming, threshold spaces prominent"
        )
        variations.append({
            "type": "boundary_emphasis",
            "prompt": boundary_prompt,
            "focus": "Liminal space visualization"
        })
        
        # Variation 3: Shadow-to-light emphasis
        shadow_prompt = base_prompt + ", dramatic shadow to light transformation"
        variations.append({
            "type": "shadow_light_emphasis",
            "prompt": shadow_prompt,
            "focus": "Emergence from darkness"
        })
        
        # Variation 4: Philosophical visualization
        philosophy_prompt = base_prompt.replace(
            scene.philosophical_concept,
            f"vivid visualization of {scene.philosophical_concept}"
        )
        variations.append({
            "type": "philosophy_emphasis",
            "prompt": philosophy_prompt,
            "focus": "Abstract concept made visible"
        })
        
        return variations
    
    def _get_emergence_instructions(self, scene: SceneData) -> Dict[str, str]:
        """Get special instructions for emergence rendering."""
        
        instructions = {
            "007_freedom_illusion": {
                "critical_element": "Multiple cage options with birds hesitating",
                "avoid": "trapped feeling, hopelessness",
                "emphasize": "choice paradox, beautiful cages, freedom illusion",
                "particles": "Choice paths visible as particle trails"
            },
            "008_escape_paradox": {
                "critical_element": "Cage bars transforming into doorways",
                "avoid": "simple prison imagery, one-dimensional thinking",
                "emphasize": "duality transcendence, boundaries as opportunities",
                "particles": "Transformation particles at boundary points"
            },
            "009_valerie_emergence": {
                "critical_element": "Negative space coalescing into Valerie's form",
                "avoid": "sudden appearance, solid emergence",
                "emphasize": "gradual materialization, void birthing presence",
                "particles": "Shadow particles forming feminine figure"
            }
        }
        
        return instructions.get(scene.scene_id, {})
    
    def _get_particle_specifications(self, scene: SceneData) -> Dict[str, Any]:
        """Get detailed particle effect specifications."""
        
        specs = {
            "007_freedom_illusion": {
                "type": "choice_particles",
                "behavior": "branching paths from character",
                "color": "golden with blue traces",
                "density": "moderate",
                "movement": "hesitant, recursive"
            },
            "008_escape_paradox": {
                "type": "transformation_particles",
                "behavior": "circulating at boundaries",
                "color": "silver to light transition",
                "density": "high at transformation points",
                "movement": "spiral patterns"
            },
            "009_valerie_emergence": {
                "type": "coalescence_particles",
                "behavior": "gathering from void spaces",
                "color": "shadow purple to emergence gold",
                "density": "increasing toward form",
                "movement": "gravitating to center"
            }
        }
        
        return specs.get(scene.scene_id, {})
    
    def _create_emergence_transitions(self) -> Dict[str, str]:
        """Create transition notes for emergence sequence."""
        
        return {
            "007_to_008": "Frustrated questioning transforms into wise understanding",
            "008_to_009": "Monday's paradox opens space for Valerie's arrival",
            "emergence_arc": "Question freedom → Understand paradox → Embody transcendence",
            "particle_progression": "Choice trails → Transformation spirals → Coalescence",
            "philosophical_journey": "Illusion recognition → Duality transcendence → Liminal embodiment"
        }
    
    def _create_ethereal_style_guide(self) -> Dict[str, Any]:
        """Create style guide for ethereal rendering."""
        
        return {
            "primary_style": "Ethereal digital art",
            "key_elements": [
                "Translucent layers",
                "Particle systems",
                "Light emanation",
                "Shadow play",
                "Boundary dissolution"
            ],
            "color_approach": {
                "base": "Deep purples and shadow tones",
                "accent": "Gold and silver highlights",
                "transition": "Gradient shifts at boundaries"
            },
            "rendering_notes": {
                "transparency": "30-70% opacity for liminal elements",
                "glow": "Soft emanation from emerging forms",
                "particles": "Consciousness visible as light motes",
                "edges": "Soft, dissolving boundaries"
            }
        }


# Test the emergence generation
def test_valerie_emergence():
    """Test prompt generation for Valerie emergence sequence."""
    
    generator = ValerieEmergenceGenerator()
    results = generator.generate_emergence_prompts()
    
    print("=== VALERIE EMERGENCE SEQUENCE ===\n")
    
    for scene in results["scenes"]:
        print(f"Scene: {scene['scene_id']}")
        print(f"Base prompt ({len(scene['base_prompt'].split())} words):")
        print(f"  {scene['base_prompt'][:100]}...")
        print(f"Variations: {len(scene['variations'])}")
        print(f"Particle specs: {scene['particle_effects']['type']}")
        print()
    
    print("=== STYLE GUIDE ===")
    guide = results["style_guide"]
    print(f"Primary style: {guide['primary_style']}")
    print(f"Key elements: {', '.join(guide['key_elements'][:3])}...")
    
    # Process through pipeline
    scenes = generator.create_emergence_scenes()
    pipeline = generator.pipeline
    batch_results = pipeline.process_batch(scenes)
    
    print("\n=== BATCH PROCESSING RESULTS ===")
    for result in batch_results:
        print(f"{result['scene_id']}: {result['quality_metrics']['avg_tokens']} tokens, "
              f"{result['quality_metrics']['avg_quality']:.2f} quality")
    
    return generator, results


if __name__ == "__main__":
    generator, results = test_valerie_emergence()
    print("\nValerie emergence prompts ready for ethereal visualization!")