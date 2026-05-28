import unittest
import subprocess
import os

class TestArmstrongNumber(unittest.TestCase):
    def setUp(self):
        self.script_path = os.path.join(
            os.path.dirname(__file__), "..",
            "math", "Armstrong-Number", "Armstrong-Number.py"
        )
        self.script_path = os.path.abspath(self.script_path)

    def run_script(self, inputs):
        # Join inputs with newline and add 'n' at the end to quit the program
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

    def test_armstrong_number(self):
        output = self.run_script(["153"])
        self.assertIn("153 is an Armstrong Number!", output)

    def test_non_armstrong_number(self):
        output = self.run_script(["154"])
        self.assertIn("154 is NOT an Armstrong Number.", output)

    def test_negative_number(self):
        # Entering -5 first (fails), then 153 to exit cleanly
        output = self.run_script(["-5", "153"])
        self.assertIn("Please enter a positive number!", output)
        self.assertIn("153 is an Armstrong Number!", output)

    def test_invalid_input(self):
        # Entering "abc" (fails), then 153 to exit cleanly
        output = self.run_script(["abc", "153"])
        self.assertIn("Oops! That doesn't look like a valid integer.", output)
        self.assertIn("153 is an Armstrong Number!", output)

if __name__ == '__main__':
    unittest.main()
