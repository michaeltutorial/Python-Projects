# 🎯 QuizMaster Pro

A desktop quiz application built with Python and Tkinter. Load questions from
JSON, pick a category and difficulty, beat the timer, and track your high scores.

![QuizMaster Pro screenshot](screenshot.png)

---

## ✨ Features

- 📚 **Question bank loaded from JSON** — swap topics without touching code
- 🗂️ **Multiple categories & difficulty levels**
- ⏱️ **Per-question countdown timer** (15 seconds)
- 🏆 **High scores tracked per category + difficulty**
- 💾 **Score history persisted to disk** (`scores.json`)
- 🎨 **Clean, screen-based GUI** (start → quiz → results)
- 🧱 **Clean OOP architecture** — data, persistence, and UI are separate classes

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Tkinter** (standard library GUI)
- **JSON** for question bank and score storage

No third-party dependencies required.

---

## 🚀 Installation & Running

```bash
# 1. Clone the repo
git clone https://github.com/your-username/quiz-app.git
cd quiz-app

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Run the app
python main.py
