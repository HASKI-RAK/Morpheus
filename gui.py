# gui.py
import tkinter as tk
from tkinter import ttk

import source.simulator.gui as simulator_gui
import source.synthesizer.gui as synthesizer_gui


class SelectionGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Morpheus")
        self.geometry("100x150")
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        ttk.Button(
            self, text="Simulate Learner Profiles", command=self.call_simulation
        ).grid(row=0, column=0, pady=20)
        ttk.Button(
            self, text="Synthesize Learner Profiles", command=self.call_synthesis
        ).grid(row=0, column=1, pady=20)

    def center_window(self, width=325, height=150):
        """
        center GUI window in the screen
        :param width:
        :param height:
        :return:
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def call_simulation(self):
        """
        simulate data GUI
        :return:
        """
        self.destroy()
        simulator_gui.start_gui()

    def call_synthesis(self):
        """
        synthesize data GUI
        :return:
        """
        self.destroy()
        synthesizer_gui.start_gui()


if __name__ == "__main__":
    app = SelectionGUI()
    app.mainloop()
