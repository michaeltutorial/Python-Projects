import random

try:
    from .base_game import Game
except ImportError:
    from base_game import Game

WORDS = ["python", "arcade", "refactor", "polymorphism", "decorator", "iterator"]


class Hangman(Game):
    name = "Hangman"

    def play(self) -> int:
        self._print_header("Guess the word — 6 wrong guesses allowed")
        word = random.choice(WORDS)
        guessed: set[str] = set()
        wrong = 0

        while wrong < 6:
            display = " ".join(c if c in guessed else "_" for c in word)
            print(f"\n  {display}   (wrong: {wrong}/6)")

            if all(c in guessed for c in word):
                points = 50 - wrong * 5
                self.score += points
                print(f"  🎉 Solved! +{points} points")
                return self.score

            letter = self._prompt("Guess a letter").lower()
            if len(letter) != 1 or not letter.isalpha():
                print("  Single letter only.")
                continue
            if letter in guessed:
                print("  Already guessed.")
                continue

            guessed.add(letter)
            if letter not in word:
                wrong += 1

        print(f"\n  💀 Out of guesses. Word was: {word}")
        return self.score