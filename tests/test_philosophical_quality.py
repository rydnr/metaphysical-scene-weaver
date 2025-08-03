"""Test examples for philosophical quality validation."""

# Example test case for Quinn's quality validator

test_philosophical_entry = {
    "entry_id": "0008",
    "dialogue": "I'm saying that true freedom begins with recognizing our constraints. You cannot escape a cage you don't know exists.",
    "philosophical_analysis": {
        "primary_concept": "freedom",
        "secondary_concepts": ["consciousness", "constraints"],
        "depth_level": 2,
        "school": "existentialism",
        "concept_consistency": True
    },
    "narrator_voice": {
        "type": "sage",
        "philosophical_weight": "heavy",
        "tone": "contemplative"
    },
    "visual_symbols": ["transparent_cage", "keys_inside_locks"],
    "expected_quality": {
        "philosophical_accuracy": 0.95,
        "depth_appropriate": True,
        "concept_evolution": "freedom concept deepens from simple choice to paradoxical constraint awareness",
        "voice_consistency": True
    }
}

test_edge_cases = [
    {
        "case": "concept_drift",
        "description": "When 'freedom' suddenly means something different",
        "should_flag": True
    },
    {
        "case": "depth_mismatch", 
        "description": "Surface dialogue tagged as depth level 4",
        "should_flag": True
    },
    {
        "case": "voice_inconsistency",
        "description": "Sage voice suddenly becomes provocateur mid-concept",
        "should_flag": True
    }
]

# Validation thresholds
QUALITY_THRESHOLDS = {
    "philosophical_accuracy": 0.8,
    "concept_consistency": 0.9,
    "depth_alignment": 0.85,
    "voice_coherence": 0.9
}