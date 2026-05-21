import unittest
import importlib.util
import os
import sys

class TestNumberGuessing(unittest.TestCase):
    def setUp(self):
        # Load the module dynamically since it has hyphens in the name
        module_name = "number_guessing"
        file_path = os.path.join("games", "Number-Guessing-Game", "Number-Guessing-Game.py")
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = self.module
        spec.loader.exec_module(self.module)

    def test_play_round_with_guesses_win(self):
        # Test winning exactly on the last attempt
        won, attempts = self.module.play_round_with_guesses([10, 20, 50], number=50, max_attempts=3)
        self.assertTrue(won)
        self.assertEqual(attempts, 3)

    def test_play_round_with_guesses_lose(self):
        # Test running out of attempts
        won, attempts = self.module.play_round_with_guesses([10, 20, 30], number=50, max_attempts=3)
        self.assertFalse(won)
        self.assertEqual(attempts, 3)

    def test_play_round_with_guesses_win_early(self):
        # Test winning before max attempts are reached
        won, attempts = self.module.play_round_with_guesses([50, 60, 70], number=50, max_attempts=5)
        self.assertTrue(won)
        self.assertEqual(attempts, 1)

if __name__ == "__main__":
    unittest.main()
