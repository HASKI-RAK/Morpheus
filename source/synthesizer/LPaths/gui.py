# gui.py
import tkinter as tk
from tkinter import ttk

from source.synthesizer.LPaths.config import MODELS
from source.synthesizer.LPaths.synthesizer import synthesize_learning_paths
from source.synthesizer.LPaths.utils import store_data_in_csv


class DataSynthesizerLP(tk.Tk):
    def __init__(self):
        """
        initialize GUI class for learning paths
        """
        super().__init__()

        self.title("Data Generator")
        self.geometry("700x300")

        self.num_students = tk.IntVar(value=100)
        self.file_name_var = tk.StringVar(value="synthesized_learning_path_data.csv")  # nopep8
        self.learning_style_info = {
            "Processing": None,
            "Perception": None,
            "Understanding": None,
            "Input": None,
        }
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        """
        create widgets for configurating learning path data
        """
        ttk.Label(self, text="Number of Students:").grid(row=0, column=0,
                                                         sticky=tk.W)
        ttk.Entry(self, textvariable=self.num_students).grid(
            row=0, column=1, sticky=tk.W
        )

        ttk.Label(self, text="File Name to Save:").grid(row=1, column=0,
                                                        sticky=tk.W)
        ttk.Entry(self, textvariable=self.file_name_var).grid(
            row=1, column=1, sticky=tk.W
        )

        ttk.Label(self, text="Learning Styles:").grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        self.dist_frame = ttk.Frame(self)
        self.dist_frame.grid(row=3, column=0, columnspan=5, sticky=tk.W)

        ttk.Label(self, text="Processing:").grid(row=3, column=0, sticky=tk.W,
                                                 pady=10)
        self.combobox_processing = ttk.Combobox(self)
        self.combobox_processing["values"] = ("Active", "Reflective")
        self.combobox_processing.current(0)
        self.combobox_processing.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(self, text="Perception:").grid(row=4, column=0, sticky=tk.W,
                                                 pady=10)
        self.combobox_perception = ttk.Combobox(self)
        self.combobox_perception["values"] = ("Sensory", "Intuitive")
        self.combobox_perception.current(0)
        self.combobox_perception.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(self, text="Understanding:").grid(
            row=5, column=0, sticky=tk.W, pady=10
        )
        self.combobox_understanding = ttk.Combobox(self)
        self.combobox_understanding["values"] = ("Sequential", "Global")
        self.combobox_understanding.current(0)
        self.combobox_understanding.grid(row=5, column=1, padx=10, pady=10)

        ttk.Label(self, text="Input:").grid(row=6, column=0, sticky=tk.W,
                                            pady=10)
        self.combobox_input = ttk.Combobox(self)
        self.combobox_input["values"] = ("Sequential", "Global")
        self.combobox_input.current(0)
        self.combobox_input.grid(row=6, column=1, padx=10, pady=10)

        ttk.Button(self, text="\u25B6", command=self.generate_data).grid(
            row=20, column=0, pady=20
        )

    def center_window(self, width=700, height=300):
        """
        center GUI window in the screen
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def generate_data(self):
        """
        call models with information given from the GUI to synthesize data
        """
        self.learning_style_info["Processing"] = self.combobox_processing.get()
        self.learning_style_info["Perception"] = self.combobox_perception.get()
        self.learning_style_info["Understanding"] = self.combobox_understanding.get()  # nopep8
        self.learning_style_info["Input"] = self.combobox_input.get()

        num_students = self.num_students.get()
        file_name = self.file_name_var.get().replace(".csv", "")

        data_dict = synthesize_learning_paths(
            self.learning_style_info["Processing"],
            self.learning_style_info["Perception"],
            self.learning_style_info["Understanding"],
            self.learning_style_info["Input"],
            num_students,
            file_name,
            MODELS,
        )
        store_data_in_csv(data_dict, file_name)
        tk.messagebox.showinfo(
            "Success", f"Synthesized learning path data " f"saved to {file_name}"  # nopep8
        )
        self.destroy()


if __name__ == "__main__":
    app = DataSynthesizerLP()
    app.mainloop()
