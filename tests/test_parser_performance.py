"""Performance testing and optimization for script parser."""

import time
import re
from typing import List, Tuple, Callable
import random
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.script_parser import ScriptParser
from core.script_parser_v2 import EnhancedScriptParser


class PerformanceProfiler:
    """Profile parser performance with various script sizes."""
    
    def __init__(self):
        self.results = []
        
    def generate_script(self, num_entries: int, 
                       avg_dialogue_length: int = 100,
                       metadata_prob: float = 0.3,
                       stage_prob: float = 0.4) -> str:
        """Generate a synthetic script for testing."""
        speakers = ['Evan', 'Monday', 'Valerie', 'Architect', 'Observer']
        script_lines = []
        
        for i in range(1, num_entries + 1):
            # Entry ID and speaker
            speaker = random.choice(speakers)
            line = f"[{i:04d}] {speaker}: <<"
            
            # Generate dialogue
            words = []
            for _ in range(random.randint(50, avg_dialogue_length)):
                word_length = random.randint(3, 10)
                word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
                words.append(word)
            
            line += ' '.join(words) + '>>'
            
            # Add metadata randomly
            if random.random() < metadata_prob:
                num_meta = random.randint(1, 3)
                for _ in range(num_meta):
                    meta = ''.join(random.choices(string.ascii_lowercase, k=10))
                    line += f' [[{meta}]]'
            
            # Add stage directions randomly
            if random.random() < stage_prob:
                num_stage = random.randint(1, 2)
                for _ in range(num_stage):
                    stage = ' '.join(random.choices(string.ascii_lowercase, k=5))
                    line += f' ({stage})'
            
            script_lines.append(line)
            
            # Add some blank lines
            if random.random() < 0.1:
                script_lines.append('')
        
        return '\n'.join(script_lines)
    
    def time_function(self, func: Callable, *args, **kwargs) -> Tuple[float, any]:
        """Time a function execution."""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return end - start, result
    
    def profile_parser(self, parser_class, script_sizes: List[int], 
                      iterations: int = 3):
        """Profile parser performance across different script sizes."""
        results = {}
        
        for size in script_sizes:
            print(f"\nTesting with {size} entries...")
            script = self.generate_script(size)
            
            times = []
            for i in range(iterations):
                parser = parser_class()
                duration, entries = self.time_function(parser.parse_text, script)
                times.append(duration)
                
                if i == 0:  # Validate on first iteration
                    print(f"  Parsed {len(entries)} entries")
            
            avg_time = sum(times) / len(times)
            results[size] = {
                'avg_time': avg_time,
                'entries_per_second': size / avg_time,
                'min_time': min(times),
                'max_time': max(times)
            }
            
            print(f"  Average time: {avg_time:.3f}s")
            print(f"  Entries/second: {size / avg_time:.0f}")
        
        return results


class RegexOptimizer:
    """Test and optimize regex patterns."""
    
    def __init__(self):
        self.test_cases = self._generate_test_cases()
        
    def _generate_test_cases(self) -> List[Tuple[str, str, bool]]:
        """Generate test cases for regex patterns."""
        return [
            # Pattern name, test string, should match
            ('dialogue', '[0001] Evan: <<Hello world>>', True),
            ('dialogue', '[0001] [2-panel] Monday: <<Complex>>', True),
            ('dialogue', '[abc] Invalid: <<test>>', False),
            ('dialogue', '[0001] : <<No speaker>>', False),
            ('metadata', '[[philosophical question]]', True),
            ('metadata', '[[nested [[brackets]] here]]', True),
            ('stage', '(looks around)', True),
            ('stage', '(complex (nested) parens)', True),
        ]
    
    def compare_patterns(self):
        """Compare different regex pattern implementations."""
        # Original patterns
        original_patterns = {
            'dialogue': re.compile(
                r'\[(\d+)\]\s*(?:\[(\d+)-panel\])?\s*(\w+):\s*<<(.+?)>>',
                re.DOTALL
            ),
            'metadata': re.compile(r'\[\[(.*?)\]\]', re.DOTALL),
            'stage': re.compile(r'\(([^)]+)\)')
        }
        
        # Optimized patterns - avoid DOTALL when possible, use more specific patterns
        optimized_patterns = {
            'dialogue': re.compile(
                r'^\[(\d{4})\]\s*(?:\[(\d+)-panel\])?\s*([\w_]+):\s*<<(.*)$',
                re.MULTILINE
            ),
            'metadata': re.compile(r'\[\[([^\]]+)\]\]'),
            'stage': re.compile(r'\(([^()]+)\)')
        }
        
        # Test performance
        test_text = self._generate_large_test_text()
        
        print("Pattern Performance Comparison:")
        print("-" * 50)
        
        for pattern_name in ['dialogue', 'metadata', 'stage']:
            print(f"\n{pattern_name.capitalize()} Pattern:")
            
            # Test original
            start = time.perf_counter()
            original_matches = list(original_patterns[pattern_name].finditer(test_text))
            original_time = time.perf_counter() - start
            
            # Test optimized
            start = time.perf_counter()
            optimized_matches = list(optimized_patterns[pattern_name].finditer(test_text))
            optimized_time = time.perf_counter() - start
            
            print(f"  Original: {original_time:.6f}s ({len(original_matches)} matches)")
            print(f"  Optimized: {optimized_time:.6f}s ({len(optimized_matches)} matches)")
            print(f"  Speedup: {original_time / optimized_time:.2f}x")
            
            # Verify same results
            if pattern_name != 'dialogue':  # Dialogue pattern changed behavior
                if len(original_matches) != len(optimized_matches):
                    print(f"  WARNING: Match count differs!")
    
    def _generate_large_test_text(self, lines: int = 10000) -> str:
        """Generate large text for performance testing."""
        profiler = PerformanceProfiler()
        return profiler.generate_script(lines)
    
    def test_catastrophic_backtracking(self):
        """Test for catastrophic backtracking in regex patterns."""
        print("\nTesting for Catastrophic Backtracking:")
        print("-" * 50)
        
        # Patterns that could cause issues
        risky_patterns = [
            (r'<<(.+?)>>', 'greedy_dialogue'),  # Original
            (r'<<([^>]+)>>', 'negated_class'),  # Better
            (r'\[\[(.+?)\]\]', 'greedy_metadata'),  # Original
            (r'\[\[([^\]]+)\]\]', 'negated_metadata'),  # Better
        ]
        
        # Test with pathological input
        pathological_inputs = [
            '<<' + 'a' * 1000 + '<<',  # Nested opening brackets
            '[[' + 'b' * 1000 + '[[',  # Nested metadata
            '<<' + 'c' * 1000,  # Unclosed dialogue
        ]
        
        for pattern_str, name in risky_patterns:
            pattern = re.compile(pattern_str)
            print(f"\n{name}: {pattern_str}")
            
            for test_input in pathological_inputs[:1]:  # Test one to avoid hanging
                try:
                    start = time.perf_counter()
                    matches = pattern.findall(test_input)
                    duration = time.perf_counter() - start
                    print(f"  Input length {len(test_input)}: {duration:.6f}s")
                    
                    if duration > 0.1:
                        print(f"  WARNING: Slow performance detected!")
                except Exception as e:
                    print(f"  ERROR: {e}")


def main():
    """Run performance tests."""
    print("Script Parser Performance Testing")
    print("=" * 50)
    
    # Test parser performance
    profiler = PerformanceProfiler()
    
    print("\nComparing Parser Implementations:")
    script_sizes = [100, 500, 1000, 5000]
    
    print("\nOriginal Parser:")
    original_results = profiler.profile_parser(ScriptParser, script_sizes, iterations=3)
    
    print("\nEnhanced Parser:")
    enhanced_results = profiler.profile_parser(EnhancedScriptParser, script_sizes, iterations=3)
    
    # Compare results
    print("\nPerformance Comparison:")
    print("-" * 50)
    print(f"{'Size':<10} {'Original (s)':<15} {'Enhanced (s)':<15} {'Speedup':<10}")
    print("-" * 50)
    
    for size in script_sizes:
        orig_time = original_results[size]['avg_time']
        enh_time = enhanced_results[size]['avg_time']
        speedup = orig_time / enh_time
        print(f"{size:<10} {orig_time:<15.3f} {enh_time:<15.3f} {speedup:<10.2f}x")
    
    # Test regex optimization
    print("\n" + "=" * 50)
    optimizer = RegexOptimizer()
    optimizer.compare_patterns()
    optimizer.test_catastrophic_backtracking()
    
    # Memory usage test
    print("\n" + "=" * 50)
    print("Memory Usage Test:")
    print("-" * 50)
    
    # Generate a very large script
    huge_script = profiler.generate_script(10000)
    print(f"Script size: {len(huge_script) / 1024 / 1024:.2f} MB")
    
    # Test memory efficiency
    import tracemalloc
    
    tracemalloc.start()
    parser = EnhancedScriptParser()
    entries = parser.parse_text(huge_script)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Parsed {len(entries)} entries")
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()