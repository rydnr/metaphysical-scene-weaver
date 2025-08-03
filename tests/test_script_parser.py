"""Tests for the script parser module."""

import pytest
from pathlib import Path
from src.core.script_parser import ScriptParser, ScriptEntry


class TestScriptParser:
    """Test cases for ScriptParser."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return ScriptParser()
    
    def test_parse_simple_dialogue(self, parser):
        """Test parsing a simple dialogue entry."""
        text = "[0001] Evan: <<Hello, how are you?>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert entries[0].id == "0001"
        assert entries[0].speaker == "Evan"
        assert entries[0].dialogue == "Hello, how are you?"
    
    def test_parse_with_panel_count(self, parser):
        """Test parsing entry with panel count."""
        text = "[0042] [2-panel] Monday: <<Reality bends around consciousness.>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert entries[0].panel_count == 2
        assert entries[0].speaker == "Monday"
    
    def test_parse_multiline_dialogue(self, parser):
        """Test parsing multiline dialogue."""
        text = """[0001] Evan: <<This is a long dialogue
        that spans multiple lines
        and continues here.>>"""
        
        entries = parser.parse_text(text)
        assert len(entries) == 1
        assert "multiple lines" in entries[0].dialogue
    
    def test_parse_with_metadata(self, parser):
        """Test parsing entries with metadata."""
        text = "[0001] Evan: <<Hello.>> [[philosophical question]]"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert "philosophical question" in entries[0].metadata
    
    def test_parse_with_stage_directions(self, parser):
        """Test parsing entries with stage directions."""
        text = "[0001] Evan: <<Hello.>> (looks thoughtful)"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert "looks thoughtful" in entries[0].stage_directions
    
    def test_parse_multiple_entries(self, parser):
        """Test parsing multiple entries."""
        text = """
        [0001] Evan: <<First line.>>
        [0002] Monday: <<Second line.>>
        [0003] Evan: <<Third line.>>
        """
        
        entries = parser.parse_text(text)
        assert len(entries) == 3
        assert entries[1].speaker == "Monday"
        assert entries[2].id == "0003"
    
    def test_extract_scene_descriptions(self, parser):
        """Test extracting scene descriptions."""
        entries = [
            ScriptEntry("0001", "Evan", "Hello", stage_directions=["looks around nervously"]),
            ScriptEntry("0002", "Monday", "Welcome", stage_directions=["gestures broadly"])
        ]
        
        scenes = parser.extract_scene_descriptions(entries)
        assert "0001" in scenes
        assert "looks around nervously" in scenes["0001"]["visual_cues"]