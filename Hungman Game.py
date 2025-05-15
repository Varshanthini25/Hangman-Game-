import tkinter as tk
import random

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Game with Timer")

        # Categories and words
        self.categories = {
            "fruits": ["apple", "banana", "mango", "grape", "orange", "pineapple", "strawberry","blueberry","guava","kiwi"],
            "animals": ["elephant", "tiger", "giraffe", "kangaroo", "panda", "zebra", "lion","horse","rabbit","pig"],
            "birds": ["parrot", "eagle", "penguin", "sparrow", "peacock", "owl", "flamingo","crow","dove"],
            "sports": ["football", "cricket", "tennis", "badminton", "basketball", "hockey", "volleyball","golf","boxing"],
            "planets": ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"],
            "trees": ["oak", "pine", "maple", "willow", "mango", "coconut", "baobab","apple","neem"],
            "technologies": ["computer", "internet", "software", "hardware", "robotics", "artificial", "blockchain","cloud computing","edge computing"]
        }

        self.attempts_allowed = 7
        self.time_limit = 60  # seconds per word

        # Widgets
        self.label_title = tk.Label(master, text="🎮 Hangman Game", font=("Helvetica", 16, "bold"))
        self.label_title.pack(pady=10)

        self.category_label = tk.Label(master, text="Choose a category:", font=("Helvetica", 12))
        self.category_label.pack()

        self.category_var = tk.StringVar(master)
        self.category_var.set("fruits")  # default value

        self.dropdown = tk.OptionMenu(master, self.category_var, *self.categories.keys())
        self.dropdown.pack(pady=5)

        self.start_button = tk.Button(master, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)

        self.timer_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.timer_label.pack(pady=5)

        self.info_label = tk.Label(master, text="", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        self.word_label = tk.Label(master, text="", font=("Helvetica", 20, "bold"))
        self.word_label.pack(pady=10)

        self.guess_entry = tk.Entry(master, font=("Helvetica", 14), width=5, justify='center')
        self.guess_entry.pack()
        self.guess_entry.bind("<Return>", self.process_guess)

        self.message_label = tk.Label(master, text="", font=("Helvetica", 12))
        self.message_label.pack(pady=5)

        self.reset_button = tk.Button(master, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(pady=10)

        # Game variables
        self.word = ""
        self.word_display = []
        self.guessed_letters = set()
        self.attempts_left = self.attempts_allowed
        self.time_left = self.time_limit
        self.timer_running = False

    def start_game(self):
        self.word = random.choice(self.categories[self.category_var.get()])
        self.word_display = ["_"] * len(self.word)
        self.guessed_letters.clear()
        self.attempts_left = self.attempts_allowed
        self.time_left = self.time_limit
        self.timer_running = True

        self.update_display()
        self.message_label.config(text="")
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()

        self.update_timer()

    def update_display(self):
        self.word_label.config(text=" ".join(self.word_display))
        self.info_label.config(text=f"Attempts left: {self.attempts_left}   |   Category: {self.category_var.get().capitalize()}")
        self.timer_label.config(text=f"Time left: {self.time_left} sec")

    def update_timer(self):
        if self.timer_running:
            if self.time_left > 0:
                self.timer_label.config(text=f"Time left: {self.time_left} sec")
                self.time_left -= 1
                self.master.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="⏳ Time's up! Word reset.")
                self.message_label.config(text=f"Time's up! The word was: {self.word}")
                self.reset_word()

    def reset_word(self):
        # Pick new word, reset variables and timer
        self.word = random.choice(self.categories[self.category_var.get()])
        self.word_display = ["_"] * len(self.word)
        self.guessed_letters.clear()
        self.attempts_left = self.attempts_allowed
        self.time_left = self.time_limit
        self.message_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.update_display()

    def process_guess(self, event):
        if not self.timer_running:
            return

        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="❌ Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="⚠️ You already guessed that letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            self.message_label.config(text="✅ Good job! Letter is in the word.")
            for i, ch in enumerate(self.word):
                if ch == guess:
                    self.word_display[i] = guess
        else:
            self.attempts_left -= 1
            self.message_label.config(text=f"❌ Wrong guess! Attempts left: {self.attempts_left}")

        self.update_display()

        if "_" not in self.word_display:
            self.message_label.config(text=f"🎉 Congratulations! You guessed the word: {self.word}")
            self.timer_running = False
            self.guess_entry.config(state="disabled")

        if self.attempts_left <= 0:
            self.message_label.config(text=f"💀 Game Over! The correct word was: {self.word}")
            self.timer_running = False
            self.guess_entry.config(state="disabled")

    def reset_game(self):
        self.timer_running = False
        self.word = ""
        self.word_display = []
        self.guessed_letters.clear()
        self.attempts_left = self.attempts_allowed
        self.time_left = self.time_limit
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.word_label.config(text="")
        self.info_label.config(text="")
        self.timer_label.config(text="")
        self.message_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
