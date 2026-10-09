# 🎮 Python Arcade — A Portfolio of Games

A polished, object-oriented arcade app featuring **four classic games** behind a single menu,
with persistent high scores saved to disk. Built to demonstrate clean architecture, the
refactor from procedural to OOP code, and idiomatic Python.




---

## Table of Contents

- [Features](#-features)
- [Games](#-games)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [How It Works](#-how-it-works)
- [Scoring](#-scoring)
- [Adding a New Game](#-adding-a-new-game)
- [The Refactor Story](#-the-refactor-story)
- [Skills Demonstrated](#-skills-demonstrated)
- [Testing](#-testing-optional)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [License](#-license)

---

## ✨ Features

- **Four complete games** — Blackjack, Hangman, Higher/Lower, and Number Guessing
- **Single unified menu** — pick a game, play, return to menu
- **Persistent high scores** — saved to `scores.json`, survive between sessions
- **Multi-player support** — switch players without restarting the app
- **Leaderboards** — top 5 scores per game
- **Zero dependencies** — pure Python 3.10+ standard library
- **Extensible** — adding a new game takes ~2 lines of glue code
- **Clean OOP design** — abstract base class, polymorphic dispatch, single-responsibility classes

---

## 🎲 Games

### Blackjack
Classic 21 against a dealer. Start with 100 chips and bet each round.
Dealer hits on soft 16, stands on hard 17. Blackjack pays even money (no doubling in v1).

- **Win condition:** Get closer to 21 than the dealer without going over
- **Scoring:** Peak chip count across the session
- **Controls:** `h` to hit, `s` to stand

### Hangman
Guess a hidden word one letter at a time. Six wrong guesses and you're out.

- **Word list:** Python-themed terms (`python`, `polymorphism`, `decorator`, ...)
- **Scoring:** `50 - (wrong_guesses × 5)` points for a win, 0 for a loss
- **Controls:** Enter a single letter each turn

### Higher / Lower
A random number appears — guess whether the next one will be higher or lower.

- **Range:** 1–100
- **Scoring:** +10 points per correct guess; streak ends on first wrong answer
- **Controls:** `h` for higher, `l` for lower

### Number Guessing
The computer picks a number between 1 and 100. Find it with feedback.

- **Feedback:** "Higher!" or "Lower!" after each guess
- **Scoring:** `max(10, 110 - (tries × 10))` — fewer tries, more points
- **Controls:** Enter a number each turn

---

## 🚀 Quick Start

### Requirements

- **Python 3.10+** (uses `set[str]` and `int | None` syntax)
- No external packages

### Run it

```bash
git clone https://github.com/yourname/python-arcade.git
cd python-arcade
python main.py





## EXAMPLE SESSION
Enter your name: Alex

==================================================
  🎮  PYTHON ARCADE  —  Player: Alex
==================================================
  1. Blackjack          (best: 0)
  2. Hangman            (best: 0)
  3. Higher / Lower     (best: 0)
  4. Number Guessing    (best: 0)
  5. View leaderboards
  6. Switch player
  0. Quit

Choose: 3

==================================================
  HIGHER / LOWER — Guess if the next card is higher or lower
==================================================

  Current number: 47

Higher or Lower? (h/l, 'q' to quit) > h
  Next number: 82
  ✅ Correct! Streak: 1 | Score: 10

  Current number: 82

Higher or Lower? (h/l, 'q' to quit) > l
  Next number: 61
  ✅ Correct! Streak: 2 | Score: 20
  ...
  🏆 New high score: 60!
