from abc import ABC, abstractmethod


class Game(ABC):
    """Abstract base for all arcade games."""

    name: str = "Game"

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.score = 0
        self.rounds_played = 0

    @abstractmethod
    def play(self) -> int:
        """Run one session of the game. Returns the final score."""
        ...

    def _prompt(self, message: str) -> str:
        return input(f"\n{message} > ").strip()

    def _print_header(self, subtitle: str = ""):
        print("\n" + "=" * 50)
        print(f"  {self.name.upper()}" + (f" — {subtitle}" if subtitle else ""))
        print("=" * 50)

    def __repr__(self):
        return f"<{self.__class__.__name__} player={self.player_name!r} score={self.score}>"
