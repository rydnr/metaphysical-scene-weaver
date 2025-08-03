"""Concept network system for tracking philosophical concept relationships and evolution."""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import networkx as nx
import logging
from datetime import datetime


@dataclass
class ConceptNode:
    """Represents a philosophical concept in the network."""
    name: str
    category: str
    weight: float = 1.0
    first_appearance: Optional[datetime] = None
    occurrences: int = 0
    contexts: List[str] = field(default_factory=list)
    related_emotions: List[str] = field(default_factory=list)
    visual_associations: List[str] = field(default_factory=list)


@dataclass
class ConceptRelation:
    """Represents a relationship between two concepts."""
    source: str
    target: str
    relation_type: str
    strength: float = 1.0
    contexts: List[str] = field(default_factory=list)
    co_occurrence_count: int = 0


class ConceptNetwork:
    """Manages the network of philosophical concepts and their relationships."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.graph = nx.DiGraph()
        self.concept_history = []
        self.relation_types = {
            'implies': 'logical implication',
            'contradicts': 'logical contradiction',
            'complements': 'complementary relationship',
            'transforms_to': 'conceptual transformation',
            'precedes': 'temporal precedence',
            'causes': 'causal relationship',
            'depends_on': 'dependency relationship',
            'emerges_from': 'emergent relationship',
            'synthesizes_with': 'dialectical synthesis',
            'opposes': 'opposition/tension'
        }
        
    def add_concept(
        self,
        name: str,
        category: str,
        context: Optional[str] = None,
        emotions: Optional[List[str]] = None,
        visuals: Optional[List[str]] = None
    ) -> ConceptNode:
        """Add or update a concept in the network."""
        if self.graph.has_node(name):
            # Update existing concept
            node = self.graph.nodes[name]['data']
            node.occurrences += 1
            if context:
                node.contexts.append(context)
            if emotions:
                node.related_emotions.extend(emotions)
            if visuals:
                node.visual_associations.extend(visuals)
        else:
            # Create new concept
            node = ConceptNode(
                name=name,
                category=category,
                first_appearance=datetime.now(),
                occurrences=1,
                contexts=[context] if context else [],
                related_emotions=emotions or [],
                visual_associations=visuals or []
            )
            self.graph.add_node(name, data=node)
        
        # Track in history
        self.concept_history.append((datetime.now(), name, context))
        
        return node
    
    def add_relation(
        self,
        source: str,
        target: str,
        relation_type: str,
        strength: float = 1.0,
        context: Optional[str] = None
    ) -> ConceptRelation:
        """Add or strengthen a relationship between concepts."""
        # Ensure both concepts exist
        if not self.graph.has_node(source):
            self.add_concept(source, 'unknown')
        if not self.graph.has_node(target):
            self.add_concept(target, 'unknown')
        
        # Create or update edge
        if self.graph.has_edge(source, target):
            # Strengthen existing relation
            edge_data = self.graph.edges[source, target]
            edge_data['strength'] += strength * 0.1  # Incremental strengthening
            edge_data['co_occurrence_count'] += 1
            if context:
                edge_data['contexts'].append(context)
        else:
            # Create new relation
            relation = ConceptRelation(
                source=source,
                target=target,
                relation_type=relation_type,
                strength=strength,
                contexts=[context] if context else [],
                co_occurrence_count=1
            )
            self.graph.add_edge(
                source,
                target,
                relation_type=relation_type,
                strength=strength,
                contexts=relation.contexts,
                co_occurrence_count=1,
                data=relation
            )
        
        return relation
    
    def get_concept_cluster(
        self,
        concept: str,
        depth: int = 2
    ) -> Dict[str, Any]:
        """Get the cluster of related concepts around a central concept."""
        if not self.graph.has_node(concept):
            return {'central': concept, 'related': [], 'relations': []}
        
        # Use BFS to find related concepts up to specified depth
        related_concepts = set()
        relations = []
        
        current_level = {concept}
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                # Outgoing connections
                for successor in self.graph.successors(node):
                    related_concepts.add(successor)
                    edge_data = self.graph.edges[node, successor]
                    relations.append({
                        'source': node,
                        'target': successor,
                        'type': edge_data['relation_type'],
                        'strength': edge_data['strength']
                    })
                    next_level.add(successor)
                
                # Incoming connections
                for predecessor in self.graph.predecessors(node):
                    related_concepts.add(predecessor)
                    edge_data = self.graph.edges[predecessor, node]
                    relations.append({
                        'source': predecessor,
                        'target': node,
                        'type': edge_data['relation_type'],
                        'strength': edge_data['strength']
                    })
                    next_level.add(predecessor)
            
            current_level = next_level
        
        return {
            'central': concept,
            'related': list(related_concepts),
            'relations': relations
        }
    
    def find_concept_path(
        self,
        source: str,
        target: str
    ) -> Optional[List[str]]:
        """Find the conceptual path between two concepts."""
        try:
            # Try to find shortest path
            path = nx.shortest_path(self.graph, source, target)
            return path
        except nx.NetworkXNoPath:
            # Try undirected path
            try:
                undirected = self.graph.to_undirected()
                path = nx.shortest_path(undirected, source, target)
                return path
            except nx.NetworkXNoPath:
                return None
    
    def get_concept_evolution(
        self,
        concept: str,
        window_size: int = 10
    ) -> Dict[str, Any]:
        """Track how a concept has evolved over time."""
        if not self.graph.has_node(concept):
            return {'concept': concept, 'evolution': []}
        
        node_data = self.graph.nodes[concept]['data']
        
        # Get concept appearances from history
        appearances = [
            (timestamp, context)
            for timestamp, name, context in self.concept_history
            if name == concept
        ]
        
        # Analyze changes in relationships over time
        evolution_data = {
            'concept': concept,
            'first_appearance': node_data.first_appearance,
            'total_occurrences': node_data.occurrences,
            'contexts': node_data.contexts[-window_size:],  # Recent contexts
            'emotion_evolution': self._analyze_emotion_evolution(node_data),
            'visual_evolution': self._analyze_visual_evolution(node_data),
            'relationship_changes': self._analyze_relationship_changes(concept)
        }
        
        return evolution_data
    
    def detect_concept_clusters(self) -> List[Set[str]]:
        """Detect strongly connected concept clusters in the network."""
        # Find strongly connected components
        clusters = list(nx.strongly_connected_components(self.graph))
        
        # Sort by size
        clusters.sort(key=len, reverse=True)
        
        return clusters
    
    def get_central_concepts(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get the most central concepts in the network."""
        if not self.graph.nodes():
            return []
        
        # Calculate centrality measures
        pagerank = nx.pagerank(self.graph)
        betweenness = nx.betweenness_centrality(self.graph)
        
        # Combine measures
        combined_centrality = {}
        for node in self.graph.nodes():
            combined_centrality[node] = (
                pagerank.get(node, 0) * 0.6 +
                betweenness.get(node, 0) * 0.4
            )
        
        # Sort and return top concepts
        sorted_concepts = sorted(
            combined_centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_concepts[:top_n]
    
    def suggest_missing_concepts(
        self,
        existing_concepts: List[str]
    ) -> List[str]:
        """Suggest concepts that might be missing based on network patterns."""
        suggestions = set()
        
        for concept in existing_concepts:
            if not self.graph.has_node(concept):
                continue
            
            # Look for common neighbors of related concepts
            neighbors = set(self.graph.neighbors(concept))
            
            for neighbor in neighbors:
                # Check if neighbor has connections we don't
                neighbor_connections = set(self.graph.neighbors(neighbor))
                potential_missing = neighbor_connections - set(existing_concepts)
                suggestions.update(potential_missing)
        
        return list(suggestions)
    
    def _analyze_emotion_evolution(self, node: ConceptNode) -> List[Dict[str, Any]]:
        """Analyze how emotions associated with a concept have evolved."""
        emotion_timeline = []
        window_size = 5
        
        for i in range(0, len(node.related_emotions), window_size):
            window = node.related_emotions[i:i+window_size]
            if window:
                emotion_counts = defaultdict(int)
                for emotion in window:
                    emotion_counts[emotion] += 1
                
                emotion_timeline.append({
                    'window': i // window_size,
                    'dominant_emotions': sorted(
                        emotion_counts.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:3]
                })
        
        return emotion_timeline
    
    def _analyze_visual_evolution(self, node: ConceptNode) -> List[Dict[str, Any]]:
        """Analyze how visual associations have evolved."""
        visual_timeline = []
        window_size = 5
        
        for i in range(0, len(node.visual_associations), window_size):
            window = node.visual_associations[i:i+window_size]
            if window:
                visual_counts = defaultdict(int)
                for visual in window:
                    visual_counts[visual] += 1
                
                visual_timeline.append({
                    'window': i // window_size,
                    'dominant_visuals': sorted(
                        visual_counts.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:3]
                })
        
        return visual_timeline
    
    def _analyze_relationship_changes(self, concept: str) -> List[Dict[str, Any]]:
        """Analyze how relationships of a concept have changed over time."""
        changes = []
        
        # Get all edges involving this concept
        edges_out = [(concept, target) for target in self.graph.successors(concept)]
        edges_in = [(source, concept) for source in self.graph.predecessors(concept)]
        
        for edge in edges_out + edges_in:
            edge_data = self.graph.edges[edge]
            changes.append({
                'relation': f"{edge[0]} -> {edge[1]}",
                'type': edge_data['relation_type'],
                'strength': edge_data['strength'],
                'occurrences': edge_data['co_occurrence_count']
            })
        
        # Sort by strength
        changes.sort(key=lambda x: x['strength'], reverse=True)
        
        return changes[:10]  # Top 10 relationships
    
    def export_for_visualization(self) -> Dict[str, Any]:
        """Export network data for visualization."""
        nodes = []
        edges = []
        
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]['data']
            nodes.append({
                'id': node_id,
                'label': node_id,
                'category': node_data.category,
                'weight': node_data.weight,
                'occurrences': node_data.occurrences
            })
        
        for source, target in self.graph.edges():
            edge_data = self.graph.edges[source, target]
            edges.append({
                'source': source,
                'target': target,
                'type': edge_data['relation_type'],
                'weight': edge_data['strength']
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_concepts': len(nodes),
                'total_relations': len(edges),
                'average_connections': len(edges) / len(nodes) if nodes else 0
            }
        }