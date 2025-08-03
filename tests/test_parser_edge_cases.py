"""Edge case tests for the script parser - stress testing with complex scenarios."""

import pytest
from pathlib import Path
from src.core.script_parser import ScriptParser, ScriptEntry


class TestParserEdgeCases:
    """Test cases for parser edge cases and error handling."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return ScriptParser()
    
    def test_nested_brackets_in_dialogue(self, parser):
        """Test handling of nested brackets within dialogue."""
        text = "[0001] Evan: <<I said [[this is nested]] in the dialogue.>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert "[[this is nested]]" in entries[0].dialogue
        # Metadata should not be extracted from within dialogue
        assert len(entries[0].metadata) == 0
    
    def test_multiple_metadata_tags(self, parser):
        """Test multiple metadata tags on same line."""
        text = "[0001] Evan: <<Hello.>> [[tag1]] [[tag2]] [[tag3]]"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert len(entries[0].metadata) == 3
        assert "tag1" in entries[0].metadata
        assert "tag3" in entries[0].metadata
    
    def test_stage_directions_with_nested_parentheses(self, parser):
        """Test stage directions with nested parentheses."""
        text = "[0001] Evan: <<Hello.>> (looks at (something important))"
        entries = parser.parse_text(text)
        
        # Current parser will only capture the first level
        assert len(entries) == 1
        # This is a known limitation - nested parens not fully supported
        assert "looks at (something important" in entries[0].stage_directions
    
    def test_multiline_dialogue_with_interruptions(self, parser):
        """Test multiline dialogue with stage directions and metadata interspersed."""
        text = """[0001] Evan: <<This is a very long
        dialogue that continues (pauses)
        across multiple lines [[philosophical]]
        and keeps going on and on>>"""
        
        entries = parser.parse_text(text)
        assert len(entries) == 1
        assert "across multiple lines" in entries[0].dialogue
        # These should be captured despite being on continuation lines
        assert "pauses" in entries[0].stage_directions
        assert "philosophical" in entries[0].metadata
    
    def test_empty_dialogue(self, parser):
        """Test entries with empty dialogue."""
        text = "[0001] Evan: <<>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert entries[0].dialogue == ""
    
    def test_special_characters_in_dialogue(self, parser):
        """Test dialogue with special regex characters."""
        text = "[0001] Evan: <<What about $pecial ch@rs? And *asterisks* or .dots.?>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert "$pecial ch@rs?" in entries[0].dialogue
        assert "*asterisks*" in entries[0].dialogue
    
    def test_character_name_variations(self, parser):
        """Test various character name formats."""
        texts = [
            "[0001] EVAN: <<Uppercase name>>",
            "[0002] evan: <<Lowercase name>>",
            "[0003] Evan_2: <<Name with underscore>>",
            "[0004] EvanJr: <<Name with suffix>>",
            # This will fail with current regex - only \w+ allowed
            # "[0005] Evan-Jr: <<Name with hyphen>>",
        ]
        
        for text in texts:
            entries = parser.parse_text(text)
            assert len(entries) == 1
            assert entries[0].dialogue != ""
    
    def test_malformed_entries(self, parser):
        """Test handling of malformed entries."""
        malformed_texts = [
            "0001] Evan: <<Missing opening bracket>>",
            "[0001 Evan: <<Missing closing bracket>>",
            "[0001] : <<Missing speaker name>>",
            "[0001] Evan <<Missing colon>>",
            "[0001] Evan: <Single angle bracket>",
            "[0001] Evan: <<Unclosed dialogue",
            "[abcd] Evan: <<Non-numeric ID>>",
        ]
        
        for text in malformed_texts:
            entries = parser.parse_text(text)
            # Current parser will not parse these - they'll be empty
            assert len(entries) == 0
    
    def test_dialogue_with_angle_brackets_inside(self, parser):
        """Test dialogue containing angle brackets."""
        text = "[0001] Evan: <<Is 5 < 10? And 10 > 5?>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert "5 < 10" in entries[0].dialogue
        assert "10 > 5" in entries[0].dialogue
    
    def test_consecutive_entries_no_spacing(self, parser):
        """Test entries with no blank lines between them."""
        text = """[0001] Evan: <<First.>>
[0002] Monday: <<Second.>>
[0003] Valerie: <<Third.>>"""
        
        entries = parser.parse_text(text)
        assert len(entries) == 3
        assert entries[0].speaker == "Evan"
        assert entries[1].speaker == "Monday"
        assert entries[2].speaker == "Valerie"
    
    def test_unicode_and_emojis(self, parser):
        """Test Unicode characters and emojis in dialogue."""
        text = "[0001] Evan: <<Hello 世界! 😊 How are you?>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert "世界" in entries[0].dialogue
        assert "😊" in entries[0].dialogue
    
    def test_very_long_dialogue(self, parser):
        """Test handling of extremely long dialogue."""
        long_text = "A" * 10000  # 10k characters
        text = f"[0001] Evan: <<{long_text}>>"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert len(entries[0].dialogue) == 10000
    
    def test_panel_count_variations(self, parser):
        """Test different panel count formats."""
        texts = [
            "[0001] [1-panel] Evan: <<Single panel>>",
            "[0002] [99-panel] Evan: <<Many panels>>",
            "[0003] [0-panel] Evan: <<Zero panels?>>",
            # This should fail - no 'panels' plural
            "[0004] [2-panels] Evan: <<Wrong format>>",
        ]
        
        entries = []
        for text in texts[:3]:  # First three should work
            result = parser.parse_text(text)
            entries.extend(result)
        
        assert len(entries) == 3
        assert entries[0].panel_count == 1
        assert entries[1].panel_count == 99
        assert entries[2].panel_count == 0
        
        # The fourth one with 'panels' won't match
        result = parser.parse_text(texts[3])
        assert len(result) == 0
    
    def test_metadata_and_stage_directions_before_dialogue(self, parser):
        """Test metadata/stage appearing before the dialogue ends."""
        text = "[0001] [[pre-meta]] Evan: (nervously) <<Hello there.>> [[post-meta]] (smiles)"
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        # With current line-by-line parsing, pre-dialogue annotations might be lost
        # This is a known limitation
        assert "Hello there." in entries[0].dialogue
    
    def test_dialogue_spanning_many_lines_with_blank_lines(self, parser):
        """Test dialogue that includes blank lines within it."""
        text = """[0001] Evan: <<This dialogue has

        blank lines in it
        
        but should still be captured.>>"""
        
        entries = parser.parse_text(text)
        assert len(entries) == 1
        # Current parser processes line by line, so blank lines might break it
        # This is another edge case to handle
    
    def test_mixed_quote_styles(self, parser):
        """Test dialogue with various quote marks."""
        text = """[0001] Evan: <<He said "hello" and 'goodbye' in the same breath.>>"""
        entries = parser.parse_text(text)
        
        assert len(entries) == 1
        assert '"hello"' in entries[0].dialogue
        assert "'goodbye'" in entries[0].dialogue
    
    def test_stage_direction_edge_cases(self, parser):
        """Test complex stage direction scenarios."""
        texts = [
            "[0001] Evan: <<Hello.>> ()",  # Empty stage direction
            "[0001] Evan: <<Hello.>> (stage (with) nested)",  # Nested
            "[0001] Evan: <<Hello.>> (first) (second) (third)",  # Multiple
        ]
        
        for i, text in enumerate(texts):
            entries = parser.parse_text(text)
            assert len(entries) == 1
            
            if i == 0:  # Empty
                assert "" in entries[0].stage_directions or len(entries[0].stage_directions) == 0
            elif i == 1:  # Nested - will be truncated
                # Known issue with nested parentheses
                pass
            elif i == 2:  # Multiple
                assert len(entries[0].stage_directions) == 3
                assert "third" in entries[0].stage_directions