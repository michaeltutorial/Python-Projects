import random

try:
    from .base_game import Game
except ImportError:
    from base_game import Game


class NumberGuess(Game):
    name = "Number Guessing"

    def play(self) -> int:
        self._print_header("I'm thinking of a number between 1 and 100")
        target = random.randint(1, 100)
        tries = 0

        while True:
            raw = self._prompt("Your guess ('q' to quit)")
            if raw.lower() == "q":
                break
            if not raw.isdigit():
                print("  Enter a whole number.")
                continue

            guess = int(raw)
            tries += 1

            if guess < target:
                print("  ⬆️  Higher!")
            elif guess > target:
                print("  ⬇️  Lower!")
            else:
                points = max(10, 110 - tries * 10)
                self.score += points
                self.rounds_played = tries
                print(f"  🎯 Got it in {tries} tries! +{points} points")
                break

        return self.score