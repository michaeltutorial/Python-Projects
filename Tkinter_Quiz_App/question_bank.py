import json
import random
from pathlib import Path


class QuestionBank:
    """Loads questions from a JSON file and serves them by category/difficulty."""

    def __init__(self, path: str = "questions.json"):
        base_dir = Path(__file__).resolve().parent
        self.path = Path(path)
        if not self.path.is_absolute():
            self.path = base_dir / self.path
        self.data = {}
        self.load()

    def load(self):
        if not self.path.exists() or self.path.stat().st_size == 0:
            self.data = {}
            return

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, OSError):
            self.data = {}

    def categories(self):
        return list(self.data.keys())

    def difficulties(self, category: str):
        return list(self.data.get(category, {}).keys())

    def get_questions(self, category: str, difficulty: str, shuffle=True):
        questions = list(self.data.get(category, {}).get(difficulty, []))
        if shuffle:
            random.shuffle(questions)
        return questions