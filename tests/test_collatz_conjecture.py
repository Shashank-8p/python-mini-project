import unittest
import subprocess
import os

class TestCollatzConjecture(unittest.TestCase):
    def setUp(self):
        # Resolve the absolute path to the script
        self.script_path = os.path.join(
            os.path.dirname(__file__), "..",
            "math", "Collatz-Conjecture", "Collatz-Conjecture.py"
        )
        self.script_path = os.path.abspath(self.script_path)

    def run_script(self, inputs):
        """Feeding simulated user inputs to the script."""
        input_data = "\n".join(inputs + ["n"]) + "\n"
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        result = subprocess.run(
            ["python", self.script_path],
            input=input_data,
            text=True,
            capture_output=True,
            encoding='utf-8',
            env=env
        )
        return result.stdout

    def test_standard_flow(self):
        """Test a simple number sequence (4 -> 2 -> 1)."""
        output = self.run_script(["4", "n"])
        self.assertIn("Starting with: 4", output)
        self.assertIn("Total steps: 2", output)
        self.assertIn("✅ SEQUENCE COMPLETE!", output)

    def test_detailed_explanation(self):
        """Test the 'y' prompt for step-by-step details."""
        output = self.run_script(["3", "y", "n"])
        self.assertIn("Detailed Steps:", output)
        self.assertIn("3 is odd", output)
        self.assertIn("= 10", output)

    def test_mathematical_power_of_two(self):
        """Test a power of two (16), which should go straight to 1."""
        # 16 -> 8 -> 4 -> 2 -> 1 (4 steps)
        output = self.run_script(["16", "n", "n"])
        self.assertIn("Total steps: 4", output)
        self.assertIn("Highest number reached: 16", output)


    def test_input_case_insensitivity(self):
        """Ensure 'Y' and 'YES' work just as well as 'y'."""
        output = self.run_script(["3", "YES", "Y", "2", "N", "N"])
        self.assertIn("Detailed Steps:", output) # Proves YES worked
        self.assertIn("Starting with: 2", output) # Proves Y worked for 'again'

    def test_recovery_from_multiple_bad_inputs(self):
        """Test if the script can handle 3 errors in a row and still work."""
        output = self.run_script(["abc", "-10", "0", "5", "n", "n"])
        self.assertIn("❌ Please enter a valid number!", output)
        self.assertIn("❌ Please enter a positive integer!", output)
        self.assertIn("Starting with: 5", output) # Proves it eventually succeeded
    
    def test_complex_sequence_27(self):
        """Test number 27, known for its long path (111 steps)."""
        output = self.run_script(["27", "n", "n"])
        self.assertIn("Total steps: 111", output)
        self.assertIn("Highest number reached: 9232", output)

    def test_cache_logic_via_loop(self):
        """Run the script twice to verify the loop and goodbye message work."""
        # 4 (no details, yes again), then 2 (no details, no again)
        output = self.run_script(["4", "n", "y", "2", "n"])
        self.assertIn("Starting with: 4", output)
        self.assertIn("Starting with: 2", output)
        self.assertIn("Goodbye!", output)

    def test_invalid_string_input(self):
        """Ensure script handles non-integers without crashing."""
        output = self.run_script(["abc", "1", "n"])
        self.assertIn("❌ Please enter a valid number!", output)

    def test_zero_input_validation(self):
        """Ensure script rejects zero or negative integers."""
        output = self.run_script(["0", "1", "n"])
        self.assertIn("❌ Please enter a positive integer!", output)

    def test_large_input_guardrail(self):
        """Test the MAX_INPUT (10^12) constraint."""
        large_val = str(10**12 + 1)
        output = self.run_script([large_val, "1", "n"])
        self.assertIn("⚠️ Input too large!", output)

if __name__ == '__main__':
    unittest.main()