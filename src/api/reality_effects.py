"""
Reality Dissolution Effects API
Special endpoints for scenes 010-012 climax sequence
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import asyncio
from datetime import datetime

router = APIRouter(prefix="/reality", tags=["reality_effects"])

class RealityEffect(BaseModel):
    """Visual effect for reality dissolution"""
    effect_type: str = Field(..., description="fracture|dissolve|loop|transcend")
    intensity: float = Field(0.5, ge=0.0, le=1.0)
    duration: Optional[float] = Field(None, description="Effect duration in seconds")
    parameters: Dict[str, Any] = Field(default_factory=dict)

class DissolutionRequest(BaseModel):
    """Request for reality dissolution sequence"""
    scene_id: str
    base_prompt: str
    dissolution_level: float = Field(0.5, ge=0.0, le=1.0)
    effects: List[RealityEffect] = Field(default_factory=list)
    philosophical_depth: int = Field(4, ge=1, le=4)
    multi_panel: bool = False

class DissolutionResponse(BaseModel):
    """Enhanced prompt with reality effects"""
    scene_id: str
    enhanced_prompts: List[Dict[str, Any]]
    effect_metadata: Dict[str, Any]
    token_count: int
    dissolution_score: float

class RealityEffectEngine:
    """Engine for applying reality dissolution effects"""
    
    EFFECT_TEMPLATES = {
        "fracture": {
            "visual": "reality splitting into {intensity} fractal shards",
            "style": "cubist fragmentation, kaleidoscope perspective",
            "particles": "glass_shatter"
        },
        "dissolve": {
            "visual": "boundaries melting like {intensity} liquid mirrors",
            "style": "Salvador Dali surrealism, fluid reality",
            "particles": "reality_melt"
        },
        "loop": {
            "visual": "infinite recursive {intensity} temporal echoes",
            "style": "M.C. Escher impossible geometry, fractal recursion",
            "particles": "time_spiral"
        },
        "transcend": {
            "visual": "consciousness expanding beyond {intensity} dimensional limits",
            "style": "abstract expressionism, pure light and form",
            "particles": "enlightenment_burst"
        }
    }
    
    def apply_effect(self, prompt: str, effect: RealityEffect) -> str:
        """Apply reality effect to prompt"""
        template = self.EFFECT_TEMPLATES.get(effect.effect_type, {})
        if not template:
            return prompt
            
        # Build effect description
        intensity_desc = ["subtle", "moderate", "intense", "overwhelming"][
            int(effect.intensity * 3)
        ]
        
        visual = template["visual"].format(intensity=intensity_desc)
        style = template["style"]
        
        # Enhance prompt with effect
        enhanced = f"{prompt}, {visual}, {style}"
        
        # Add custom parameters
        if effect.parameters:
            params = ", ".join(f"{k}: {v}" for k, v in effect.parameters.items())
            enhanced += f", {params}"
            
        return enhanced
    
    def calculate_dissolution(self, effects: List[RealityEffect]) -> float:
        """Calculate overall dissolution score"""
        if not effects:
            return 0.0
            
        scores = []
        weights = {
            "fracture": 0.7,
            "dissolve": 0.8,
            "loop": 0.9,
            "transcend": 1.0
        }
        
        for effect in effects:
            base_score = weights.get(effect.effect_type, 0.5)
            scores.append(base_score * effect.intensity)
            
        return min(sum(scores) / len(scores), 1.0)

engine = RealityEffectEngine()

@router.post("/dissolve", response_model=DissolutionResponse)
async def apply_dissolution(request: DissolutionRequest):
    """Apply reality dissolution effects to scene"""
    
    enhanced_prompts = []
    base_prompt = request.base_prompt
    
    if request.multi_panel:
        # Create progression across panels
        panel_count = 3 if request.scene_id == "012" else 2
        
        for i in range(panel_count):
            # Progressive intensity
            panel_intensity = (i + 1) / panel_count
            
            # Apply effects with increasing intensity
            enhanced = base_prompt
            for effect in request.effects:
                scaled_effect = effect.copy()
                scaled_effect.intensity *= panel_intensity
                enhanced = engine.apply_effect(enhanced, scaled_effect)
            
            enhanced_prompts.append({
                "panel": i + 1,
                "prompt": enhanced,
                "intensity": panel_intensity,
                "tokens": len(enhanced.split())  # Rough estimate
            })
    else:
        # Single panel with full effects
        enhanced = base_prompt
        for effect in request.effects:
            enhanced = engine.apply_effect(enhanced, effect)
            
        enhanced_prompts.append({
            "panel": 1,
            "prompt": enhanced,
            "intensity": request.dissolution_level,
            "tokens": len(enhanced.split())
        })
    
    # Calculate metrics
    dissolution_score = engine.calculate_dissolution(request.effects)
    total_tokens = sum(p["tokens"] for p in enhanced_prompts)
    
    return DissolutionResponse(
        scene_id=request.scene_id,
        enhanced_prompts=enhanced_prompts,
        effect_metadata={
            "effects_applied": len(request.effects),
            "philosophical_depth": request.philosophical_depth,
            "multi_panel": request.multi_panel,
            "timestamp": datetime.now().isoformat()
        },
        token_count=total_tokens,
        dissolution_score=dissolution_score
    )

@router.get("/effect-library")
async def get_effect_library():
    """Get available reality effects and their descriptions"""
    return {
        "effects": engine.EFFECT_TEMPLATES,
        "intensity_levels": {
            "0.0-0.25": "subtle",
            "0.25-0.50": "moderate", 
            "0.50-0.75": "intense",
            "0.75-1.0": "overwhelming"
        },
        "recommended_sequences": {
            "010": ["fracture", "dissolve"],
            "011": ["loop", "fracture"],
            "012": ["transcend", "dissolve", "loop"]
        }
    }

@router.post("/climax-sequence")
async def generate_climax_sequence(scenes: List[str] = ["010", "011", "012"]):
    """Generate complete reality dissolution sequence"""
    
    sequence_prompts = {}
    
    # Scene-specific configurations
    configs = {
        "010": {
            "effects": [
                RealityEffect(effect_type="fracture", intensity=0.6),
                RealityEffect(effect_type="dissolve", intensity=0.4)
            ],
            "dissolution": 0.5,
            "multi_panel": True
        },
        "011": {
            "effects": [
                RealityEffect(effect_type="loop", intensity=0.8),
                RealityEffect(effect_type="fracture", intensity=0.7)
            ],
            "dissolution": 0.8,
            "multi_panel": False
        },
        "012": {
            "effects": [
                RealityEffect(effect_type="transcend", intensity=0.9),
                RealityEffect(effect_type="dissolve", intensity=0.8),
                RealityEffect(effect_type="loop", intensity=0.6)
            ],
            "dissolution": 1.0,
            "multi_panel": True
        }
    }
    
    for scene_id in scenes:
        if scene_id not in configs:
            continue
            
        config = configs[scene_id]
        
        # Generate base prompt (would come from team)
        base = f"Scene {scene_id} philosophical climax"
        
        request = DissolutionRequest(
            scene_id=scene_id,
            base_prompt=base,
            dissolution_level=config["dissolution"],
            effects=config["effects"],
            philosophical_depth=4,
            multi_panel=config["multi_panel"]
        )
        
        response = await apply_dissolution(request)
        sequence_prompts[scene_id] = response.dict()
    
    return {
        "sequence": "reality_dissolution",
        "scenes": sequence_prompts,
        "total_dissolution": sum(
            s["dissolution_score"] for s in sequence_prompts.values()
        ) / len(sequence_prompts),
        "ready_for_generation": True
    }