"""Main orchestrator for the Metaphysical Scene Weaver system."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import logging
from dataclasses import dataclass

from ..processors.context_analyzer import ContextAnalyzer
from ..processors.philosophical_interpreter import PhilosophicalInterpreter
from ..processors.emotional_mapper import EmotionalMapper
from ..processors.metaphor_translator import MetaphorTranslator
from ..processors.scene_synthesizer import SceneSynthesizer
from ..processors.prompt_generator import PromptGenerator
from .script_parser import ScriptParser, ScriptEntry
from .character_state_tracker import CharacterStateTracker


@dataclass
class EnrichedScene:
    """Represents a scene with all enrichment layers applied."""
    entry_id: str
    prompt: str
    metadata: Dict[str, Any]
    philosophy: Dict[str, Any]
    emotion: Dict[str, Any]
    visual_elements: List[str]


class SceneWeaver:
    """Main orchestrator that coordinates all components to transform scripts into visual prompts."""
    
    def __init__(
        self,
        characters_file: Path,
        places_file: Path,
        style: str = "comic book",
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the Scene Weaver with all necessary components."""
        self.logger = logging.getLogger(__name__)
        
        # Load data files
        self.characters = self._load_json(characters_file)
        self.places = self._load_json(places_file)
        
        # Initialize components
        self.parser = ScriptParser()
        self.state_tracker = CharacterStateTracker()
        self.context_analyzer = ContextAnalyzer(self.characters, self.places)
        self.philosophical_interpreter = PhilosophicalInterpreter()
        self.emotional_mapper = EmotionalMapper()
        self.metaphor_translator = MetaphorTranslator()
        self.scene_synthesizer = SceneSynthesizer()
        self.prompt_generator = PromptGenerator(style)
        
        # Configuration
        self.config = config or self._default_config()
        
        # Processing state
        self.current_session = []
        self.enriched_scenes = []
        
    def _load_json(self, filepath: Path) -> Dict[str, Any]:
        """Load JSON data from file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'philosophy_weight': 0.4,
            'emotion_weight': 0.3,
            'visual_weight': 0.3,
            'enable_continuity': True,
            'enable_metaphors': True,
            'max_prompt_length': 500,
            'depth_threshold': {
                'simple': 0,
                'philosophical': 1,
                'metaphysical': 2,
                'existential': 3
            }
        }
    
    def process_script(self, script_path: Path) -> List[EnrichedScene]:
        """Process an entire script file and return enriched scenes."""
        self.logger.info(f"Processing script: {script_path}")
        
        # Parse script
        entries = self.parser.parse_file(script_path)
        self.logger.info(f"Parsed {len(entries)} entries from script")
        
        # Process each entry
        enriched_scenes = []
        for i, entry in enumerate(entries):
            try:
                enriched_scene = self.process_entry(entry, i, entries)
                enriched_scenes.append(enriched_scene)
                self.enriched_scenes.append(enriched_scene)
            except Exception as e:
                self.logger.error(f"Error processing entry {entry.id}: {str(e)}")
                continue
        
        return enriched_scenes
    
    def process_entry(
        self, 
        entry: ScriptEntry, 
        index: int, 
        all_entries: List[ScriptEntry]
    ) -> EnrichedScene:
        """Process a single script entry into an enriched scene."""
        self.logger.debug(f"Processing entry {entry.id}: {entry.speaker}")
        
        # Update character state
        self.state_tracker.update_from_entry(entry)
        
        # Analyze context
        context = self.context_analyzer.analyze_context(
            entry, 
            index, 
            all_entries,
            self.state_tracker.get_current_states()
        )
        
        # Extract philosophical layer
        philosophy = self.philosophical_interpreter.interpret(
            entry.dialogue,
            context,
            entry.metadata
        )
        
        # Map emotions to visuals
        character_state = self.state_tracker.get_state(entry.speaker.lower())
        emotion = self.emotional_mapper.map_emotion_to_visuals(
            character_state['emotional'],
            character_state.get('intensity', 0.5)
        )
        
        # Translate metaphors
        metaphors = self.metaphor_translator.translate_to_visual(
            philosophy['primary_concept'],
            context,
            entry.stage_directions
        )
        
        # Synthesize complete scene
        scene_data = self.scene_synthesizer.synthesize_scene({
            'entry': entry,
            'context': context,
            'philosophy': philosophy,
            'emotion': emotion,
            'metaphors': metaphors,
            'character_state': character_state,
            'continuity': self._get_continuity_data(index)
        })
        
        # Generate final prompt
        prompt = self.prompt_generator.generate_prompt(scene_data)
        
        # Create metadata
        metadata = self._create_metadata(
            entry, context, philosophy, emotion, scene_data
        )
        
        return EnrichedScene(
            entry_id=entry.id,
            prompt=prompt,
            metadata=metadata,
            philosophy=philosophy,
            emotion=emotion,
            visual_elements=scene_data.get('special_elements', [])
        )
    
    def _get_continuity_data(self, index: int) -> Dict[str, Any]:
        """Get continuity data from previous scenes."""
        if not self.config['enable_continuity'] or index == 0:
            return {}
            
        # Get data from previous scene
        if self.enriched_scenes:
            prev_scene = self.enriched_scenes[-1]
            return {
                'previous_emotion': prev_scene.emotion,
                'previous_setting': prev_scene.metadata.get('setting'),
                'visual_motifs': prev_scene.visual_elements
            }
        return {}
    
    def _create_metadata(
        self,
        entry: ScriptEntry,
        context: Dict[str, Any],
        philosophy: Dict[str, Any],
        emotion: Dict[str, Any],
        scene_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create comprehensive metadata for the scene."""
        return {
            'entry_id': entry.id,
            'speaker': entry.speaker,
            'panel_count': entry.panel_count,
            'philosophical_depth': philosophy.get('depth_level', 0),
            'primary_emotion': emotion.get('primary'),
            'visual_complexity': scene_data.get('complexity', 'medium'),
            'continuity_notes': scene_data.get('continuity', {}),
            'timestamp': context.get('narrative_time'),
            'setting': scene_data.get('setting', {}).get('name'),
            'special_effects': scene_data.get('special_elements', [])
        }
    
    def export_prompts(self, output_dir: Path):
        """Export all generated prompts to files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export individual prompts
        for scene in self.enriched_scenes:
            prompt_file = output_dir / f"scene_{scene.entry_id}.txt"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(scene.prompt)
            
            # Export metadata
            metadata_file = output_dir / f"scene_{scene.entry_id}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(scene.metadata, f, indent=2)
        
        # Export combined data
        all_scenes = []
        for scene in self.enriched_scenes:
            all_scenes.append({
                'id': scene.entry_id,
                'prompt': scene.prompt,
                'metadata': scene.metadata
            })
        
        combined_file = output_dir / "all_scenes.json"
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(all_scenes, f, indent=2)
        
        self.logger.info(f"Exported {len(self.enriched_scenes)} scenes to {output_dir}")