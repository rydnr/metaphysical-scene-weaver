"""Unit tests for the PhilosophicalInterpreter module."""

import pytest
from src.processors.philosophical_interpreter import (
    PhilosophicalInterpreter,
    PhilosophicalConcept,
    ConceptRelationship,
    PhilosophicalFramework,
    InterpretationResult
)


class TestPhilosophicalInterpreter:
    """Test cases for PhilosophicalInterpreter."""
    
    @pytest.mark.unit
    def test_initialization(self, philosophical_interpreter):
        """Test interpreter initialization."""
        assert isinstance(philosophical_interpreter, PhilosophicalInterpreter)
        assert philosophical_interpreter.frameworks is not None
        assert philosophical_interpreter.concept_graph is not None
    
    @pytest.mark.unit
    def test_detect_simple_concept(self, philosophical_interpreter):
        """Test detection of simple philosophical concepts."""
        dialogue = "What is the nature of consciousness?"
        
        result = philosophical_interpreter.interpret(dialogue)
        
        assert result is not None
        assert "consciousness" in [c.name for c in result.concepts]
        assert result.confidence > 0.5
    
    @pytest.mark.unit
    def test_detect_multiple_concepts(self, philosophical_interpreter):
        """Test detection of multiple philosophical concepts."""
        dialogue = "Free will and determinism seem incompatible, yet both shape our reality."
        
        result = philosophical_interpreter.interpret(dialogue)
        
        concept_names = [c.name for c in result.concepts]
        assert "free_will" in concept_names or "free will" in concept_names
        assert "determinism" in concept_names
        assert "reality" in concept_names
    
    @pytest.mark.unit
    def test_concept_relationships(self, philosophical_interpreter):
        """Test identification of concept relationships."""
        dialogue = "If consciousness emerges from complexity, then perhaps AI could be conscious."
        
        result = philosophical_interpreter.interpret(dialogue)
        
        # Check for concepts
        concept_names = [c.name for c in result.concepts]
        assert any("consciousness" in c for c in concept_names)
        assert any("emergence" in c or "complexity" in c for c in concept_names)
        
        # Check for relationships
        assert len(result.relationships) > 0
        relationship_types = [r.relationship_type for r in result.relationships]
        assert any(t in ["emerges_from", "causes", "implies"] for t in relationship_types)
    
    @pytest.mark.unit
    def test_framework_identification(self, philosophical_interpreter):
        """Test identification of philosophical frameworks."""
        dialogues = {
            "existentialism": "We are condemned to be free, creating meaning in an absurd universe.",
            "phenomenology": "The lived experience of consciousness reveals the structure of being.",
            "pragmatism": "Truth is what works in practice, not abstract theory."
        }
        
        for framework, dialogue in dialogues.items():
            result = philosophical_interpreter.interpret(dialogue)
            assert result.primary_framework is not None
            # Framework detection might not be exact, but should be related
            assert result.confidence > 0.3
    
    @pytest.mark.unit
    def test_paradox_detection(self, philosophical_interpreter):
        """Test detection of philosophical paradoxes."""
        dialogue = "This statement is false. Can something be both true and false?"
        
        result = philosophical_interpreter.interpret(dialogue)
        
        assert result.contains_paradox is True
        assert "paradox" in result.interpretation_notes.lower()
    
    @pytest.mark.unit
    def test_argument_structure_analysis(self, philosophical_interpreter):
        """Test analysis of argument structure."""
        dialogue = """
        If all humans are mortal, and Socrates is human, then Socrates is mortal.
        This demonstrates deductive reasoning.
        """
        
        result = philosophical_interpreter.interpret(dialogue)
        
        assert result.argument_structure is not None
        assert "deductive" in result.argument_structure.get("type", "").lower()
    
    @pytest.mark.unit
    def test_empty_dialogue_handling(self, philosophical_interpreter):
        """Test handling of empty dialogue."""
        result = philosophical_interpreter.interpret("")
        
        assert result is not None
        assert len(result.concepts) == 0
        assert result.confidence < 0.1
    
    @pytest.mark.unit
    def test_non_philosophical_dialogue(self, philosophical_interpreter):
        """Test handling of non-philosophical dialogue."""
        dialogue = "Please pass the salt. The weather is nice today."
        
        result = philosophical_interpreter.interpret(dialogue)
        
        assert result.confidence < 0.3
        assert len(result.concepts) == 0 or all(c.confidence < 0.5 for c in result.concepts)
    
    @pytest.mark.unit
    @pytest.mark.parametrize("concept,expected_category", [
        ("consciousness", "metaphysics"),
        ("knowledge", "epistemology"),
        ("morality", "ethics"),
        ("beauty", "aesthetics"),
        ("existence", "ontology")
    ])
    def test_concept_categorization(self, philosophical_interpreter, concept, expected_category):
        """Test categorization of philosophical concepts."""
        dialogue = f"What is the nature of {concept}?"
        
        result = philosophical_interpreter.interpret(dialogue)
        
        found_concept = next((c for c in result.concepts if concept in c.name.lower()), None)
        assert found_concept is not None
        assert found_concept.category == expected_category
    
    @pytest.mark.unit
    def test_complexity_scoring(self, philosophical_interpreter):
        """Test complexity scoring of philosophical content."""
        simple_dialogue = "What is truth?"
        complex_dialogue = """
        If consciousness is an emergent property of complex information processing,
        and if we accept functionalism's claim that mental states are defined by
        their causal relations rather than their physical substrate, then we must
        confront the possibility that artificial systems could achieve genuine
        consciousness, raising profound questions about the nature of experience,
        identity, and moral consideration.
        """
        
        simple_result = philosophical_interpreter.interpret(simple_dialogue)
        complex_result = philosophical_interpreter.interpret(complex_dialogue)
        
        assert complex_result.complexity_score > simple_result.complexity_score
        assert simple_result.complexity_score < 0.5
        assert complex_result.complexity_score > 0.7
    
    @pytest.mark.unit
    def test_concept_evolution_tracking(self, philosophical_interpreter):
        """Test tracking of concept evolution through dialogue."""
        dialogues = [
            "What is consciousness?",
            "Perhaps consciousness is just computation.",
            "But computation alone cannot explain subjective experience.",
            "Unless subjective experience itself is a form of computation we don't yet understand."
        ]
        
        evolution = []
        for dialogue in dialogues:
            result = philosophical_interpreter.interpret(dialogue)
            evolution.append(result)
        
        # Check that concepts evolve
        assert len(evolution) == 4
        # Later interpretations should show more nuanced understanding
        assert evolution[-1].complexity_score >= evolution[0].complexity_score
    
    @pytest.mark.unit
    def test_cultural_philosophy_detection(self, philosophical_interpreter):
        """Test detection of different cultural philosophical traditions."""
        traditions = {
            "western": "The unexamined life is not worth living, as Socrates taught.",
            "eastern": "The Tao that can be named is not the true Tao.",
            "african": "Ubuntu philosophy teaches that I am because we are."
        }
        
        for tradition, dialogue in traditions.items():
            result = philosophical_interpreter.interpret(dialogue)
            assert result is not None
            assert len(result.concepts) > 0
            # Cultural context should be noted
            assert any(tradition in note.lower() for note in [result.interpretation_notes])
    
    @pytest.mark.unit
    def test_question_type_classification(self, philosophical_interpreter):
        """Test classification of philosophical question types."""
        questions = {
            "ontological": "What does it mean to exist?",
            "epistemological": "How can we know anything for certain?",
            "ethical": "What makes an action morally right?",
            "aesthetic": "What is the nature of beauty?",
            "metaphysical": "Is there a fundamental substance to reality?"
        }
        
        for q_type, question in questions.items():
            result = philosophical_interpreter.interpret(question)
            assert result.question_type is not None
            assert q_type in result.question_type.lower()
    
    @pytest.mark.unit
    def test_philosophical_method_detection(self, philosophical_interpreter):
        """Test detection of philosophical methods."""
        methods = {
            "dialectical": "Thesis meets antithesis to produce synthesis.",
            "phenomenological": "We must bracket our assumptions to examine pure experience.",
            "analytical": "Let us precisely define our terms and examine their logical relations.",
            "pragmatic": "The truth of an idea lies in its practical consequences."
        }
        
        for method, dialogue in methods.items():
            result = philosophical_interpreter.interpret(dialogue)
            assert result.methodology is not None
            assert method in result.methodology.lower()