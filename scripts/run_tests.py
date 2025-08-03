#!/usr/bin/env python3
"""Test runner script for Metaphysical Scene Weaver.

This script provides a convenient interface for running different test suites
with appropriate configurations.
"""

import click
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime


def run_command(cmd: list, verbose: bool = True) -> tuple[int, str, str]:
    """Run a command and capture output."""
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    return result.returncode, result.stdout, result.stderr


def generate_test_report(results: dict, output_path: Path):
    """Generate a test report in JSON format."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_suites": len(results),
            "passed_suites": sum(1 for r in results.values() if r["passed"]),
            "total_time": sum(r.get("duration", 0) for r in results.values())
        },
        "suites": results
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nTest report saved to: {output_path}")


@click.command()
@click.option('--suite', '-s', 
              type=click.Choice(['all', 'unit', 'integration', 'e2e', 'edge', 'performance']),
              default='all', help='Test suite to run')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--coverage', '-c', is_flag=True, help='Generate coverage report')
@click.option('--failfast', '-f', is_flag=True, help='Stop on first failure')
@click.option('--parallel', '-p', is_flag=True, help='Run tests in parallel')
@click.option('--benchmark', '-b', is_flag=True, help='Run performance benchmarks')
@click.option('--report', '-r', help='Path to save test report')
@click.option('--markers', '-m', help='Additional pytest markers')
def main(suite, verbose, coverage, failfast, parallel, benchmark, report, markers):
    """Run Metaphysical Scene Weaver test suites."""
    print("🧪 Metaphysical Scene Weaver Test Runner")
    print("=" * 50)
    
    # Base pytest command
    cmd = ["pytest"]
    
    # Add verbosity
    if verbose:
        cmd.append("-vv")
    else:
        cmd.append("-v")
    
    # Add coverage
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    
    # Add failfast
    if failfast:
        cmd.append("-x")
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Select test suite
    suite_markers = {
        'unit': 'unit',
        'integration': 'integration',
        'e2e': 'e2e',
        'edge': 'edge_case',
        'performance': 'performance'
    }
    
    if suite != 'all':
        marker = suite_markers.get(suite)
        if marker:
            cmd.extend(["-m", marker])
    
    # Add custom markers
    if markers:
        if "-m" in cmd:
            # Combine with existing marker
            idx = cmd.index("-m")
            cmd[idx + 1] = f"({cmd[idx + 1]}) and ({markers})"
        else:
            cmd.extend(["-m", markers])
    
    # Run tests
    results = {}
    
    if suite == 'all':
        # Run each suite separately for better reporting
        for suite_name, marker in suite_markers.items():
            print(f"\n📋 Running {suite_name} tests...")
            suite_cmd = cmd.copy()
            suite_cmd.extend(["-m", marker])
            
            start_time = datetime.now()
            returncode, stdout, stderr = run_command(suite_cmd, verbose)
            duration = (datetime.now() - start_time).total_seconds()
            
            results[suite_name] = {
                "passed": returncode == 0,
                "duration": duration,
                "return_code": returncode
            }
            
            if returncode != 0 and failfast:
                print(f"\n❌ {suite_name} tests failed. Stopping due to --failfast")
                break
    else:
        start_time = datetime.now()
        returncode, stdout, stderr = run_command(cmd, verbose)
        duration = (datetime.now() - start_time).total_seconds()
        
        results[suite] = {
            "passed": returncode == 0,
            "duration": duration,
            "return_code": returncode
        }
    
    # Run benchmarks if requested
    if benchmark:
        print("\n📊 Running performance benchmarks...")
        bench_cmd = ["python", "scripts/benchmark.py", "-m", "all"]
        if verbose:
            bench_cmd.append("--visualize")
        
        returncode, stdout, stderr = run_command(bench_cmd, verbose)
        results["benchmarks"] = {
            "passed": returncode == 0,
            "return_code": returncode
        }
    
    # Generate report if requested
    if report:
        report_path = Path(report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        generate_test_report(results, report_path)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    total_passed = sum(1 for r in results.values() if r["passed"])
    total_suites = len(results)
    
    for suite_name, result in results.items():
        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        duration = result.get("duration", 0)
        print(f"{suite_name:15} {status:12} ({duration:.2f}s)")
    
    print("-" * 50)
    print(f"Total: {total_passed}/{total_suites} suites passed")
    
    # Generate coverage report URL if coverage was enabled
    if coverage and total_passed > 0:
        print(f"\n📈 Coverage report: file://{Path.cwd()}/htmlcov/index.html")
    
    # Exit with appropriate code
    sys.exit(0 if total_passed == total_suites else 1)


if __name__ == "__main__":
    main()