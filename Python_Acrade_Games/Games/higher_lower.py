import random

try:
    from .base_game import Game
except ImportError:
    from base_game import Game


class HigherLower(Game):
    name = "Higher / Lower"

    def play(self) -> int:
        self._print_header("Guess if the next card is higher or lower")
        current = random.randint(1, 100)
        streak = 0

        while True:
            print(f"\n  Current number: {current}")
            guess = self._prompt("Higher or Lower? (h/l, 'q' to quit)").lower()
            if guess == "q":
                break
            if guess not in ("h", "l"):
                print("  Please enter 'h' or 'l'.")
                continue

            nxt = random.randint(1, 100)
            correct = (nxt > current and guess == "h") or (nxt < current and guess == "l")
            print(f"  Next number: {nxt}")

            if correct:
                streak += 1
                self.score += 10
                print(f"  ✅ Correct! Streak: {streak} | Score: {self.score}")
            else:
                print(f"  ❌ Wrong. Final streak: {streak}")
                break

            current = nxt

        self.rounds_played = streak
        return self.score