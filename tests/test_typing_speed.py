import unittest
import subprocess
import os
import sys

class TestTypingSpeed(unittest.TestCase):
    def setUp(self):
        self.script_path = os.path.join("utilities", "Typing-Speed-Tester", "Typing-Speed-Tester.py")

    def run_script_with_input(self, user_input):
        process = subprocess.Popen(
            [sys.executable, self.script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=user_input)
        return stdout, stderr

    def test_typing_speed_script_runs(self):
        # The script asks to press Enter to start, then waits for the typed text.
        # We provide a newline to start, and then a dummy text to finish.
        dummy_input = "\nThis is a test run.\n"
        stdout, _ = self.run_script_with_input(dummy_input)
        
        self.assertIn("WELCOME TO TYPING SPEED TESTER", stdout)
        self.assertIn("TEST COMPLETED", stdout)
        self.assertIn("Time Taken", stdout)
        self.assertIn("Typing Speed", stdout)
        self.assertIn("Accuracy", stdout)

if __name__ == "__main__":
    unittest.main()
