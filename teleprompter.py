import tkinter as tk
from tkinter import filedialog, messagebox

class Teleprompter:
    def __init__(self, root):
        self.root = root
        self.root.title("Teleprompter")
        self.root.geometry("800x600")

        self.text = ""
        self.zoom_factor = 200  # Number of characters displayed at a time
        self.scroll_speed = 40   # Time in milliseconds between scrolls
        self.current_index = 0
        self.is_scrolling = False

        self.create_widgets()

    def create_widgets(self):
        # Text input field
        self.text_input = tk.Text(self.root, height=10, width=80)
        self.text_input.pack(pady=10)

        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        # Buttons
        load_button = tk.Button(control_frame, text="Load Speech", command=self.load_speech)
        load_button.grid(row=0, column=0, padx=5)

        start_button = tk.Button(control_frame, text="Start", command=self.start_scrolling)
        start_button.grid(row=0, column=1, padx=5)

        pause_button = tk.Button(control_frame, text="Pause/Resume", command=self.pause_resume)
        pause_button.grid(row=0, column=2, padx=5)

        # Settings frame
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=5)

        # Scroll speed
        tk.Label(settings_frame, text="Scroll Speed (ms):").grid(row=0, column=0, padx=5)
        self.scroll_speed_var = tk.IntVar(value=self.scroll_speed)
        scroll_speed_entry = tk.Entry(settings_frame, textvariable=self.scroll_speed_var, width=5)
        scroll_speed_entry.grid(row=0, column=1, padx=5)

        # Font size
        tk.Label(settings_frame, text="Font Size:").grid(row=0, column=2, padx=5)
        self.font_size_var = tk.IntVar(value=80)
        font_size_entry = tk.Entry(settings_frame, textvariable=self.font_size_var, width=5)
        font_size_entry.grid(row=0, column=3, padx=5)

        # Mirroring
        self.mirror_var = tk.BooleanVar()
        mirror_check = tk.Checkbutton(settings_frame, text="Mirror Text", variable=self.mirror_var)
        mirror_check.grid(row=0, column=4, padx=5)

        # Teleprompter display
        self.text_widget = tk.Label(self.root, text="", font=("Helvetica", self.font_size_var.get()),
                                    wraplength=1600, width=1600, justify="left", anchor="nw")
        self.text_widget.pack(pady=10)

    def load_speech(self):
        # Load a speech from a file
        filepath = filedialog.askopenfilename(title="Open Speech File", filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, 'r') as file:
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(tk.END, file.read())

    def start_scrolling(self):
        # Get the text and settings
        self.text = self.text_input.get(1.0, tk.END).strip()
        if not self.text:
            messagebox.showwarning("No Text", "Please enter or load a speech.")
            return

        self.scroll_speed = self.scroll_speed_var.get()
        font_size = self.font_size_var.get()
        self.text_widget.config(font=("Helvetica", font_size))

        if self.mirror_var.get():
            self.text_widget.config(fg="white")
            self.root.config(bg="black")
        else:
            self.text_widget.config(fg="black")
            self.root.config(bg="white")

        self.current_index = 0
        self.is_scrolling = True
        self.update_text()
        self.scroll_text()

    def pause_resume(self):
        self.is_scrolling = not self.is_scrolling
        if self.is_scrolling:
            self.scroll_text()

    def update_text(self):
        zoomed_text = self.text[self.current_index:self.current_index + self.zoom_factor]
        if self.mirror_var.get():
            zoomed_text = zoomed_text[::-1]  # Reverse text for mirroring
        self.text_widget.config(text=zoomed_text)
        self.root.update_idletasks()

    def scroll_text(self):
        if self.is_scrolling and self.current_index + self.zoom_factor < len(self.text):
            self.current_index += 1
            self.update_text()
            self.root.after(self.scroll_speed, self.scroll_text)

def main():
    root = tk.Tk()

    # Insert a famous speech (e.g., The Gettysburg Address) as default text
    default_text = (
        "Four score and seven years ago our fathers brought forth on this continent, a new nation, "
        "conceived in Liberty, and dedicated to the proposition that all men are created equal.\n\n"
        "Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived "
        "and so dedicated, can long endure. We are met on a great battlefield of that war. "
        "We have come to dedicate a portion of that field, as a final resting place for those who here "
        "gave their lives that that nation might live. It is altogether fitting and proper that we should do this.\n\n"
        "But, in a larger sense, we cannot dedicate—we cannot consecrate—we cannot hallow—this ground. "
        "The brave men, living and dead, who struggled here, have consecrated it, far above our poor power "
        "to add or detract. The world will little note, nor long remember what we say here, but it can never "
        "forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished "
        "work which they who fought here have thus far so nobly advanced. It is rather for us to be here "
        "dedicated to the great task remaining before us—that from these honored dead we take increased devotion "
        "to that cause for which they gave the last full measure of devotion—that we here highly resolve that "
        "these dead shall not have died in vain—that this nation, under God, shall have a new birth of freedom—"
        "and that government of the people, by the people, for the people, shall not perish from the earth."
    )

    app = Teleprompter(root)
    app.text_input.insert(tk.END, default_text)
    root.mainloop()

if __name__ == "__main__":
    main()
