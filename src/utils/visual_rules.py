"""Comprehensive visual mapping rules for emotional and philosophical states."""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import colorsys


class ColorTheory(Enum):
    """Color theory principles for emotional mapping."""
    WARM = "warm"  # Reds, oranges, yellows
    COOL = "cool"  # Blues, greens, purples
    NEUTRAL = "neutral"  # Grays, browns, beiges
    CONTRASTING = "contrasting"  # Complementary colors
    ANALOGOUS = "analogous"  # Adjacent on color wheel
    MONOCHROMATIC = "monochromatic"  # Single hue variations


class CinematographyStyle(Enum):
    """Cinematography styles for scene composition."""
    INTIMATE = "intimate"  # Close-ups, shallow depth
    EPIC = "epic"  # Wide shots, deep focus
    DOCUMENTARY = "documentary"  # Natural, observational
    EXPRESSIONIST = "expressionist"  # Dramatic angles, shadows
    IMPRESSIONIST = "impressionist"  # Soft focus, light play
    MINIMALIST = "minimalist"  # Clean, sparse composition
    BAROQUE = "baroque"  # Ornate, complex staging


@dataclass
class ColorPalette:
    """Defines a color palette with psychological associations."""
    primary: List[str]
    secondary: List[str]
    accent: List[str]
    theory: ColorTheory
    temperature: float  # 0.0 (cool) to 1.0 (warm)
    saturation: float  # 0.0 (desaturated) to 1.0 (vivid)
    brightness: float  # 0.0 (dark) to 1.0 (light)


@dataclass
class LightingScheme:
    """Defines lighting setup for emotional atmosphere."""
    key_light: str  # Main light source
    fill_light: str  # Secondary light to reduce shadows
    rim_light: str  # Back light for separation
    practical_lights: List[str]  # In-scene light sources
    shadows: str  # Shadow characteristics
    contrast_ratio: float  # Key to fill ratio
    color_temperature: int  # In Kelvin
    motivation: str  # Natural, artificial, mixed


@dataclass
class BodyLanguageSet:
    """Comprehensive body language descriptions."""
    posture: str
    gesture: List[str]
    movement_quality: str  # Fluid, sharp, erratic, etc.
    spatial_relationship: str  # How character uses space
    tension_points: List[str]  # Where tension is held
    energy_level: float  # 0.0 (still) to 1.0 (dynamic)


@dataclass
class FacialExpression:
    """Detailed facial expression mapping."""
    eyes: str
    eyebrows: str
    mouth: str
    jaw: str
    overall_tension: str
    micro_expressions: List[str]


@dataclass
class AtmosphericEffect:
    """Environmental and atmospheric elements."""
    weather: Optional[str]
    particles: List[str]  # Dust, pollen, light rays
    fog_density: float  # 0.0 to 1.0
    wind_strength: float  # 0.0 to 1.0
    temperature_visual: str  # Heat shimmer, breath visible
    time_distortion: Optional[str]  # Slow motion, time lapse


@dataclass
class SymbolicElement:
    """Symbolic visual elements for deeper meaning."""
    objects: List[str]
    natural_elements: List[str]
    geometric_shapes: List[str]
    recurring_motifs: List[str]
    cultural_symbols: Dict[str, List[str]]  # Culture-specific


class VisualRules:
    """Comprehensive visual rules for emotion and philosophy mapping."""
    
    def __init__(self):
        self._initialize_emotion_palettes()
        self._initialize_lighting_schemes()
        self._initialize_body_language()
        self._initialize_facial_expressions()
        self._initialize_atmospheric_effects()
        self._initialize_symbolic_elements()
        self._initialize_cultural_variations()
        self._initialize_cinematography_styles()
        
    def _initialize_emotion_palettes(self):
        """Initialize comprehensive color palettes for emotions."""
        self.emotion_palettes = {
            # Basic emotions
            'joy': ColorPalette(
                primary=['#FFD700', '#FFA500', '#FF69B4'],  # Gold, orange, pink
                secondary=['#87CEEB', '#98FB98', '#F0E68C'],  # Sky blue, pale green, khaki
                accent=['#FF1493', '#00CED1', '#32CD32'],  # Deep pink, turquoise, lime
                theory=ColorTheory.WARM,
                temperature=0.8,
                saturation=0.9,
                brightness=0.8
            ),
            'sadness': ColorPalette(
                primary=['#4682B4', '#483D8B', '#6A5ACD'],  # Steel blue, dark slate, violet
                secondary=['#778899', '#708090', '#B0C4DE'],  # Light slate, slate gray, steel
                accent=['#191970', '#000080', '#4B0082'],  # Midnight, navy, indigo
                theory=ColorTheory.COOL,
                temperature=0.2,
                saturation=0.3,
                brightness=0.4
            ),
            'anger': ColorPalette(
                primary=['#DC143C', '#B22222', '#8B0000'],  # Crimson, firebrick, dark red
                secondary=['#FF4500', '#FF6347', '#CD5C5C'],  # Orange red, tomato, indian red
                accent=['#800000', '#A52A2A', '#D2691E'],  # Maroon, brown, chocolate
                theory=ColorTheory.WARM,
                temperature=0.9,
                saturation=1.0,
                brightness=0.6
            ),
            'fear': ColorPalette(
                primary=['#2F4F4F', '#008B8B', '#5F9EA0'],  # Dark slate, cyan, cadet
                secondary=['#AFEEEE', '#E0FFFF', '#B0E0E6'],  # Pale turquoise, cyan, powder
                accent=['#00FA9A', '#3CB371', '#228B22'],  # Spring green, sea green, forest
                theory=ColorTheory.COOL,
                temperature=0.1,
                saturation=0.4,
                brightness=0.5
            ),
            
            # Nuanced emotions
            'melancholy': ColorPalette(
                primary=['#8B7D6B', '#8B7355', '#8B6969'],  # Bisque, tan, rosy brown
                secondary=['#D8BFD8', '#DDA0DD', '#DA70D6'],  # Thistle, plum, orchid
                accent=['#9370DB', '#8A2BE2', '#9400D3'],  # Purple, violet, violet
                theory=ColorTheory.ANALOGOUS,
                temperature=0.4,
                saturation=0.4,
                brightness=0.5
            ),
            'existential_dread': ColorPalette(
                primary=['#2C2C2C', '#1C1C1C', '#0C0C0C'],  # Dark grays to black
                secondary=['#4A0E4E', '#3B0F4F', '#2C1050'],  # Deep purples
                accent=['#8B0000', '#4B0000', '#2B0000'],  # Blood reds
                theory=ColorTheory.MONOCHROMATIC,
                temperature=0.1,
                saturation=0.2,
                brightness=0.2
            ),
            'transcendent_joy': ColorPalette(
                primary=['#FFFAF0', '#FFF8DC', '#FFEFD5'],  # Floral white, cornsilk, blanched
                secondary=['#FFE4B5', '#FFDAB9', '#FFE4E1'],  # Moccasin, peach, misty rose
                accent=['#FF69B4', '#FFB6C1', '#FFC0CB'],  # Hot pink, light pink, pink
                theory=ColorTheory.ANALOGOUS,
                temperature=0.7,
                saturation=0.6,
                brightness=0.95
            ),
            'bittersweet': ColorPalette(
                primary=['#D2691E', '#CD853F', '#DEB887'],  # Chocolate, peru, burlywood
                secondary=['#BC8F8F', '#F4A460', '#D2B48C'],  # Rosy brown, sandy, tan
                accent=['#8B4513', '#A0522D', '#6B4423'],  # Saddle, sienna, brown
                theory=ColorTheory.CONTRASTING,
                temperature=0.6,
                saturation=0.5,
                brightness=0.6
            ),
            'ennui': ColorPalette(
                primary=['#BEBEBE', '#C0C0C0', '#D3D3D3'],  # Gray variations
                secondary=['#DCDCDC', '#E5E5E5', '#F5F5F5'],  # Light grays
                accent=['#A9A9A9', '#808080', '#696969'],  # Dark grays
                theory=ColorTheory.NEUTRAL,
                temperature=0.5,
                saturation=0.0,
                brightness=0.7
            ),
            'wonder': ColorPalette(
                primary=['#00BFFF', '#1E90FF', '#4169E1'],  # Sky blues
                secondary=['#9370DB', '#BA55D3', '#DA70D6'],  # Purples
                accent=['#FFD700', '#FFA500', '#FF8C00'],  # Golds
                theory=ColorTheory.CONTRASTING,
                temperature=0.5,
                saturation=0.8,
                brightness=0.7
            ),
            'serenity': ColorPalette(
                primary=['#E6E6FA', '#D8BFD8', '#DDA0DD'],  # Lavender variations
                secondary=['#B0E0E6', '#ADD8E6', '#87CEEB'],  # Powder blues
                accent=['#F0FFF0', '#F5FFFA', '#F0FFFF'],  # Whites
                theory=ColorTheory.ANALOGOUS,
                temperature=0.4,
                saturation=0.3,
                brightness=0.85
            ),
            
            # Additional emotions for compatibility
            'contemplation': ColorPalette(
                primary=['#5F9EA0', '#4682B4', '#6495ED'],  # Cadet blue, steel, cornflower
                secondary=['#B0C4DE', '#ADD8E6', '#87CEEB'],  # Light steel, light blue, sky
                accent=['#708090', '#778899', '#696969'],  # Slate grays
                theory=ColorTheory.ANALOGOUS,
                temperature=0.3,
                saturation=0.4,
                brightness=0.6
            ),
            'surprise': ColorPalette(
                primary=['#FFD700', '#FF69B4', '#00CED1'],  # Gold, hot pink, turquoise
                secondary=['#FFFFE0', '#E0FFFF', '#F0E68C'],  # Light yellow, cyan, khaki
                accent=['#FF1493', '#1E90FF', '#32CD32'],  # Deep pink, dodger blue, lime
                theory=ColorTheory.CONTRASTING,
                temperature=0.6,
                saturation=0.8,
                brightness=0.7
            ),
            'disgust': ColorPalette(
                primary=['#556B2F', '#6B8E23', '#808000'],  # Dark olive, olive drab, olive
                secondary=['#8FBC8F', '#90EE90', '#98FB98'],  # Dark sea green, light green
                accent=['#2F4F4F', '#696969', '#708090'],  # Dark slate, dim gray, slate
                theory=ColorTheory.ANALOGOUS,
                temperature=0.3,
                saturation=0.4,
                brightness=0.4
            ),
            'nostalgia': ColorPalette(
                primary=['#DEB887', '#D2691E', '#CD853F'],  # Burlywood, chocolate, peru
                secondary=['#F4A460', '#DAA520', '#B8860B'],  # Sandy, goldenrod, dark golden
                accent=['#8B7355', '#A0522D', '#8B4513'],  # Tan, sienna, saddle brown
                theory=ColorTheory.WARM,
                temperature=0.6,
                saturation=0.5,
                brightness=0.6
            ),
            'yearning': ColorPalette(
                primary=['#4B0082', '#8A2BE2', '#9400D3'],  # Indigo, blue violet, violet
                secondary=['#9370DB', '#BA55D3', '#DA70D6'],  # Medium purple, orchid
                accent=['#DDA0DD', '#EE82EE', '#FF00FF'],  # Plum, violet, magenta
                theory=ColorTheory.ANALOGOUS,
                temperature=0.4,
                saturation=0.7,
                brightness=0.5
            ),
            'sublime': ColorPalette(
                primary=['#F0F8FF', '#E6E6FA', '#F5F5DC'],  # Alice blue, lavender, beige
                secondary=['#FFFAF0', '#FFF8DC', '#FAEBD7'],  # Floral white, cornsilk, blanched
                accent=['#FFD700', '#DAA520', '#F0E68C'],  # Gold, goldenrod, khaki
                theory=ColorTheory.ANALOGOUS,
                temperature=0.6,
                saturation=0.4,
                brightness=0.9
            )
        }
        
    def _initialize_lighting_schemes(self):
        """Initialize comprehensive lighting schemes."""
        self.lighting_schemes = {
            'joy': LightingScheme(
                key_light="Bright, warm key light at 45° angle",
                fill_light="Soft fill reducing shadows to 2:1 ratio",
                rim_light="Subtle golden rim light",
                practical_lights=["Candles", "Fairy lights", "Sunbeams"],
                shadows="Soft, warm-toned shadows",
                contrast_ratio=2.0,
                color_temperature=3200,  # Warm
                motivation="Natural sunlight or warm interior"
            ),
            'sadness': LightingScheme(
                key_light="Dim, cool key light from above",
                fill_light="Minimal fill, 4:1 ratio",
                rim_light="Cold blue rim light",
                practical_lights=["Rain-filtered window", "Distant streetlight"],
                shadows="Long, cool shadows",
                contrast_ratio=4.0,
                color_temperature=6500,  # Cool
                motivation="Overcast day or moonlight"
            ),
            'anger': LightingScheme(
                key_light="Harsh, direct key light",
                fill_light="Minimal fill, 8:1 ratio",
                rim_light="Red-tinted rim light",
                practical_lights=["Fire", "Neon signs", "Harsh fluorescents"],
                shadows="Sharp, high-contrast shadows",
                contrast_ratio=8.0,
                color_temperature=2000,  # Very warm
                motivation="Fire or intense artificial light"
            ),
            'fear': LightingScheme(
                key_light="Unstable, moving key light",
                fill_light="Inconsistent fill from below",
                rim_light="Eerie green or blue rim",
                practical_lights=["Flickering lights", "Lightning", "Phone screens"],
                shadows="Distorted, moving shadows",
                contrast_ratio=10.0,
                color_temperature=5000,  # Mixed
                motivation="Unknown or supernatural sources"
            ),
            'contemplation': LightingScheme(
                key_light="Soft, diffused key light",
                fill_light="Balanced fill, 1.5:1 ratio",
                rim_light="Subtle separation light",
                practical_lights=["Desk lamp", "Window light", "Candle"],
                shadows="Soft, thoughtful shadows",
                contrast_ratio=1.5,
                color_temperature=4000,  # Neutral
                motivation="Study or meditation space"
            ),
            'melancholy': LightingScheme(
                key_light="Filtered, autumn-like key light",
                fill_light="Gentle fill, 3:1 ratio",
                rim_light="Dusty, golden rim light",
                practical_lights=["Sunset through curtains", "Old lamp"],
                shadows="Nostalgic, long shadows",
                contrast_ratio=3.0,
                color_temperature=3500,  # Warm-neutral
                motivation="Late afternoon or memory"
            ),
            'existential_dread': LightingScheme(
                key_light="Void-like absence of clear key",
                fill_light="Minimal, creating isolation",
                rim_light="Faint, cold rim suggesting void",
                practical_lights=["Distant stars", "Exit signs", "Phone glow"],
                shadows="Overwhelming darkness",
                contrast_ratio=12.0,
                color_temperature=7000,  # Very cool
                motivation="Cosmic void or isolation"
            ),
            'transcendent_joy': LightingScheme(
                key_light="Radiant, all-encompassing light",
                fill_light="Ethereal fill eliminating shadows",
                rim_light="Halo-like rim light",
                practical_lights=["Divine light", "Rainbow prisms", "Crystal reflections"],
                shadows="Almost no shadows",
                contrast_ratio=1.2,
                color_temperature=5500,  # Pure white
                motivation="Spiritual or transcendent source"
            ),
            'wonder': LightingScheme(
                key_light="Dynamic, color-shifting key",
                fill_light="Prismatic fill light",
                rim_light="Aurora-like rim effects",
                practical_lights=["Northern lights", "Bioluminescence", "Magic"],
                shadows="Colorful, soft shadows",
                contrast_ratio=2.5,
                color_temperature=4500,  # Variable
                motivation="Magical or natural phenomena"
            )
        }
        
    def _initialize_body_language(self):
        """Initialize body language sets."""
        self.body_language_sets = {
            'joy': BodyLanguageSet(
                posture="Open, upright, expansive",
                gesture=["Arms spread wide", "Hands clapping", "Jumping"],
                movement_quality="Light, bouncy, fluid",
                spatial_relationship="Takes up space confidently",
                tension_points=[],
                energy_level=0.8
            ),
            'sadness': BodyLanguageSet(
                posture="Closed, hunched, protective",
                gesture=["Arms wrapped around self", "Head in hands", "Slow movements"],
                movement_quality="Heavy, dragging, minimal",
                spatial_relationship="Shrinks into small space",
                tension_points=["Shoulders", "Chest"],
                energy_level=0.2
            ),
            'anger': BodyLanguageSet(
                posture="Tense, forward-leaning, aggressive",
                gesture=["Clenched fists", "Pointing", "Sharp movements"],
                movement_quality="Sharp, explosive, direct",
                spatial_relationship="Invades space, confrontational",
                tension_points=["Jaw", "Fists", "Shoulders"],
                energy_level=0.9
            ),
            'fear': BodyLanguageSet(
                posture="Defensive, ready to flee, alert",
                gesture=["Hands up protectively", "Looking around", "Backing away"],
                movement_quality="Jerky, sudden, reactive",
                spatial_relationship="Creates distance, seeks exits",
                tension_points=["Entire body", "Eyes wide"],
                energy_level=0.7
            ),
            'contemplation': BodyLanguageSet(
                posture="Still, balanced, centered",
                gesture=["Hand to chin", "Fingers steepled", "Slow nodding"],
                movement_quality="Deliberate, measured, minimal",
                spatial_relationship="Comfortable in space",
                tension_points=["Forehead (concentration)"],
                energy_level=0.3
            ),
            'melancholy': BodyLanguageSet(
                posture="Gentle slump, wistful lean",
                gesture=["Touching old objects", "Gazing at distance", "Slow sighs"],
                movement_quality="Languid, nostalgic, drifting",
                spatial_relationship="Lost in internal space",
                tension_points=["Heart area", "Eyes"],
                energy_level=0.3
            ),
            'existential_dread': BodyLanguageSet(
                posture="Rigid or collapsed, disconnected",
                gesture=["Staring at hands", "Touching face repeatedly", "Frozen"],
                movement_quality="Mechanical or completely still",
                spatial_relationship="Feels untethered from space",
                tension_points=["Entire body", "Mind-body disconnect"],
                energy_level=0.1
            ),
            'transcendent_joy': BodyLanguageSet(
                posture="Floating, ethereal, lifted",
                gesture=["Arms raised to sky", "Spinning", "Touching everything gently"],
                movement_quality="Graceful, flowing, weightless",
                spatial_relationship="Connected to all space",
                tension_points=[],
                energy_level=0.6
            ),
            'wonder': BodyLanguageSet(
                posture="Alert, open, reaching",
                gesture=["Reaching toward", "Eyes tracking", "Mouth slightly open"],
                movement_quality="Curious, exploring, gentle",
                spatial_relationship="Drawn toward mystery",
                tension_points=["Eyes (wide focus)"],
                energy_level=0.5
            )
        }
        
    def _initialize_facial_expressions(self):
        """Initialize detailed facial expressions."""
        self.facial_expressions = {
            'joy': FacialExpression(
                eyes="Crinkled at corners, bright, engaged",
                eyebrows="Slightly raised, relaxed",
                mouth="Genuine smile, teeth showing",
                jaw="Relaxed, open",
                overall_tension="Relaxed with animation",
                micro_expressions=["Eye sparkle", "Dimples", "Laugh lines"]
            ),
            'sadness': FacialExpression(
                eyes="Downcast, possibly tearful, distant",
                eyebrows="Inner corners raised, drooping",
                mouth="Downturned, trembling",
                jaw="Slack or clenched with effort",
                overall_tension="Heavy, pulled downward",
                micro_expressions=["Lip quiver", "Tear tracks", "Red eyes"]
            ),
            'anger': FacialExpression(
                eyes="Narrowed, intense, focused",
                eyebrows="Drawn together, lowered",
                mouth="Tight, grimace or snarl",
                jaw="Clenched, muscle visible",
                overall_tension="High tension throughout",
                micro_expressions=["Nostril flare", "Vein visible", "Teeth grinding"]
            ),
            'fear': FacialExpression(
                eyes="Wide, darting, dilated pupils",
                eyebrows="Raised, pulled together",
                mouth="Open, gasping or tight",
                jaw="Dropped or clenched",
                overall_tension="Alert, ready to react",
                micro_expressions=["Rapid blinking", "Lip tremor", "Pale complexion"]
            ),
            'contemplation': FacialExpression(
                eyes="Focused inward or distant",
                eyebrows="Slightly furrowed in thought",
                mouth="Neutral or slightly pursed",
                jaw="Relaxed",
                overall_tension="Concentrated calm",
                micro_expressions=["Eye movement (processing)", "Slight head tilt"]
            ),
            'melancholy': FacialExpression(
                eyes="Soft, unfocused, wistful",
                eyebrows="Gentle furrow, slight droop",
                mouth="Slight downturn, soft",
                jaw="Relaxed with slight tension",
                overall_tension="Gentle sadness",
                micro_expressions=["Distant smile", "Slow blink", "Sigh"]
            ),
            'existential_dread': FacialExpression(
                eyes="Thousand-yard stare, hollow",
                eyebrows="Flat, expressionless",
                mouth="Slack or tight line",
                jaw="Tension without purpose",
                overall_tension="Disconnected, mask-like",
                micro_expressions=["Eye twitch", "Blank stare", "Mechanical movements"]
            ),
            'transcendent_joy': FacialExpression(
                eyes="Radiating warmth, almost glowing",
                eyebrows="Perfectly relaxed, lifted",
                mouth="Serene smile, peaceful",
                jaw="Completely relaxed",
                overall_tension="Total ease and flow",
                micro_expressions=["Inner light", "Tears of joy", "Beatific expression"]
            ),
            'wonder': FacialExpression(
                eyes="Wide with curiosity, bright",
                eyebrows="Raised in surprise/interest",
                mouth="Slightly open in awe",
                jaw="Dropped slightly",
                overall_tension="Alert relaxation",
                micro_expressions=["Pupil dilation", "Quick smile", "Head tilt"]
            )
        }
        
    def _initialize_atmospheric_effects(self):
        """Initialize atmospheric and environmental effects."""
        self.atmospheric_effects = {
            'joy': AtmosphericEffect(
                weather="Sunny with gentle breeze",
                particles=["Pollen", "Butterflies", "Light sparkles"],
                fog_density=0.0,
                wind_strength=0.3,
                temperature_visual="Warm air shimmer",
                time_distortion=None
            ),
            'sadness': AtmosphericEffect(
                weather="Light rain or overcast",
                particles=["Raindrops", "Falling leaves"],
                fog_density=0.4,
                wind_strength=0.1,
                temperature_visual="Cool mist",
                time_distortion="Slow motion moments"
            ),
            'anger': AtmosphericEffect(
                weather="Storm brewing or heat wave",
                particles=["Dust", "Sparks", "Debris"],
                fog_density=0.1,
                wind_strength=0.7,
                temperature_visual="Heat waves rising",
                time_distortion="Quick cuts, time jumps"
            ),
            'fear': AtmosphericEffect(
                weather="Fog or sudden weather changes",
                particles=["Shadows moving", "Things in peripheral"],
                fog_density=0.7,
                wind_strength=0.5,
                temperature_visual="Cold spots, breath visible",
                time_distortion="Time dilation, frozen moments"
            ),
            'contemplation': AtmosphericEffect(
                weather="Still, clear conditions",
                particles=["Dust motes in light", "Gentle snow"],
                fog_density=0.2,
                wind_strength=0.0,
                temperature_visual="Neutral, comfortable",
                time_distortion="Time suspension"
            ),
            'melancholy': AtmosphericEffect(
                weather="Autumn day, golden hour",
                particles=["Falling leaves", "Dust in sunbeams"],
                fog_density=0.3,
                wind_strength=0.2,
                temperature_visual="Cool but gentle",
                time_distortion="Memory flashes"
            ),
            'existential_dread': AtmosphericEffect(
                weather="Void-like, no weather",
                particles=["Ash", "Static", "Void particles"],
                fog_density=0.8,
                wind_strength=0.0,
                temperature_visual="Neither hot nor cold",
                time_distortion="Time meaningless"
            ),
            'transcendent_joy': AtmosphericEffect(
                weather="Perfect conditions, golden light",
                particles=["Light orbs", "Flower petals", "Prismatic effects"],
                fog_density=0.1,
                wind_strength=0.2,
                temperature_visual="Perfect temperature",
                time_distortion="Eternal moment"
            ),
            'wonder': AtmosphericEffect(
                weather="Aurora, unusual phenomena",
                particles=["Fireflies", "Star dust", "Magic sparkles"],
                fog_density=0.2,
                wind_strength=0.3,
                temperature_visual="Changing temperatures",
                time_distortion="Time expansion"
            )
        }
        
    def _initialize_symbolic_elements(self):
        """Initialize symbolic visual elements."""
        self.symbolic_elements = {
            'joy': SymbolicElement(
                objects=["Balloons", "Flowers blooming", "Musical instruments"],
                natural_elements=["Sun", "Rainbow", "Birds singing"],
                geometric_shapes=["Circles", "Spirals upward", "Stars"],
                recurring_motifs=["Light", "Growth", "Connection"],
                cultural_symbols={
                    'western': ["Smiley face", "Thumbs up", "Hearts"],
                    'eastern': ["Cherry blossoms", "Rising sun", "Cranes"]
                }
            ),
            'sadness': SymbolicElement(
                objects=["Wilted flowers", "Empty chairs", "Photographs"],
                natural_elements=["Rain", "Bare trees", "Setting sun"],
                geometric_shapes=["Downward triangles", "Broken circles"],
                recurring_motifs=["Water", "Emptiness", "Distance"],
                cultural_symbols={
                    'western': ["Tears", "Black clothing", "Handkerchief"],
                    'eastern': ["Falling petals", "Autumn leaves", "Moon"]
                }
            ),
            'anger': SymbolicElement(
                objects=["Broken objects", "Clenched tools", "Fire"],
                natural_elements=["Storm", "Volcano", "Thorns"],
                geometric_shapes=["Jagged lines", "Sharp triangles", "Zigzags"],
                recurring_motifs=["Heat", "Destruction", "Conflict"],
                cultural_symbols={
                    'western': ["Red face", "Steam", "Fist"],
                    'eastern': ["Dragon", "Thunder", "Oni mask"]
                }
            ),
            'fear': SymbolicElement(
                objects=["Shadows", "Doors ajar", "Broken mirrors"],
                natural_elements=["Dark forest", "Fog", "Unknown depths"],
                geometric_shapes=["Distorted shapes", "Maze patterns"],
                recurring_motifs=["Darkness", "Unknown", "Trapped"],
                cultural_symbols={
                    'western': ["Monsters", "Skulls", "Dark corridors"],
                    'eastern': ["Yokai", "Dark water", "Cursed objects"]
                }
            ),
            'contemplation': SymbolicElement(
                objects=["Books", "Hourglass", "Telescope"],
                natural_elements=["Still water", "Mountains", "Stars"],
                geometric_shapes=["Mandala", "Golden ratio", "Infinity"],
                recurring_motifs=["Reflection", "Time", "Knowledge"],
                cultural_symbols={
                    'western': ["Thinker pose", "Library", "Question mark"],
                    'eastern': ["Zen garden", "Tea ceremony", "Meditation pose"]
                }
            ),
            'melancholy': SymbolicElement(
                objects=["Old letters", "Faded photographs", "Empty swing"],
                natural_elements=["Autumn leaves", "Misty morning", "Twilight"],
                geometric_shapes=["Incomplete circles", "Fading lines"],
                recurring_motifs=["Memory", "Time passing", "What was"],
                cultural_symbols={
                    'western': ["Sepia tones", "Old music box", "Dusty attic"],
                    'eastern': ["Mono no aware", "Wabi-sabi", "Falling leaves"]
                }
            ),
            'existential_dread': SymbolicElement(
                objects=["Void", "Broken clocks", "Empty frames"],
                natural_elements=["Black hole", "Infinite space", "Abyss"],
                geometric_shapes=["Void shapes", "Impossible geometry", "Fractals"],
                recurring_motifs=["Meaninglessness", "Infinity", "Isolation"],
                cultural_symbols={
                    'western': ["Scream painting", "Void", "Sisyphus"],
                    'eastern': ["Emptiness", "Samsara wheel", "Void meditation"]
                }
            ),
            'transcendent_joy': SymbolicElement(
                objects=["Prisms", "Crystals", "Divine light"],
                natural_elements=["Aurora", "Summit view", "Ocean infinity"],
                geometric_shapes=["Sacred geometry", "Halos", "Ascending spirals"],
                recurring_motifs=["Unity", "Light", "Transcendence"],
                cultural_symbols={
                    'western': ["Angels", "Halos", "Divine light"],
                    'eastern': ["Enlightenment", "Lotus", "Third eye"]
                }
            ),
            'wonder': SymbolicElement(
                objects=["Telescope", "Map", "Compass"],
                natural_elements=["Galaxy", "Rainbow", "Aurora"],
                geometric_shapes=["Expanding circles", "Question marks", "Spirals"],
                recurring_motifs=["Discovery", "Mystery", "Possibility"],
                cultural_symbols={
                    'western': ["Wide eyes", "Open book", "Treasure map"],
                    'eastern': ["Dharma wheel", "Phoenix", "Journey symbols"]
                }
            )
        }
        
    def _initialize_cultural_variations(self):
        """Initialize cultural variations in emotional expression."""
        self.cultural_variations = {
            'western': {
                'emotion_intensity': 0.8,  # More externalized
                'personal_space': 1.0,  # Larger personal space
                'eye_contact': 0.8,  # Direct eye contact common
                'touch_comfort': 0.6,  # Moderate touch comfort
                'color_associations': {
                    'white': 'purity, weddings',
                    'black': 'death, formality',
                    'red': 'passion, anger'
                }
            },
            'eastern': {
                'emotion_intensity': 0.5,  # More internalized
                'personal_space': 0.7,  # Smaller personal space in crowds
                'eye_contact': 0.4,  # Less direct eye contact
                'touch_comfort': 0.3,  # Less touch in public
                'color_associations': {
                    'white': 'death, mourning',
                    'red': 'luck, celebration',
                    'gold': 'prosperity, divine'
                }
            },
            'latin': {
                'emotion_intensity': 0.9,  # Highly expressive
                'personal_space': 0.6,  # Close personal space
                'eye_contact': 0.9,  # Very direct
                'touch_comfort': 0.9,  # High touch culture
                'color_associations': {
                    'yellow': 'death, caution',
                    'red': 'passion, life',
                    'purple': 'mourning, penance'
                }
            },
            'middle_eastern': {
                'emotion_intensity': 0.7,  # Context-dependent
                'personal_space': 0.5,  # Very close for same gender
                'eye_contact': 0.6,  # Gender-dependent
                'touch_comfort': 0.7,  # Same-gender touch common
                'color_associations': {
                    'green': 'islam, paradise',
                    'blue': 'protection, spirituality',
                    'gold': 'divine, precious'
                }
            },
            'african': {
                'emotion_intensity': 0.8,  # Expressive
                'personal_space': 0.6,  # Community-oriented
                'eye_contact': 0.5,  # Respect-based variations
                'touch_comfort': 0.8,  # Touch as communication
                'color_associations': {
                    'white': 'spirituality, ancestors',
                    'red': 'life, vitality',
                    'black': 'maturity, masculinity'
                }
            }
        }
        
    def _initialize_cinematography_styles(self):
        """Initialize cinematography styles for different moods."""
        self.cinematography_styles = {
            'intimate': {
                'shot_types': ["Close-up", "Extreme close-up", "Medium shot"],
                'camera_movement': ["Slow push-in", "Handheld", "Subtle drift"],
                'depth_of_field': "Shallow",
                'composition': "Center-weighted, tight framing",
                'aspect_ratio': "1.85:1 or 2.39:1"
            },
            'epic': {
                'shot_types': ["Wide shot", "Extreme wide", "Aerial"],
                'camera_movement': ["Crane", "Drone", "Steadicam"],
                'depth_of_field': "Deep",
                'composition': "Rule of thirds, leading lines",
                'aspect_ratio': "2.39:1 or wider"
            },
            'documentary': {
                'shot_types': ["Medium shot", "Wide shot", "Observational"],
                'camera_movement': ["Handheld", "Static observation", "Following"],
                'depth_of_field': "Natural",
                'composition': "Found framing, real environments",
                'aspect_ratio': "16:9 or 1.85:1"
            },
            'expressionist': {
                'shot_types': ["Dutch angle", "Extreme angles", "Distorted"],
                'camera_movement': ["Dramatic tilts", "Rapid movements", "Unsettling"],
                'depth_of_field': "Selective focus",
                'composition': "Off-balance, geometric",
                'aspect_ratio': "Any, including unusual"
            },
            'impressionist': {
                'shot_types': ["Soft focus", "Through objects", "Fragmented"],
                'camera_movement': ["Floating", "Dreamlike", "Time-lapse"],
                'depth_of_field': "Variable, soft",
                'composition': "Painterly, light-focused",
                'aspect_ratio': "1.66:1 or 1.85:1"
            },
            'minimalist': {
                'shot_types': ["Static wide", "Symmetrical", "Clean singles"],
                'camera_movement': ["Minimal to none", "Precise when used"],
                'depth_of_field': "Consistent",
                'composition': "Geometric, negative space",
                'aspect_ratio': "2.39:1 or 1.85:1"
            },
            'baroque': {
                'shot_types': ["Complex staging", "Deep focus", "Layered"],
                'camera_movement': ["Elaborate tracking", "360 degree", "Choreographed"],
                'depth_of_field': "Deep, everything in focus",
                'composition': "Dense, ornate, multiple planes",
                'aspect_ratio': "2.39:1 for grandeur"
            }
        }
    
    def get_emotion_visuals(self, emotion: str, intensity: float = 0.5, 
                           cultural_context: str = 'western') -> Dict[str, Any]:
        """Get comprehensive visual mapping for an emotion."""
        # Normalize emotion string
        emotion = emotion.lower().replace(' ', '_')
        
        # Get base visual elements
        palette = self.emotion_palettes.get(emotion, self.emotion_palettes['contemplation'])
        lighting = self.lighting_schemes.get(emotion, self.lighting_schemes['contemplation'])
        body_language = self.body_language_sets.get(emotion, self.body_language_sets['contemplation'])
        facial = self.facial_expressions.get(emotion, self.facial_expressions['contemplation'])
        atmosphere = self.atmospheric_effects.get(emotion, self.atmospheric_effects['contemplation'])
        symbols = self.symbolic_elements.get(emotion, self.symbolic_elements['contemplation'])
        
        # Apply cultural variations
        cultural = self.cultural_variations.get(cultural_context, self.cultural_variations['western'])
        
        # Adjust for intensity
        adjusted_palette = self._adjust_palette_intensity(palette, intensity)
        adjusted_lighting = self._adjust_lighting_intensity(lighting, intensity)
        adjusted_body = self._adjust_body_language_intensity(body_language, intensity, cultural)
        
        # Select cinematography style
        cinema_style = self._select_cinematography_style(emotion, intensity)
        
        return {
            'emotion': emotion,
            'intensity': intensity,
            'cultural_context': cultural_context,
            'color_palette': adjusted_palette,
            'lighting': adjusted_lighting,
            'body_language': adjusted_body,
            'facial_expression': facial,
            'atmosphere': atmosphere,
            'symbols': symbols,
            'cinematography': self.cinematography_styles[cinema_style],
            'cultural_modifiers': cultural
        }
    
    def blend_emotions(self, primary: str, secondary: str, 
                      blend_ratio: float = 0.7) -> Dict[str, Any]:
        """Blend two emotions to create complex emotional states."""
        primary_visuals = self.get_emotion_visuals(primary)
        secondary_visuals = self.get_emotion_visuals(secondary)
        
        # Blend color palettes
        blended_palette = self._blend_palettes(
            primary_visuals['color_palette'],
            secondary_visuals['color_palette'],
            blend_ratio
        )
        
        # Blend lighting
        blended_lighting = self._blend_lighting(
            primary_visuals['lighting'],
            secondary_visuals['lighting'],
            blend_ratio
        )
        
        # Combine body language
        combined_body = self._combine_body_language(
            primary_visuals['body_language'],
            secondary_visuals['body_language'],
            blend_ratio
        )
        
        # Mix atmospheric effects
        mixed_atmosphere = self._mix_atmosphere(
            primary_visuals['atmosphere'],
            secondary_visuals['atmosphere'],
            blend_ratio
        )
        
        return {
            'primary_emotion': primary,
            'secondary_emotion': secondary,
            'blend_ratio': blend_ratio,
            'color_palette': blended_palette,
            'lighting': blended_lighting,
            'body_language': combined_body,
            'facial_expression': self._blend_facial_expressions(
                primary_visuals['facial_expression'],
                secondary_visuals['facial_expression'],
                blend_ratio
            ),
            'atmosphere': mixed_atmosphere,
            'symbols': self._merge_symbols(
                primary_visuals['symbols'],
                secondary_visuals['symbols']
            ),
            'cinematography': self._select_blended_cinematography(primary, secondary)
        }
    
    def get_transition_visuals(self, from_emotion: str, to_emotion: str, 
                             progress: float = 0.5) -> Dict[str, Any]:
        """Get visual elements for emotional transitions."""
        from_visuals = self.get_emotion_visuals(from_emotion)
        to_visuals = self.get_emotion_visuals(to_emotion)
        
        # Calculate transition elements
        transition_palette = self._calculate_transition_palette(
            from_visuals['color_palette'],
            to_visuals['color_palette'],
            progress
        )
        
        transition_lighting = self._calculate_transition_lighting(
            from_visuals['lighting'],
            to_visuals['lighting'],
            progress
        )
        
        transition_atmosphere = self._calculate_transition_atmosphere(
            from_visuals['atmosphere'],
            to_visuals['atmosphere'],
            progress
        )
        
        return {
            'from_emotion': from_emotion,
            'to_emotion': to_emotion,
            'progress': progress,
            'color_palette': transition_palette,
            'lighting': transition_lighting,
            'atmosphere': transition_atmosphere,
            'body_language_shift': self._get_body_language_shift(
                from_visuals['body_language'],
                to_visuals['body_language'],
                progress
            ),
            'cinematography_transition': self._get_cinematography_transition(
                from_emotion, to_emotion, progress
            )
        }
    
    def _adjust_palette_intensity(self, palette: ColorPalette, 
                                intensity: float) -> Dict[str, Any]:
        """Adjust color palette based on emotional intensity."""
        # Adjust saturation and brightness based on intensity
        adjusted_saturation = palette.saturation * (0.5 + intensity * 0.5)
        adjusted_brightness = palette.brightness * (0.6 + intensity * 0.4)
        
        return {
            'primary_colors': palette.primary,
            'secondary_colors': palette.secondary,
            'accent_colors': palette.accent,
            'saturation': adjusted_saturation,
            'brightness': adjusted_brightness,
            'temperature': palette.temperature,
            'theory': palette.theory.value
        }
    
    def _adjust_lighting_intensity(self, lighting: LightingScheme, 
                                 intensity: float) -> Dict[str, Any]:
        """Adjust lighting based on emotional intensity."""
        # Increase contrast ratio with intensity
        adjusted_contrast = lighting.contrast_ratio * (0.5 + intensity * 1.5)
        
        return {
            'key_light': lighting.key_light,
            'fill_light': lighting.fill_light,
            'rim_light': lighting.rim_light,
            'practical_lights': lighting.practical_lights,
            'shadows': f"{'Harsh' if intensity > 0.7 else 'Soft'} {lighting.shadows}",
            'contrast_ratio': adjusted_contrast,
            'color_temperature': lighting.color_temperature,
            'motivation': lighting.motivation
        }
    
    def _adjust_body_language_intensity(self, body: BodyLanguageSet, 
                                      intensity: float,
                                      cultural: Dict[str, float]) -> Dict[str, Any]:
        """Adjust body language based on intensity and culture."""
        # Apply cultural emotion intensity modifier
        cultural_intensity = intensity * cultural['emotion_intensity']
        
        return {
            'posture': body.posture,
            'gestures': body.gesture,
            'movement_quality': body.movement_quality,
            'spatial_relationship': body.spatial_relationship,
            'tension_points': body.tension_points,
            'energy_level': body.energy_level * cultural_intensity,
            'cultural_adjustments': {
                'personal_space': cultural['personal_space'],
                'eye_contact': cultural['eye_contact'],
                'touch_comfort': cultural['touch_comfort']
            }
        }
    
    def _select_cinematography_style(self, emotion: str, intensity: float) -> str:
        """Select appropriate cinematography style based on emotion and intensity."""
        style_mapping = {
            'joy': 'intimate' if intensity < 0.5 else 'epic',
            'sadness': 'intimate' if intensity > 0.5 else 'minimalist',
            'anger': 'expressionist' if intensity > 0.7 else 'documentary',
            'fear': 'expressionist',
            'contemplation': 'minimalist',
            'melancholy': 'impressionist',
            'existential_dread': 'expressionist' if intensity > 0.5 else 'minimalist',
            'transcendent_joy': 'epic' if intensity > 0.7 else 'impressionist',
            'wonder': 'baroque' if intensity > 0.6 else 'documentary',
            'serenity': 'minimalist',
            'ennui': 'minimalist',
            'bittersweet': 'impressionist'
        }
        
        return style_mapping.get(emotion, 'documentary')
    
    def _blend_palettes(self, palette1: Dict, palette2: Dict, 
                       ratio: float) -> Dict[str, Any]:
        """Blend two color palettes."""
        return {
            'primary_colors': palette1['primary_colors'][:2] + palette2['primary_colors'][:1],
            'secondary_colors': self._mix_colors(
                palette1['secondary_colors'], 
                palette2['secondary_colors'], 
                ratio
            ),
            'accent_colors': palette2['accent_colors'][:1] if ratio < 0.8 else palette1['accent_colors'],
            'saturation': palette1['saturation'] * ratio + palette2['saturation'] * (1 - ratio),
            'brightness': palette1['brightness'] * ratio + palette2['brightness'] * (1 - ratio),
            'temperature': palette1['temperature'] * ratio + palette2['temperature'] * (1 - ratio)
        }
    
    def _blend_lighting(self, lighting1: Dict, lighting2: Dict, 
                       ratio: float) -> Dict[str, Any]:
        """Blend two lighting schemes."""
        return {
            'key_light': lighting1['key_light'] if ratio > 0.5 else lighting2['key_light'],
            'fill_light': f"Mixed: {lighting1['fill_light']} and {lighting2['fill_light']}",
            'contrast_ratio': lighting1['contrast_ratio'] * ratio + lighting2['contrast_ratio'] * (1 - ratio),
            'color_temperature': int(
                lighting1['color_temperature'] * ratio + 
                lighting2['color_temperature'] * (1 - ratio)
            )
        }
    
    def _combine_body_language(self, body1: Dict, body2: Dict, 
                             ratio: float) -> Dict[str, Any]:
        """Combine body language from two emotions."""
        return {
            'posture': f"{body1['posture']} with hints of {body2['posture']}",
            'gestures': body1['gestures'][:2] + body2['gestures'][:1],
            'energy_level': body1['energy_level'] * ratio + body2['energy_level'] * (1 - ratio),
            'movement_quality': f"{body1['movement_quality']} transitioning to {body2['movement_quality']}"
        }
    
    def _mix_atmosphere(self, atmo1: AtmosphericEffect, atmo2: AtmosphericEffect,
                       ratio: float) -> Dict[str, Any]:
        """Mix atmospheric effects."""
        return {
            'weather': atmo1.weather if ratio > 0.5 else atmo2.weather,
            'particles': atmo1.particles[:2] + atmo2.particles[:1],
            'fog_density': atmo1.fog_density * ratio + atmo2.fog_density * (1 - ratio),
            'wind_strength': atmo1.wind_strength * ratio + atmo2.wind_strength * (1 - ratio),
            'time_distortion': atmo1.time_distortion if ratio > 0.7 else atmo2.time_distortion
        }
    
    def _blend_facial_expressions(self, face1: FacialExpression, face2: FacialExpression,
                                ratio: float) -> Dict[str, Any]:
        """Blend facial expressions."""
        return {
            'eyes': f"{face1.eyes} with traces of {face2.eyes}",
            'mouth': face1.mouth if ratio > 0.6 else face2.mouth,
            'overall_tension': f"Mixed: {face1.overall_tension} and {face2.overall_tension}",
            'micro_expressions': face1.micro_expressions[:2] + face2.micro_expressions[:1]
        }
    
    def _merge_symbols(self, symbols1: SymbolicElement, 
                      symbols2: SymbolicElement) -> Dict[str, Any]:
        """Merge symbolic elements from two emotions."""
        return {
            'objects': list(set(symbols1.objects[:2] + symbols2.objects[:1])),
            'natural_elements': list(set(symbols1.natural_elements[:2] + symbols2.natural_elements[:1])),
            'recurring_motifs': list(set(symbols1.recurring_motifs[:2] + symbols2.recurring_motifs[:1]))
        }
    
    def _select_blended_cinematography(self, emotion1: str, emotion2: str) -> str:
        """Select cinematography for blended emotions."""
        style1 = self._select_cinematography_style(emotion1, 0.5)
        style2 = self._select_cinematography_style(emotion2, 0.5)
        
        # Prefer more dynamic style
        style_hierarchy = ['baroque', 'expressionist', 'epic', 'impressionist', 
                         'documentary', 'intimate', 'minimalist']
        
        if style_hierarchy.index(style1) < style_hierarchy.index(style2):
            return style1
        return style2
    
    def _mix_colors(self, colors1: List[str], colors2: List[str], 
                   ratio: float) -> List[str]:
        """Mix two color lists based on ratio."""
        num_from_first = int(len(colors1) * ratio)
        return colors1[:num_from_first] + colors2[:len(colors1) - num_from_first]
    
    def _calculate_transition_palette(self, from_palette: Dict, to_palette: Dict,
                                    progress: float) -> Dict[str, Any]:
        """Calculate palette for smooth transition."""
        return {
            'primary_colors': self._mix_colors(
                from_palette['primary_colors'],
                to_palette['primary_colors'],
                1 - progress
            ),
            'saturation': from_palette['saturation'] * (1 - progress) + to_palette['saturation'] * progress,
            'brightness': from_palette['brightness'] * (1 - progress) + to_palette['brightness'] * progress,
            'temperature': from_palette['temperature'] * (1 - progress) + to_palette['temperature'] * progress,
            'transition_effect': 'smooth_blend' if progress < 0.8 else 'approaching_target'
        }
    
    def _calculate_transition_lighting(self, from_lighting: Dict, to_lighting: Dict,
                                     progress: float) -> Dict[str, Any]:
        """Calculate lighting for smooth transition."""
        return {
            'contrast_ratio': from_lighting['contrast_ratio'] * (1 - progress) + to_lighting['contrast_ratio'] * progress,
            'color_temperature': int(
                from_lighting['color_temperature'] * (1 - progress) + 
                to_lighting['color_temperature'] * progress
            ),
            'transition_quality': 'gradual_shift' if progress < 0.5 else 'accelerating_change'
        }
    
    def _calculate_transition_atmosphere(self, from_atmo: Any, to_atmo: Any,
                                       progress: float) -> Dict[str, Any]:
        """Calculate atmospheric transition."""
        # Handle both dict and AtmosphericEffect objects
        if hasattr(from_atmo, 'fog_density'):
            from_fog = from_atmo.fog_density
            from_wind = from_atmo.wind_strength
        else:
            from_fog = from_atmo.get('fog_density', 0.0)
            from_wind = from_atmo.get('wind_strength', 0.0)
            
        if hasattr(to_atmo, 'fog_density'):
            to_fog = to_atmo.fog_density
            to_wind = to_atmo.wind_strength
        else:
            to_fog = to_atmo.get('fog_density', 0.0)
            to_wind = to_atmo.get('wind_strength', 0.0)
        
        return {
            'fog_density': from_fog * (1 - progress) + to_fog * progress,
            'wind_strength': from_wind * (1 - progress) + to_wind * progress,
            'particle_transition': 'fading_out' if progress < 0.5 else 'fading_in'
        }
    
    def _get_body_language_shift(self, from_body: Any, to_body: Any,
                                progress: float) -> Dict[str, Any]:
        """Get body language shift description."""
        # Handle both dict and BodyLanguageSet objects
        if hasattr(from_body, 'posture'):
            from_posture = from_body.posture
            from_energy = from_body.energy_level
        else:
            from_posture = from_body.get('posture', 'neutral')
            from_energy = from_body.get('energy_level', 0.5)
            
        if hasattr(to_body, 'posture'):
            to_posture = to_body.posture
            to_energy = to_body.energy_level
        else:
            to_posture = to_body.get('posture', 'neutral')
            to_energy = to_body.get('energy_level', 0.5)
        
        return {
            'posture_shift': f"From {from_posture} to {to_posture}",
            'energy_transition': from_energy * (1 - progress) + to_energy * progress,
            'movement_evolution': 'initiating_change' if progress < 0.3 else 'completing_transition'
        }
    
    def _get_cinematography_transition(self, from_emotion: str, to_emotion: str,
                                     progress: float) -> Dict[str, Any]:
        """Get cinematography transition strategy."""
        from_style = self._select_cinematography_style(from_emotion, 0.5)
        to_style = self._select_cinematography_style(to_emotion, 0.5)
        
        return {
            'from_style': from_style,
            'to_style': to_style,
            'transition_technique': 'cross_dissolve' if progress < 0.5 else 'match_cut',
            'camera_movement': 'smooth_transition' if from_style != to_style else 'continuous'
        }