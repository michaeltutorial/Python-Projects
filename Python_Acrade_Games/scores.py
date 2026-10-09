import json
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "scores.json"


class ScoreManager:
    """Loads/saves high scores per game per player."""

    def __init__(self, path: Path = SCORES_FILE):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2))

    def record(self, game: str, player: str, score: int) -> bool:
        """Store score if it's a new high score. Returns True if beaten."""
        player_scores = self.data.setdefault(game, {})
        best = player_scores.get(player, 0)
        if score > best:
            player_scores[player] = score
            self.save()
            return True
        return False

    def high_score(self, game: str, player: str) -> int:
        return self.data.get(game, {}).get(player, 0)

    def leaderboard(self, game: str):
        entries = self.data.get(game, {})
        return sorted(entries.items(), key=lambda kv: kv[1], reverse=True)