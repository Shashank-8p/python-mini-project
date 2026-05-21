import unittest
import subprocess
import os
import sys

class TestArmstrongNumber(unittest.TestCase):
    def setUp(self):
        # Path to the Armstrong-Number.py script
        self.script_path = os.path.join("math", "Armstrong-Number", "Armstrong-Number.py")

    def run_script_with_input(self, user_input):
        # Run the script as a subprocess and provide input via stdin
        process = subprocess.Popen(
            [sys.executable, self.script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=user_input)
        return stdout, stderr

    def test_valid_armstrong_number(self):
        stdout, _ = self.run_script_with_input("153\n")
        self.assertIn("153 is an Armstrong Number!", stdout)

    def test_invalid_armstrong_number(self):
        stdout, _ = self.run_script_with_input("154\n")
        self.assertIn("154 is NOT an Armstrong Number.", stdout)

    def test_invalid_input_handling(self):
        # The script asks again if input is invalid, so we send invalid then valid
        stdout, _ = self.run_script_with_input("abc\n153\n")
        self.assertIn("That doesn't look like a valid number", stdout)
        self.assertIn("153 is an Armstrong Number!", stdout)
        
    def test_negative_input(self):
        stdout, _ = self.run_script_with_input("-5\n153\n")
        self.assertIn("Please enter a positive number!", stdout)

if __name__ == "__main__":
    unittest.main()
