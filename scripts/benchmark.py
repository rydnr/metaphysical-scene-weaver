"""Performance benchmarking system for Metaphysical Scene Weaver.

This script provides comprehensive performance testing for all components,
measuring speed, memory usage, and scalability.
"""

import time
import tracemalloc
import psutil
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from concurrent.futures import ProcessPoolExecutor, as_completed
import click

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.script_parser import ScriptParser
from src.core.scene_weaver import SceneWeaver
from src.core.character_state_tracker import CharacterStateTracker
from src.processors.philosophical_interpreter import PhilosophicalInterpreter
from src.processors.emotional_mapper import EmotionalMapper
from src.processors.metaphor_translator import MetaphorTranslator
from src.processors.context_analyzer import ContextAnalyzer
from src.processors.prompt_generator import PromptGenerator
from src.processors.scene_synthesizer import SceneSynthesizer


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""
    test_name: str
    module: str
    execution_time: float
    memory_peak: float
    memory_delta: float
    cpu_percent: float
    input_size: int
    output_size: int
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class BenchmarkSuite:
    """Collection of benchmark results."""
    suite_name: str
    timestamp: datetime
    system_info: Dict[str, Any]
    results: List[BenchmarkResult]
    summary: Dict[str, float]


class PerformanceBenchmark:
    """Main benchmarking system."""
    
    def __init__(self, output_dir: Path = Path("benchmark_results")):
        """Initialize benchmark system.
        
        Args:
            output_dir: Directory for storing benchmark results
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
        
    def measure_performance(
        self,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        test_name: str = "unnamed_test",
        module: str = "unknown"
    ) -> BenchmarkResult:
        """Measure performance of a single function call.
        
        Args:
            func: Function to benchmark
            args: Positional arguments
            kwargs: Keyword arguments
            test_name: Name of the test
            module: Module being tested
            
        Returns:
            BenchmarkResult with performance metrics
        """
        if kwargs is None:
            kwargs = {}
        
        # Get input size estimate
        input_size = self._estimate_size(args, kwargs)
        
        # Start monitoring
        process = psutil.Process(os.getpid())
        cpu_before = process.cpu_percent(interval=0.1)
        
        # Memory tracking
        tracemalloc.start()
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Time execution
        start_time = time.perf_counter()
        success = True
        error = None
        result = None
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            success = False
            error = str(e)
        
        end_time = time.perf_counter()
        
        # Stop monitoring
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        cpu_after = process.cpu_percent(interval=0.1)
        
        # Calculate metrics
        execution_time = end_time - start_time
        memory_peak = peak / 1024 / 1024  # MB
        memory_delta = mem_after - mem_before
        cpu_percent = (cpu_before + cpu_after) / 2
        output_size = self._estimate_size(result) if result else 0
        
        return BenchmarkResult(
            test_name=test_name,
            module=module,
            execution_time=execution_time,
            memory_peak=memory_peak,
            memory_delta=memory_delta,
            cpu_percent=cpu_percent,
            input_size=input_size,
            output_size=output_size,
            success=success,
            error=error
        )
    
    def benchmark_script_parser(self, input_sizes: List[int] = None) -> List[BenchmarkResult]:
        """Benchmark script parser with various input sizes.
        
        Args:
            input_sizes: List of input sizes to test
            
        Returns:
            List of benchmark results
        """
        if input_sizes is None:
            input_sizes = [10, 50, 100, 500, 1000]
        
        parser = ScriptParser()
        results = []
        
        for size in input_sizes:
            # Generate test input
            test_input = self._generate_script_input(size)
            
            result = self.measure_performance(
                parser.parse_text,
                args=(test_input,),
                test_name=f"parse_{size}_entries",
                module="script_parser"
            )
            results.append(result)
        
        return results
    
    def benchmark_philosophy_interpreter(self, complexity_levels: List[str] = None) -> List[BenchmarkResult]:
        """Benchmark philosophical interpreter with various complexity levels.
        
        Args:
            complexity_levels: Complexity levels to test
            
        Returns:
            List of benchmark results
        """
        if complexity_levels is None:
            complexity_levels = ["simple", "moderate", "complex"]
        
        interpreter = PhilosophicalInterpreter()
        results = []
        
        for level in complexity_levels:
            # Generate test dialogue
            dialogue = self._generate_philosophical_dialogue(level)
            
            result = self.measure_performance(
                interpreter.interpret,
                args=(dialogue,),
                test_name=f"interpret_{level}",
                module="philosophical_interpreter"
            )
            results.append(result)
        
        return results
    
    def benchmark_emotion_mapper(self, batch_sizes: List[int] = None) -> List[BenchmarkResult]:
        """Benchmark emotion mapper with various batch sizes.
        
        Args:
            batch_sizes: Batch sizes to test
            
        Returns:
            List of benchmark results
        """
        if batch_sizes is None:
            batch_sizes = [1, 10, 50, 100]
        
        mapper = EmotionalMapper()
        results = []
        
        for size in batch_sizes:
            # Generate test entries
            entries = [self._generate_dialogue_entry() for _ in range(size)]
            
            result = self.measure_performance(
                mapper.map_emotions,
                args=(entries,),
                test_name=f"map_{size}_emotions",
                module="emotional_mapper"
            )
            results.append(result)
        
        return results
    
    def benchmark_full_pipeline(self, script_sizes: List[int] = None) -> List[BenchmarkResult]:
        """Benchmark full processing pipeline.
        
        Args:
            script_sizes: Script sizes to test
            
        Returns:
            List of benchmark results
        """
        if script_sizes is None:
            script_sizes = [10, 50, 100]
        
        weaver = SceneWeaver()
        results = []
        
        for size in script_sizes:
            # Generate test script
            script = self._generate_script_input(size)
            
            result = self.measure_performance(
                weaver.process_script,
                args=(script,),
                test_name=f"full_pipeline_{size}",
                module="scene_weaver"
            )
            results.append(result)
        
        return results
    
    def run_stress_test(
        self,
        module: str,
        duration: int = 60,
        concurrent_requests: int = 10
    ) -> Dict[str, Any]:
        """Run stress test on a module.
        
        Args:
            module: Module to stress test
            duration: Test duration in seconds
            concurrent_requests: Number of concurrent requests
            
        Returns:
            Stress test results
        """
        print(f"Running stress test on {module} for {duration}s with {concurrent_requests} concurrent requests...")
        
        # Select appropriate test function
        if module == "script_parser":
            test_func = lambda: ScriptParser().parse_text(self._generate_script_input(100))
        elif module == "philosophical_interpreter":
            test_func = lambda: PhilosophicalInterpreter().interpret(self._generate_philosophical_dialogue("complex"))
        else:
            raise ValueError(f"Unknown module: {module}")
        
        start_time = time.time()
        results = []
        errors = 0
        
        with ProcessPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = []
            
            while time.time() - start_time < duration:
                # Submit new tasks
                for _ in range(concurrent_requests - len(futures)):
                    future = executor.submit(self.measure_performance, test_func, test_name="stress_test", module=module)
                    futures.append(future)
                
                # Collect completed tasks
                completed = []
                for future in as_completed(futures, timeout=0.1):
                    try:
                        result = future.result()
                        results.append(result)
                        if not result.success:
                            errors += 1
                    except Exception:
                        errors += 1
                    completed.append(future)
                
                # Remove completed futures
                for future in completed:
                    futures.remove(future)
        
        # Calculate statistics
        response_times = [r.execution_time for r in results if r.success]
        memory_usage = [r.memory_peak for r in results if r.success]
        
        return {
            "total_requests": len(results),
            "successful_requests": len(results) - errors,
            "error_rate": errors / len(results) if results else 0,
            "avg_response_time": np.mean(response_times) if response_times else 0,
            "p95_response_time": np.percentile(response_times, 95) if response_times else 0,
            "p99_response_time": np.percentile(response_times, 99) if response_times else 0,
            "avg_memory": np.mean(memory_usage) if memory_usage else 0,
            "max_memory": np.max(memory_usage) if memory_usage else 0,
        }
    
    def generate_report(self, suite_name: str = "benchmark_suite") -> BenchmarkSuite:
        """Generate comprehensive benchmark report.
        
        Args:
            suite_name: Name for the benchmark suite
            
        Returns:
            BenchmarkSuite with all results
        """
        # Collect system information
        system_info = {
            "platform": os.uname().sysname,
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total / 1024 / 1024 / 1024,  # GB
            "python_version": sys.version,
        }
        
        # Calculate summary statistics
        if self.results:
            summary = {
                "total_tests": len(self.results),
                "successful_tests": len([r for r in self.results if r.success]),
                "avg_execution_time": np.mean([r.execution_time for r in self.results]),
                "avg_memory_usage": np.mean([r.memory_peak for r in self.results]),
                "total_time": sum(r.execution_time for r in self.results),
            }
        else:
            summary = {}
        
        suite = BenchmarkSuite(
            suite_name=suite_name,
            timestamp=datetime.now(),
            system_info=system_info,
            results=self.results,
            summary=summary
        )
        
        # Save results
        self._save_results(suite)
        
        return suite
    
    def visualize_results(self, suite: BenchmarkSuite):
        """Create visualizations of benchmark results.
        
        Args:
            suite: Benchmark suite to visualize
        """
        # Create output directory for plots
        plot_dir = self.output_dir / "plots"
        plot_dir.mkdir(exist_ok=True)
        
        # 1. Execution time by module
        plt.figure(figsize=(10, 6))
        modules = {}
        for result in suite.results:
            if result.module not in modules:
                modules[result.module] = []
            modules[result.module].append(result.execution_time)
        
        module_names = list(modules.keys())
        module_times = [modules[m] for m in module_names]
        
        plt.boxplot(module_times, labels=module_names)
        plt.ylabel("Execution Time (seconds)")
        plt.title("Performance by Module")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(plot_dir / "execution_time_by_module.png")
        plt.close()
        
        # 2. Memory usage heatmap
        plt.figure(figsize=(12, 8))
        
        # Group by test name and input size
        memory_data = {}
        for result in suite.results:
            key = (result.test_name, result.input_size)
            if key not in memory_data:
                memory_data[key] = []
            memory_data[key].append(result.memory_peak)
        
        # Create matrix for heatmap
        test_names = sorted(set(r.test_name for r in suite.results))
        input_sizes = sorted(set(r.input_size for r in suite.results))
        
        if test_names and input_sizes:
            matrix = np.zeros((len(test_names), len(input_sizes)))
            for i, test in enumerate(test_names):
                for j, size in enumerate(input_sizes):
                    key = (test, size)
                    if key in memory_data:
                        matrix[i, j] = np.mean(memory_data[key])
            
            sns.heatmap(matrix, xticklabels=input_sizes, yticklabels=test_names,
                       cmap="YlOrRd", annot=True, fmt=".1f")
            plt.xlabel("Input Size")
            plt.ylabel("Test Name")
            plt.title("Memory Usage Heatmap (MB)")
            plt.tight_layout()
            plt.savefig(plot_dir / "memory_usage_heatmap.png")
            plt.close()
        
        # 3. Performance scaling plot
        plt.figure(figsize=(10, 6))
        
        # Group by module and input size
        scaling_data = {}
        for result in suite.results:
            if result.module not in scaling_data:
                scaling_data[result.module] = {"sizes": [], "times": []}
            scaling_data[result.module]["sizes"].append(result.input_size)
            scaling_data[result.module]["times"].append(result.execution_time)
        
        for module, data in scaling_data.items():
            if data["sizes"]:
                # Sort by size
                sorted_indices = np.argsort(data["sizes"])
                sizes = np.array(data["sizes"])[sorted_indices]
                times = np.array(data["times"])[sorted_indices]
                plt.plot(sizes, times, marker='o', label=module)
        
        plt.xlabel("Input Size")
        plt.ylabel("Execution Time (seconds)")
        plt.title("Performance Scaling")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(plot_dir / "performance_scaling.png")
        plt.close()
    
    def _estimate_size(self, *args) -> int:
        """Estimate size of objects in bytes."""
        size = 0
        for arg in args:
            if isinstance(arg, str):
                size += len(arg)
            elif isinstance(arg, (list, tuple)):
                size += sum(self._estimate_size(item) for item in arg)
            elif isinstance(arg, dict):
                size += sum(self._estimate_size(k, v) for k, v in arg.items())
            else:
                size += 100  # Default estimate
        return size
    
    def _generate_script_input(self, num_entries: int) -> str:
        """Generate test script input."""
        entries = []
        for i in range(num_entries):
            speaker = "Evan" if i % 2 == 0 else "Monday"
            dialogue = f"This is test dialogue entry {i} discussing philosophical concepts."
            entries.append(f"[{i:04d}] {speaker}: <<{dialogue}>>")
        return "\n".join(entries)
    
    def _generate_philosophical_dialogue(self, complexity: str) -> str:
        """Generate philosophical dialogue of varying complexity."""
        if complexity == "simple":
            return "What is the meaning of life?"
        elif complexity == "moderate":
            return "If consciousness is an emergent property of complex neural networks, does that mean artificial intelligence could achieve true self-awareness?"
        else:  # complex
            return """The paradox of identity through time challenges our intuitions: if every atom in your body is replaced over seven years, 
            are you still the same person? This connects to broader questions about consciousness, continuity, and the nature of self. 
            Consider the implications for digital consciousness transfer and the persistence of identity across substrates."""
    
    def _generate_dialogue_entry(self) -> Dict[str, Any]:
        """Generate a test dialogue entry."""
        return {
            "id": "0001",
            "speaker": "TestSpeaker",
            "dialogue": "This is a test dialogue with emotional content.",
            "context": {"scene": "test", "mood": "contemplative"}
        }
    
    def _save_results(self, suite: BenchmarkSuite):
        """Save benchmark results to file."""
        timestamp = suite.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{suite.suite_name}_{timestamp}.json"
        
        # Convert to serializable format
        data = {
            "suite_name": suite.suite_name,
            "timestamp": suite.timestamp.isoformat(),
            "system_info": suite.system_info,
            "results": [asdict(r) for r in suite.results],
            "summary": suite.summary
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Results saved to {filename}")


@click.command()
@click.option('--modules', '-m', multiple=True, default=['all'], 
              help='Modules to benchmark (all, parser, philosophy, emotion, pipeline)')
@click.option('--stress-test', is_flag=True, help='Run stress tests')
@click.option('--visualize', is_flag=True, help='Generate visualization plots')
@click.option('--output-dir', '-o', default='benchmark_results', help='Output directory')
def main(modules, stress_test, visualize, output_dir):
    """Run performance benchmarks for Metaphysical Scene Weaver."""
    benchmark = PerformanceBenchmark(Path(output_dir))
    
    print("Starting performance benchmarks...")
    
    # Run selected benchmarks
    if 'all' in modules or 'parser' in modules:
        print("\nBenchmarking Script Parser...")
        benchmark.results.extend(benchmark.benchmark_script_parser())
    
    if 'all' in modules or 'philosophy' in modules:
        print("\nBenchmarking Philosophical Interpreter...")
        benchmark.results.extend(benchmark.benchmark_philosophy_interpreter())
    
    if 'all' in modules or 'emotion' in modules:
        print("\nBenchmarking Emotional Mapper...")
        benchmark.results.extend(benchmark.benchmark_emotion_mapper())
    
    if 'all' in modules or 'pipeline' in modules:
        print("\nBenchmarking Full Pipeline...")
        benchmark.results.extend(benchmark.benchmark_full_pipeline())
    
    # Run stress tests if requested
    if stress_test:
        print("\nRunning stress tests...")
        stress_results = {}
        for module in ['script_parser', 'philosophical_interpreter']:
            if 'all' in modules or module.replace('_', '') in modules:
                stress_results[module] = benchmark.run_stress_test(module)
        
        print("\nStress Test Results:")
        for module, results in stress_results.items():
            print(f"\n{module}:")
            for key, value in results.items():
                print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    # Generate report
    suite = benchmark.generate_report()
    
    print(f"\nBenchmark Summary:")
    print(f"Total tests: {suite.summary.get('total_tests', 0)}")
    print(f"Successful: {suite.summary.get('successful_tests', 0)}")
    print(f"Average execution time: {suite.summary.get('avg_execution_time', 0):.4f}s")
    print(f"Average memory usage: {suite.summary.get('avg_memory_usage', 0):.2f}MB")
    
    # Generate visualizations if requested
    if visualize:
        print("\nGenerating visualizations...")
        benchmark.visualize_results(suite)
        print(f"Plots saved to {benchmark.output_dir / 'plots'}")


if __name__ == "__main__":
    main()