"""
Results Runner Script
---------------------
Executes the unit tests and main agent program, redirecting stdout/stderr to capture
real execution output into `src/output.txt`.

Note on LLM Generation:
-----------------------
Code generated with assistance from LLM, verified for automated artifact generation.
"""

import sys
import io
import unittest
from pathlib import Path

# Add current directory to sys.path
src_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(src_dir))

from warehouse_agent import main as run_agent_demo
from test_agent import TestWarehouseAgent


def run_all_and_save():
    output_path = src_dir / 'output.txt'
    output_buffer = io.StringIO()

    # Tee output to both terminal and string buffer
    class TeeWriter:
        def __init__(self, *writers):
            self.writers = writers

        def write(self, text):
            for w in self.writers:
                w.write(text)

        def flush(self):
            for w in self.writers:
                w.flush()

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    tee_stdout = TeeWriter(original_stdout, output_buffer)
    tee_stderr = TeeWriter(original_stderr, output_buffer)

    sys.stdout = tee_stdout
    sys.stderr = tee_stderr

    try:
        print("=" * 70)
        print("               LAB 1: GOAL-BASED AGENT EXECUTION LOG")
        print("=" * 70)
        print("\n--- STEP 1: Running Unit Test Suite ---")
        
        suite = unittest.TestLoader().loadTestsFromTestCase(TestWarehouseAgent)
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        test_result = runner.run(suite)

        print("\n--- STEP 2: Running Main Warehouse Agent Demo ---")
        run_agent_demo()

        print("\n--- SUMMARY ---")
        print(f"Tests Run: {test_result.testsRun}")
        print(f"Errors: {len(test_result.errors)}")
        print(f"Failures: {len(test_result.failures)}")
        print(f"Overall Status: {'PASSED' if test_result.wasSuccessful() else 'FAILED'}")
        print("=" * 70)

    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    # Write captured output buffer to src/output.txt
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_buffer.getvalue())

    print(f"\n[+] Real execution output successfully saved to: {output_path}")


if __name__ == "__main__":
    run_all_and_save()
