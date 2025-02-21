import tkinter as tk
from pynput.keyboard import Controller, Listener, Key
import threading

keyboard = Controller()

class QuickAccentApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("400x60+760+0")
        self.root.configure(bg='lightgray')
        self.root.withdraw()

        self.frame = tk.Frame(self.root, bg='lightgray', padx=10, pady=10)
        self.frame.pack(expand=True)

        self.accents = {'a': 'àâ', 'e': 'èéëê', 'i': 'ïî', 'o': 'ô', 'u': 'ùüû', 'c': 'ç'}
        self.active_key, self.letter_labels, self.selected_index, self.menu_active, self.space_count = None, [], -1, False, 0
        self.selection_timer = None

    def show_accents(self, key):
        if key in self.accents:
            for label in self.letter_labels: label.destroy()
            self.letter_labels = [tk.Label(self.frame, text=ch, font=("Arial", 16), bg='lightgray') for ch in self.accents[key]]
            for label in self.letter_labels: label.pack(side=tk.LEFT, padx=5)
            self.selected_index, self.menu_active, self.space_count = -1, True, 0
            self.update_selection()
            self.root.deiconify()

    def update_selection(self):
        for i, label in enumerate(self.letter_labels):
            label.configure(bg="white" if i == self.selected_index else "lightgray", fg="black")

    def navigate_selection(self):
        if self.letter_labels:
            self.selected_index = (self.selected_index + 1) % len(self.letter_labels) if self.selected_index != -1 else 0
            self.space_count += 1
            self.update_selection()

    def on_letter_selected(self):
        if 0 <= self.selected_index < len(self.letter_labels):
            letter = self.letter_labels[self.selected_index].cget("text")
            self.root.withdraw()
            self.menu_active = False
            for _ in range(self.space_count + 2): keyboard.press(Key.backspace); keyboard.release(Key.backspace)
            keyboard.type(letter)

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char in self.accents:
                self.active_key = key.char
            elif key == Key.space and self.menu_active:
                self.navigate_selection()
                if self.selection_timer: self.root.after_cancel(self.selection_timer)
                self.selection_timer = self.root.after(400, self.on_letter_selected)
        except Exception as e:
            print(f"Error: {e}")

    def on_release(self, key):
        if key == Key.space and self.active_key and not self.menu_active:
            self.show_accents(self.active_key)
        self.active_key = None

    def start_listener(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def start(self):
        threading.Thread(target=self.start_listener, daemon=True).start()
        self.root.mainloop()

if __name__ == '__main__':
    QuickAccentApp().start()