import tkinter as tk
from tkinter import ttk, messagebox

from question_bank import QuestionBank
from score_manager import ScoreManager


QUESTION_TIME = 15  # seconds per question


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QuizMaster Pro")
        self.geometry("640x460")
        self.resizable(False, False)

        self.bank = QuestionBank()
        self.scores = ScoreManager()

        # state
        self.questions = []
        self.q_index = 0
        self.score = 0
        self.time_left = QUESTION_TIME
        self.timer_id = None
        self.current_answer = None
        self.selected_category = None
        self.selected_difficulty = None

        self._build_start_screen()

    # ---------- Screens ----------
    def _clear(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        for w in self.winfo_children():
            w.destroy()

    def _build_start_screen(self):
        self._clear()
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="🎯 QuizMaster Pro",
                  font=("Segoe UI", 24, "bold")).pack(pady=(0, 20))

        ttk.Label(frame, text="Category:").pack(anchor="w")
        self.category_var = tk.StringVar(value=self.bank.categories()[0])
        cat_box = ttk.Combobox(frame, textvariable=self.category_var,
                               values=self.bank.categories(), state="readonly")
        cat_box.pack(fill="x", pady=(0, 10))
        cat_box.bind("<<ComboboxSelected>>", self._update_difficulties)

        ttk.Label(frame, text="Difficulty:").pack(anchor="w")
        self.difficulty_var = tk.StringVar()
        self.diff_box = ttk.Combobox(frame, textvariable=self.difficulty_var,
                                     state="readonly")
        self.diff_box.pack(fill="x", pady=(0, 20))
        self._update_difficulties()

        ttk.Button(frame, text="Start Quiz",
                   command=self._start_quiz).pack(fill="x", pady=5)
        ttk.Button(frame, text="View High Scores",
                   command=self._show_scores).pack(fill="x", pady=5)

        best = self.scores.best_overall()
        ttk.Label(frame, text=f"Best score overall: {best}",
                  foreground="gray").pack(pady=(20, 0))

    def _update_difficulties(self, event=None):
        diffs = self.bank.difficulties(self.category_var.get())
        self.diff_box["values"] = diffs
        if diffs:
            self.difficulty_var.set(diffs[0])

    def _start_quiz(self):
        cat = self.category_var.get()
        diff = self.difficulty_var.get()
        self.questions = self.bank.get_questions(cat, diff)
        if not self.questions:
            messagebox.showwarning("No questions",
                                   "No questions available for that selection.")
            return
        self.selected_category = cat
        self.selected_difficulty = diff
        self.q_index = 0
        self.score = 0
        self._build_quiz_screen()
        self._load_question()

    # ---------- Quiz Screen ----------
    def _build_quiz_screen(self):
        self._clear()

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        self.progress_lbl = ttk.Label(top, text="", font=("Segoe UI", 10))
        self.progress_lbl.pack(side="left")

        self.score_lbl = ttk.Label(top, text="Score: 0",
                                   font=("Segoe UI", 10, "bold"))
        self.score_lbl.pack(side="right")

        self.timer_lbl = ttk.Label(self, text="", font=("Segoe UI", 14, "bold"),
                                   foreground="darkred")
        self.timer_lbl.pack(pady=(0, 5))

        self.question_lbl = ttk.Label(self, text="", wraplength=580,
                                      font=("Segoe UI", 14))
        self.question_lbl.pack(pady=20, padx=20)

        self.option_buttons = []
        for i in range(4):
            btn = ttk.Button(self, text="", width=60,
                             command=lambda i=i: self._select_option(i))
            btn.pack(pady=4)
            self.option_buttons.append(btn)

        nav = ttk.Frame(self, padding=10)
        nav.pack(fill="x", side="bottom")
        ttk.Button(nav, text="Quit", command=self._build_start_screen).pack(side="left")
        self.next_btn = ttk.Button(nav, text="Next ▶", state="disabled",
                                   command=self._next_question)
        self.next_btn.pack(side="right")

    def _load_question(self):
        q = self.questions[self.q_index]
        self.current_answer = None
        self.next_btn.config(state="disabled")

        self.progress_lbl.config(
            text=f"Question {self.q_index + 1} / {len(self.questions)}")
        self.score_lbl.config(text=f"Score: {self.score}")
        self.question_lbl.config(text=q["question"])

        for i, opt in enumerate(q["options"]):
            self.option_buttons[i].config(text=opt, state="normal",
                                          style="TButton")
        # hide extra buttons if fewer than 4 options
        for j in range(len(q["options"]), 4):
            self.option_buttons[j].config(text="", state="disabled")

        # timer
        self.time_left = QUESTION_TIME
        self._tick()

    def _tick(self):
        self.timer_lbl.config(text=f"⏱ {self.time_left}s")
        if self.time_left <= 0:
            self._reveal_answer(timeout=True)
            return
        self.time_left -= 1
        self.timer_id = self.after(1000, self._tick)

    def _select_option(self, idx):
        if self.current_answer is not None:
            return
        q = self.questions[self.q_index]
        chosen = q["options"][idx]
        self.current_answer = chosen
        if chosen == q["answer"]:
            self.score += 1
        self.score_lbl.config(text=f"Score: {self.score}")
        self._reveal_answer()

    def _reveal_answer(self, timeout=False):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        q = self.questions[self.q_index]
        correct = q["answer"]

        for i, btn in enumerate(self.option_buttons):
            text = btn.cget("text")
            if not text:
                continue
            btn.config(state="disabled")
            if text == correct:
                btn.config(style="Correct.TButton")
            elif text == self.current_answer:
                btn.config(style="Wrong.TButton")

        if timeout:
            self.timer_lbl.config(text="⏰ Time's up!")
        self.next_btn.config(state="normal")

    def _next_question(self):
        self.q_index += 1
        if self.q_index >= len(self.questions):
            self._end_quiz()
        else:
            self._load_question()

    # ---------- End Screen ----------
    def _end_quiz(self):
        total = len(self.questions)
        is_high = self.scores.record(self.selected_category,
                                     self.selected_difficulty,
                                     self.score, total)

        self._clear()
        frame = ttk.Frame(self, padding=40)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Quiz Complete!",
                  font=("Segoe UI", 22, "bold")).pack(pady=10)
        ttk.Label(frame,
                  text=f"You scored {self.score} / {total}",
                  font=("Segoe UI", 16)).pack(pady=5)

        if is_high:
            ttk.Label(frame, text="🏆 New High Score!",
                      foreground="green",
                      font=("Segoe UI", 14, "bold")).pack(pady=10)

        hs = self.scores.high_score(self.selected_category,
                                    self.selected_difficulty)
        ttk.Label(frame,
                  text=f"High score for this set: {hs}").pack(pady=5)

        ttk.Button(frame, text="Play Again",
                   command=self._build_start_screen).pack(pady=20, fill="x")

    def _show_scores(self):
        hs = self.scores.data.get("high_scores", {})
        if not hs:
            messagebox.showinfo("High Scores", "No scores recorded yet.")
            return
        msg = "\n".join(f"{k}: {v}" for k, v in sorted(hs.items()))
        messagebox.showinfo("High Scores", msg)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()