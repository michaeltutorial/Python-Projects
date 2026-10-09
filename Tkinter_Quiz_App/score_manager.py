import json
from datetime import datetime
from pathlib import Path


class ScoreManager:
    """Tracks high scores and per-category progress in a JSON file."""

    def __init__(self, path: str = "score.json"):
        base_dir = Path(__file__).resolve().parent
        self.path = Path(path)
        if not self.path.is_absolute():
            self.path = base_dir / self.path
        self.data = {"high_scores": {}, "history": []}
        self.load()

    def load(self):
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass  # start fresh if file is corrupted

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def record(self, category: str, difficulty: str, score: int, total: int):
        key = f"{category} | {difficulty}"
        best = self.data["high_scores"].get(key, 0)
        is_high = score > best
        if is_high:
            self.data["high_scores"][key] = score

        self.data["history"].append({
            "category": category,
            "difficulty": difficulty,
            "score": score,
            "total": total,
            "when": datetime.now().isoformat(timespec="seconds"),
        })
        self.save()
        return is_high

    def high_score(self, category: str, difficulty: str) -> int:
        return self.data["high_scores"].get(f"{category} | {difficulty}", 0)

    def best_overall(self) -> int:
        return max(self.data["high_scores"].values(), default=0)