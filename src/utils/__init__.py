"""Utility modules for the Metaphysical Scene Weaver."""

# Import visual rules first (no dependencies)
from .visual_rules import (
    VisualRules,
    ColorPalette,
    LightingScheme,
    BodyLanguageSet,
    FacialExpression,
    AtmosphericEffect,
    SymbolicElement,
    ColorTheory,
    CinematographyStyle
)

# Import concept networks (requires networkx)
try:
    from .concept_networks import ConceptNetwork, ConceptNode, ConceptRelation
    CONCEPT_NETWORKS_AVAILABLE = True
except ImportError:
    CONCEPT_NETWORKS_AVAILABLE = False
    ConceptNetwork = ConceptNode = ConceptRelation = None

# Import websocket handler (requires websockets)
try:
    from .websocket_handler import (
        WebSocketHandler,
        WebSocketConfig,
        ConnectionState,
        ConnectionMetrics,
        EnhancedSemantestClient
    )
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    WebSocketHandler = WebSocketConfig = ConnectionState = ConnectionMetrics = EnhancedSemantestClient = None

__all__ = [
    # Visual rules
    'VisualRules',
    'ColorPalette',
    'LightingScheme', 
    'BodyLanguageSet',
    'FacialExpression',
    'AtmosphericEffect',
    'SymbolicElement',
    'ColorTheory',
    'CinematographyStyle',
]

# Add websocket if available
if WEBSOCKET_AVAILABLE:
    __all__.extend([
        'WebSocketHandler',
        'WebSocketConfig',
        'ConnectionState',
        'ConnectionMetrics',
        'EnhancedSemantestClient'
    ])

# Add concept networks if available
if CONCEPT_NETWORKS_AVAILABLE:
    __all__.extend(['ConceptNetwork', 'ConceptNode', 'ConceptRelation'])