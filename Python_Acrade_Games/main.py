"""
Python Arcade — entry point.

Responsibilities:
  1. Bootstrap the ScoreManager (loads scores.json)
  2. Show the menu loop
  3. Dispatch the user's choice to the right Game subclass
  4. Persist any new high scores
"""
from GAMES.blackjack import Blackjack
from GAMES.hangman import Hangman
from GAMES.higher_lower import HigherLower
from GAMES.number_guess import NumberGuess
from scores import ScoreManager

# Registry: menu key -> Game class.
# Adding a new game = one line here + one new module. No other changes needed.
GAMES = {
    "1": Blackjack,
    "2": Hangman,
    "3": HigherLower,
    "4": NumberGuess,
}


def print_menu(scores: ScoreManager, player: str) -> None:
    """Render the main menu, showing the player's best score per game."""
    print("\n" + "=" * 50)
    print(f"  🎮  PYTHON ARCADE  —  Player: {player}")
    print("=" * 50)
    for key, cls in GAMES.items():
        best = scores.high_score(cls.name, player)
        print(f"  {key}. {cls.name:<18} (best: {best})")
    print("  5. View leaderboards")
    print("  6. Switch player")
    print("  0. Quit")


def show_leaderboards(scores: ScoreManager) -> None:
    """Print the top 5 scores for every registered game."""
    for cls in GAMES.values():
        print(f"\n  ── {cls.name} ──")
        board = scores.leaderboard(cls.name)
        if not board:
            print("    (no scores yet)")
        for name, score in board[:5]:
            print(f"    {name:<15} {score}")


def main() -> None:
    scores = ScoreManager()                        # loads scores.json on init
    player = input("Enter your name: ").strip() or "Guest"

    while True:                                    # main event loop
        print_menu(scores, player)
        choice = input("\nChoose: ").strip()

        # --- Meta commands ---
        if choice == "0":
            scores.save()
            print("Thanks for playing! 👋")
            return

        if choice == "5":
            show_leaderboards(scores)
            continue

        if choice == "6":
            player = input("New player name: ").strip() or "Guest"
            continue

        # --- Game dispatch ---
        game_cls = GAMES.get(choice)
        if game_cls is None:
            print("  Invalid choice.")
            continue

        game = game_cls(player)                    # polymorphic instantiation
        final_score = game.play()                  # same call works for ALL games

        # --- Persist result ---
        if final_score > 0:
            if scores.record(game.name, player, final_score):
                print(f"  🏆 New high score: {final_score}!")
            else:
                print(f"  Session score: {final_score}")


if __name__ == "__main__":
    main()
