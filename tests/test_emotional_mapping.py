"""Test suite for emotional mapping and visual rules."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processors.emotional_mapper import EmotionalMapper, EmotionCategory
from src.utils.visual_rules import VisualRules
from src.core.character_state_tracker import CharacterStateTracker
from src.core.script_engine import ScriptEntry
import json
from datetime import datetime


def test_basic_emotion_detection():
    """Test basic emotion detection from dialogue."""
    print("\n=== Testing Basic Emotion Detection ===")
    mapper = EmotionalMapper()
    
    test_cases = [
        ("I'm so happy to see you!", ["smiling broadly"], "joy"),
        ("This fills me with existential dread", ["stares into void"], "existential_dread"),
        ("I feel both happy and sad", ["wistful smile"], "bittersweet"),
        ("The sunset fills me with such wonder", ["gazes in awe"], "wonder"),
        ("I long for the days of my youth", ["sighs deeply"], "nostalgia"),
    ]
    
    for dialogue, directions, expected in test_cases:
        state = mapper.analyze_emotional_content(
            dialogue, 
            directions, 
            {'time_context': 'day'}
        )
        print(f"\nDialogue: '{dialogue}'")
        print(f"Expected: {expected}, Got: {state.primary.value}")
        print(f"Intensity: {state.intensity:.2f}")
        print(f"Valence: {state.valence:.2f}")
        print(f"Visual palette: {state.visual_palette[:2]}")


def test_emotion_blending():
    """Test blending of emotions for complex states."""
    print("\n\n=== Testing Emotion Blending ===")
    mapper = EmotionalMapper()
    
    blend_tests = [
        ("joy", "sadness", 0.7, "bittersweet moment"),
        ("love", "fear", 0.6, "anxious attachment"),
        ("anger", "determination", 0.5, "righteous fury"),
        ("melancholy", "serenity", 0.4, "peaceful sadness"),
    ]
    
    for primary, secondary, ratio, description in blend_tests:
        blended = mapper.blend_emotions(primary, secondary, ratio)
        print(f"\n{description}: {primary} + {secondary} ({ratio:.1f})")
        print(f"Colors: {blended['color_palette']['primary_colors'][:2]}")
        print(f"Lighting: {blended['lighting']['contrast_ratio']:.1f} contrast")
        print(f"Body language: {blended['body_language']['movement_quality']}")


def test_cultural_variations():
    """Test cultural variations in emotional expression."""
    print("\n\n=== Testing Cultural Variations ===")
    mapper = EmotionalMapper()
    
    cultures = ['western', 'eastern', 'latin']
    emotion = 'joy'
    
    for culture in cultures:
        mapper.set_cultural_context(culture)
        visuals = mapper.map_emotion_to_visuals(emotion, 0.7)
        
        print(f"\n{culture.capitalize()} expression of {emotion}:")
        print(f"Emotion intensity modifier: {visuals['cultural_modifiers']['emotion_intensity']}")
        print(f"Eye contact comfort: {visuals['cultural_modifiers']['eye_contact']}")
        print(f"Personal space: {visuals['cultural_modifiers']['personal_space']}")
        print(f"Body language energy: {visuals['body_language']['energy_level']:.2f}")


def test_emotion_transitions():
    """Test smooth emotional transitions."""
    print("\n\n=== Testing Emotion Transitions ===")
    mapper = EmotionalMapper()
    
    transitions = [
        ("serenity", "wonder", "discovering something beautiful"),
        ("anger", "sadness", "rage turning to grief"),
        ("fear", "determination", "overcoming terror"),
        ("melancholy", "transcendent_joy", "breakthrough moment"),
    ]
    
    for from_em, to_em, description in transitions:
        print(f"\n{description}: {from_em} → {to_em}")
        for progress in [0.0, 0.3, 0.7, 1.0]:
            transition = mapper.get_emotion_transition(from_em, to_em, progress)
            print(f"  {progress:.0%}: {transition['body_language_shift']['movement_evolution']}")


def test_nuanced_emotion_visuals():
    """Test visual mapping for nuanced emotions."""
    print("\n\n=== Testing Nuanced Emotion Visuals ===")
    rules = VisualRules()
    
    nuanced_emotions = [
        'melancholy',
        'existential_dread', 
        'transcendent_joy',
        'bittersweet',
        'ennui',
        'wonder',
        'serenity',
        'sublime'
    ]
    
    for emotion in nuanced_emotions:
        visuals = rules.get_emotion_visuals(emotion, 0.6)
        print(f"\n{emotion.upper()}:")
        print(f"  Primary colors: {visuals['color_palette']['primary_colors'][:2]}")
        print(f"  Lighting: {visuals['lighting']['motivation']}")
        print(f"  Key atmosphere: {visuals['atmosphere']['weather']}")
        print(f"  Body language: {visuals['body_language']['posture']}")
        print(f"  Facial expression: {visuals['facial_expression']['overall_tension']}")
        print(f"  Cinematography: {visuals['cinematography']['shot_types'][0]}")


def test_character_arc_with_emotions():
    """Test character emotional arc tracking."""
    print("\n\n=== Testing Character Emotional Arc ===")
    tracker = CharacterStateTracker()
    
    # Simulate a character's emotional journey
    entries = [
        ScriptEntry("1", "SOPHIA", "Life seems so ordinary.", 
                   ["looks around mundanely"], ["philosophy", "beginning"]),
        ScriptEntry("2", "SOPHIA", "Wait... what if nothing is as it seems?", 
                   ["eyes widen with curiosity"], ["philosophy", "questioning"]),
        ScriptEntry("3", "SOPHIA", "This fills me with such existential dread.", 
                   ["stares into the void"], ["philosophy", "crisis"]),
        ScriptEntry("4", "SOPHIA", "But perhaps meaninglessness itself has meaning...", 
                   ["contemplative pause"], ["philosophy", "breakthrough"]),
        ScriptEntry("5", "SOPHIA", "I feel a strange transcendent joy in this understanding.", 
                   ["serene smile"], ["philosophy", "enlightenment"]),
    ]
    
    for entry in entries:
        tracker.update_from_entry(entry)
    
    # Get arc summary
    arc_summary = tracker.generate_arc_summary('sophia')
    print(f"\nCharacter Arc Summary for {arc_summary['character']}:")
    print(f"Total moments: {arc_summary['total_moments']}")
    print(f"Emotional journey: {json.dumps(arc_summary['emotional_journey'], indent=2)}")
    print(f"Philosophical journey: {arc_summary['philosophical_journey']}")
    print(f"Awareness progression: {arc_summary['awareness_progression']}")
    print(f"Current position: {arc_summary['current_position']}")


def test_complex_emotional_scenarios():
    """Test complex emotional scenarios with multiple layers."""
    print("\n\n=== Testing Complex Emotional Scenarios ===")
    mapper = EmotionalMapper()
    
    scenarios = [
        {
            'dialogue': "I smile through my tears, remembering better days.",
            'directions': ["bittersweet expression", "touches old photograph"],
            'expected_primary': 'bittersweet',
            'expected_secondary': 'nostalgia'
        },
        {
            'dialogue': "The void calls to me, yet I find it strangely beautiful.",
            'directions': ["gazes into darkness", "slight smile"],
            'expected_primary': 'existential_dread',
            'expected_secondary': 'sublime'
        },
        {
            'dialogue': "My heart races with both terror and fascination!",
            'directions': ["wide eyes", "leaning forward despite fear"],
            'expected_primary': 'fear',
            'expected_secondary': 'wonder'
        }
    ]
    
    for scenario in scenarios:
        state = mapper.analyze_emotional_content(
            scenario['dialogue'],
            scenario['directions'],
            {'time_context': 'twilight'}
        )
        
        print(f"\nScenario: '{scenario['dialogue']}'")
        print(f"Primary emotion: {state.primary.value} (intensity: {state.intensity:.2f})")
        if state.secondary:
            print(f"Secondary emotion: {state.secondary.value}")
        print(f"Visual elements:")
        print(f"  - Lighting: {state.lighting_mood}")
        print(f"  - Colors: {', '.join(state.visual_palette[:3])}")
        print(f"  - Body language: {', '.join(state.body_language[:2])}")
        print(f"  - Expression: {state.facial_expression}")


def test_emotion_intensity_variations():
    """Test how intensity affects visual mapping."""
    print("\n\n=== Testing Emotion Intensity Variations ===")
    mapper = EmotionalMapper()
    
    emotion = 'anger'
    intensities = [0.2, 0.5, 0.8, 1.0]
    
    print(f"Emotion: {emotion}")
    for intensity in intensities:
        visuals = mapper.map_emotion_to_visuals(emotion, intensity)
        print(f"\nIntensity {intensity:.1f}:")
        print(f"  Saturation: {visuals['color_palette']['saturation']:.2f}")
        print(f"  Contrast ratio: {visuals['lighting']['contrast_ratio']:.1f}")
        print(f"  Energy level: {visuals['body_language']['energy_level']:.2f}")
        print(f"  Shadow type: {visuals['lighting']['shadows'].split()[0]}")


if __name__ == "__main__":
    print("EMOTIONAL MAPPING TEST SUITE")
    print("=" * 50)
    
    test_basic_emotion_detection()
    test_emotion_blending()
    test_cultural_variations()
    test_emotion_transitions()
    test_nuanced_emotion_visuals()
    test_character_arc_with_emotions()
    test_complex_emotional_scenarios()
    test_emotion_intensity_variations()
    
    print("\n\nAll tests completed!")
    print("=" * 50)